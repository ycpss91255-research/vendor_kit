# 獨立審查請求：vendor_kit 契約／流程圖 v2（第七輪）

你是獨立審查者。請依下列標準審查附件的 47 頁 PNG（已隨指令附上）與 drawio XML，並對照「決策紀錄」（interface_spec.md）逐頁檢查。請只用繁體中文回答。

## 審查標準（使用者定的）
1. 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。
2. 顏色要有明確一致的意義，以各頁底部圖例為準；沒有的顏色不可出現。
3. 字要少，一般人（非工程師）也看得懂；專有名詞要在該頁底部「本頁名詞」表裡。
4. 線段：不穿無關方框、不交叉、不壓字、不裁切、不懸空、不該折的不折。
5. 線上文字 12pt。
6. 內容要跟 notes 的決策一致，且不可出現任何特定工具名（如 base）當實例，一律用 <repo>。
7. 每個方塊只放一件事（一個動作、一個判斷、一個檔案、一個最小單元）；一格裡有兩件事（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）就是問題，要拆成兩格。

## 本輪改動
第七輪：依第六輪 16 項必修＋選修與 v2.8 澄清（uninstall 刪除集合補 baseline 根檔；install 日誌規則；E(c) 薄殼檢查在改第一行之前；--local 三分支含檔案存在與 6-37；離線工具 tar 由使用者 add --local；dev vendor_kit inspect 在主機側；橙色一致；菱形頂點入口；迴圈；便條溢出）。共 47 頁。

## 特別注意
對照 interface_spec.md 逐頁找：
(1) 第六輪 16 項是否修掉；
(2) 頁間入口出口；
(3) 每格一件事（只算真的兩個獨立動作）；
(4) legend／名詞表。
只回報真正的問題；已接受的設計不要再質疑。若某頁沒有問題請明說。最後給一句總評：這 47 頁能否交給使用者看（允許少量選修）。

## 要你回答的格式
逐頁列出：
(A) 排版問題
(B) 顏色不符圖例
(C) 一般人看不懂的點與名詞表遺漏
(D) 與 notes 矛盾之處
每項給元件或線段 id（在 drawio XML 中的 mxCell id；找不到就寫元件上的文字）與一句說明，並標明是否必修（必須修才可交付）。
最後一行給「可以交付」或「還不行」。

## 附件 PNG 的頁次（依附上的順序）
1. 契約 v2：不變量與角色
2. 契約 v2：動詞介面表
3. 契約 v2：規則、選項表、不開的動詞
4. 契約 v2：目錄樹與檔案範例
5. 契約 v2：schema
6. 契約 v2：動詞 × 檔案矩陣
7. 契約 v2：工具 repo 契約③
8. 契約 v2：啟動器 ↔ 引擎契約④
9. 契約 v2：CI 契約⑤ 與驗收矩陣
10. 架構圖 v2
11. 流程 v2：bootstrap.sh（1）
12. 流程 v2：bootstrap.sh（2）
13. 流程 v2：install（1）
14. 流程 v2：install（2）
15. 流程 v2：add（1）
16. 流程 v2：add（1′）
17. 流程 v2：add（2）
18. 流程 v2：sync（1）
19. 流程 v2：sync（1′）
20. 流程 v2：sync（2）
21. 流程 v2：upgrade A
22. 流程 v2：upgrade B（1）
23. 流程 v2：upgrade B（1′）
24. 流程 v2：upgrade B（2）
25. 流程 v2：upgrade B（2′）
26. 流程 v2：upgrade 逐檔判斷
27. 流程 v2：upgrade E(a)(b)
28. 流程 v2：upgrade E(c)（1）
29. 流程 v2：upgrade E(c)（2）
30. 流程 v2：dev <repo>
31. 流程 v2：dev vendor_kit
32. 流程 v2：undev <repo>
33. 流程 v2：undev vendor_kit
34. 流程 v2：remove（1）
35. 流程 v2：remove（2）
36. 流程 v2：uninstall（1）
37. 流程 v2：uninstall（2）
38. 流程 v2：prune
39. 流程 v2：update
40. 狀態機 v2：初始檔五態
41. 狀態機 v2：交易與進度日誌
42. 相容性矩陣 v2
43. 結束碼決策表 v2
44. 流程 v2：release（1）
45. 流程 v2：release（2）
46. 流程 v2：離線包（1）
47. 流程 v2：離線包（2）

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

# 附件：drawio XML（v2_only.drawio 全文，為符合輸入長度上限做了無損語意的縮寫）

縮寫對照：`<c>` = mxCell；`v=` = value；`s=` = style；`sc=` = strokeColor；`fc=` = fillColor；`fs=` = fontSize；`fst=` = fontStyle；`fco=` = fontColor；`swfc=` = swimlaneFillColor；`<g x y w h pts/>` = mxGeometry（pts 為線段折點，以「;」分隔）；`⏎` = <br>；`【…】` = 粗體；省略了 parent="1"、vertex="1"、html/rounded/spacing/align 等純排版 token；未寫 sc/fc 的線段為預設黑色；未寫 edgeStyle 的線段皆為 orthogonalEdgeStyle。所有 id、文字、顏色、字級、source/target、座標與折點皆完整保留。

```xml
<mxfile>
<diagram id="v1p1" name="契約 v2：不變量與角色"><c id="title" v="契約① 使用者介面（1／3）── 目的、角色、不變量（interface_spec v2；&lt;repo&gt; = 工具 repo 名）" s="text;fs=18;fst=1"><g x=40 y=20 w=960 h=34/></c>
<c id="p1_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p1_pend" v="【本頁無待拍板】⏎本頁只有目的、角色、不變量與初始檔規則；動詞表在 p1b、選項／結束碼／規則在 p1c" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p1A" v="0. 目的與角色（契約只對兩個黃橢圓承諾）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=234/></c>
<c id="p1A_goal" v="目的（一句話）：工具 repo 把 dist/ 打包成 GHCR image；下游專案靠 bootstrap.sh + just vendor_kit add／upgrade／dev 拿到工具、跟上新版、在本機開發工具本身；其餘自動。⏎契約只對兩個黃橢圓承諾；我們（灰橢圓）不對自己承諾。" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1A"><g x=20 y=50 w=740 h=106/></c>
<c id="p1A_r1" v="工具 repo 開發者（供應側）⏎照契約③ p3 出貨 dist 與 image" s="ellipse;fc=#FFF4C3;sc=#000000;fs=14;fs=12" parent="p1A"><g x=790 y=50 w=240 h=106/></c>
<c id="p1A_r2" v="使用者（下游專案）⏎每天打 just 的人；用 p1b 的動詞" s="ellipse;fc=#FFF4C3;sc=#000000;fs=14;fs=12" parent="p1A"><g x=1050 y=50 w=240 h=106/></c>
<c id="p1A_r3" v="vendor_kit 開發者（我們）⏎維護引擎與啟動器；不對自己承諾" s="ellipse;fc=#CCCCCC;sc=#000000;fs=14;fs=12" parent="p1A"><g x=1310 y=50 w=230 h=106/></c>
<c id="p1A_tech" v="【技術路線 [定]】：自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file（行內合併）；【第一版不放 vendir／Copier】。依據：無單一工具全包四項（拉、鎖、初始檔、合併）；vendir 只省 docker 三行；Copier 要求範本是帶 tag 的 git repo" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1A"><g x=20 y=168 w=1520 h=46/></c>
<c id="p1A_tech_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1A"><g x=1508 y=170 w=30 h=20/></c>
<c id="p1B" v="1. 不變量（ADR；一列一主題，規則／條件／動作／結束碼分格）＋ 初始檔規則（§5；B = baseline、D = 磁碟上你的檔、N = 目標版範本 /dist/&lt;repo&gt;）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=350 w=1560 h=1123/></c>
<c id="p1B_inv" v="【1. 不變量（ADR）[定]：vendor_kit 對使用者的檔 ── 可以建（明說建了什麼）、要改先問（-y 免問）、永不刪、永不覆蓋。】⏎「永不覆蓋」= 不用工具版本取代使用者客製內容；例外只有三處：根 justfile 一行、根 .dockerignore 三行、已納管初始檔經同意的換版／三方合併。never fail silently（結束碼 0／1／2／3）。" s="fc=#ffffff;sc=#b85450;fs=14;fs=12" parent="p1B"><g x=20 y=50 w=1520 h=48/></c>
<c id="p1B_inv_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=1508 y=52 w=30 h=20/></c>
<c id="p1B_t_h0" v="主題" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=114 w=170 h=30/></c>
<c id="p1B_t_h1" v="規則（一格一件事）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=190 y=114 w=430 h=30/></c>
<c id="p1B_t_h2" v="條件" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=620 y=114 w=300 h=30/></c>
<c id="p1B_t_h3" v="動作" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=920 y=114 w=340 h=30/></c>
<c id="p1B_t_h4" v="結束碼／訊息" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=1260 y=114 w=280 h=30/></c>
<c id="p1B_t_r0c0" v="【自動化（sync）只碰不進 git 的東西】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=144 w=170 h=57/></c>
<c id="p1B_t_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=146 w=30 h=20/></c>
<c id="p1B_t_r0c1_0" v="可寫範圍 = cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=144 w=430 h=26/></c>
<c id="p1B_t_r0c1_1" v="不碰使用者的檔、不寫薄殼四檔、不寫 gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=170 w=430 h=31/></c>
<c id="p1B_t_r0c2" v="引擎 ref ≠ gen/.stamp 第一行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=144 w=300 h=57/></c>
<c id="p1B_t_r0c3" v="不重寫薄殼，只提示" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=144 w=340 h=57/></c>
<c id="p1B_t_r0c4" v="1 印 6-1「vendor_kit 已更新 &lt;vX&gt; → &lt;vY&gt;，請執行：just vendor_kit upgrade vendor_kit」" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=144 w=280 h=57/></c>
<c id="p1B_t_r1c0" v="【薄殼重產只由 install／upgrade vendor_kit 做】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=201 w=170 h=68/></c>
<c id="p1B_t_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=203 w=30 h=20/></c>
<c id="p1B_t_r1c1_0" v="薄殼四檔與 gen/.stamp 只由 install／upgrade vendor_kit 重產" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=201 w=430 h=26/></c>
<c id="p1B_t_r1c1_1" v="重產前先比對薄殼自描述首行（# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=…）：引擎重算 hash + 對 image 內模板二次比對" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=227 w=430 h=42/></c>
<c id="p1B_t_r1c2_0" v="首行 hash 相符" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=201 w=300 h=26/></c>
<c id="p1B_t_r1c2_1" v="首行 hash 不符（薄殼被改過）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=227 w=300 h=42/></c>
<c id="p1B_t_r1c3_0" v="重產" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=201 w=340 h=26/></c>
<c id="p1B_t_r1c3_1" v="不動任何薄殼、列出差異（使用者 git checkout 還原後再跑）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=227 w=340 h=42/></c>
<c id="p1B_t_r1c4_0" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=201 w=280 h=26/></c>
<c id="p1B_t_r1c4_1" v="1 印 6-28" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=227 w=280 h=42/></c>
<c id="p1B_t_r2c0" v="【CI 為真（frozen）與 -y 無關】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=269 w=170 h=83/></c>
<c id="p1B_t_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=271 w=30 h=20/></c>
<c id="p1B_t_r2c1_0" v="frozen = 不寫任何 tracked 檔、不查最新版" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=269 w=430 h=26/></c>
<c id="p1B_t_r2c1_1" v="仍拉鎖定版 image、仍寫 cache/、gen/" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=295 w=430 h=26/></c>
<c id="p1B_t_r2c1_2" v="-y 只在本機免詢問、不解除 frozen；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=321 w=430 h=31/></c>
<c id="p1B_t_r2c2_0" v="環境變數 CI 非空且不為 0／false（GitHub／GitLab 都設 CI=true；check.sh 自己 export CI=1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=269 w=300 h=57/></c>
<c id="p1B_t_r2c2_1" v="frozen 下需要寫 tracked 檔" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=326 w=300 h=26/></c>
<c id="p1B_t_r2c3_0" v="進 frozen" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=269 w=340 h=57/></c>
<c id="p1B_t_r2c3_1" v="不寫，印需改的檔清單（與 -y 無關）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=326 w=340 h=26/></c>
<c id="p1B_t_r2c4_0" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=269 w=280 h=57/></c>
<c id="p1B_t_r2c4_1" v="1" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=326 w=280 h=26/></c>
<c id="p1B_t_r3c0" v="【「會碰使用者東西」只有三處】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=352 w=170 h=84/></c>
<c id="p1B_t_r3c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=354 w=30 h=20/></c>
<c id="p1B_t_r3c1_0" v="根 justfile 一行（問後加／刪）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=352 w=430 h=26/></c>
<c id="p1B_t_r3c1_1" v="根 .dockerignore 三行（問後 append／刪）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=378 w=430 h=26/></c>
<c id="p1B_t_r3c1_2" v="初始檔（init.toml 的 dest；含 strategy=append 經同意加的行）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=404 w=430 h=32/></c>
<c id="p1B_t_r3c2_0" v="使用者 .gitignore：工具以 strategy=append 宣告且你同意" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=352 w=300 h=42/></c>
<c id="p1B_t_r3c2_1" v="其餘：未宣告的使用者 .gitignore、.git/info/exclude、.git 本身" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=394 w=300 h=42/></c>
<c id="p1B_t_r3c3_0" v="才加行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=352 w=340 h=42/></c>
<c id="p1B_t_r3c3_1" v="不碰" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=394 w=340 h=42/></c>
<c id="p1B_t_r3c4_0" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=352 w=280 h=42/></c>
<c id="p1B_t_r3c4_1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=394 w=280 h=42/></c>
<c id="p1B_t_r4c0" v="【詢問通則】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=436 w=170 h=110/></c>
<c id="p1B_t_r4c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=438 w=30 h=20/></c>
<c id="p1B_t_r4c1_0" v="詢問一律有拒絕分支" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=436 w=430 h=26/></c>
<c id="p1B_t_r4c1_1" v="-y 只省略詢問：不授權覆蓋既有未納管檔、不硬加 append 行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=462 w=430 h=84/></c>
<c id="p1B_t_r4c2_0" v="明確回答「否」" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=436 w=300 h=42/></c>
<c id="p1B_t_r4c2_1" v="需詢問但無 tty／EOF 且無 -y" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=478 w=300 h=42/></c>
<c id="p1B_t_r4c2_2" v="EOF／Ctrl-C 中途中斷" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=520 w=300 h=26/></c>
<c id="p1B_t_r4c3_0" v="不寫；新檔（從未建立）→ state=declined；已納管檔 → state 不變、只記 declined_hash" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=436 w=340 h=42/></c>
<c id="p1B_t_r4c3_1" v="不寫" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=478 w=340 h=42/></c>
<c id="p1B_t_r4c3_2" v="中止整個 apply、不套用、不記 declined" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=520 w=340 h=26/></c>
<c id="p1B_t_r4c4_0" v="繼續（該檔略過）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=436 w=280 h=42/></c>
<c id="p1B_t_r4c4_1" v="1 印 6-4「需要確認但沒有終端可互動。請加 -y，或在終端執行。」" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=478 w=280 h=42/></c>
<c id="p1B_t_r4c4_2" v="1" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=520 w=280 h=26/></c>
<c id="p1B_t_r5c0" v="【失敗恢復與零寫入】" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=546 w=170 h=120/></c>
<c id="p1B_t_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=158 y=548 w=30 h=20/></c>
<c id="p1B_t_r5c1_0" v="所有合併在暫存完成 → 逐檔原子替換" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=546 w=430 h=26/></c>
<c id="p1B_t_r5c1_1" v="apply 進度日誌在第一個寫入前建立、最後一步刪除" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=572 w=430 h=26/></c>
<c id="p1B_t_r5c1_2" v="結束碼 3 一律零寫入（無例外）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=598 w=430 h=26/></c>
<c id="p1B_t_r5c1_3" v="「不留半成品」只對第一次 install 成立；衝突（2）與自身升級要求重跑（1）是獨立狀態" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=190 y=624 w=430 h=42/></c>
<c id="p1B_t_r5c2_0" v="寫入中途失敗" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=546 w=300 h=26/></c>
<c id="p1B_t_r5c2_1" v="下次可寫動詞遇到未完成日誌" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=572 w=300 h=26/></c>
<c id="p1B_t_r5c2_2" v="唯讀動詞（sync／update／help）遇到未完成日誌" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=620 y=598 w=300 h=68/></c>
<c id="p1B_t_r5c3_0" v="明列已完成／未完成" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=546 w=340 h=26/></c>
<c id="p1B_t_r5c3_1" v="先恢復再繼續" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=572 w=340 h=26/></c>
<c id="p1B_t_r5c3_2" v="不恢復，只提示" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=920 y=598 w=340 h=68/></c>
<c id="p1B_t_r5c4_0" v="1" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=546 w=280 h=26/></c>
<c id="p1B_t_r5c4_1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=572 w=280 h=26/></c>
<c id="p1B_t_r5c4_2" v="1 印 6-33（help 不受影響）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1260 y=598 w=280 h=68/></c>
<c id="p1I_l" v="初始檔規則（同不變量；每列一種情況、一格一件事）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p1B"><g x=20 y=682 w=900 h=28/></c>
<c id="p1I_h0" v="時機" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=714 w=150 h=30/></c>
<c id="p1I_h1" v="情況" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=170 y=714 w=360 h=30/></c>
<c id="p1I_h2" v="做法（逐字問句見 6-20～6-22）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=530 y=714 w=1010 h=30/></c>
<c id="p1I_r0c0" v="add" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=744 w=150 h=26/></c>
<c id="p1I_r0c1" v="檔不存在" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=744 w=360 h=26/></c>
<c id="p1I_r0c2" v="建（印出建了什麼）；state=managed" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=744 w=1010 h=26/></c>
<c id="p1I_r1c0" v="add" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=770 w=150 h=26/></c>
<c id="p1I_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=138 y=772 w=30 h=20/></c>
<c id="p1I_r1c1" v="檔已存在（strategy=copy）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=770 w=360 h=26/></c>
<c id="p1I_r1c2" v="不納管、不覆蓋（-y 也不覆蓋），印 6-11「&lt;X&gt; 已存在，未納管；範本在 .vendor_kit/cache/&lt;repo&gt;/files/ 可自行比對」；state=unmanaged" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=770 w=1010 h=26/></c>
<c id="p1I_r2c0" v="add（strategy=append）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=796 w=150 h=57/></c>
<c id="p1I_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=138 y=798 w=30 h=20/></c>
<c id="p1I_r2c1" v="檔已存在" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=796 w=360 h=57/></c>
<c id="p1I_r2c2" v="問 6-21「要在 &lt;X&gt; 加這幾行嗎」→ append，實際插入的行記在 metadata lines（原本就有的相同行不認領）；state=appended；重跑不重複；拒絕 → 不加行、不納管（state=unmanaged）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=796 w=1010 h=57/></c>
<c id="p1I_r3c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=853 w=150 h=26/></c>
<c id="p1I_r3c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=138 y=855 w=30 h=20/></c>
<c id="p1I_r3c1" v="D 缺（使用者刪了已納管檔）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=853 w=360 h=26/></c>
<c id="p1I_r3c2" v="state=deleted，維持刪除、不重建" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=853 w=1010 h=26/></c>
<c id="p1I_r4c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=879 w=150 h=26/></c>
<c id="p1I_r4c1" v="D==N 或 B==N（新版沒改／你的檔已等於新版）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=879 w=360 h=26/></c>
<c id="p1I_r4c2" v="不動" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=879 w=1010 h=26/></c>
<c id="p1I_r5c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=905 w=150 h=26/></c>
<c id="p1I_r5c1" v="D==B（新版改了、你沒改）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=905 w=360 h=26/></c>
<c id="p1I_r5c2" v="問 6-22「&lt;X&gt; 換成新版？」→ 換；拒絕 → state 仍 managed、只記 declined_hash（N 的 hash 變了才再問）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=905 w=1010 h=26/></c>
<c id="p1I_r6c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=931 w=150 h=42/></c>
<c id="p1I_r6c1" v="三者皆異（兩邊都改）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=931 w=360 h=42/></c>
<c id="p1I_r6c2" v="問 6-22「你和新版都改了 &lt;X&gt;，要三方合併嗎？」→ git merge-file --diff3；衝突留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline、回 2；baseline 仍推到新版（合併結果解析失敗 → 2 留原檔、baseline 不推、記 conflicts）；拒絕 → state 不變、只記 declined_hash" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=931 w=1010 h=42/></c>
<c id="p1I_r7c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=973 w=150 h=26/></c>
<c id="p1I_r7c1" v="N 缺（新版刪除該檔）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=973 w=360 h=26/></c>
<c id="p1I_r7c2" v="不刪，只 warn" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=973 w=1010 h=26/></c>
<c id="p1I_r8c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=999 w=150 h=26/></c>
<c id="p1I_r8c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=138 y=1001 w=30 h=20/></c>
<c id="p1I_r8c1" v="新版新增初始檔（Q14）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=999 w=360 h=26/></c>
<c id="p1I_r8c2" v="問 6-22「要建 &lt;X&gt; 嗎」（-y 建）；拒絕 → 從未建立，state=declined + declined_hash，之後不問；新版 N 的 hash 變了才再問；dest 在 CI 路徑時先印 6-29" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=999 w=1010 h=26/></c>
<c id="p1I_r9c0" v="upgrade（append）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1025 w=150 h=26/></c>
<c id="p1I_r9c1" v="找到上次加的行（原文相同；CRLF／LF 等價）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=1025 w=360 h=26/></c>
<c id="p1I_r9c2" v="問後替換；拒絕 → state 仍 appended、只記 declined_hash；零命中或多處命中 → 保留只 warn、印新內容" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=1025 w=1010 h=26/></c>
<c id="p1I_r10c0" v="upgrade" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1051 w=150 h=26/></c>
<c id="p1I_r10c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=138 y=1053 w=30 h=20/></c>
<c id="p1I_r10c1" v="二進位／symlink（不合併）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=1051 w=360 h=26/></c>
<c id="p1I_r10c2" v="你沒改 → 問 6-22「&lt;X&gt; 是二進位檔，要換成新版嗎？」後才換（拒絕 → state 不變、只記 declined_hash）；改過 → 保留 + warn" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=1051 w=1010 h=26/></c>
<c id="p1I_r11c0" v="remove／uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1077 w=150 h=26/></c>
<c id="p1I_r11c1" v="任何" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=170 y=1077 w=360 h=26/></c>
<c id="p1I_r11c2" v="永不刪初始檔，印清單；append 行問 6-21「要刪我們加在 &lt;X&gt; 的這幾行嗎」後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=530 y=1077 w=1010 h=26/></c>
<c id="p1_lg0" v="黃橢圓：契約承諾的角色" s="ellipse;fc=#FFF4C3;sc=#000000;fs=14;fs=12"><g x=40 y=1497 w=260 h=52/></c>
<c id="p1_lg1" v="灰橢圓：不承諾（我們）" s="ellipse;fc=#CCCCCC;sc=#000000;fs=14;fs=12"><g x=320 y=1497 w=260 h=52/></c>
<c id="p1_lg2" v="白底紅粗框：不變量" s="fc=#ffffff;sc=#b85450;fs=14;fs=12"><g x=600 y=1503 w=160 h=40/></c>
<c id="p1_lg3" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=780 y=1503 w=190 h=40/></c>
<c id="p1_lg4" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=990 y=1503 w=110 h=40/></c>
<c id="p1_lgt" v="橢圓／方框顏色只在本頁有效⏎動詞表 p1b；選項、結束碼、規則 p1c；流程細節一律在流程頁" s="text;fs=12;sc=none;fc=none"><g x=1120 y=1493 w=300 h=60/></c>
<c id="p1_lg5" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=1569 w=200 h=40/></c>
<c id="p1_lg6" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=260 y=1569 w=200 h=40/></c>
<c id="p1_lg6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=428 y=1571 w=30 h=20/></c>
<c id="p1_lg7" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=480 y=1569 w=220 h=40/></c>
<c id="p1_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1625 w=300 h=28/></c>
<c id="p1_tk0" v="&lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1659 w=150 h=40/></c>
<c id="p1_tv0" v="工具 repo 名（占位符）；.vendor_kit/cache/&lt;repo&gt;/ = 專案裡展開的工具檔；ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist = 它的 image；&lt;ns&gt; = 工具 just 模組的命名空間" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1659 w=610 h=40/></c>
<c id="p1_tk1" v="不變量（ADR）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1699 w=150 h=40/></c>
<c id="p1_tv1" v="整個專案最高優先的四句：可以建、要改先問、永不刪、永不覆蓋；記在 docs/adr/（短格式 ADR），每個決議都對照它；不另建 PRD.md" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1699 w=610 h=40/></c>
<c id="p1_tk2" v="ADR" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1739 w=150 h=40/></c>
<c id="p1_tv2" v="Architecture Decision Record：一份記錄「為什麼這樣決定」的短文件（docs/adr/）；破壞性變更、提高 floor 都要記一筆" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1739 w=610 h=40/></c>
<c id="p1_tk3" v="tracked 檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1779 w=150 h=40/></c>
<c id="p1_tv3" v="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1779 w=610 h=40/></c>
<c id="p1_tk4" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1819 w=150 h=55/></c>
<c id="p1_tv4" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1819 w=610 h=55/></c>
<c id="p1_tk5" v="CI／runner" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1874 w=150 h=40/></c>
<c id="p1_tv5" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1874 w=610 h=40/></c>
<c id="p1_tk6" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1914 w=150 h=55/></c>
<c id="p1_tv6" v="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1914 w=610 h=55/></c>
<c id="p1_tk7" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1969 w=150 h=55/></c>
<c id="p1_tv7" v="每次工具 recipe 的自動前置（_sync）：比印記、比 gen/.stamp；只寫 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp，不碰薄殼、不寫 gen/.stamp；引擎 ref ≠ gen/.stamp 就退出 1 印 6-1（install／upgrade vendor_kit 不被擋）；無參數走快路徑" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1969 w=610 h=55/></c>
<c id="p1_tk8" v="薄殼自描述首行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2024 w=150 h=55/></c>
<c id="p1_tv8" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 CRLF→LF 正規化 hash&gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2024 w=610 h=55/></c>
<c id="p1_tk9" v="strategy = &quot;append&quot;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2079 w=150 h=55/></c>
<c id="p1_tv9" v="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2079 w=610 h=55/></c>
<c id="p1_tk10" v="CRLF／LF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2134 w=150 h=40/></c>
<c id="p1_tv10" v="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2134 w=610 h=40/></c>
<c id="p1_tk11" v="三方合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2174 w=150 h=40/></c>
<c id="p1_tv11" v="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2174 w=610 h=40/></c>
<c id="p1_tk12" v="baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1659 w=150 h=40/></c>
<c id="p1_tv12" v=".vendor_kit/baseline/&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1659 w=610 h=40/></c>
<c id="p1_tk13" v="N（目標版範本）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1699 w=150 h=40/></c>
<c id="p1_tv13" v="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&lt;id&gt;/、掛進引擎的 /dist/&lt;repo&gt;（唯讀），不是 cache；cache/&lt;repo&gt;/ 在 apply 決定套用後才 materialize" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1699 w=610 h=40/></c>
<c id="p1_tk14" v="初始檔五態（state）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1739 w=150 h=55/></c>
<c id="p1_tv14" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1739 w=610 h=55/></c>
<c id="p1_tk15" v="declined／declined_hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1794 w=150 h=55/></c>
<c id="p1_tv15" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1794 w=610 h=55/></c>
<c id="p1_tk16" v="conflicts（衝突中檔案）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1849 w=150 h=55/></c>
<c id="p1_tv16" v="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1849 w=610 h=55/></c>
<c id="p1_tk17" v="進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1904 w=150 h=55/></c>
<c id="p1_tv17" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1904 w=610 h=55/></c>
<c id="p1_tk18" v="tty／trap" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1959 w=150 h=40/></c>
<c id="p1_tv18" v="tty = 互動終端（能問問題）；沒有 tty（管線、CI）又需詢問且無 -y → 1 印 6-4；trap = shell 的收尾勾子，啟動器用它在中斷時清容器與 .tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1959 w=610 h=40/></c>
<c id="p1_tk19" v="根 .dockerignore 三行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1999 w=150 h=71/></c>
<c id="p1_tv19" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1999 w=610 h=71/></c>
<c id="p1_tk20" v="根 justfile 四行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2070 w=150 h=55/></c>
<c id="p1_tv20" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2070 w=610 h=55/></c>
<c id="p1_tk21" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2125 w=150 h=55/></c>
<c id="p1_tv21" v="baseline/&lt;repo&gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2125 w=610 h=55/></c>
</diagram>
<diagram id="v1p1b" name="契約 v2：動詞介面表"><c id="title" v="契約① 使用者介面（2／3）── 動詞介面表（interface_spec §1.2；just vendor_kit &lt;verb&gt; [args]）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p1b_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p1b_pend" v="【本頁無待拍板】⏎選項總表（Q25）、結束碼、不開的動詞在 p1c；每個動詞的流程在流程頁 p5～" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p1B" v="2. 契約① 使用者介面：常用 3 + 進階 8 + 一次性 1 + help（綠底 常用、白底 進階、藍底 一次性；一列一動詞、「做什麼」欄一格一件事；6-N = interface_spec §6 訊息編號）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=1822/></c>
<c id="p1B_h0" v="動詞＋語法" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=50 w=220 h=30/></c>
<c id="p1B_h1" v="反向" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=240 y=50 w=84 h=30/></c>
<c id="p1B_h2" v="做什麼（一格一件事；細節見流程頁）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=324 y=50 w=980 h=30/></c>
<c id="p1B_h3" v="結束碼" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=1304 y=50 w=180 h=30/></c>
<c id="p1B_h4" v="組" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1B"><g x=1484 y=50 w=56 h=30/></c>
<c id="p1B_r0c0" v="bootstrap.sh⏎sh bootstrap.sh [-t &lt;repo&gt;[@&lt;tag&gt;]]… [-y] [--local &lt;image tag 或 tar&gt;] [--timeout &lt;秒&gt;] [-h]" s="fc=#dae8fc;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=80 w=220 h=182/></c>
<c id="p1B_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=82 w=30 h=20/></c>
<c id="p1B_r0c1" v="uninstall（反向呼叫）" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=240 y=80 w=84 h=182/></c>
<c id="p1B_r0c2_0" v="前置：在 git repo 內（否 → 1 印 6-16）；just ≥ 1.33.0（不足 → 1 印 6-23）；floor 檢查；已有 version.toml → 用該行引擎（不用內嵌）" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=80 w=980 h=26/></c>
<c id="p1B_r0c2_1" v="docker image inspect 引擎 image：本機有 → 不 pull（離線可用）" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=106 w=980 h=26/></c>
<c id="p1B_r0c2_2" v="本機無 → docker pull 引擎 ref（逾時 → 1 印 6-31）；--local &lt;tar&gt;：改 docker load，再讀 .digest 旁檔" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=132 w=980 h=26/></c>
<c id="p1B_r0c2_3" v="呼叫引擎 install" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=158 w=980 h=26/></c>
<c id="p1B_r0c2_4" v="對每個 -t 呼叫 add &lt;repo&gt;[@&lt;tag&gt;]（轉發 -y；EOF 不算同意）" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=184 w=980 h=26/></c>
<c id="p1B_r0c2_5" v="--local：version.local.toml（vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id）在 install 成功後才寫、失敗清除；version.toml 仍寫正式 ref" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=210 w=980 h=26/></c>
<c id="p1B_r0c2_6" v="再跑一次 = 呼叫 install（冪等修復）；不自刪；離線包 = bootstrap.sh --local；取得：releases/latest/download/bootstrap.sh" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=324 y=236 w=980 h=26/></c>
<c id="p1B_r0c3" v="0；1 失敗不留半成品（只對第一次 install 成立）；3" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=1304 y=80 w=180 h=182/></c>
<c id="p1B_r0c4" v="一次性" s="fc=#dae8fc;sc=#999999;fs=12" parent="p1B"><g x=1484 y=80 w=56 h=182/></c>
<c id="p1B_r1c0" v="install⏎install [-y] [--no-justfile]⏎install &lt;repo&gt; 誤用 → 1 印 6-17" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=262 w=220 h=146/></c>
<c id="p1B_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=264 w=30 h=20/></c>
<c id="p1B_r1c1" v="uninstall" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=262 w=84 h=146/></c>
<c id="p1B_r1c2_0" v="前置：在 git repo 內（否 → 1 印 6-16）；上層與下層皆無 .vendor_kit/（否 → 1 印 6-35）；不被 gen/.stamp 關卡擋" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=262 w=980 h=26/></c>
<c id="p1B_r1c2_1" v="第一次／修復判定用薄殼自描述首行：不存在 → 第一次；hash 相符 → 重產；不符 → 1 印 6-28 列差異不動" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=288 w=980 h=26/></c>
<c id="p1B_r1c2_2" v="建 .vendor_kit/：version.toml（schema、written_by）、薄殼四檔、baseline/.gitkeep（不建 metadata）、gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=314 w=980 h=26/></c>
<c id="p1B_r1c2_3" v="根 justfile：無 → 建逐字四行（import &#x27;.vendor_kit/entry.just&#x27;／空行／default:／\t@just --list）；有 → 問 6-20（-y 直接加）；已含 → 不再加；--no-justfile 只印指示" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=340 w=980 h=42/></c>
<c id="p1B_r1c2_4" v="根 .dockerignore：無 → 建三行（.vendor_kit/cache/、gen/、.tmp.*）；有 → 問 6-34 後 append，記於 baseline/.vendor_kit.toml；印建立或修改了什麼" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=382 w=980 h=26/></c>
<c id="p1B_r1c3" v="0／1／3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=262 w=180 h=146/></c>
<c id="p1B_r1c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=262 w=56 h=146/></c>
<c id="p1B_r2c0" v="uninstall⏎uninstall [-y] [--dry-run]" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=408 w=220 h=156/></c>
<c id="p1B_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=410 w=30 h=20/></c>
<c id="p1B_r2c1" v="install" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=408 w=84 h=156/></c>
<c id="p1B_r2c2_0" v="前置：預檢全部工具（有 dev 覆寫 → 1 提示先 undev）；hash 相符的保護清單在任何 remove 之前生效" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=408 w=980 h=26/></c>
<c id="p1B_r2c2_1" v="apply：拿鎖、重驗指紋 → 建日誌 .tmp.uninstall.&lt;id&gt;.toml" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=434 w=980 h=26/></c>
<c id="p1B_r2c2_2" v="逐工具 remove（保護模式）：只刪自產（hash 相符）的檔；未知或被改的保留並回報；目錄非空則保留；不 rm -rf" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=460 w=980 h=26/></c>
<c id="p1B_r2c2_3" v="任一工具回 1 → 中止並列出已完成部分；初始檔一律保留並印清單" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=486 w=980 h=26/></c>
<c id="p1B_r2c2_4" v="根 justfile 那行：問 6-20「要從 justfile 刪這一行嗎」只刪完全相同的行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=512 w=980 h=26/></c>
<c id="p1B_r2c2_5" v="根 .dockerignore 三行與 append 行：問後只刪原文相同的 → 最後刪日誌" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=538 w=980 h=26/></c>
<c id="p1B_r2c3" v="0／1／3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=408 w=180 h=156/></c>
<c id="p1B_r2c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=408 w=56 h=156/></c>
<c id="p1B_r3c0" v="add &lt;repo&gt;[@&lt;tag&gt;]⏎add &lt;repo&gt;[@&lt;tag&gt;] [--source &lt;image&gt;] [--local &lt;tar&gt;] [-y] [--dry-run] [--timeout &lt;秒&gt;]⏎&lt;repo&gt;：[A-Za-z0-9_][A-Za-z0-9_.-]*、不得為 vendor_kit" s="fc=#d5e8d4;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=564 w=220 h=182/></c>
<c id="p1B_r3c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=566 w=30 h=20/></c>
<c id="p1B_r3c1" v="remove" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=240 y=564 w=84 h=182/></c>
<c id="p1B_r3c2_0" v="前置：已接入且完成 → 0 無變更；@&lt;tag&gt; 與鎖定不同 → 1 提示 upgrade；私有 image 無憑證又未指定 @&lt;tag&gt; → 1 印 6-3；dest 撞名／越界 → 拒絕" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=564 w=980 h=26/></c>
<c id="p1B_r3c2_1" v="前置：&lt;ns&gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module（just --dump）(c) 保留名 vendor_kit 撞名 → 1 拒絕" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=590 w=980 h=26/></c>
<c id="p1B_r3c2_2" v="resolve → 主機 docker 展開到 .tmp.dist.&lt;id&gt;/&lt;repo&gt;/ → apply：拿鎖、重驗指紋、建日誌（metadata [progress]）；逐檔讀 /dist" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=616 w=980 h=26/></c>
<c id="p1B_r3c2_3" v="初始檔：無 → 建；有 → 不納管（unmanaged，印 6-11；-y 也不覆蓋）；strategy=&quot;append&quot; 且已存在 → 問 6-21（-y 免問，印出加了什麼）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=642 w=980 h=26/></c>
<c id="p1B_r3c2_4" v="收尾①：materialize → cache/&lt;repo&gt;/ + gen/&lt;repo&gt;.stamp" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=668 w=980 h=26/></c>
<c id="p1B_r3c2_5" v="收尾②：baseline/&lt;repo&gt;/ + metadata（complete=true；--local &lt;tar&gt;：.digest 旁檔取正式 index digest、記 local_image_id）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=694 w=980 h=26/></c>
<c id="p1B_r3c2_6" v="收尾③：gen/tools.just 重生 → version.toml 最後寫 → 刪日誌" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=720 w=980 h=26/></c>
<c id="p1B_r3c3" v="0；1（version.toml 一律未動：dest 不合法、CI 為真需改 tracked、指紋不同、失敗）；3" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1304 y=564 w=180 h=182/></c>
<c id="p1B_r3c4" v="常用" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1484 y=564 w=56 h=182/></c>
<c id="p1B_r4c0" v="remove &lt;repo&gt;⏎remove &lt;repo&gt; [-y] [--dry-run]⏎裸跑 → 用法 + 1" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=746 w=220 h=78/></c>
<c id="p1B_r4c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=748 w=30 h=20/></c>
<c id="p1B_r4c1" v="add" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=746 w=84 h=78/></c>
<c id="p1B_r4c2_0" v="前置：有 dev 覆寫 → 1 提示先 undev；未接 = 0 + 提示；兩段（resolve → apply、重驗指紋）但不經 docker create/cp" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=746 w=980 h=26/></c>
<c id="p1B_r4c2_1" v="建日誌 .tmp.remove.&lt;id&gt;.toml 後刪：version.toml 該行、cache/&lt;repo&gt;/、baseline/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp、gen/tools.just 該工具所有 mod? 行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=772 w=980 h=26/></c>
<c id="p1B_r4c2_2" v="初始檔永不刪，印清單；append 過的行 → 問 6-21「要刪我們加在 &lt;X&gt; 的這幾行嗎」只刪原文相同的（CRLF/LF 等價）→ 刪日誌" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=798 w=980 h=26/></c>
<c id="p1B_r4c3" v="0／1／3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=746 w=180 h=78/></c>
<c id="p1B_r4c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=746 w=56 h=78/></c>
<c id="p1B_r5c0" v="update [&lt;repo&gt;]⏎update [&lt;repo&gt;] [--exit-code]⏎&lt;repo&gt; 可省 = 全部含 vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=824 w=220 h=88/></c>
<c id="p1B_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=826 w=30 h=20/></c>
<c id="p1B_r5c1" v="（upgrade 的前一步）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=824 w=84 h=88/></c>
<c id="p1B_r5c2_0" v="只查 registry（tags/list 取 SemVer 最大正式版，預發行排除），不動任何檔；不受 frozen 影響；單段、不經 docker create/cp" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=824 w=980 h=26/></c>
<c id="p1B_r5c2_1" v="無 registry 憑證時對需認證的工具回 1 印 6-3，其他工具照查再彙總；末行固定 6-15「套用：just vendor_kit upgrade」" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=850 w=980 h=62/></c>
<c id="p1B_r5c3" v="0 已列出；1 查詢失敗（任一工具 1 → 整體 1）；--exit-code 有新版 → 2；3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=824 w=180 h=88/></c>
<c id="p1B_r5c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=824 w=56 h=88/></c>
<c id="p1B_r6c0" v="upgrade &lt;repo&gt;[@&lt;tag&gt;]（工具）⏎upgrade [&lt;repo&gt;[@&lt;tag&gt;]] [-y] [--dry-run] [--timeout &lt;秒&gt;]⏎@&lt;tag&gt; 限單一 repo；比現版舊 → warn 仍執行" s="fc=#d5e8d4;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=912 w=220 h=188/></c>
<c id="p1B_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=914 w=30 h=20/></c>
<c id="p1B_r6c1" v="git revert 整組 commit" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=240 y=912 w=84 h=188/></c>
<c id="p1B_r6c2_0" v="前置：無 baseline → 1 提示 add；工具在 dev 覆寫中 → 1 提示先 undev；不帶 repo 先完整預檢（含 dev 中工具、新增 &lt;ns&gt;／dest 撞名）再動任何東西" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=912 w=980 h=26/></c>
<c id="p1B_r6c2_1" v="(0) conflicts 非空且檔案仍含 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline → 2 停；(1) 有待合併（version.toml 已 B、baseline 仍 A）→ 只補到 B 然後停，印 6-14；(2) 沒有待合併才查最新（或 @&lt;tag&gt;；frozen 不查）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=938 w=980 h=42/></c>
<c id="p1B_r6c2_2" v="resolve → 主機 docker → apply（拿鎖、重驗、建日誌）→ 逐檔狀態機（p1 表；N 讀自 /dist/&lt;repo&gt;）問 6-22；拒絕 → 已納管檔 state 不變只記 declined_hash、新檔 state=declined；CI 為真且需改 tracked 檔 → 1 印清單（與 -y 無關）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=980 w=980 h=42/></c>
<c id="p1B_r6c2_3" v="baseline 推到新版（有衝突仍推；解析失敗不推）+ metadata" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1022 w=980 h=26/></c>
<c id="p1B_r6c2_4" v="materialize cache/、gen/&lt;repo&gt;.stamp；gen/tools.just 重生" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1048 w=980 h=26/></c>
<c id="p1B_r6c2_5" v="version.toml 最後寫 → 刪日誌；--dry-run：只印會問哪些檔與 6-6～6-8、不寫" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1074 w=980 h=26/></c>
<c id="p1B_r6c3" v="0；1 工具層不動 version.toml；2 有衝突（留標記、印檔名、baseline 仍推；解完重跑；merge-file I/O 錯誤 → 1）；3" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1304 y=912 w=180 h=188/></c>
<c id="p1B_r6c4" v="常用" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1484 y=912 w=56 h=188/></c>
<c id="p1B_r7c0" v="upgrade（不帶 repo：全部含自身）⏎upgrade [-y] [--dry-run] [--timeout &lt;秒&gt;]" s="fc=#d5e8d4;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1100 w=220 h=126/></c>
<c id="p1B_r7c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1102 w=30 h=20/></c>
<c id="p1B_r7c1" v="git revert 整組 commit" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=240 y=1100 w=84 h=126/></c>
<c id="p1B_r7c2_0" v="resolve 先判斷「引擎有新版？」：否 → 只升全部工具（同上列；Q27 彙總）；是 → 本次只改第一行、工具不升：舊引擎 apply（拿鎖、重驗、建日誌）只改 vendor_kit 正規行" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1100 w=980 h=42/></c>
<c id="p1B_r7c2_1" v="啟動器 apply 前後各 grep 一次正規行：ref 變了 → local 覆寫有 vendor_kit= 則 docker image inspect 驗 ID 用該 image，否則 docker pull 新 ref → 用新引擎跑 upgrade vendor_kit（下一列）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1142 w=980 h=42/></c>
<c id="p1B_r7c2_2" v="第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b「引擎版本已鎖定為 &lt;vY&gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」，不再重跑" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1184 w=980 h=42/></c>
<c id="p1B_r7c3" v="1 印 6-2「已升級引擎 &lt;vX&gt; → &lt;vY&gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」（已改第一行後回 1 是明列例外）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1100 w=180 h=126/></c>
<c id="p1B_r7c4" v="常用" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1100 w=56 h=126/></c>
<c id="p1B_r8c0" v="upgrade vendor_kit[@&lt;tag&gt;]⏎upgrade vendor_kit[@&lt;tag&gt;] [-y]⏎單段救援路徑（不依賴 resolve/apply 與 gen/）" s="fc=#d5e8d4;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1226 w=220 h=104/></c>
<c id="p1B_r8c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1228 w=30 h=20/></c>
<c id="p1B_r8c1" v="git revert 整組 commit" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=240 y=1226 w=84 h=104/></c>
<c id="p1B_r8c2_0" v="啟動器讀正規行（local 覆寫優先：docker image inspect 驗 vendor_kit_image_id、不 pull）→ 該引擎跑；不被 gen/.stamp 關卡擋" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1226 w=980 h=26/></c>
<c id="p1B_r8c2_1" v="查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版且薄殼首行 hash 相符 → 改第一行 → 啟動器再以新 ref 跑一次 → 新引擎重產薄殼四檔 + gen/.stamp → 1 印 6-2；無新版且相符 → 0；只重產薄殼 → 1 印 6-2；被改 → 1 印 6-28" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1252 w=980 h=42/></c>
<c id="p1B_r8c2_2" v="@&lt;舊版&gt; 降版：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（要退回請 git revert）" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1294 w=980 h=36/></c>
<c id="p1B_r8c3" v="0 無變更；1 印 6-2；3 印 6-10" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1226 w=180 h=104/></c>
<c id="p1B_r8c4" v="常用" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1226 w=56 h=104/></c>
<c id="p1B_r9c0" v="dev &lt;repo&gt;⏎dev &lt;repo&gt; -p &lt;dir&gt;／dev vendor_kit -i &lt;tag&gt;⏎-p（工具必填）與 -i（僅 vendor_kit，只能 tag）互斥" s="fc=#d5e8d4;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1330 w=220 h=110/></c>
<c id="p1B_r9c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1332 w=30 h=20/></c>
<c id="p1B_r9c1" v="undev" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=240 y=1330 w=84 h=110/></c>
<c id="p1B_r9c2_0" v="前置：工具必須已在 version.toml（否 → 1）；&lt;dir&gt;/dist/init.toml 存在（缺 → 1）；CI 為真 → 拒絕；單段、不經 docker create/cp" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1330 w=980 h=26/></c>
<c id="p1B_r9c2_1" v="工具：version.local.toml [tools].&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；cache/&lt;repo&gt;/ 改 symlink → &lt;dir&gt;/dist；gen/&lt;repo&gt;.stamp 第一行 path:&lt;dir&gt;；之後啟動器掛 -v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro，sync 跳過 materialize／verify" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1356 w=980 h=42/></c>
<c id="p1B_r9c2_2" v="自身：version.local.toml vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id；之後啟動器每次 docker image inspect 驗 ID、不 pull；-i 的 image 以 LABEL P／schema 判為「舊」→ 允許但禁止重產 tracked 薄殼" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=324 y=1398 w=980 h=42/></c>
<c id="p1B_r9c3" v="0／1／3" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1330 w=180 h=110/></c>
<c id="p1B_r9c4" v="常用" s="fc=#d5e8d4;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1330 w=56 h=110/></c>
<c id="p1B_r10c0" v="undev &lt;repo&gt;⏎undev &lt;repo&gt;／undev vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1440 w=220 h=84/></c>
<c id="p1B_r10c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1442 w=30 h=20/></c>
<c id="p1B_r10c1" v="dev" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=1440 w=84 h=84/></c>
<c id="p1B_r10c2_0" v="未啟用 = 0 + 提示；兩段：建日誌 .tmp.undev.&lt;id&gt;.toml → 撤 version.local.toml 該行（undev vendor_kit 一併撤 vendor_kit_image_id；最後一個覆寫撤掉後刪整個檔）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1440 w=980 h=42/></c>
<c id="p1B_r10c2_1" v="工具：重新 materialize 鎖定版（經 docker create/cp）；失敗 → 1 保留可恢復狀態。undev vendor_kit：下次 just 用 version.toml 引擎；gen/.stamp ≠ ref → 只提示 6-1、不重寫" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1482 w=980 h=42/></c>
<c id="p1B_r10c3" v="0／1／3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1440 w=180 h=84/></c>
<c id="p1B_r10c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1440 w=56 h=84/></c>
<c id="p1B_r11c0" v="sync [&lt;repo&gt;]⏎sync [&lt;repo&gt;]／sync --verify⏎&lt;repo&gt; 可省 = 全部；--verify = 每檔 sha256 全驗" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1524 w=220 h=152/></c>
<c id="p1B_r11c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1526 w=30 h=20/></c>
<c id="p1B_r11c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=1524 w=84 h=152/></c>
<c id="p1B_r11c2_0" v="每次工具 recipe 自動前置（_sync）；快路徑（無參數）：啟動器只用 grep 比 gen/*.stamp 第一行 vs version.toml、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1524 w=980 h=42/></c>
<c id="p1B_r11c2_1" v="引擎 ref ≠ gen/.stamp 第一行 → 1 印 6-1 不重寫（install／upgrade vendor_kit 跳過此關）；未完成交易 → 1 印 6-33 不恢復；CI 為真下任何 local 覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1566 w=980 h=42/></c>
<c id="p1B_r11c2_2" v="只寫 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp。每工具：覆寫 path → 跳過（仍查完成標記、落後）；cache 缺或印記 ≠ 鎖定 digest → materialize；否則 verify（--verify／CI 為真／版本變動時）→ 失敗 → 重裝 + warn；tools.just 缺 → 重生" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1608 w=980 h=42/></c>
<c id="p1B_r11c2_3" v="無待辦 → resolve 回 apply|no 快路徑 0（不起第二個容器）；baseline 落後：本機 warn 提示 upgrade、CI 為真 → 1 印 6-5" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1650 w=980 h=26/></c>
<c id="p1B_r11c3" v="0；1：薄殼不符、無完成標記（6-13）、CI 為真下 baseline 落後（6-5）或任何 local 覆寫；3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1524 w=180 h=152/></c>
<c id="p1B_r11c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1524 w=56 h=152/></c>
<c id="p1B_r12c0" v="prune⏎prune [-y] [--dry-run]" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1676 w=220 h=84/></c>
<c id="p1B_r12c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1B"><g x=208 y=1678 w=30 h=20/></c>
<c id="p1B_r12c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=1676 w=84 h=84/></c>
<c id="p1B_r12c2_0" v="兩段：resolve prune 輸出 keep 清單（version.toml + version.local.toml 引用的全部 image）→ 啟動器 docker {container,image,network,volume} ls --filter label=io.github.&lt;org&gt;.vendor_kit=1 列候選、扣掉 keep" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1676 w=980 h=42/></c>
<c id="p1B_r12c2_1" v="問 6-32「要刪除以上 vendor_kit 資源嗎？」（-y 免問）→ docker rm／image rm／network rm／volume rm；image 只刪「帶 label 且本專案未引用」者（--dry-run 先看）；活躍的 .tmp.&lt;verb&gt;.&lt;id&gt;.toml 不刪、列出提示 6-33；apply prune 刪失效的 .tmp.dist.*" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1718 w=980 h=42/></c>
<c id="p1B_r12c3" v="0／1／3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1676 w=180 h=84/></c>
<c id="p1B_r12c4" v="進階" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1676 w=56 h=84/></c>
<c id="p1B_r13c0" v="help／h⏎help" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1B"><g x=20 y=1760 w=220 h=42/></c>
<c id="p1B_r13c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=240 y=1760 w=84 h=42/></c>
<c id="p1B_r13c2" v="命名空間層說明（just 做不到 just vendor_kit --help）；各動詞 --help 由引擎印；不觸網、不安裝；明寫「已接入的專案跑 sync，不是 install」；sync 說明 =「依 version.toml 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案」" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=324 y=1760 w=980 h=42/></c>
<c id="p1B_r13c3" v="0" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1304 y=1760 w=180 h=42/></c>
<c id="p1B_r13c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1B"><g x=1484 y=1760 w=56 h=42/></c>
<c id="p1b_lg0" v="綠底：常用動詞" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=1948 w=130 h=40/></c>
<c id="p1b_lg1" v="白底：進階動詞" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=190 y=1948 w=130 h=40/></c>
<c id="p1b_lg2" v="藍底：一次性（bootstrap.sh）" s="fc=#dae8fc;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=340 y=1948 w=210 h=40/></c>
<c id="p1b_lg3" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=570 y=1948 w=190 h=40/></c>
<c id="p1b_lg4" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=780 y=1948 w=110 h=40/></c>
<c id="p1b_lg5" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=910 y=1948 w=200 h=40/></c>
<c id="p1b_lgt" v="一列 = 一個動詞；「做什麼」欄一格一件事⏎「反向」= 收回它做的事的動詞" s="text;fs=12;sc=none;fc=none"><g x=1130 y=1938 w=300 h=60/></c>
<c id="p1b_lg6" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=2014 w=200 h=40/></c>
<c id="p1b_lg6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=208 y=2016 w=30 h=20/></c>
<c id="p1b_lg7" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=2014 w=220 h=40/></c>
<c id="p1b_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=2070 w=300 h=28/></c>
<c id="p1b_tk0" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2104 w=150 h=40/></c>
<c id="p1b_tv0" v="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2104 w=610 h=40/></c>
<c id="p1b_tk1" v="N（目標版範本）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2144 w=150 h=40/></c>
<c id="p1b_tv1" v="逐檔判斷與 dry-run 讀的「新版」= 啟動器展開到暫存 .tmp.dist.&lt;id&gt;/、掛進引擎的 /dist/&lt;repo&gt;（唯讀），不是 cache；cache/&lt;repo&gt;/ 在 apply 決定套用後才 materialize" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2144 w=610 h=40/></c>
<c id="p1b_tk2" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2184 w=150 h=55/></c>
<c id="p1b_tv2" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2184 w=610 h=55/></c>
<c id="p1b_tk3" v="docker image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2239 w=150 h=55/></c>
<c id="p1b_tv3" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2239 w=610 h=55/></c>
<c id="p1b_tk4" v=".digest 旁檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2294 w=150 h=55/></c>
<c id="p1b_tv4" v="離線包 &lt;name&gt;.tar 旁的 &lt;name&gt;.tar.digest：一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2294 w=610 h=55/></c>
<c id="p1b_tk5" v="初始檔五態（state）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2104 w=150 h=55/></c>
<c id="p1b_tv5" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2104 w=610 h=55/></c>
<c id="p1b_tk6" v="救援路徑" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2159 w=150 h=55/></c>
<c id="p1b_tv6" v="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&lt;tag&gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2159 w=610 h=55/></c>
<c id="p1b_tk7" v="「引擎已變」" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2214 w=150 h=55/></c>
<c id="p1b_tv7" v="不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行；ref 變了且 == 計畫的 engine → 用新 ref（local 覆寫時 inspect 驗 ID）跑 upgrade vendor_kit；第二次又變 → 1 印 6-2b" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2214 w=610 h=55/></c>
</diagram>
<diagram id="v1p1c" name="契約 v2：規則、選項表、不開的動詞"><c id="title" v="契約① 使用者介面（3／3）── 規則、選項表（Q25）、結束碼（Q23／Q27）、不開的動詞、訊息文字（§6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p1c_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p1c_pend" v="【本頁無待拍板】⏎選項與結束碼以 interface_spec §1.1／§2 為準；訊息文字 §6 逐字（本頁只列 p1／p1b 引用到的）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p1C" v="3. 規則、選項總表（Q25）、結束碼總表（Q23／Q27）、不開的動詞、訊息文字（interface_spec §6 逐字）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=1777/></c>
<c id="p1C_pair_t" v="兩層成對（反向）" s="text;fs=12;sc=none;fc=none;fst=1" parent="p1C"><g x=20 y=50 w=200 h=24/></c>
<c id="p1C_pd0" v="專案層（vendor_kit 自己）" s="text;fs=12;sc=none;fc=none" parent="p1C"><g x=20 y=74 w=200 h=30/></c>
<c id="p1C_pa0" v="install" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=225 y=74 w=110 h=30/></c>
<c id="p1C_pb0" v="uninstall" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=410 y=74 w=110 h=30/></c>
<c id="p1C_pe0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="p1C_pa0" target="p1C_pb0"></c>
<c id="p1C_pd1" v="工具層" s="text;fs=12;sc=none;fc=none" parent="p1C"><g x=20 y=112 w=200 h=30/></c>
<c id="p1C_pa1" v="add" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=225 y=112 w=110 h=30/></c>
<c id="p1C_pb1" v="remove" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=410 y=112 w=110 h=30/></c>
<c id="p1C_pe1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="p1C_pa1" target="p1C_pb1"></c>
<c id="p1C_pd2" v="本機開發" s="text;fs=12;sc=none;fc=none" parent="p1C"><g x=20 y=150 w=200 h=30/></c>
<c id="p1C_pa2" v="dev" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=225 y=150 w=110 h=30/></c>
<c id="p1C_pb2" v="undev" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=410 y=150 w=110 h=30/></c>
<c id="p1C_pe2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="p1C_pa2" target="p1C_pb2"></c>
<c id="p1C_pd3" v="只查 → 套用（apt 語意）" s="text;fs=12;sc=none;fc=none" parent="p1C"><g x=20 y=188 w=200 h=30/></c>
<c id="p1C_pa3" v="update" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=225 y=188 w=110 h=30/></c>
<c id="p1C_pb3" v="upgrade" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p1C"><g x=410 y=188 w=110 h=30/></c>
<c id="p1C_pe3" v="前一步" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="p1C_pa3" target="p1C_pb3"></c>
<c id="p1C_no" v="【不開的動詞與理由】⏎init（→ install）／ensure（→ sync）／diff（= upgrade --dry-run）／accept（解完衝突重跑 upgrade）／rollback（git revert）／--repair（併進 install 冪等修復）／--purge（明確不提供：永不刪使用者檔；開 issue）／--porcelain（不做；v2 候選，本版無待拍板）／--tag（版本一律 &lt;repo&gt;@&lt;tag&gt;）／materialize、verify、merge（引擎內部步驟，不對外）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=236 w=740 h=92/></c>
<c id="p1C_no_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=728 y=238 w=30 h=20/></c>
<c id="p1C_s1" v="【recipe 規則】⏎動詞 recipe 一律 verb *args 一行轉發（set positional-arguments 只在 vendor.just）、放 tracked 的 vendor.just；[group(&#x27;常用&#x27;)]／[group(&#x27;進階&#x27;)]；每次呼叫引擎附 --protocol P（在子命令之前）；entry.just 與 gen/tools.just 只含 mod／mod?／import?，零 set 零 recipe（被 import 檔的 set 會外溢到根檔）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=342 w=740 h=77/></c>
<c id="p1C_s1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=728 y=344 w=30 h=20/></c>
<c id="p1C_s2" v="【執行位置（Q20）】⏎專案根 = 含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在專案根執行：recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &lt;dir&gt; 執行」；sync 豁免（工具 _sync 已 cd 回專案根）；須在某 git repo 內；禁止巢狀（上層或下層已有 → 1 印 6-35）；引擎不讀 .git、不碰 index、不做 git init" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=433 w=740 h=92/></c>
<c id="p1C_s2_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=728 y=435 w=30 h=20/></c>
<c id="p1C_s3" v="【兩段編排的兩個獨立屬性（p3b 契約④）】⏎需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve → 主機 docker → apply，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=539 w=740 h=77/></c>
<c id="p1C_s3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=728 y=541 w=30 h=20/></c>
<c id="p1C_dry" v="【--dry-run（所有頁一致）】⏎唯讀預覽（仍拉 image 展開到暫存，讀 /dist/&lt;repo&gt;）：印會建／會問哪些檔、6-6～6-8、metadata 遷移；本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單（version.toml 不動；與 -y 無關）；-y 也不覆蓋既有未納管檔、不硬加 append 行；EOF 不算同意" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=630 w=740 h=77/></c>
<c id="p1C_dry_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=728 y=632 w=30 h=20/></c>
<c id="p1C_opt_l" v="選項總表（Q25；短選項只給常用）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p1C"><g x=790 y=50 w=700 h=28/></c>
<c id="p1C_opt_h0" v="選項" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=82 w=170 h=30/></c>
<c id="p1C_opt_h1" v="短形" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=960 y=82 w=50 h=30/></c>
<c id="p1C_opt_h2" v="型別" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=1010 y=82 w=90 h=30/></c>
<c id="p1C_opt_h3" v="適用" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=1100 y=82 w=200 h=30/></c>
<c id="p1C_opt_h4" v="說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=1300 y=82 w=240 h=30/></c>
<c id="p1C_opt_r0c0" v="--tool &lt;repo&gt;[@&lt;tag&gt;]" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=112 w=170 h=42/></c>
<c id="p1C_opt_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=928 y=114 w=30 h=20/></c>
<c id="p1C_opt_r0c1" v="-t" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=112 w=50 h=42/></c>
<c id="p1C_opt_r0c2" v="string，可重複" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=112 w=90 h=42/></c>
<c id="p1C_opt_r0c3" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=112 w=200 h=42/></c>
<c id="p1C_opt_r0c4" v="接入的工具與版本；@&lt;tag&gt; 省略 = 最新正式版" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=112 w=240 h=42/></c>
<c id="p1C_opt_r1c0" v="--yes" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=154 w=170 h=57/></c>
<c id="p1C_opt_r1c1" v="-y" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=154 w=50 h=57/></c>
<c id="p1C_opt_r1c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=154 w=90 h=57/></c>
<c id="p1C_opt_r1c3" v="bootstrap.sh、install、uninstall、add、remove、upgrade、prune" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=154 w=200 h=57/></c>
<c id="p1C_opt_r1c4" v="免詢問（不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=154 w=240 h=57/></c>
<c id="p1C_opt_r2c0" v="--path &lt;dir&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=211 w=170 h=26/></c>
<c id="p1C_opt_r2c1" v="-p" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=211 w=50 h=26/></c>
<c id="p1C_opt_r2c2" v="string" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=211 w=90 h=26/></c>
<c id="p1C_opt_r2c3" v="dev &lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=211 w=200 h=26/></c>
<c id="p1C_opt_r2c4" v="本機工具目錄" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=211 w=240 h=26/></c>
<c id="p1C_opt_r3c0" v="--image &lt;tag&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=237 w=170 h=26/></c>
<c id="p1C_opt_r3c1" v="-i" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=237 w=50 h=26/></c>
<c id="p1C_opt_r3c2" v="string" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=237 w=90 h=26/></c>
<c id="p1C_opt_r3c3" v="dev vendor_kit" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=237 w=200 h=26/></c>
<c id="p1C_opt_r3c4" v="本機引擎 image tag（只能 tag）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=237 w=240 h=26/></c>
<c id="p1C_opt_r4c0" v="--help" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=263 w=170 h=26/></c>
<c id="p1C_opt_r4c1" v="-h" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=263 w=50 h=26/></c>
<c id="p1C_opt_r4c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=263 w=90 h=26/></c>
<c id="p1C_opt_r4c3" v="全部" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=263 w=200 h=26/></c>
<c id="p1C_opt_r4c4" v="由引擎印；bootstrap.sh 自印" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=263 w=240 h=26/></c>
<c id="p1C_opt_r5c0" v="--dry-run" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=289 w=170 h=42/></c>
<c id="p1C_opt_r5c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=289 w=50 h=42/></c>
<c id="p1C_opt_r5c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=289 w=90 h=42/></c>
<c id="p1C_opt_r5c3" v="uninstall、add、remove、upgrade、prune" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=289 w=200 h=42/></c>
<c id="p1C_opt_r5c4" v="唯讀預覽（仍拉 image 展開）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=289 w=240 h=42/></c>
<c id="p1C_opt_r6c0" v="--source &lt;image&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=331 w=170 h=42/></c>
<c id="p1C_opt_r6c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=331 w=50 h=42/></c>
<c id="p1C_opt_r6c2" v="string" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=331 w=90 h=42/></c>
<c id="p1C_opt_r6c3" v="add" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=331 w=200 h=42/></c>
<c id="p1C_opt_r6c4" v="image 路徑不符 &lt;org&gt;/&lt;repo&gt;-dist 慣例時" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=331 w=240 h=42/></c>
<c id="p1C_opt_r7c0" v="--local &lt;image tag 或 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=373 w=170 h=57/></c>
<c id="p1C_opt_r7c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=928 y=375 w=30 h=20/></c>
<c id="p1C_opt_r7c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=373 w=50 h=57/></c>
<c id="p1C_opt_r7c2" v="string" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=373 w=90 h=57/></c>
<c id="p1C_opt_r7c3" v="bootstrap.sh、add" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=373 w=200 h=57/></c>
<c id="p1C_opt_r7c4" v="離線：tar 先 docker load；值的判別已定（含 / 或 .tar 結尾 → 檔案，其餘 → tag；見名詞表）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=373 w=240 h=57/></c>
<c id="p1C_opt_r8c0" v="--exit-code" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=430 w=170 h=26/></c>
<c id="p1C_opt_r8c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=430 w=50 h=26/></c>
<c id="p1C_opt_r8c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=430 w=90 h=26/></c>
<c id="p1C_opt_r8c3" v="update" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=430 w=200 h=26/></c>
<c id="p1C_opt_r8c4" v="有新版回 2" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=430 w=240 h=26/></c>
<c id="p1C_opt_r9c0" v="--timeout &lt;秒&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=456 w=170 h=42/></c>
<c id="p1C_opt_r9c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=928 y=458 w=30 h=20/></c>
<c id="p1C_opt_r9c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=456 w=50 h=42/></c>
<c id="p1C_opt_r9c2" v="正整數" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=456 w=90 h=42/></c>
<c id="p1C_opt_r9c3" v="bootstrap.sh、add、upgrade、sync、undev" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=456 w=200 h=42/></c>
<c id="p1C_opt_r9c4" v="= VENDOR_KIT_PULL_TIMEOUT，由啟動器攔截、不轉發引擎；優先於環境變數" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=456 w=240 h=42/></c>
<c id="p1C_opt_r10c0" v="--no-justfile" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=498 w=170 h=26/></c>
<c id="p1C_opt_r10c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=498 w=50 h=26/></c>
<c id="p1C_opt_r10c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=498 w=90 h=26/></c>
<c id="p1C_opt_r10c3" v="install" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=498 w=200 h=26/></c>
<c id="p1C_opt_r10c4" v="跳過根 justfile 步驟只印指示" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=498 w=240 h=26/></c>
<c id="p1C_opt_r11c0" v="--protocol P" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=524 w=170 h=26/></c>
<c id="p1C_opt_r11c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=524 w=50 h=26/></c>
<c id="p1C_opt_r11c2" v="整數" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=524 w=90 h=26/></c>
<c id="p1C_opt_r11c3" v="內部" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=524 w=200 h=26/></c>
<c id="p1C_opt_r11c4" v="薄殼→引擎全域旗標，不列 help" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=524 w=240 h=26/></c>
<c id="p1C_opt_r12c0" v="--verify" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=790 y=550 w=170 h=42/></c>
<c id="p1C_opt_r12c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=928 y=552 w=30 h=20/></c>
<c id="p1C_opt_r12c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=960 y=550 w=50 h=42/></c>
<c id="p1C_opt_r12c2" v="bool" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=550 w=90 h=42/></c>
<c id="p1C_opt_r12c3" v="sync" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1100 y=550 w=200 h=42/></c>
<c id="p1C_opt_r12c4" v="每檔 sha256 全驗（= CI 為真時的行為）；無參數 sync 走快路徑" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1300 y=550 w=240 h=42/></c>
<c id="p1C_opt_n" v="版本一律寫在位置參數：&lt;repo&gt;@&lt;tag&gt;、vendor_kit@&lt;tag&gt;；@&lt;tag&gt; 比現版舊 → warn 仍執行。短選項只有 -t、-y、-p、-i、-h。" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=790 y=602 w=750 h=46/></c>
<c id="p1C_opt_n_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=1508 y=604 w=30 h=20/></c>
<c id="p1C_ex_l" v="結束碼總表（§2；多工具彙總見下框）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p1C"><g x=20 y=723 w=700 h=28/></c>
<c id="p1C_ex_h0" v="碼" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=755 w=50 h=30/></c>
<c id="p1C_ex_h1" v="定義" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=70 y=755 w=700 h=30/></c>
<c id="p1C_ex_h2" v="動詞例外／特例" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=770 y=755 w=770 h=30/></c>
<c id="p1C_ex_r0c0" v="0" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=785 w=50 h=42/></c>
<c id="p1C_ex_r0c1" v="成功（含 warn）；add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符皆 0 + 提示" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=785 w=700 h=42/></c>
<c id="p1C_ex_r0c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=770 y=785 w=770 h=42/></c>
<c id="p1C_ex_r1c0" v="1" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=827 w=50 h=42/></c>
<c id="p1C_ex_r1c1" v="一般失敗、需使用者處理／重跑；工具層動詞回 1 時 version.toml 不動" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=827 w=700 h=42/></c>
<c id="p1C_ex_r1c2" v="自身升級：已改 version.toml 第一行後回 1（明列例外）；upgrade vendor_kit 重產薄殼後回 1 要求 commit 並重跑（6-2）；sync 薄殼不符回 1（6-1）；印記不符、薄殼被改（6-28）——既定回 1 的情境維持 1，不因提示含 upgrade 而改 3" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=770 y=827 w=770 h=42/></c>
<c id="p1C_ex_r2c0" v="2" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=869 w=50 h=26/></c>
<c id="p1C_ex_r2c1" v="合併衝突（留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=869 w=700 h=26/></c>
<c id="p1C_ex_r2c2" v="update --exit-code 有新版回 2；合併結果 TOML／just 解析失敗 → 2 留原檔、該檔 baseline 不推、記入 conflicts" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=770 y=869 w=770 h=26/></c>
<c id="p1C_ex_r3c0" v="3" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=895 w=50 h=57/></c>
<c id="p1C_ex_r3c1" v="現有薄殼／檔案／引擎的組合需先升級或退回才能繼續，且零寫入；「舊」一律以 P／schema 比，不以 SemVer；網路／認證／不存在 → 1，不得偽裝成 3；floor 檢查在任何上網之前" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=895 w=700 h=57/></c>
<c id="p1C_ex_r3c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=738 y=897 w=30 h=20/></c>
<c id="p1C_ex_r3c2" v="(a) 薄殼 P &lt; 引擎 floor_P → 6-18；(b) 引擎讀到 schema &gt; 支援上限 → 6-19；(c) upgrade vendor_kit@&lt;舊版&gt; 目標引擎 P／schema 低於現有檔 → 6-10；(d) dev vendor_kit -i 的引擎 P／schema 低於薄殼首行者要重產 tracked 薄殼 → 拒絕；(e) 舊薄殼跑新 major 一般動詞 → 6-36 提示先 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=770 y=895 w=770 h=57/></c>
<c id="p1C_multi" v="【多工具彙總（Q27）】：不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p1C"><g x=20 y=966 w=1520 h=30/></c>
<c id="p1C_multi_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p1C"><g x=1508 y=968 w=30 h=20/></c>
<c id="p1C_msg_l" v="訊息文字清單（§6 逐字；每句含可直接複製的指令）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p1C"><g x=20 y=1010 w=900 h=28/></c>
<c id="p1C_mL_h0" v="#" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1042 w=50 h=30/></c>
<c id="p1C_mL_h1" v="時機" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=70 y=1042 w=170 h=30/></c>
<c id="p1C_mL_h2" v="文字（逐字；&lt;…&gt; 占位符）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=240 y=1042 w=530 h=30/></c>
<c id="p1C_mL_r0c0" v="6-1" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1072 w=50 h=42/></c>
<c id="p1C_mL_r0c1" v="sync：gen/.stamp 第一行 ≠ 引擎 ref" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1072 w=170 h=42/></c>
<c id="p1C_mL_r0c2" v="vendor_kit 已更新 &lt;vX&gt; → &lt;vY&gt;，請執行：just vendor_kit upgrade vendor_kit（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1072 w=530 h=42/></c>
<c id="p1C_mL_r1c0" v="6-2" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1114 w=50 h=42/></c>
<c id="p1C_mL_r1c1" v="upgrade vendor_kit 重產薄殼後" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1114 w=170 h=42/></c>
<c id="p1C_mL_r1c2" v="已升級引擎 &lt;vX&gt; → &lt;vY&gt; 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1114 w=530 h=42/></c>
<c id="p1C_mL_r2c0" v="6-2b" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1156 w=50 h=42/></c>
<c id="p1C_mL_r2c1" v="第一行已改但未重產／第二次又變" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1156 w=170 h=42/></c>
<c id="p1C_mL_r2c2" v="引擎版本已鎖定為 &lt;vY&gt;，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1156 w=530 h=42/></c>
<c id="p1C_mL_r3c0" v="6-3" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1198 w=50 h=57/></c>
<c id="p1C_mL_r3c1" v="update／upgrade／add 無 registry 憑證" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1198 w=170 h=57/></c>
<c id="p1C_mL_r3c2" v="無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1198 w=530 h=57/></c>
<c id="p1C_mL_r4c0" v="6-4" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1255 w=50 h=42/></c>
<c id="p1C_mL_r4c1" v="需詢問但無 tty／EOF 且無 -y" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1255 w=170 h=42/></c>
<c id="p1C_mL_r4c2" v="需要確認但沒有終端可互動。請加 -y，或在終端執行。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1255 w=530 h=42/></c>
<c id="p1C_mL_r5c0" v="6-5" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1297 w=50 h=42/></c>
<c id="p1C_mL_r5c1" v="CI 下 baseline 落後；Renovate PR 需合併" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1297 w=170 h=42/></c>
<c id="p1C_mL_r5c2" v="請在本機執行 just vendor_kit upgrade &lt;repo&gt; -y 後 commit 並 push（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1297 w=530 h=42/></c>
<c id="p1C_mL_r6c0" v="6-6／6-7／6-8" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1339 w=50 h=57/></c>
<c id="p1C_mL_r6c1" v="dry-run／check.sh 提醒（不紅燈）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1339 w=170 h=57/></c>
<c id="p1C_mL_r6c2" v="有 &lt;N&gt; 個範本你拒絕過／&lt;X&gt; 沒納管，與範本差 &lt;N&gt; 行／&lt;Y&gt; 你拒絕過，&lt;vZ&gt; 有新版" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1339 w=530 h=57/></c>
<c id="p1C_mL_r7c0" v="6-9" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1396 w=50 h=26/></c>
<c id="p1C_mL_r7c1" v="不在專案根執行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1396 w=170 h=26/></c>
<c id="p1C_mL_r7c2" v="請到 &lt;dir&gt; 執行（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1396 w=530 h=26/></c>
<c id="p1C_mL_r8c0" v="6-10" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1422 w=50 h=42/></c>
<c id="p1C_mL_r8c1" v="upgrade vendor_kit@&lt;舊版&gt; 無法無損讀" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1422 w=170 h=42/></c>
<c id="p1C_mL_r8c2" v="目標引擎 &lt;vY&gt;（協定 &lt;P&gt;、schema &lt;M&gt;）無法無損讀取現有檔（schema &lt;N&gt;）。未修改任何檔。要退回舊版請 git revert 相關 commit。（結束 3）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1422 w=530 h=42/></c>
<c id="p1C_mL_r9c0" v="6-11" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1464 w=50 h=26/></c>
<c id="p1C_mL_r9c1" v="add 初始檔已存在（copy）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1464 w=170 h=26/></c>
<c id="p1C_mL_r9c2" v="&lt;X&gt; 已存在，未納管；範本在 .vendor_kit/cache/&lt;repo&gt;/files/ 可自行比對" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1464 w=530 h=26/></c>
<c id="p1C_mL_r10c0" v="6-12" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1490 w=50 h=26/></c>
<c id="p1C_mL_r10c1" v="apply 重驗指紋不同" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1490 w=170 h=26/></c>
<c id="p1C_mL_r10c2" v="專案狀態在執行期間變動，未寫入任何檔。請重跑：just vendor_kit &lt;verb&gt; …（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1490 w=530 h=26/></c>
<c id="p1C_mL_r11c0" v="6-13" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1516 w=50 h=42/></c>
<c id="p1C_mL_r11c1" v="sync metadata 無完成標記" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1516 w=170 h=42/></c>
<c id="p1C_mL_r11c2" v="&lt;repo&gt; 未完成接入，請執行：just vendor_kit add &lt;repo&gt;（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1516 w=530 h=42/></c>
<c id="p1C_mL_r12c0" v="6-14" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1558 w=50 h=42/></c>
<c id="p1C_mL_r12c1" v="upgrade 補完待合併後另有新版" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1558 w=170 h=42/></c>
<c id="p1C_mL_r12c2" v="已補齊 &lt;repo&gt; 至 &lt;vB&gt;；另有新版 &lt;vX&gt;，再跑一次 just vendor_kit upgrade &lt;repo&gt; 可升" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1558 w=530 h=42/></c>
<c id="p1C_mL_r13c0" v="6-15" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1600 w=50 h=26/></c>
<c id="p1C_mL_r13c1" v="update 末行" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1600 w=170 h=26/></c>
<c id="p1C_mL_r13c2" v="套用：just vendor_kit upgrade" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1600 w=530 h=26/></c>
<c id="p1C_mL_r14c0" v="6-16" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1626 w=50 h=42/></c>
<c id="p1C_mL_r14c1" v="install 非 git repo" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1626 w=170 h=42/></c>
<c id="p1C_mL_r14c2" v="目前目錄不在 Git repository 內。請先自行執行 git init，再重新執行 bootstrap.sh。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1626 w=530 h=42/></c>
<c id="p1C_mL_r15c0" v="6-17" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1668 w=50 h=26/></c>
<c id="p1C_mL_r15c1" v="install &lt;repo&gt; 誤用" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1668 w=170 h=26/></c>
<c id="p1C_mL_r15c2" v="install 不接受工具名稱。接入工具請執行：just vendor_kit add &lt;repo&gt;（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1668 w=530 h=26/></c>
<c id="p1C_mL_r16c0" v="6-18" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=20 y=1694 w=50 h=26/></c>
<c id="p1C_mL_r16c1" v="薄殼／版本低於 floor" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=70 y=1694 w=170 h=26/></c>
<c id="p1C_mL_r16c2" v="目前薄殼或引擎低於支援下限 &lt;floor&gt;。請以 bootstrap.sh 重建。（結束 3、零寫入）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=240 y=1694 w=530 h=26/></c>
<c id="p1C_mR_h0" v="#" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1042 w=50 h=30/></c>
<c id="p1C_mR_h1" v="時機" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=840 y=1042 w=170 h=30/></c>
<c id="p1C_mR_h2" v="文字（逐字；&lt;…&gt; 占位符）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p1C"><g x=1010 y=1042 w=530 h=30/></c>
<c id="p1C_mR_r0c0" v="6-19" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1072 w=50 h=57/></c>
<c id="p1C_mR_r0c1" v="引擎讀到 schema 高於支援上限" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1072 w=170 h=57/></c>
<c id="p1C_mR_r0c2" v="無法讀取 &lt;file&gt;：schema &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;。請使用支援此 schema 的引擎，或使用 version.toml 指定的引擎。（結束 3）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1072 w=530 h=57/></c>
<c id="p1C_mR_r1c0" v="6-20" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1129 w=50 h=42/></c>
<c id="p1C_mR_r1c1" v="問句：根 justfile" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1129 w=170 h=42/></c>
<c id="p1C_mR_r1c2" v="要在 justfile 加這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;／要從 justfile 刪這一行嗎：import &#x27;.vendor_kit/entry.just&#x27;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1129 w=530 h=42/></c>
<c id="p1C_mR_r2c0" v="6-21" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1171 w=50 h=26/></c>
<c id="p1C_mR_r2c1" v="問句：append" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1171 w=170 h=26/></c>
<c id="p1C_mR_r2c2" v="要在 &lt;X&gt; 加這幾行嗎（接列出行）／要刪我們加在 &lt;X&gt; 的這幾行嗎（接列出行）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1171 w=530 h=26/></c>
<c id="p1C_mR_r3c0" v="6-22" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1197 w=50 h=42/></c>
<c id="p1C_mR_r3c1" v="問句：upgrade 逐檔" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1197 w=170 h=42/></c>
<c id="p1C_mR_r3c2" v="&lt;X&gt; 換成新版？／你和新版都改了 &lt;X&gt;，要三方合併嗎？／要建 &lt;X&gt; 嗎／&lt;X&gt; 是二進位檔，要換成新版嗎？" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1197 w=530 h=42/></c>
<c id="p1C_mR_r4c0" v="6-23" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1239 w=50 h=42/></c>
<c id="p1C_mR_r4c1" v="bootstrap just 太舊" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1239 w=170 h=42/></c>
<c id="p1C_mR_r4c2" v="需要 just ≥ 1.33.0，目前為 &lt;version&gt;。請使用 GitHub release 版。+ 固定兩行 下載：&lt;平台對應 URL&gt;、安裝：&lt;不覆蓋既有檔的安裝指令&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1239 w=530 h=42/></c>
<c id="p1C_mR_r5c0" v="6-24" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1281 w=50 h=57/></c>
<c id="p1C_mR_r5c1" v="docker pull 失敗" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1281 w=170 h=57/></c>
<c id="p1C_mR_r5c2" v="原文 + 三分類（網路／認證／不存在；另「主機錯誤」：daemon 不可用、磁碟滿）；認證類：&lt;ref&gt; 不存在或無權限（GHCR 未登入一律 denied），私有請先 docker login &lt;host&gt;；僅 add／bootstrap 追加 離線可用：--local &lt;tar&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1281 w=530 h=57/></c>
<c id="p1C_mR_r6c0" v="6-26" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1338 w=50 h=42/></c>
<c id="p1C_mR_r6c1" v="flock 逾時" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1338 w=170 h=42/></c>
<c id="p1C_mR_r6c2" v="專案目錄被鎖定（PID &lt;pid&gt;，自 &lt;time&gt;）；60 秒內未釋放。確認無其他 vendor_kit 在跑後重試，或設 VENDOR_KIT_NO_LOCK=1。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1338 w=530 h=42/></c>
<c id="p1C_mR_r7c0" v="6-28" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1380 w=50 h=57/></c>
<c id="p1C_mR_r7c1" v="薄殼被改（install／upgrade vendor_kit）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1380 w=170 h=57/></c>
<c id="p1C_mR_r7c2" v="偵測到薄殼被修改：&lt;files&gt;。未重產任何薄殼。請先檢視下列差異；確認並手動還原（git checkout -- .vendor_kit/&lt;file&gt;）後，再執行 just vendor_kit upgrade vendor_kit。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1380 w=530 h=57/></c>
<c id="p1C_mR_r8c0" v="6-29" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1437 w=50 h=42/></c>
<c id="p1C_mR_r8c1" v="新增初始檔 dest 在 CI 路徑" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1437 w=170 h=42/></c>
<c id="p1C_mR_r8c2" v="注意：新版範本將建立或修改 CI 設定 &lt;X&gt;。請確認下列內容後再決定是否套用。" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1437 w=530 h=42/></c>
<c id="p1C_mR_r9c0" v="6-30" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1479 w=50 h=42/></c>
<c id="p1C_mR_r9c1" v="啟動器驗 vk-resolve 失敗" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1479 w=170 h=42/></c>
<c id="p1C_mR_r9c2" v="引擎輸出不完整或不相容（&lt;原因&gt;），未執行任何動作。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1479 w=530 h=42/></c>
<c id="p1C_mR_r10c0" v="6-31" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1521 w=50 h=42/></c>
<c id="p1C_mR_r10c1" v="pull 逾時" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1521 w=170 h=42/></c>
<c id="p1C_mR_r10c2" v="拉取 &lt;ref&gt; 超過 &lt;秒&gt; 秒未完成，已中止。可用 --timeout &lt;秒&gt; 或 VENDOR_KIT_PULL_TIMEOUT 調整。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1521 w=530 h=42/></c>
<c id="p1C_mR_r11c0" v="6-32" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1563 w=50 h=26/></c>
<c id="p1C_mR_r11c1" v="問句：prune" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1563 w=170 h=26/></c>
<c id="p1C_mR_r11c2" v="要刪除以上 vendor_kit 資源嗎？" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1563 w=530 h=26/></c>
<c id="p1C_mR_r12c0" v="6-33" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1589 w=50 h=42/></c>
<c id="p1C_mR_r12c1" v="唯讀動詞偵測未完成交易" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1589 w=170 h=42/></c>
<c id="p1C_mR_r12c2" v="偵測到未完成的 &lt;verb&gt;（&lt;id&gt;）。請先重跑：just vendor_kit &lt;verb&gt; &lt;targets&gt;（sync／update 結束 1；help 不受影響；prune 只列出不刪）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1589 w=530 h=42/></c>
<c id="p1C_mR_r13c0" v="6-34" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1631 w=50 h=42/></c>
<c id="p1C_mR_r13c1" v="問句：根 .dockerignore" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1631 w=170 h=42/></c>
<c id="p1C_mR_r13c2" v="要在 .dockerignore 加這三行嗎：.vendor_kit/cache/ .vendor_kit/gen/ .vendor_kit/.tmp.*" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1631 w=530 h=42/></c>
<c id="p1C_mR_r14c0" v="6-35" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1673 w=50 h=42/></c>
<c id="p1C_mR_r14c1" v="install 巢狀" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1673 w=170 h=42/></c>
<c id="p1C_mR_r14c2" v="&lt;dir&gt; 已有 .vendor_kit/，不允許巢狀接入。請到該目錄執行，或先 uninstall。（結束 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1673 w=530 h=42/></c>
<c id="p1C_mR_r15c0" v="6-36" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p1C"><g x=790 y=1715 w=50 h=42/></c>
<c id="p1C_mR_r15c1" v="舊薄殼跑新 major 一般動詞" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=840 y=1715 w=170 h=42/></c>
<c id="p1C_mR_r15c2" v="薄殼協定 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般動詞需求。請先執行：just vendor_kit upgrade vendor_kit（結束 3、零寫入）" s="fc=#ffffff;sc=#999999;fs=12" parent="p1C"><g x=1010 y=1715 w=530 h=42/></c>
<c id="p1c_lg0" v="綠底：常用動詞" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=1903 w=130 h=40/></c>
<c id="p1c_lg1" v="白底：進階動詞" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=190 y=1903 w=130 h=40/></c>
<c id="p1c_lg2" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=340 y=1903 w=190 h=40/></c>
<c id="p1c_lg3" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=550 y=1903 w=110 h=40/></c>
<c id="p1c_lg4" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=680 y=1903 w=200 h=40/></c>
<c id="p1c_lg5" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=900 y=1903 w=200 h=40/></c>
<c id="p1c_lg5_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1068 y=1905 w=30 h=20/></c>
<c id="p1c_lgt" v="「反向」= 收回它做的事的動詞⏎表格：一列一個選項／結束碼／訊息" s="text;fs=12;sc=none;fc=none"><g x=1120 y=1893 w=300 h=60/></c>
<c id="p1c_lg6" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1969 w=220 h=40/></c>
<c id="p1c_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=2025 w=300 h=28/></c>
<c id="p1c_tk0" v="組（常用／進階／一次性）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2059 w=150 h=40/></c>
<c id="p1c_tv0" v="常用 = 每天會打的（add／upgrade／dev）；進階 = 偶爾才用；一次性 = 只在第一次接入跑的 bootstrap.sh（release 附的腳本，不是 just 動詞）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2059 w=610 h=40/></c>
<c id="p1c_tk1" v="反向" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2099 w=150 h=40/></c>
<c id="p1c_tv1" v="把該動詞做的事收回的動詞（install↔uninstall、add↔remove、dev↔undev）；upgrade 沒有動詞反向，靠 git revert（把整組升級 commit 反做一次的 git 指令）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2099 w=610 h=40/></c>
<c id="p1c_tk2" v="apt 語意" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2139 w=150 h=28/></c>
<c id="p1c_tv2" v="跟 Debian 的 apt 一樣分兩步：update 只查有沒有新版、不動檔；upgrade 才真的套用" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2139 w=610 h=28/></c>
<c id="p1c_tk3" v="--local 值的判別" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2167 w=150 h=40/></c>
<c id="p1c_tv3" v="已定：--local &lt;值&gt; 含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立（tag 含 / 且存在同名檔）→ 1 提示用 ./ 或完整 ref 消歧" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2167 w=610 h=40/></c>
<c id="p1c_tk4" v="pull 逾時" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2207 w=150 h=40/></c>
<c id="p1c_tv4" v="VENDOR_KIT_PULL_TIMEOUT／--timeout &lt;秒&gt;：單次 pull 總秒數，預設 300、只收正整數；逾時 → 1 印 6-31；啟動器自讀、不轉發引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2207 w=610 h=40/></c>
<c id="p1c_tk5" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2247 w=150 h=55/></c>
<c id="p1c_tv5" v="0 成功（含 warn）；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級已改第一行後要求重跑也回 1）；2 = 有衝突要你處理，或 update --exit-code 有新版；3 = 版本／協定／schema 不合，須先升級或退回，回 3 時零寫入" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2247 w=610 h=55/></c>
<c id="p1c_tk6" v="--protocol P" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2059 w=150 h=40/></c>
<c id="p1c_tv6" v="薄殼每次呼叫引擎都附的協定整數（第一版 P=1，在子命令之前）；引擎接受 [floor_P, current_P] 並依呼叫方 P 回應；太舊 → 一般動詞乾淨回 3 印 6-36，救援路徑永久可用" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2059 w=610 h=40/></c>
<c id="p1c_tk7" v="floor" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2099 w=150 h=40/></c>
<c id="p1c_tv7" v="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2099 w=610 h=40/></c>
<c id="p1c_tk8" v="mod／mod?／import／import?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2139 w=150 h=55/></c>
<c id="p1c_tv8" v="just 的載入：mod &lt;ns&gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2139 w=610 h=55/></c>
<c id="p1c_tk9" v="專案根" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2194 w=150 h=71/></c>
<c id="p1c_tv9" v="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &lt;dir&gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2194 w=610 h=71/></c>
</diagram>
<diagram id="v1p2" name="契約 v2：目錄樹與檔案範例"><c id="title" v="契約② 專案裡的檔（1／3）── 目錄樹與檔案範例（interface_spec §4；誰寫它、誰可以改、進不進 git）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p2_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p2_pend" v="【本頁無待拍板】⏎檔名 version.toml 已定（§4.1：它是「該裝哪版」的宣告，不是 lock 產物）；右欄範例框逐字（等寬、保留縮排），說明一律放框外" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=81/></c>
<c id="p2_lbl" v="3. 目錄樹（專案根 = 含 .vendor_kit/ 的目錄；每格：用途｜寫：誰產生｜改：誰可改）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=109 w=620 h=28/></c>
<c id="t_root" v="【專案/】（使用者的；專案根）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=40 y=143 w=200 h=46/></c>
<c id="t_just" v="【justfile】 ── 使用者的 just 入口；install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;（無 → 建四行；有 → 問／-y；已含 → 不再加）⏎寫：install｜改：使用者隨意；uninstall 問後只刪完全相同的那行；add 只讀它查撞名" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=70 y=197 w=560 h=77/></c>
<c id="t_just_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=199 w=30 h=20/></c>
<c id="t_di" v="【.dockerignore】 ── 使用者的；install 加三行 .vendor_kit/cache/、gen/、.tmp.*（無 → 建；有 → 問 6-34／-y）⏎寫：install（記於 baseline/.vendor_kit.toml）｜改：使用者隨意；uninstall 問後只刪原文相同行" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=70 y=282 w=560 h=77/></c>
<c id="t_di_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=284 w=30 h=20/></c>
<c id="t_vk" v="【.vendor_kit/】 ── 根目錄只多這一個；薄殼 + 狀態 + 快取都在裡面；上層或下層不得再有一個（禁止巢狀）⏎寫：install、upgrade vendor_kit 重產薄殼（先比對薄殼首行）｜改：人不改；uninstall 只刪 hash 相符的自產檔" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=70 y=367 w=560 h=77/></c>
<c id="t_vk_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=369 w=30 h=20/></c>
<c id="t_ver" v="【version.toml】 ── 進 git：唯一來源。vendor_kit = &quot;&lt;ref&gt;&quot; 正規行（唯一）、schema、written_by、[tools] 一行一工具 tag@digest⏎寫：install／add／upgrade／remove（apply 最後才寫）｜改：使用者可手改、Renovate PR 改；sync 只讀" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=452 w=530 h=77/></c>
<c id="t_ver_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=454 w=30 h=20/></c>
<c id="t_vl" v="【version.local.toml】 ── 不進 git（自有 .gitignore 擋）；與 version.toml 同形：工具覆寫 path:&lt;dir&gt;；引擎覆寫 tag + vendor_kit_image_id⏎寫：dev／undev（含 image ID）；bootstrap --local 在 install 成功後才寫｜改：不建議手改；uninstall hash 相符才刪；CI 為真下有任何覆寫 → sync 回 1" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=100 y=537 w=530 h=108/></c>
<c id="t_vl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=539 w=30 h=20/></c>
<c id="t_gi" v="【.gitignore】 ── 進 git，我們自己的：cache/ gen/ version.local.toml .tmp.*；第一行自描述⏎寫：install／upgrade vendor_kit 重產｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=653 w=530 h=61/></c>
<c id="t_gi_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=655 w=30 h=20/></c>
<c id="t_entry" v="【entry.just】 ── 進 git：mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;（零 set 零 recipe）；第一行自描述⏎寫：引擎 launcher-gen（install／upgrade vendor_kit）｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=722 w=530 h=61/></c>
<c id="t_entry_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=724 w=30 h=20/></c>
<c id="t_vj" v="【vendor.just】 ── 進 git：動詞 recipe 一行轉發 + 啟動器本體（POSIX sh；set positional-arguments 只放這；附 --protocol P）；第一行自描述⏎寫：引擎 launcher-gen｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=791 w=530 h=77/></c>
<c id="t_vj_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=793 w=30 h=20/></c>
<c id="t_ci" v="【ci/check.sh】 ── 進 git：下游 CI 呼叫的契約檢查（⓪–⑤ 六步，契約⑤ p3c）；第一行 shebang、第二行自描述、之後 export CI=1⏎寫：引擎 launcher-gen｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=876 w=530 h=61/></c>
<c id="t_ci_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=878 w=30 h=20/></c>
<c id="t_bl" v="【baseline/】 ── 進 git：install 建 .gitkeep（git 不追蹤空目錄）；&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；.vendor_kit.toml = install 對根 .dockerignore 的 append 記錄⏎寫：install（.gitkeep）；add 建 &lt;repo&gt;/、upgrade 推進（有衝突仍推）｜改：人不改（改了合併就錯）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=100 y=945 w=530 h=92/></c>
<c id="t_bl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=947 w=30 h=20/></c>
<c id="t_meta" v="【&lt;repo&gt;/.vendor_kit.toml】 ── 進 git：metadata（欄位見 p2b）；兼作該目錄佔位⏎寫：add／upgrade（install 不建）｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=130 y=1045 w=500 h=61/></c>
<c id="t_meta_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1047 w=30 h=20/></c>
<c id="t_gen" v="【gen/】 ── 不進 git：引擎產生的三種檔（下列三格），各自由不同動詞寫⏎寫：引擎｜改：人不改（會被覆蓋）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=100 y=1114 w=530 h=46/></c>
<c id="t_gen_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1116 w=30 h=20/></c>
<c id="t_tools" v="【tools.just】 ── 每個 &lt;ns&gt;.just 一行 mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27;（上方一行 # &lt;description&gt;；零 set 零 recipe）⏎寫：sync／add／remove／upgrade 重生（最後寫、與 cache 同一 apply 內原子替換）｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1168 w=500 h=92/></c>
<c id="t_tools_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1170 w=30 h=20/></c>
<c id="t_gstamp" v="【.stamp】 ── 只記產生薄殼的引擎 ref（一行；local 覆寫時為 &lt;tag&gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1（不重寫）⏎寫：只由 install／upgrade vendor_kit｜改：人不改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1268 w=500 h=61/></c>
<c id="t_gstamp_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1270 w=30 h=20/></c>
<c id="t_rstamp" v="【&lt;repo&gt;.stamp】 ── 每工具一個印記：第一行 index digest（dev 時 path:&lt;dir&gt;），之後每檔 sha256；sync 用它決定要不要 materialize⏎寫：引擎 materialize｜改：不可改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1337 w=500 h=61/></c>
<c id="t_rstamp_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1339 w=30 h=20/></c>
<c id="t_repo" v="【cache/&lt;repo&gt;/】 ── 不進 git、使用者不可改；只放從暫存 /dist 展開的內容（dev 時是 symlink → &lt;dir&gt;/dist）⏎寫：引擎 materialize（apply 決定套用之後）｜改：不可改（verify 失敗 → 重裝並 warn）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=100 y=1406 w=530 h=77/></c>
<c id="t_repo_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1408 w=30 h=20/></c>
<c id="t_files" v="【files/ …】 ── 工具檔案（dist/files/ 全部；無 symlink，展開時驗）｜寫：materialize｜改：不可改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1491 w=500 h=46/></c>
<c id="t_init" v="【init.toml】 ── 初始檔清單（[[file]] src／dest／strategy = &quot;copy&quot;|&quot;append&quot;；schema；description）｜寫：materialize｜改：不可改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1545 w=500 h=61/></c>
<c id="t_init_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1547 w=30 h=20/></c>
<c id="t_rjust" v="【just/&lt;ns&gt;.just】 ── 工具的 just 模組，每檔一個頂層命名空間（&lt;repo&gt;.just 必有；含私有 _sync）｜寫：materialize｜改：不可改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=130 y=1614 w=500 h=46/></c>
<c id="t_rjust_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1616 w=30 h=20/></c>
<c id="t_tmp" v="【.tmp.&lt;verb&gt;.&lt;id&gt;.toml】、【.tmp.dist.&lt;id&gt;/】 ── 不進 git：remove／uninstall／undev／prune 的進度日誌；啟動器暫存（展開的 dist、vk-resolve）⏎寫：apply 第一個寫入前建、最後一步刪；啟動器 mktemp、trap 刪｜改：人不改；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=100 y=1668 w=530 h=92/></c>
<c id="t_tmp_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1670 w=30 h=20/></c>
<c id="t_user" v="【初始檔】（例 Dockerfile…；路徑由 init.toml 的 dest 決定）── 使用者的；進 git；state 記在 metadata（五態）⏎寫：add 建（已存在不納管；append 問後加行）、upgrade 逐檔問後換／三方合併／建新檔｜改：使用者隨意；remove／uninstall 永不刪，印清單" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=70 y=1768 w=560 h=77/></c>
<c id="t_user_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=598 y=1770 w=30 h=20/></c>
<c id="te1" s="fs=12;exitX=0.07;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_root" target="t_just"><g pts=54,235.5/></c>
<c id="te21" s="fs=12;exitX=0.07;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_root" target="t_di"><g pts=54,320.5/></c>
<c id="te2" s="fs=12;exitX=0.07;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_root" target="t_vk"><g pts=54,405.5/></c>
<c id="te3" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_ver"><g pts=84,490.5/></c>
<c id="te4" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_vl"><g pts=84,591.0/></c>
<c id="te5" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_gi"><g pts=84,683.5/></c>
<c id="te6" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_entry"><g pts=84,752.5/></c>
<c id="te7" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_vj"><g pts=84,829.5/></c>
<c id="te8" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_ci"><g pts=84,906.5/></c>
<c id="te9" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_bl"><g pts=84,991.0/></c>
<c id="te10" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_bl" target="t_meta"><g pts=114,1075.5/></c>
<c id="te11" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_gen"><g pts=84,1137.0/></c>
<c id="te12" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_gen" target="t_tools"><g pts=114,1214.0/></c>
<c id="te13" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_gen" target="t_gstamp"><g pts=114,1298.5/></c>
<c id="te15" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_gen" target="t_rstamp"><g pts=114,1367.5/></c>
<c id="te14" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_repo"><g pts=84,1444.5/></c>
<c id="te16" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_repo" target="t_files"><g pts=114,1514.0/></c>
<c id="te17" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_repo" target="t_init"><g pts=114,1575.5/></c>
<c id="te18" s="fs=12;exitX=0.0264;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_repo" target="t_rjust"><g pts=114,1637.0/></c>
<c id="te20" s="fs=12;exitX=0.025;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_vk" target="t_tmp"><g pts=84,1714.0/></c>
<c id="te19" s="fs=12;exitX=0.07;exitY=1;entryX=0;entryY=0.5" edge="1" source="t_root" target="t_user"><g pts=54,1806.5/></c>
<c id="p2_ver_l" v=".vendor_kit/version.toml（進 git；schema = 1）── 啟動器只靠 grep 讀正規行" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=109 w=940 h=28/></c>
<c id="p2_ver" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;ghcr.io/&lt;org&gt;/vendor_kit:v1.0.0@sha256:&lt;digest&gt;&quot;⏎schema = 1⏎written_by = &quot;v1.0.0&quot;⏎⏎[tools]⏎&lt;repo&gt; = &quot;ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist:v2.3.0@sha256:&lt;digest&gt;&quot;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=141 w=497 h=108/></c>
<c id="p2_ver_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1125 y=143 w=30 h=20/></c>
<c id="p2_ver_n" v="第 1 行 = 唯一正規行：行首無空白、鍵後一空白、=、一空白、雙引號、【無尾端註解】、LF（regex 讀不到就是 1）⏎schema：格式版本，引擎讀、啟動器不讀；written_by：寫入引擎版本，純資訊⏎[tools]：每工具一行 tag@digest（多架構 index digest）" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=1169 y=141 w=431 h=108/></c>
<c id="p2_vl_l" v=".vendor_kit/version.local.toml（不進 git；與 version.toml 同形）── dev 寫、undev 刪、bootstrap --local 寫" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=263 w=940 h=28/></c>
<c id="p2_vl" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vendor_kit = &quot;vendor_kit:dev&quot;⏎vendor_kit_image_id = &quot;sha256:&lt;image id&gt;&quot;⏎schema = 1⏎written_by = &quot;v1.0.0&quot;⏎⏎[tools]⏎&lt;repo&gt; = &quot;path:/home/me/&lt;repo&gt;&quot;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=295 w=346 h=124/></c>
<c id="p2_vl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=974 y=297 w=30 h=20/></c>
<c id="p2_vl_n" v="vendor_kit：dev vendor_kit -i &lt;tag&gt; 寫的本機引擎 image，只能 tag（docker load 後無 RepoDigests）；同樣是正規行、無尾端註解⏎vendor_kit_image_id：啟動器每次 docker image inspect 比對、不 pull；同 tag 重 build 才會被發現；undev 一併撤⏎[tools].&lt;repo&gt;：dev &lt;repo&gt; -p &lt;dir&gt; 寫 path:&lt;dir&gt;；cache/&lt;repo&gt;/ 變 symlink → &lt;dir&gt;/dist；啟動器掛 -v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=1018 y=295 w=582 h=124/></c>
<c id="p2_jf_l" v="根 justfile（使用者的；install 新建時逐字四行；已有時只加第一行）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=433 w=940 h=28/></c>
<c id="p2_jf" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;import &#x27;.vendor_kit/entry.just&#x27;⏎⏎default:⏎&#9;@just --list&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=465 w=300 h=77/></c>
<c id="p2_jf_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=928 y=467 w=30 h=20/></c>
<c id="p2_jf_n" v="第 4 行行首是【真 tab】（recipe 本體必須縮排；default: @just --list 寫成單行是 just 語法錯誤，所以拆兩行）⏎已有 justfile → 問 6-20 只加第 1 行；uninstall 只刪完全相同的那行" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=972 y=465 w=628 h=77/></c>
<c id="p2_di_l" v="根 .dockerignore（使用者的；install append 三行；uninstall 問後只刪原文相同行）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=556 w=940 h=28/></c>
<c id="p2_di" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/cache/⏎.vendor_kit/gen/⏎.vendor_kit/.tmp.*&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=588 w=300 h=61/></c>
<c id="p2_di_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=928 y=590 w=30 h=20/></c>
<c id="p2_di_n" v="無 → 建；有 → 問 6-34 後 append（-y 免問）；插入的行記於 baseline/.vendor_kit.toml⏎工具以專案根當 build context 時靠它排除 cache" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=972 y=588 w=628 h=61/></c>
<c id="p2_tj_l" v=".vendor_kit/gen/tools.just（不進 git；每個 &lt;ns&gt;.just 一行 mod?；零 set 零 recipe）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=663 w=940 h=28/></c>
<c id="p2_tj" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# &lt;description&gt;⏎mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=695 w=353 h=46/></c>
<c id="p2_tj_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=981 y=697 w=30 h=20/></c>
<c id="p2_tj_n" v="# &lt;description&gt;：來自 init.toml 頂層 description；缺則 &lt;repo&gt; &lt;tag&gt;⏎mod?：cache 缺檔時其他 recipe 與 just vendor_kit sync 仍可跑" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=1025 y=695 w=575 h=46/></c>
<c id="p2_sh_l" v="薄殼自描述首行（entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=755 w=940 h=28/></c>
<c id="p2_sh" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;# vendor_kit-shell/1 engine=v1.0.0 sha256=&lt;hash&gt;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=787 w=396 h=61/></c>
<c id="p2_sh_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1024 y=789 w=30 h=20/></c>
<c id="p2_sh_n" v="&lt;P&gt; = 協定版本（1）、engine = 產生它的引擎；&lt;hash&gt; = 其餘內容 CRLF→LF 正規化後的 sha256⏎引擎重算 hash + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=1068 y=787 w=532 h=61/></c>
<c id="p2_st_l" v=".vendor_kit/gen/&lt;repo&gt;.stamp（每工具印記；materialize 寫）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=862 w=940 h=28/></c>
<c id="p2_st" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;sha256:&lt;hex64&gt;⏎&lt;sha256&gt; files/…⏎&lt;sha256&gt; init.toml⏎&lt;sha256&gt; just/&lt;ns&gt;.just&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=894 w=300 h=77/></c>
<c id="p2_st_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=928 y=896 w=30 h=20/></c>
<c id="p2_st_n" v="第 1 行：多架構 index digest（add --local 亦為正式 digest）；dev 時 path:&lt;dir&gt;；無 image:&lt;tag&gt; 形⏎之後每檔一行 &lt;sha256&gt; &lt;相對路徑&gt;；verify 逐檔比；檔內沒有註解" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=972 y=894 w=628 h=77/></c>
<c id="p2_gs_l" v=".vendor_kit/gen/.stamp（只由 install／upgrade vendor_kit 寫）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=985 w=940 h=28/></c>
<c id="p2_gs" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;ghcr.io/&lt;org&gt;/vendor_kit:v1.0.0@sha256:&lt;digest&gt;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=1017 w=389 h=46/></c>
<c id="p2_gs_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1017 y=1019 w=30 h=20/></c>
<c id="p2_gs_n" v="唯一一行：產生薄殼的引擎 ref（local 覆寫時為 &lt;tag&gt;）；≠ version.toml 正規行 → sync 退出 1 印 6-1" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=1061 y=1017 w=539 h=46/></c>
<c id="p2_tv_l" v=".vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml（remove／uninstall／undev／prune 進度日誌；&lt;id&gt; = UTC 時間戳 + 隨機）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=1077 w=940 h=28/></c>
<c id="p2_tv" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1⏎written_by = &quot;v1.0.0&quot;⏎verb = &quot;remove&quot;⏎id = &quot;&lt;id&gt;&quot;⏎targets = [&quot;&lt;repo&gt;&quot;]⏎started = &quot;&lt;UTC ISO 8601&gt;&quot;⏎done = [...]⏎pending = [...]⏎consents = [...]&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=660 y=1109 w=300 h=155/></c>
<c id="p2_tv_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=928 y=1111 w=30 h=20/></c>
<c id="p2_tv_n" v="consents = 已取得的同意；done／pending = 已完成／未完成步驟⏎第一個寫入前建、成功結束時整個檔刪除；未完成 → 可寫動詞先恢復、唯讀動詞印 6-33" s="fc=#ffffff;sc=#999999;fs=14;fs=12"><g x=972 y=1109 w=628 h=155/></c>
<c id="p2_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=660 y=1284 w=200 h=28/></c>
<c id="p2_tk0" v="唯一來源" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1318 w=150 h=30/></c>
<c id="p2_tv0" v="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1318 w=790 h=30/></c>
<c id="p2_tk1" v="vendor_kit = 正規行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1348 w=150 h=57/></c>
<c id="p2_tv1" v="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&lt;ref&gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1348 w=790 h=57/></c>
<c id="p2_tk2" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1405 w=150 h=42/></c>
<c id="p2_tv2" v="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1405 w=790 h=42/></c>
<c id="p2_tk3" v="image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1447 w=150 h=42/></c>
<c id="p2_tv3" v="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1447 w=790 h=42/></c>
<c id="p2_tk4" v="薄殼" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1489 w=150 h=42/></c>
<c id="p2_tv4" v=".vendor_kit/ 進 git、vendor_kit 擁有、人不改的四檔：entry.just、vendor.just、.gitignore、ci/check.sh；只轉發、不做事；每檔自描述首行；只由 install／upgrade vendor_kit 重產" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1489 w=790 h=42/></c>
<c id="p2_tk5" v="薄殼自描述首行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1531 w=150 h=42/></c>
<c id="p2_tv5" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 CRLF→LF 正規化 hash&gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1531 w=790 h=42/></c>
<c id="p2_tk6" v="gen/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1573 w=150 h=42/></c>
<c id="p2_tv6" v="引擎產生的檔，不進 git，三種：tools.just（sync／add／remove／upgrade 重生）、.stamp（只由 install／upgrade vendor_kit 寫）、&lt;repo&gt;.stamp（materialize 寫）" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1573 w=790 h=42/></c>
<c id="p2_tk7" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1615 w=150 h=42/></c>
<c id="p2_tv7" v="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &lt;tag&gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1615 w=790 h=42/></c>
<c id="p2_tk8" v="印記 gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1657 w=150 h=42/></c>
<c id="p2_tv8" v="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&lt;dir&gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1657 w=790 h=42/></c>
<c id="p2_tk9" v="mod／mod?／import／import?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1699 w=150 h=57/></c>
<c id="p2_tv9" v="just 的載入：mod &lt;ns&gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1699 w=790 h=57/></c>
<c id="p2_tk10" v="cache/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1756 w=150 h=42/></c>
<c id="p2_tv10" v="工具 image 的 /dist 展開副本，收在 .vendor_kit/ 裡；不進 git、不可改；dev 時是 symlink → &lt;dir&gt;/dist；印記不在這裡（在 gen/&lt;repo&gt;.stamp）" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1756 w=790 h=42/></c>
<c id="p2_tk11" v="初始檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1798 w=150 h=42/></c>
<c id="p2_tv11" v="工具 init.toml 列出、add 時建到專案的檔（例 Dockerfile）；歸使用者，進 git；已存在就不納管；upgrade 逐檔問；五態記在 metadata" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1798 w=790 h=42/></c>
<c id="p2_tk12" v="初始檔五態（state）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1840 w=150 h=42/></c>
<c id="p2_tv12" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1840 w=790 h=42/></c>
<c id="p2_tk13" v="baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1882 w=150 h=42/></c>
<c id="p2_tv13" v=".vendor_kit/baseline/&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，不由 version.toml 推導）；三方合併的共同祖先；同目錄 .vendor_kit.toml = metadata；install 只建 baseline/.gitkeep" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1882 w=790 h=42/></c>
<c id="p2_tk14" v="baseline/.gitkeep" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1924 w=150 h=42/></c>
<c id="p2_tv14" v="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&lt;repo&gt;/.vendor_kit.toml 兼作該工具目錄的佔位）" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1924 w=790 h=42/></c>
<c id="p2_tk15" v="進度日誌檔 .tmp.*" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=1966 w=150 h=42/></c>
<c id="p2_tv15" v="remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；&lt;id&gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=1966 w=790 h=42/></c>
<c id="p2_tk16" v="暫存 .tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=2008 w=150 h=42/></c>
<c id="p2_tv16" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=2008 w=790 h=42/></c>
<c id="p2_tk17" v="根 justfile 四行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=2050 w=150 h=42/></c>
<c id="p2_tv17" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=2050 w=790 h=42/></c>
<c id="p2_tk18" v="根 .dockerignore 三行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=2092 w=150 h=57/></c>
<c id="p2_tv18" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=2092 w=790 h=57/></c>
<c id="p2_tk19" v="專案根" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=660 y=2149 w=150 h=57/></c>
<c id="p2_tv19" v="含 .vendor_kit/ 的目錄（monorepo 子專案各自一套；不是 git toplevel）；vendor_kit 動詞只准在該層執行（recipe 檢查 invocation_directory() == justfile_directory()，否則 1 印 6-9「請到 &lt;dir&gt; 執行」；sync 豁免）；禁止巢狀（上層或下層已有 → 1 印 6-35）；須在某 git repo 內；引擎不讀 .git" s="fc=#ffffff;sc=#999999;fs=12"><g x=810 y=2149 w=790 h=57/></c>
<c id="p2_lg0" v="綠框：進 git" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=40 y=2236.0 w=120 h=40/></c>
<c id="p2_lg1" v="灰虛線：不進 git（可重建）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=180 y=2236.0 w=200 h=40/></c>
<c id="p2_lg2" v="黃底綠框：使用者的檔（進 git）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=400 y=2236.0 w=230 h=40/></c>
<c id="p2_lg3" v="等寬字：檔案內容範例" s="fc=#ffffff;sc=#999999;fs=12"><g x=650 y=2236.0 w=170 h=40/></c>
<c id="p2_lg4" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=840 y=2236.0 w=200 h=40/></c>
<c id="p2_lg4_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1008 y=2238.0 w=30 h=20/></c>
<c id="p2_lg5" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1060 y=2236.0 w=220 h=40/></c>
<c id="p2_lgt" v="樹線 = 目錄包含；範例框右邊 = 框外說明⏎綠標籤 = v2 改；schema 表 p2b、矩陣 p2c" s="text;fs=12;sc=none;fc=none"><g x=1300 y=2226.0 w=300 h=60/></c>
</diagram>
<diagram id="v1p2b" name="契約 v2：schema：version.toml／local／metadata／印記／薄殼首行"><c id="title" v="契約② 專案裡的檔（2／3）── schema：version.toml／version.local.toml／metadata／印記／薄殼首行（interface_spec §4）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p2b_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p2b_pend" v="【本頁無待拍板】⏎欄位名、型別、必填以 interface_spec §4 為準；範例見 p2；動詞 × 檔案矩陣見 p2c" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p2B" v="4. 檔案 schema（欄位／型別／必填／說明；一列一欄位）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=1362/></c>
<c id="p2b_gen" v="【TOML 通則（所有 vendor_kit 寫的檔）】⏎每檔 schema = N（integer）+ written_by = &quot;&lt;vX&gt;&quot;（string，純資訊，不作讀取門檻）；讀取門檻只看 schema；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯、重複宣告 → 1；schema 高於本引擎支援 → 3 印 6-19 零寫入；讀任一舊 schema → 直接寫當前 schema（不鏈式）；只在本來要寫該檔的明確動作寫回；引擎寫回固定格式並重讀驗證。第一版 schema = 1" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2B"><g x=20 y=50 w=750 h=92/></c>
<c id="p2b_gen_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=738 y=52 w=30 h=20/></c>
<c id="p2b_ver_l" v="4.1 .vendor_kit/version.toml" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=20 y=156 w=750 h=28/></c>
<c id="p2b_ver_m" v="進 git：是；唯一來源。寫入者 install／add／upgrade／remove（apply 最後寫）；使用者、Renovate 可手改；sync 只讀" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p2B"><g x=20 y=188 w=750 h=30/></c>
<c id="p2b_canon" v="【version.toml 正規行契約】⏎vendor_kit 行唯一正規形：整行 vendor_kit = &quot;&lt;ref&gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號基本字串、無尾端註解、LF 結尾）；引擎寫出一律此形。讀取（啟動器、引擎、Renovate preset 共用）regex：^vendor_kit[[:space:]]*=[[:space:]]*&quot;\([^&quot;]*\)&quot;[[:space:]]*$（POSIX BRE，不用 \s）；命中數必須恰為 1（grep -c），0 或重複 → 1。第一行只是 install 寫出慣例、不是契約；頂層鍵必在 [tools] 之前。禁止：BOM、重複鍵、[vendor_kit] 表旁路等 regex 讀不到／讀錯的等價寫法。公開格式：工具可讀它寫來源紀錄" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2B"><g x=20 y=232 w=750 h=108/></c>
<c id="p2b_canon_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=738 y=234 w=30 h=20/></c>
<c id="p2b_ver_h0" v="欄位" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=354 w=190 h=30/></c>
<c id="p2b_ver_h1" v="型別／必填" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=210 y=354 w=130 h=30/></c>
<c id="p2b_ver_h2" v="說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=340 y=354 w=430 h=30/></c>
<c id="p2b_ver_r0c0" v="vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=384 w=190 h=42/></c>
<c id="p2b_ver_r0c1" v="string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=384 w=130 h=42/></c>
<c id="p2b_ver_r0c2" v="引擎 ref ghcr.io/&lt;org&gt;/vendor_kit:vN@sha256:&lt;digest&gt;（多架構 index digest）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=384 w=430 h=42/></c>
<c id="p2b_ver_r1c0" v="schema" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=426 w=190 h=26/></c>
<c id="p2b_ver_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=178 y=428 w=30 h=20/></c>
<c id="p2b_ver_r1c1" v="integer／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=426 w=130 h=26/></c>
<c id="p2b_ver_r1c2" v="啟動器不讀、只引擎讀" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=426 w=430 h=26/></c>
<c id="p2b_ver_r2c0" v="written_by" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=452 w=190 h=26/></c>
<c id="p2b_ver_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=178 y=454 w=30 h=20/></c>
<c id="p2b_ver_r2c1" v="string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=452 w=130 h=26/></c>
<c id="p2b_ver_r2c2" v="寫入引擎版本，純資訊" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=452 w=430 h=26/></c>
<c id="p2b_ver_r3c0" v="[tools].&lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=478 w=190 h=57/></c>
<c id="p2b_ver_r3c1" v="string／每工具" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=478 w=130 h=57/></c>
<c id="p2b_ver_r3c2" v="ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist:&lt;tag&gt;@sha256:&lt;digest&gt;（index digest；add --local 亦寫正式 index digest，來自 .digest 旁檔）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=478 w=430 h=57/></c>
<c id="p2b_vl_l" v="4.2 .vendor_kit/version.local.toml" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=20 y=549 w=750 h=28/></c>
<c id="p2b_vl_m" v="不進 git（自有 .gitignore 擋）；與 version.toml 同形（同一套讀寫器）；寫入者 dev／undev／bootstrap --local；uninstall 刪；最後一個覆寫撤掉後 undev 刪除整個檔；不交 Renovate；frozen 下存在任何覆寫 → sync 回 1；啟動器先讀它再退回 version.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p2B"><g x=20 y=581 w=750 h=61/></c>
<c id="p2b_vl_m_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=738 y=583 w=30 h=20/></c>
<c id="p2b_vl_h0" v="欄位" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=656 w=190 h=30/></c>
<c id="p2b_vl_h1" v="型別／必填" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=210 y=656 w=130 h=30/></c>
<c id="p2b_vl_h2" v="說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=340 y=656 w=430 h=30/></c>
<c id="p2b_vl_r0c0" v="vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=686 w=190 h=26/></c>
<c id="p2b_vl_r0c1" v="string／否" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=686 w=130 h=26/></c>
<c id="p2b_vl_r0c2" v="本機引擎 image tag（只能 tag，docker load 後無 RepoDigests）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=686 w=430 h=26/></c>
<c id="p2b_vl_r1c0" v="vendor_kit_image_id" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=712 w=190 h=57/></c>
<c id="p2b_vl_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=178 y=714 w=30 h=20/></c>
<c id="p2b_vl_r1c1" v="string／有 vendor_kit 時必填" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=712 w=130 h=57/></c>
<c id="p2b_vl_r1c2" v="sha256:&lt;hex64&gt;，dev 時解析；啟動器每次 docker image inspect 比對，同 tag 重 build 才會被發現；undev vendor_kit 一併撤" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=712 w=430 h=57/></c>
<c id="p2b_vl_r2c0" v="schema、written_by" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=769 w=190 h=42/></c>
<c id="p2b_vl_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=178 y=771 w=30 h=20/></c>
<c id="p2b_vl_r2c1" v="integer、string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=769 w=130 h=42/></c>
<c id="p2b_vl_r2c2" v="同通則" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=769 w=430 h=42/></c>
<c id="p2b_vl_r3c0" v="[tools].&lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=811 w=190 h=42/></c>
<c id="p2b_vl_r3c1" v="string／否" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=210 y=811 w=130 h=42/></c>
<c id="p2b_vl_r3c2" v="path:&lt;dir&gt;（絕對路徑）；cache/&lt;repo&gt;/ 為 symlink → &lt;dir&gt;/dist" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=340 y=811 w=430 h=42/></c>
<c id="p2b_gen_l" v="4.4 gen/.stamp、gen/&lt;repo&gt;.stamp、gen/tools.just（不進 git）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=20 y=867 w=750 h=28/></c>
<c id="p2b_gn_h0" v="檔" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=899 w=180 h=30/></c>
<c id="p2b_gn_h1" v="寫入者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=200 y=899 w=180 h=30/></c>
<c id="p2b_gn_h2" v="內容" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=380 y=899 w=390 h=30/></c>
<c id="p2b_gn_r0c0" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=929 w=180 h=57/></c>
<c id="p2b_gn_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=168 y=931 w=30 h=20/></c>
<c id="p2b_gn_r0c1" v="只由 install／upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=200 y=929 w=180 h=57/></c>
<c id="p2b_gn_r0c2" v="第一行 = 產生薄殼的引擎 ref（local 覆寫時為 &lt;tag&gt;），供 sync grep 快速比對；不承擔薄殼 hash；fresh clone 缺此檔時相容判定改用薄殼自描述首行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=380 y=929 w=390 h=57/></c>
<c id="p2b_gn_r1c0" v="gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=986 w=180 h=88/></c>
<c id="p2b_gn_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=168 y=988 w=30 h=20/></c>
<c id="p2b_gn_r1c1" v="materialize" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=200 y=986 w=180 h=88/></c>
<c id="p2b_gn_r1c2" v="第一行 = 多架構 index digest sha256:&lt;hex64&gt;（與 version.toml 一致；add --local 亦為正式 index digest，本機驗證用 metadata local_image_id）或 dev 時 path:&lt;dir&gt;；無 image:&lt;tag&gt; 形；之後每檔一行 &lt;sha256&gt; &lt;相對路徑&gt;；verify 逐檔比" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=380 y=986 w=390 h=88/></c>
<c id="p2b_gn_r2c0" v="gen/tools.just" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=1074 w=180 h=73/></c>
<c id="p2b_gn_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=168 y=1076 w=30 h=20/></c>
<c id="p2b_gn_r2c1" v="sync／add／remove／upgrade 重生；最後寫、與 cache 同一 apply 內原子替換" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=200 y=1074 w=180 h=73/></c>
<c id="p2b_gn_r2c2" v="每個 &lt;ns&gt;.just 一行 mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27;（一工具可多行），每行上方一行 # &lt;description&gt;；零 set 零 recipe" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=380 y=1074 w=390 h=73/></c>
<c id="p2b_tmp_l" v="4.6 .vendor_kit/.tmp.*（皆由自有 .gitignore 的 .tmp.* 擋）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=20 y=1161 w=750 h=28/></c>
<c id="p2b_tmp_h0" v="檔" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=1193 w=170 h=30/></c>
<c id="p2b_tmp_h1" v="內容" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=190 y=1193 w=580 h=30/></c>
<c id="p2b_tmp_r0c0" v=".tmp.&lt;verb&gt;.&lt;id&gt;.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=1223 w=170 h=73/></c>
<c id="p2b_tmp_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=158 y=1225 w=30 h=20/></c>
<c id="p2b_tmp_r0c1" v="remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；&lt;id&gt; = 交易 id（UTC 時間戳 + 隨機，不用 &lt;repo&gt; 以免 uninstall 多工具撞名）；內容 = schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪；未完成 → 可寫動詞恢復、唯讀動詞印 6-33；prune 不刪未恢復者" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=190 y=1223 w=580 h=73/></c>
<c id="p2b_tmp_r1c0" v=".tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=20 y=1296 w=170 h=42/></c>
<c id="p2b_tmp_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=158 y=1298 w=30 h=20/></c>
<c id="p2b_tmp_r1c1" v="啟動器暫存（展開的工具 dist、vk-resolve）；mktemp -d &quot;&lt;專案根&gt;/.vendor_kit/.tmp.dist.XXXXXX&quot;；trap 刪；prune 清殘留" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=190 y=1296 w=580 h=42/></c>
<c id="p2b_mt_l" v="4.3 baseline/&lt;repo&gt;/.vendor_kit.toml（metadata）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=790 y=50 w=750 h=28/></c>
<c id="p2b_mt_m" v="進 git；寫入者 add／upgrade；兼作 baseline/&lt;repo&gt;/ 空目錄佔位；apply 重驗指紋時一起比；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列。註：install 對根 .dockerignore 的三行 append 不屬任何工具，記於 baseline/.vendor_kit.toml（同 schema，只含 [[file]] dest=.dockerignore state=appended lines=三行），uninstall 讀它刪原文相同行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p2B"><g x=790 y=82 w=750 h=77/></c>
<c id="p2b_mt_m_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=1508 y=84 w=30 h=20/></c>
<c id="p2b_mt_h0" v="欄位" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=173 w=190 h=30/></c>
<c id="p2b_mt_h1" v="型別／必填" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=980 y=173 w=130 h=30/></c>
<c id="p2b_mt_h2" v="說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=1110 y=173 w=430 h=30/></c>
<c id="p2b_mt_r0c0" v="schema、written_by" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=203 w=190 h=42/></c>
<c id="p2b_mt_r0c1" v="integer、string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=203 w=130 h=42/></c>
<c id="p2b_mt_r0c2" v="同通則" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=203 w=430 h=42/></c>
<c id="p2b_mt_r1c0" v="source" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=245 w=190 h=57/></c>
<c id="p2b_mt_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=247 w=30 h=20/></c>
<c id="p2b_mt_r1c1" v="string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=245 w=130 h=57/></c>
<c id="p2b_mt_r1c2" v="這份 baseline 來自哪個工具 image &lt;ref&gt;（tag@index digest）= 最後合併版本；≠ version.toml → sync 本機 warn／CI 為真 1 印 6-5；upgrade 先補待合併到該版然後停" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=245 w=430 h=57/></c>
<c id="p2b_mt_r2c0" v="local_image_id" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=302 w=190 h=42/></c>
<c id="p2b_mt_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=304 w=30 h=20/></c>
<c id="p2b_mt_r2c1" v="string／add --local 時" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=302 w=130 h=42/></c>
<c id="p2b_mt_r2c2" v="sha256:&lt;hex64&gt;：本機 image ID ↔ source 的 index digest 對照，供離線驗證" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=302 w=430 h=42/></c>
<c id="p2b_mt_r3c0" v="complete" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=344 w=190 h=42/></c>
<c id="p2b_mt_r3c1" v="bool／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=344 w=130 h=42/></c>
<c id="p2b_mt_r3c2" v="add 走完 materialize → 初始檔 → baseline 才 true；缺或 false → sync 1 印 6-13；true 且再 add → 0 無變更" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=344 w=430 h=42/></c>
<c id="p2b_mt_r4c0" v="conflicts" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=386 w=190 h=42/></c>
<c id="p2b_mt_r4c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=388 w=30 h=20/></c>
<c id="p2b_mt_r4c1" v="array of string／是（可空）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=386 w=130 h=42/></c>
<c id="p2b_mt_r4c2" v="upgrade 回 2 時留標記或解析失敗的 dest 清單；仍含標籤 → 2 停；解析失敗的 dest 其 baseline 不推；解完重跑才清空" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=386 w=430 h=42/></c>
<c id="p2b_mt_r5c0" v="[[file]].dest" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=428 w=190 h=26/></c>
<c id="p2b_mt_r5c1" v="string" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=428 w=130 h=26/></c>
<c id="p2b_mt_r5c2" v="相對專案根" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=428 w=430 h=26/></c>
<c id="p2b_mt_r6c0" v="[[file]].state" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=454 w=190 h=57/></c>
<c id="p2b_mt_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=456 w=30 h=20/></c>
<c id="p2b_mt_r6c1" v="string（單一列舉）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=454 w=130 h=57/></c>
<c id="p2b_mt_r6c2" v="managed（已納管）／appended（append 已插入）／declined（新增檔被拒、從未納管）／unmanaged（本來就有、沒納管）／deleted（使用者刪了已納管檔，upgrade 維持刪除）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=454 w=430 h=57/></c>
<c id="p2b_mt_r7c0" v="[[file]]⏎.declined_hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=511 w=190 h=73/></c>
<c id="p2b_mt_r7c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=513 w=30 h=20/></c>
<c id="p2b_mt_r7c1" v="string／選填" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=511 w=130 h=73/></c>
<c id="p2b_mt_r7c2" v="最近一次被拒絕的那版範本 N 的 sha256。已納管檔（managed／appended，含二進位）拒絕本次更新 → state 不變、只記此欄；新檔（從未建立）被拒 → state=declined + 此欄；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=511 w=430 h=73/></c>
<c id="p2b_mt_r8c0" v="[[file]].lines" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=584 w=190 h=42/></c>
<c id="p2b_mt_r8c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=586 w=30 h=20/></c>
<c id="p2b_mt_r8c1" v="array of string／只在 appended" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=584 w=130 h=42/></c>
<c id="p2b_mt_r8c2" v="實際插入的行原文（原本就存在的相同行不認領；CRLF/LF 等價比對）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=584 w=430 h=42/></c>
<c id="p2b_mt_r9c0" v="[progress]" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=626 w=190 h=57/></c>
<c id="p2b_mt_r9c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=948 y=628 w=30 h=20/></c>
<c id="p2b_mt_r9c1" v="table／交易中" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=980 y=626 w=130 h=57/></c>
<c id="p2b_mt_r9c2" v="state = &quot;in-progress&quot;、started（UTC ISO 8601）、verb、id、done／pending（array）；第一個寫入前建立、最後一步刪除；存在 → 可寫動詞先恢復、唯讀動詞印 6-33" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=1110 y=626 w=430 h=57/></c>
<c id="p2b_sm" v="【upgrade 逐檔狀態機（B = baseline、D = 磁碟、N = 新版讀自 /dist/&lt;repo&gt;；只對 state=managed、無待解衝突）】⏎D 缺 → state=deleted、維持刪除；D==N → 不動；B==N → 不動；D==B → 問後寫 N；三者皆異 → 問後 git merge-file --diff3（標籤 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 等），衝突 → 2；不論結果 baseline 推到 N（解析失敗除外）。N 缺（新版刪檔）→ 不刪只 warn。二進位／symlink 不合併：未改 → 問後換、改過保留 + warn。合併後對 TOML／just 類目標重新解析，失敗 → 2 留原檔、dest 入 conflicts、baseline 不推。拒絕：已納管檔 state 不變、只記 declined_hash；新增檔（從未建立）→ state=declined + declined_hash。五態轉移圖見狀態機頁" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2B"><g x=790 y=697 w=750 h=124/></c>
<c id="p2b_sm_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=1508 y=699 w=30 h=20/></c>
<c id="p2b_sh_l" v="4.5 薄殼（進 git，vendor_kit 擁有，人不改）與使用者的兩個根檔" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2B"><g x=790 y=835 w=750 h=28/></c>
<c id="p2b_sh_h0" v="檔" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=867 w=170 h=30/></c>
<c id="p2b_sh_h1" v="內容" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2B"><g x=960 y=867 w=580 h=30/></c>
<c id="p2b_sh_r0c0" v="自描述首行" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=897 w=170 h=73/></c>
<c id="p2b_sh_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=928 y=899 w=30 h=20/></c>
<c id="p2b_sh_r0c1" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行（第一行 shebang）：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;hash&gt;；hash = 首行（含其換行）之後全部位元組 CRLF→LF 正規化後的 sha256；引擎重算比對 + 對 image 內薄殼模板二次比對；不符 → 1 印 6-28 列差異不動；mode 變更只 warn" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=897 w=580 h=73/></c>
<c id="p2b_sh_r1c0" v="entry.just" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=970 w=170 h=26/></c>
<c id="p2b_sh_r1c1" v="mod vendor_kit &#x27;vendor.just&#x27; + import? &#x27;gen/tools.just&#x27;；零 set 零 recipe" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=970 w=580 h=26/></c>
<c id="p2b_sh_r2c0" v="vendor.just" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=996 w=170 h=42/></c>
<c id="p2b_sh_r2c1" v="動詞 recipe 一行轉發 + 啟動器本體（POSIX sh recipe）；set positional-arguments 只放這" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=996 w=580 h=42/></c>
<c id="p2b_sh_r3c0" v=".gitignore" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=1038 w=170 h=26/></c>
<c id="p2b_sh_r3c1" v="cache/、gen/、version.local.toml、.tmp.*" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=1038 w=580 h=26/></c>
<c id="p2b_sh_r4c0" v="ci/check.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=1064 w=170 h=26/></c>
<c id="p2b_sh_r4c1" v="契約⑤ p3c：shebang、自描述、export CI=1、⓪–⑤ 六步" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=1064 w=580 h=26/></c>
<c id="p2b_sh_r5c0" v="根 justfile（使用者的）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=1090 w=170 h=42/></c>
<c id="p2b_sh_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=928 y=1092 w=30 h=20/></c>
<c id="p2b_sh_r5c1" v="install 只加一行 import &#x27;.vendor_kit/entry.just&#x27;；無檔則建，內容逐字四行：import 一行／空行／default:／\t@just --list；uninstall 只刪完全相同行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=1090 w=580 h=42/></c>
<c id="p2b_sh_r6c0" v="根 .dockerignore（使用者的）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2B"><g x=790 y=1132 w=170 h=42/></c>
<c id="p2b_sh_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2B"><g x=928 y=1134 w=30 h=20/></c>
<c id="p2b_sh_r6c1" v="install append 三行 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34）；uninstall 問後只刪原文相同行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2B"><g x=960 y=1132 w=580 h=42/></c>
<c id="p2b_lg0" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=40 y=1488 w=190 h=40/></c>
<c id="p2b_lg1" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=250 y=1488 w=110 h=40/></c>
<c id="p2b_lg2" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=380 y=1488 w=200 h=40/></c>
<c id="p2b_lg3" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=600 y=1488 w=200 h=40/></c>
<c id="p2b_lg3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=768 y=1490 w=30 h=20/></c>
<c id="p2b_lg4" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=820 y=1488 w=220 h=40/></c>
<c id="p2b_lgt" v="一列一個欄位；「型別／必填」照 interface_spec §4⏎範例（等寬字）見 p2" s="text;fs=12;sc=none;fc=none"><g x=1060 y=1478 w=300 h=60/></c>
<c id="p2b_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1544 w=300 h=28/></c>
<c id="p2b_tk0" v="schema／written_by" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1578 w=150 h=55/></c>
<c id="p2b_tv0" v="每個 vendor_kit 寫的 TOML 都有 schema = N（integer，讀取門檻只看它）+ written_by = &quot;&lt;vX&gt;&quot;（純資訊）；同 schema 只加不改；讀時忽略未知欄位、寫時保留；只拒絕型別錯／重複宣告 → 1；schema 高於本引擎 → 3 印 6-19 零寫入" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1578 w=610 h=55/></c>
<c id="p2b_tk1" v="vendor_kit = 正規行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1633 w=150 h=55/></c>
<c id="p2b_tv1" v="version.toml 引擎 ref 的唯一正規形：整行 vendor_kit = &quot;&lt;ref&gt;&quot;（行首無空白、鍵後一個空白、=、一個空白、雙引號、無尾端註解、LF）；讀取 regex ^vendor_kit[[:space:]]*=（POSIX BRE）；命中數必須恰 1，0 或重複 → 1；禁 BOM／重複鍵／[vendor_kit] 表旁路" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1633 w=610 h=55/></c>
<c id="p2b_tk2" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1688 w=150 h=55/></c>
<c id="p2b_tv2" v="同目錄的 dev 覆寫（不進 git；與 version.toml 同形）：[tools].&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id；啟動器先讀它再退回 version.toml；frozen 下存在任何覆寫 → sync 回 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1688 w=610 h=55/></c>
<c id="p2b_tk3" v="image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1743 w=150 h=55/></c>
<c id="p2b_tv3" v="docker 本機給每個 image 內容的 sha256（docker image inspect --format &#x27;{{.Id}}&#x27;）；tag 是人取的名字（可重 build 換內容）、digest 是 registry 端的指紋；本機引擎覆寫記 tag + vendor_kit_image_id，啟動器每次 inspect 比對" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1743 w=610 h=55/></c>
<c id="p2b_tk4" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1798 w=150 h=55/></c>
<c id="p2b_tv4" v="baseline/&lt;repo&gt;/.vendor_kit.toml：schema + written_by、source（來源 ref@digest = 最後合併版本）、local_image_id、complete（完成標記）、conflicts、[[file]] dest／state／declined_hash／lines、[progress] 進度日誌" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1798 w=610 h=55/></c>
<c id="p2b_tk5" v="初始檔五態（state）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1853 w=150 h=55/></c>
<c id="p2b_tv5" v="metadata 對每個 dest 記單一 state：managed（已納管）／appended（append 已插入）／declined（新增檔被拒）／unmanaged（本來就有沒納管）／deleted（使用者刪了）；已納管檔拒絕換版只記 declined_hash；不動檔不紅燈" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1853 w=610 h=55/></c>
<c id="p2b_tk6" v="declined／declined_hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1908 w=150 h=55/></c>
<c id="p2b_tv6" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1908 w=610 h=55/></c>
<c id="p2b_tk7" v="conflicts（衝突中檔案）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1963 w=150 h=55/></c>
<c id="p2b_tv7" v="metadata 的 dest 清單：upgrade 回 2 時留標記或解析失敗的檔；仍含 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline → 2 停（檔案失蹤不算已解）；解析失敗的 dest 其 baseline 不推；解完重跑才清空（拿鎖後）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1963 w=610 h=55/></c>
<c id="p2b_tk8" v="進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2018 w=150 h=55/></c>
<c id="p2b_tv8" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2018 w=610 h=55/></c>
<c id="p2b_tk9" v="三方合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1578 w=150 h=40/></c>
<c id="p2b_tv9" v="拿 baseline（B）、你現在的檔（D）、新版範本（N）三份用 git merge-file --diff3 合；衝突留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記並回 2；baseline 仍推到新版（解析失敗除外）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1578 w=610 h=40/></c>
<c id="p2b_tk10" v="印記 gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1618 w=150 h=40/></c>
<c id="p2b_tv10" v="每工具一個：第一行 = 裝的是哪個 index digest（dev 時 path:&lt;dir&gt;；無 image: 形）、之後每檔 sha256；sync 用它判斷要不要重新 materialize；gen/.stamp 只記引擎 ref" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1618 w=610 h=40/></c>
<c id="p2b_tk11" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1658 w=150 h=55/></c>
<c id="p2b_tv11" v="只記「gen/ 與薄殼是哪個引擎產生的」（引擎 ref 一行；local 覆寫時為 &lt;tag&gt;）；只由 install／upgrade vendor_kit 寫；≠ version.toml 正規行 → sync 退出 1 印 6-1；fresh clone 缺此檔時相容判定改用薄殼首行" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1658 w=610 h=55/></c>
<c id="p2b_tk12" v="薄殼自描述首行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1713 w=150 h=55/></c>
<c id="p2b_tv12" v="entry.just／vendor.just／.gitignore 第一行、ci/check.sh 第二行：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 CRLF→LF 正規化 hash&gt;；引擎重算 + 對 image 內模板二次比對，不符 → 1 印 6-28 列差異不動" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1713 w=610 h=55/></c>
<c id="p2b_tk13" v="mod／mod?／import／import?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1768 w=150 h=55/></c>
<c id="p2b_tv13" v="just 的載入：mod &lt;ns&gt; &#x27;檔&#x27; 把整個檔掛成命名空間；mod? = 檔不在也不報錯（gen/tools.just 一律用它，cache 缺檔時 just vendor_kit sync 仍可進入）；import &#x27;檔&#x27; 把內容併進來（根 justfile 那一行）；import? = 檔不在也不報錯（entry.just 掛 gen/tools.just）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1768 w=610 h=55/></c>
<c id="p2b_tk14" v="進度日誌檔 .tmp.*" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1823 w=150 h=55/></c>
<c id="p2b_tv14" v="remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；&lt;id&gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1823 w=610 h=55/></c>
<c id="p2b_tk15" v="暫存 .tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1878 w=150 h=40/></c>
<c id="p2b_tv15" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1878 w=610 h=40/></c>
<c id="p2b_tk16" v="多架構 index／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1918 w=150 h=40/></c>
<c id="p2b_tv16" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1918 w=610 h=40/></c>
<c id="p2b_tk17" v=".digest 旁檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1958 w=150 h=55/></c>
<c id="p2b_tv17" v="離線包 &lt;name&gt;.tar 旁的 &lt;name&gt;.tar.digest：一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1958 w=610 h=55/></c>
</diagram>
<diagram id="v1p2c" name="契約 v2：動詞 × 檔案矩陣"><c id="title" v="契約② 專案裡的檔（3／3）── 動詞 × 檔案矩陣、會碰／不碰使用者東西、version.toml 怎麼被讀" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p2c_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p2c_pend" v="【本頁無待拍板】⏎寫 = 產生／覆蓋；刪 = 移除；— = 不碰；依 interface_spec §1.2 副作用欄與 §4 寫入者" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p2C" v="5. 動詞 × 檔案（一列一動詞、一欄一檔；細節見 p1b 與流程頁）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=1500/></c>
<c id="p2c_tc_l" v="「會碰使用者東西」只有三處（不變量：可以建、要改先問、永不刪、永不覆蓋；拒絕 → 不寫：新檔 state=declined、已納管檔只記 declined_hash）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2C"><g x=20 y=50 w=1300 h=28/></c>
<c id="p2c_tc_h0" v="東西" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=82 w=200 h=30/></c>
<c id="p2c_tc_h1" v="怎麼碰" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=220 y=82 w=1320 h=30/></c>
<c id="p2c_tc_r0c0" v="根 justfile 一行" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=112 w=200 h=42/></c>
<c id="p2c_tc_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=188 y=114 w=30 h=20/></c>
<c id="p2c_tc_r0c1" v="install：無 → 建四行（import + 空行 + default: + \t@just --list）；有 → 問 6-20（-y 直接加並印出）；已含 → 不再加；根檔是 symlink → 不寫、印遷移指示｜uninstall：問 6-20，只刪與我們寫的完全相同的行｜add：只讀它做撞名檢查（just --dump --dump-format json）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=220 y=112 w=1320 h=42/></c>
<c id="p2c_tc_r1c0" v="根 .dockerignore 三行" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=154 w=200 h=26/></c>
<c id="p2c_tc_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=188 y=156 w=30 h=20/></c>
<c id="p2c_tc_r1c1" v="install：無 → 建；有 → 問 6-34 後 append（-y 免問），插入的行記於 baseline/.vendor_kit.toml｜uninstall：問後只刪原文相同的行｜工具 build 以專案根當 context 時靠它排除 cache" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=220 y=154 w=1320 h=26/></c>
<c id="p2c_tc_r2c0" v="初始檔（init.toml 的 dest）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=180 w=200 h=42/></c>
<c id="p2c_tc_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=188 y=182 w=30 h=20/></c>
<c id="p2c_tc_r2c1" v="add：無 → 建；有 → 不納管、不覆蓋（unmanaged，印 6-11）；strategy=append 問 6-21 後加行｜upgrade：逐檔狀態機後問 6-22（換／三方合併／建新檔／二進位）；拒絕 → declined_hash（新檔 state=declined）；N 變了才再問｜remove／uninstall：永不刪，印清單；append 行問後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=220 y=180 w=1320 h=42/></c>
<c id="p2c_not" v="【不碰】：使用者的 .gitignore（除非工具以 strategy=append 宣告且你同意）、.git/info/exclude（dev 也不寫）、.git 本身（引擎不讀 .git、不碰 index、不做 git init）；我們要忽略的路徑全放 .vendor_kit/.gitignore；-y 不授權覆蓋既有未納管檔、不硬加 append 行" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2C"><g x=20 y=236 w=1520 h=46/></c>
<c id="p2c_not_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=238 w=30 h=20/></c>
<c id="p2c_mx_l" v="表 A：進 git 的宣告、使用者的兩個根檔、薄殼、gen/.stamp（動詞 × 檔案）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2C"><g x=20 y=296 w=1200 h=28/></c>
<c id="p2c_mx_h0" v="動詞" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=328 w=130 h=30/></c>
<c id="p2c_mx_h1" v="version.toml" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=150 y=328 w=210 h=30/></c>
<c id="p2c_mx_h2" v="version.local.toml" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=360 y=328 w=240 h=30/></c>
<c id="p2c_mx_h3" v="根 justfile" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=600 y=328 w=210 h=30/></c>
<c id="p2c_mx_h4" v="根 .dockerignore" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=810 y=328 w=200 h=30/></c>
<c id="p2c_mx_h5" v="薄殼（tracked 四檔）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=1010 y=328 w=300 h=30/></c>
<c id="p2c_mx_h6" v="gen/.stamp" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=1310 y=328 w=230 h=30/></c>
<c id="p2c_mx_r0c0" v="install" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=358 w=130 h=42/></c>
<c id="p2c_mx_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=360 w=30 h=20/></c>
<c id="p2c_mx_r0c1" v="寫（schema、written_by、正規行）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=358 w=210 h=42/></c>
<c id="p2c_mx_r0c2" v="—（bootstrap --local 成功後才寫 tag + image ID）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=358 w=240 h=42/></c>
<c id="p2c_mx_r0c3" v="無 → 建四行；有 → 問加一行；已含 → 不再加" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=358 w=210 h=42/></c>
<c id="p2c_mx_r0c4" v="無 → 建三行；有 → 問後 append" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=358 w=200 h=42/></c>
<c id="p2c_mx_r0c5" v="首行 hash 相符才重產；不符 → 1 印 6-28" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=358 w=300 h=42/></c>
<c id="p2c_mx_r0c6" v="寫（引擎 ref）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=358 w=230 h=42/></c>
<c id="p2c_mx_r1c0" v="uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=400 w=130 h=26/></c>
<c id="p2c_mx_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=402 w=30 h=20/></c>
<c id="p2c_mx_r1c1" v="hash 相符才刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=400 w=210 h=26/></c>
<c id="p2c_mx_r1c2" v="hash 相符才刪；否則保留並回報" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=400 w=240 h=26/></c>
<c id="p2c_mx_r1c3" v="問後只刪相同的行（之後才刪日誌）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=400 w=210 h=26/></c>
<c id="p2c_mx_r1c4" v="問後只刪原文相同三行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=400 w=200 h=26/></c>
<c id="p2c_mx_r1c5" v="只刪 hash 相符的自產檔；未知或被改的保留並回報" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=400 w=300 h=26/></c>
<c id="p2c_mx_r1c6" v="刪（自產）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=400 w=230 h=26/></c>
<c id="p2c_mx_r2c0" v="add" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=426 w=130 h=26/></c>
<c id="p2c_mx_r2c1" v="最後加 [tools] 一行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=426 w=210 h=26/></c>
<c id="p2c_mx_r2c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=426 w=240 h=26/></c>
<c id="p2c_mx_r2c3" v="—（只讀：撞名檢查）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=426 w=210 h=26/></c>
<c id="p2c_mx_r2c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=426 w=200 h=26/></c>
<c id="p2c_mx_r2c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=426 w=300 h=26/></c>
<c id="p2c_mx_r2c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=426 w=230 h=26/></c>
<c id="p2c_mx_r3c0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=452 w=130 h=26/></c>
<c id="p2c_mx_r3c1" v="刪一行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=452 w=210 h=26/></c>
<c id="p2c_mx_r3c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=452 w=240 h=26/></c>
<c id="p2c_mx_r3c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=452 w=210 h=26/></c>
<c id="p2c_mx_r3c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=452 w=200 h=26/></c>
<c id="p2c_mx_r3c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=452 w=300 h=26/></c>
<c id="p2c_mx_r3c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=452 w=230 h=26/></c>
<c id="p2c_mx_r4c0" v="upgrade（工具）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=478 w=130 h=26/></c>
<c id="p2c_mx_r4c1" v="最後改一行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=478 w=210 h=26/></c>
<c id="p2c_mx_r4c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=478 w=240 h=26/></c>
<c id="p2c_mx_r4c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=478 w=210 h=26/></c>
<c id="p2c_mx_r4c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=478 w=200 h=26/></c>
<c id="p2c_mx_r4c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=478 w=300 h=26/></c>
<c id="p2c_mx_r4c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=478 w=230 h=26/></c>
<c id="p2c_mx_r5c0" v="upgrade（不帶 repo）遇引擎新版" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=504 w=130 h=57/></c>
<c id="p2c_mx_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=506 w=30 h=20/></c>
<c id="p2c_mx_r5c1" v="只改正規行（舊引擎）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=504 w=210 h=57/></c>
<c id="p2c_mx_r5c2" v="—（覆寫時啟動器 docker image inspect 驗 ID）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=504 w=240 h=57/></c>
<c id="p2c_mx_r5c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=504 w=210 h=57/></c>
<c id="p2c_mx_r5c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=504 w=200 h=57/></c>
<c id="p2c_mx_r5c5" v="接手：新引擎跑 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=504 w=300 h=57/></c>
<c id="p2c_mx_r5c6" v="同下列" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=504 w=230 h=57/></c>
<c id="p2c_mx_r6c0" v="upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=561 w=130 h=42/></c>
<c id="p2c_mx_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=563 w=30 h=20/></c>
<c id="p2c_mx_r6c1" v="有新版才改正規行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=561 w=210 h=42/></c>
<c id="p2c_mx_r6c2" v="—（覆寫優先，inspect 驗 ID、不 pull）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=561 w=240 h=42/></c>
<c id="p2c_mx_r6c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=561 w=210 h=42/></c>
<c id="p2c_mx_r6c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=561 w=200 h=42/></c>
<c id="p2c_mx_r6c5" v="首行 hash 相符才重產四檔；降版讀不了 → 3 不動" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=561 w=300 h=42/></c>
<c id="p2c_mx_r6c6" v="寫（引擎 ref）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=561 w=230 h=42/></c>
<c id="p2c_mx_r7c0" v="dev" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=603 w=130 h=42/></c>
<c id="p2c_mx_r7c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=605 w=30 h=20/></c>
<c id="p2c_mx_r7c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=603 w=210 h=42/></c>
<c id="p2c_mx_r7c2" v="加行（工具 path:／引擎 tag + vendor_kit_image_id）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=603 w=240 h=42/></c>
<c id="p2c_mx_r7c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=603 w=210 h=42/></c>
<c id="p2c_mx_r7c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=603 w=200 h=42/></c>
<c id="p2c_mx_r7c5" v="—（-i 舊 image 禁止重產）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=603 w=300 h=42/></c>
<c id="p2c_mx_r7c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=603 w=230 h=42/></c>
<c id="p2c_mx_r8c0" v="undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=645 w=130 h=42/></c>
<c id="p2c_mx_r8c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=647 w=30 h=20/></c>
<c id="p2c_mx_r8c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=645 w=210 h=42/></c>
<c id="p2c_mx_r8c2" v="刪行（含 image ID；建日誌後；最後一個覆寫撤掉刪整檔）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=645 w=240 h=42/></c>
<c id="p2c_mx_r8c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=645 w=210 h=42/></c>
<c id="p2c_mx_r8c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=645 w=200 h=42/></c>
<c id="p2c_mx_r8c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=645 w=300 h=42/></c>
<c id="p2c_mx_r8c6" v="—（undev vendor_kit 後不符只印 6-1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=645 w=230 h=42/></c>
<c id="p2c_mx_r9c0" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=687 w=130 h=26/></c>
<c id="p2c_mx_r9c1" v="—（只讀）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=687 w=210 h=26/></c>
<c id="p2c_mx_r9c2" v="—（只讀；CI 為真下有覆寫 → 1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=687 w=240 h=26/></c>
<c id="p2c_mx_r9c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=687 w=210 h=26/></c>
<c id="p2c_mx_r9c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=687 w=200 h=26/></c>
<c id="p2c_mx_r9c5" v="不寫（不符 → 1 印 6-1）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=687 w=300 h=26/></c>
<c id="p2c_mx_r9c6" v="不寫（只比對）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=687 w=230 h=26/></c>
<c id="p2c_mx_r10c0" v="update" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=713 w=130 h=26/></c>
<c id="p2c_mx_r10c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=713 w=210 h=26/></c>
<c id="p2c_mx_r10c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=713 w=240 h=26/></c>
<c id="p2c_mx_r10c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=713 w=210 h=26/></c>
<c id="p2c_mx_r10c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=713 w=200 h=26/></c>
<c id="p2c_mx_r10c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=713 w=300 h=26/></c>
<c id="p2c_mx_r10c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=713 w=230 h=26/></c>
<c id="p2c_mx_r11c0" v="prune" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=739 w=130 h=26/></c>
<c id="p2c_mx_r11c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=741 w=30 h=20/></c>
<c id="p2c_mx_r11c1" v="—（只讀：哪些 image 仍被引用）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=739 w=210 h=26/></c>
<c id="p2c_mx_r11c2" v="—（只讀：keep 含覆寫 tag）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=739 w=240 h=26/></c>
<c id="p2c_mx_r11c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=739 w=210 h=26/></c>
<c id="p2c_mx_r11c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=739 w=200 h=26/></c>
<c id="p2c_mx_r11c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=739 w=300 h=26/></c>
<c id="p2c_mx_r11c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=739 w=230 h=26/></c>
<c id="p2c_mx_r12c0" v="任何動詞（結束碼 3）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=765 w=130 h=42/></c>
<c id="p2c_mx_r12c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=767 w=30 h=20/></c>
<c id="p2c_mx_r12c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=765 w=210 h=42/></c>
<c id="p2c_mx_r12c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=360 y=765 w=240 h=42/></c>
<c id="p2c_mx_r12c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=600 y=765 w=210 h=42/></c>
<c id="p2c_mx_r12c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=810 y=765 w=200 h=42/></c>
<c id="p2c_mx_r12c5" v="零寫入（無任何例外；救援路徑回 3 也零寫入）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=765 w=300 h=42/></c>
<c id="p2c_mx_r12c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1310 y=765 w=230 h=42/></c>
<c id="p2c_my_l" v="表 B：baseline／gen 兩檔／cache／初始檔／.tmp.*" s="text;fs=13;sc=none;fc=none;fst=1" parent="p2C"><g x=20 y=821 w=1200 h=28/></c>
<c id="p2c_my_h0" v="動詞" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=853 w=130 h=30/></c>
<c id="p2c_my_h1" v="baseline/ + metadata" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=150 y=853 w=250 h=30/></c>
<c id="p2c_my_h2" v="gen/tools.just" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=400 y=853 w=190 h=30/></c>
<c id="p2c_my_h3" v="gen/&lt;repo&gt;.stamp" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=590 y=853 w=190 h=30/></c>
<c id="p2c_my_h4" v="cache/&lt;repo&gt;/" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=780 y=853 w=230 h=30/></c>
<c id="p2c_my_h5" v="初始檔" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=1010 y=853 w=320 h=30/></c>
<c id="p2c_my_h6" v=".tmp.*" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p2C"><g x=1330 y=853 w=210 h=30/></c>
<c id="p2c_my_r0c0" v="install" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=883 w=130 h=57/></c>
<c id="p2c_my_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=885 w=30 h=20/></c>
<c id="p2c_my_r0c1" v="建 baseline/.gitkeep（不建 metadata）；.dockerignore 記錄寫 baseline/.vendor_kit.toml" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=883 w=250 h=57/></c>
<c id="p2c_my_r0c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=883 w=190 h=57/></c>
<c id="p2c_my_r0c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=883 w=190 h=57/></c>
<c id="p2c_my_r0c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=883 w=230 h=57/></c>
<c id="p2c_my_r0c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=883 w=320 h=57/></c>
<c id="p2c_my_r0c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=883 w=210 h=57/></c>
<c id="p2c_my_r1c0" v="uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=940 w=130 h=42/></c>
<c id="p2c_my_r1c1" v="先預檢（hash 相符清單）→ 逐工具 remove；未知或被改的保留" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=940 w=250 h=42/></c>
<c id="p2c_my_r1c2" v="刪（自產）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=940 w=190 h=42/></c>
<c id="p2c_my_r1c3" v="刪（自產）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=940 w=190 h=42/></c>
<c id="p2c_my_r1c4" v="刪（未知檔保留並回報）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=940 w=230 h=42/></c>
<c id="p2c_my_r1c5" v="永不刪；append 行問後刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=940 w=320 h=42/></c>
<c id="p2c_my_r1c6" v=".tmp.uninstall.&lt;id&gt;.toml（最後刪）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=940 w=210 h=42/></c>
<c id="p2c_my_r1c6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=942 w=30 h=20/></c>
<c id="p2c_my_r2c0" v="add" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=982 w=130 h=42/></c>
<c id="p2c_my_r2c1" v="建 &lt;repo&gt;/ + metadata（complete、五態、lines、source）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=982 w=250 h=42/></c>
<c id="p2c_my_r2c2" v="重生" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=982 w=190 h=42/></c>
<c id="p2c_my_r2c3" v="materialize 寫" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=982 w=190 h=42/></c>
<c id="p2c_my_r2c4" v="materialize" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=982 w=230 h=42/></c>
<c id="p2c_my_r2c5" v="無 → 建；有 → 不納管；append 問後加" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=982 w=320 h=42/></c>
<c id="p2c_my_r2c6" v="—（日誌在 metadata [progress]）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=982 w=210 h=42/></c>
<c id="p2c_my_r2c6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=984 w=30 h=20/></c>
<c id="p2c_my_r3c0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1024 w=130 h=26/></c>
<c id="p2c_my_r3c1" v="刪 &lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1024 w=250 h=26/></c>
<c id="p2c_my_r3c2" v="刪該工具所有 mod? 行" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1024 w=190 h=26/></c>
<c id="p2c_my_r3c3" v="刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1024 w=190 h=26/></c>
<c id="p2c_my_r3c4" v="刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1024 w=230 h=26/></c>
<c id="p2c_my_r3c5" v="永不刪；append 行問後刪（原文相同）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1024 w=320 h=26/></c>
<c id="p2c_my_r3c6" v=".tmp.remove.&lt;id&gt;.toml" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1024 w=210 h=26/></c>
<c id="p2c_my_r3c6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=1026 w=30 h=20/></c>
<c id="p2c_my_r4c0" v="upgrade（工具）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1050 w=130 h=42/></c>
<c id="p2c_my_r4c1" v="推到新版（衝突仍推；解析失敗不推）+ metadata" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1050 w=250 h=42/></c>
<c id="p2c_my_r4c2" v="重生" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1050 w=190 h=42/></c>
<c id="p2c_my_r4c3" v="materialize 寫" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1050 w=190 h=42/></c>
<c id="p2c_my_r4c4" v="materialize" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1050 w=230 h=42/></c>
<c id="p2c_my_r4c5" v="逐檔問：換／三方合併／append 行替換／建新檔／二進位" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1050 w=320 h=42/></c>
<c id="p2c_my_r4c6" v="—（日誌在 metadata [progress]）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1050 w=210 h=42/></c>
<c id="p2c_my_r4c6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=1052 w=30 h=20/></c>
<c id="p2c_my_r5c0" v="upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1092 w=130 h=42/></c>
<c id="p2c_my_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=1094 w=30 h=20/></c>
<c id="p2c_my_r5c1" v="schema 遷移（dry-run 明列）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1092 w=250 h=42/></c>
<c id="p2c_my_r5c2" v="重生" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1092 w=190 h=42/></c>
<c id="p2c_my_r5c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1092 w=190 h=42/></c>
<c id="p2c_my_r5c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1092 w=230 h=42/></c>
<c id="p2c_my_r5c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1092 w=320 h=42/></c>
<c id="p2c_my_r5c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1092 w=210 h=42/></c>
<c id="p2c_my_r6c0" v="dev" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1134 w=130 h=26/></c>
<c id="p2c_my_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=1136 w=30 h=20/></c>
<c id="p2c_my_r6c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1134 w=250 h=26/></c>
<c id="p2c_my_r6c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1134 w=190 h=26/></c>
<c id="p2c_my_r6c3" v="寫 path:&lt;dir&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1134 w=190 h=26/></c>
<c id="p2c_my_r6c4" v="改成 symlink → &lt;dir&gt;/dist" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1134 w=230 h=26/></c>
<c id="p2c_my_r6c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1134 w=320 h=26/></c>
<c id="p2c_my_r6c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1134 w=210 h=26/></c>
<c id="p2c_my_r7c0" v="undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1160 w=130 h=26/></c>
<c id="p2c_my_r7c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=1162 w=30 h=20/></c>
<c id="p2c_my_r7c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1160 w=250 h=26/></c>
<c id="p2c_my_r7c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1160 w=190 h=26/></c>
<c id="p2c_my_r7c3" v="重寫（materialize）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1160 w=190 h=26/></c>
<c id="p2c_my_r7c4" v="重新 materialize（經 docker）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1160 w=230 h=26/></c>
<c id="p2c_my_r7c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1160 w=320 h=26/></c>
<c id="p2c_my_r7c6" v=".tmp.undev.&lt;id&gt;.toml" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1160 w=210 h=26/></c>
<c id="p2c_my_r8c0" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1186 w=130 h=42/></c>
<c id="p2c_my_r8c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=1188 w=30 h=20/></c>
<c id="p2c_my_r8c1" v="—（只讀 complete、source 落後）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1186 w=250 h=42/></c>
<c id="p2c_my_r8c2" v="缺或需重生 → 重生" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1186 w=190 h=42/></c>
<c id="p2c_my_r8c3" v="materialize 時寫" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1186 w=190 h=42/></c>
<c id="p2c_my_r8c4" v="materialize／重裝（只拉鎖定版）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1186 w=230 h=42/></c>
<c id="p2c_my_r8c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1186 w=320 h=42/></c>
<c id="p2c_my_r8c6" v="—（有未完成 → 1 印 6-33 不恢復）" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1186 w=210 h=42/></c>
<c id="p2c_my_r9c0" v="update" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1228 w=130 h=26/></c>
<c id="p2c_my_r9c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1228 w=250 h=26/></c>
<c id="p2c_my_r9c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1228 w=190 h=26/></c>
<c id="p2c_my_r9c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1228 w=190 h=26/></c>
<c id="p2c_my_r9c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1228 w=230 h=26/></c>
<c id="p2c_my_r9c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1228 w=320 h=26/></c>
<c id="p2c_my_r9c6" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1228 w=210 h=26/></c>
<c id="p2c_my_r10c0" v="prune" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p2C"><g x=20 y=1254 w=130 h=57/></c>
<c id="p2c_my_r10c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=118 y=1256 w=30 h=20/></c>
<c id="p2c_my_r10c1" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=150 y=1254 w=250 h=57/></c>
<c id="p2c_my_r10c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=400 y=1254 w=190 h=57/></c>
<c id="p2c_my_r10c3" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=590 y=1254 w=190 h=57/></c>
<c id="p2c_my_r10c4" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=780 y=1254 w=230 h=57/></c>
<c id="p2c_my_r10c5" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1010 y=1254 w=320 h=57/></c>
<c id="p2c_my_r10c6" v=".tmp.prune.&lt;id&gt;.toml；刪失效 .tmp.dist.*、已完成殘留；活躍的不刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p2C"><g x=1330 y=1254 w=210 h=57/></c>
<c id="p2c_reno" v="【version.toml 怎麼被讀】⏎・啟動器（sh）：以正規行 regex 於 version.local.toml（覆寫優先）→ version.toml 取 vendor_kit；命中數 ≠ 1 → 1；不解析 TOML（resolve 的 vk-resolve 才是它的輸入）；快路徑用 grep 比 gen/*.stamp⏎・引擎 version 模組：TOML 讀寫（schema 轉換）+ version.local.toml 覆寫；flock；apply 最後才寫 version.toml⏎・Renovate preset：regex manager（**/.vendor_kit/version.toml；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR⏎・deploy：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（工具契約一句；vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2C"><g x=20 y=1325 w=750 h=155/></c>
<c id="p2c_reno_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=738 y=1327 w=30 h=20/></c>
<c id="p2c_rule" v="【規則摘要】⏎・version.toml 是唯一來源：sync 拿它對印記，不一致就 materialize（只拉鎖定版）；apply 拿鎖後先重驗 resolve 給的輸入指紋，不同 → 1 印 6-12⏎・自動化（sync）只碰 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp：不碰使用者的檔、不寫薄殼、不寫 gen/.stamp；薄殼 ≠ 引擎 ref → 1 印 6-1（install／upgrade vendor_kit 不被擋）⏎・baseline 是上次合併的歷史狀態，不由 version.toml 推導（待合併時 version 已 B、baseline 仍 A）⏎・進 git 的只有：根 justfile 那行、根 .dockerignore 三行、.vendor_kit/（不含 cache/、gen/、version.local.toml、.tmp.*）、初始檔；人只改：justfile、初始檔、version.toml（手動升版）⏎・舊薄殼（--protocol P 太舊）跑新 major 引擎的一般動詞 → 3 零寫入（6-36）；救援路徑永遠可用" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p2C"><g x=790 y=1325 w=750 h=155/></c>
<c id="p2c_rule_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p2C"><g x=1508 y=1327 w=30 h=20/></c>
<c id="p2c_lg0" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=40 y=1626 w=190 h=40/></c>
<c id="p2c_lg1" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=250 y=1626 w=110 h=40/></c>
<c id="p2c_lg2" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=380 y=1626 w=200 h=40/></c>
<c id="p2c_lg3" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=600 y=1626 w=200 h=40/></c>
<c id="p2c_lg3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=768 y=1628 w=30 h=20/></c>
<c id="p2c_lg4" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=820 y=1626 w=220 h=40/></c>
<c id="p2c_lgt" v="表格：一列一動詞、一欄一檔⏎目錄樹與範例 p2、schema p2b" s="text;fs=12;sc=none;fc=none"><g x=1060 y=1616 w=300 h=60/></c>
<c id="p2c_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1682 w=300 h=28/></c>
<c id="p2c_tk0" v="唯一來源" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1716 w=150 h=40/></c>
<c id="p2c_tv0" v="version.toml：專案「該裝哪版」只看它；印記、gen/、薄殼由它推導；baseline 是上次合併的歷史狀態，不由它推導" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1716 w=610 h=40/></c>
<c id="p2c_tk1" v="tracked 檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1756 w=150 h=40/></c>
<c id="p2c_tv1" v="進 git 的檔（git 追蹤中）：version.toml、薄殼四檔、baseline/、初始檔、根 justfile、根 .dockerignore；相對的是 cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1756 w=610 h=40/></c>
<c id="p2c_tk2" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1796 w=150 h=55/></c>
<c id="p2c_tv2" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1796 w=610 h=55/></c>
<c id="p2c_tk3" v="輸入指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1851 w=150 h=55/></c>
<c id="p2c_tv3" v="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1851 w=610 h=55/></c>
<c id="p2c_tk4" v="進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1906 w=150 h=55/></c>
<c id="p2c_tv4" v="add／upgrade 記 metadata [progress]（state=in-progress、started、verb、id、done／pending）；remove／uninstall／undev／prune 放 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml；第一個寫入前建、最後一步刪；可寫動詞先恢復再繼續，唯讀動詞（sync／update／help）只印 6-33 不恢復" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1906 w=610 h=55/></c>
<c id="p2c_tk5" v="進度日誌檔 .tmp.*" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1961 w=150 h=55/></c>
<c id="p2c_tv5" v="remove／uninstall／undev／prune 的進度日誌（metadata 會被刪或不存在）；&lt;id&gt; = 交易 id（UTC 時間戳 + 隨機）；內容 schema、written_by、verb、id、targets、started、done／pending、consents；成功結束時刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1961 w=610 h=55/></c>
<c id="p2c_tk6" v="救援路徑" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2016 w=150 h=55/></c>
<c id="p2c_tv6" v="單段 docker run、不依賴 resolve/apply 與 gen/ 的動詞：install、upgrade vendor_kit[@&lt;tag&gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help；任何 ≥ floor 的舊薄殼永遠可經此叫任何引擎重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2016 w=610 h=55/></c>
<c id="p2c_tk7" v="Renovate preset" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1716 w=150 h=55/></c>
<c id="p2c_tv7" v="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1716 w=610 h=55/></c>
<c id="p2c_tk8" v="deploy" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1771 w=150 h=40/></c>
<c id="p2c_tv8" v="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1771 w=610 h=40/></c>
<c id="p2c_tk9" v="根 justfile 四行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1811 w=150 h=55/></c>
<c id="p2c_tv9" v="install 新建根 justfile 時逐字：import &#x27;.vendor_kit/entry.just&#x27;／（空行）／default:／\t@just --list（default: @just --list 單行是 just 語法錯誤）；已有 justfile 只問後加 import 那一行；uninstall 只刪完全相同行" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1811 w=610 h=55/></c>
<c id="p2c_tk10" v="根 .dockerignore 三行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1866 w=150 h=71/></c>
<c id="p2c_tv10" v="install 加進使用者根 .dockerignore 的 .vendor_kit/cache/、.vendor_kit/gen/、.vendor_kit/.tmp.*（無則建；有則問 6-34 後 append、-y 免問）；插入的行記於 baseline/.vendor_kit.toml；uninstall 問後只刪原文相同行；工具以專案根當 build context 時靠它排除 cache" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1866 w=610 h=71/></c>
<c id="p2c_tk11" v="baseline/.gitkeep" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1937 w=150 h=40/></c>
<c id="p2c_tv11" v="install 建的空佔位檔：git 不追蹤空目錄，所以 baseline/ 靠它進 git；metadata 由 add 才建（baseline/&lt;repo&gt;/.vendor_kit.toml 兼作該工具目錄的佔位）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1937 w=610 h=40/></c>
<c id="p2c_tk12" v="declined／declined_hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1977 w=150 h=55/></c>
<c id="p2c_tv12" v="拒絕的記錄：新增檔被拒 → state=declined；已納管檔拒絕換版／合併 → state 不變只記 declined_hash（那版範本 N 的 sha256）；新版 N 的 hash ≠ declined_hash → 再問一次，相同 → 不問但印 6-6／6-8；EOF／Ctrl-C 不記 declined" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1977 w=610 h=55/></c>
</diagram>
<diagram id="v1p3" name="契約 v2：工具 repo 契約③"><c id="title" v="契約③ 工具 repo 要交的（供應側；interface_spec §4.7、§4.8、§3.6；改了要升 major 並公告）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p3_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p3_pend" v="【本頁無待拍板】⏎dist/files/ 的 symlink 已定禁止；dist 文字檔一律 LF、check.sh --dist 擋 CRLF 已定於 issue #29；Dockerfile.dist 必含 LABEL（16 條必修）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=81/></c>
<c id="p3L4" v="契約③ 工具 repo 要交的（dist 佈局、init.toml、_sync、Dockerfile.dist、image 與 label、離線包）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=109 w=1560 h=1120/></c>
<c id="p3_dist" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;&lt;repo&gt;/ # 工具 repo⏎├─ dist/⏎│ ├─ files/… # 全部出貨（原樣展開）⏎│ ├─ init.toml # 初始檔清單（下表）⏎│ └─ just/&lt;ns&gt;.just # 一檔一命名空間（含 _sync）⏎└─ Dockerfile.dist # 逐字三行（下框）&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=20 y=50 w=440 h=108/></c>
<c id="p3_dock_l" v="Dockerfile.dist（逐字三行；純資料 image）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L4"><g x=20 y=170 w=440 h=28/></c>
<c id="p3_dock" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;FROM scratch⏎LABEL io.github.&lt;org&gt;.vendor_kit=1⏎COPY dist/ /dist/&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=20 y=202 w=440 h=61/></c>
<c id="d4_1" v="【dist/files/】⏎全部出貨；materialize 原樣展開到 .vendor_kit/cache/&lt;repo&gt;/files/；symlink／hardlink／特殊檔第一版禁止（check.sh --dist 擋、引擎展開時也驗）；文字檔一律 LF [#29]" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=480 y=50 w=253 h=155/></c>
<c id="d4_1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=701 y=52 w=30 h=20/></c>
<c id="d4_2" v="【dist/init.toml】⏎schema、description（單行）、[[file]] src／dest／strategy=&quot;copy&quot;|&quot;append&quot;（預設 copy），dest 相對專案根；用 copy 指向根 .gitignore／.dockerignore／.editorconfig → --dist 報錯（要用 append）；欄位表見下" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=749 y=50 w=253 h=155/></c>
<c id="d4_2_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=970 y=52 w=30 h=20/></c>
<c id="d4_3" v="【dist/just/&lt;ns&gt;.just】⏎每檔一個頂層命名空間，數量工具自決，&lt;repo&gt;.just 必須存在；每檔含私有 _sync（F1，見下）；撞名 → add 拒絕；recipe 用 cd {{quote(justfile_directory())}} 回專案根（禁止相對 working-directory）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=1018 y=50 w=253 h=155/></c>
<c id="d4_3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1239 y=52 w=30 h=20/></c>
<c id="d4_4" v="【Dockerfile.dist】⏎逐字三行：FROM scratch／LABEL io.github.&lt;org&gt;.vendor_kit=1／COPY dist/ /dist/；純資料，不承諾可執行、vendor_kit 不檢查 binary（Q21：只搬移）；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加，pull 無法追加）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=1287 y=50 w=253 h=155/></c>
<c id="d4_4_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1508 y=52 w=30 h=20/></c>
<c id="d4_5" v="【工具 image】⏎ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist:&lt;tag&gt;⏎多架構 amd64 + arm64（同一次 buildx、COPY-only；CI 驗兩平台位元組一致）；version.toml 與印記記 index digest（#26）；公開／私有自決（公開不可逆）；已釋出 image／index 子 digest 永不刪；LABEL …vendor_kit=1" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12" parent="p3L4"><g x=480 y=221 w=253 h=186/></c>
<c id="d4_5_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=701 y=223 w=30 h=20/></c>
<c id="d4_6" v="【引擎 image】⏎ghcr.io/&lt;org&gt;/vendor_kit:vN⏎公開；多架構（只驗兩平台 LABEL 一致）；LABEL …vendor_kit=1、.protocol=&lt;floor_P&gt;-&lt;current_P&gt;、.schema=&lt;N&gt;（啟動器不起容器即可判 floor）；每平台 docker save tar + .digest 旁檔；Release 資產永不刪" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12" parent="p3L4"><g x=749 y=221 w=253 h=186/></c>
<c id="d4_6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=970 y=223 w=30 h=20/></c>
<c id="d4_7" v="【工具 repo 的 CI】⏎跑 vendor_kit 出貨的 check.sh --dist：dist 佈局、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink、LF、just 1.33.0 解析每個 &lt;ns&gt;.just、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台一致" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=1018 y=221 w=253 h=186/></c>
<c id="d4_7_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1239 y=223 w=30 h=20/></c>
<c id="d4_8" v="【deploy（一句話契約）】⏎工具 recipe 產生的交付物在執行期不得依賴 .vendor_kit/、version.toml、GHCR（需要的檔打包時複製進去）；vendor_kit 不檢查；保證方式 = 工具 repo 自己在乾淨機器解包驗收；version.toml 公開格式可供來源紀錄" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L4"><g x=1287 y=221 w=253 h=186/></c>
<c id="d4_8_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1508 y=223 w=30 h=20/></c>
<c id="p3_dest" v="【dest 規則（引擎在任何寫入前驗，不只供應端 lint）】：src 相對 dist/、正規化、不得越出 dist/；dest 相對專案根、正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；兩工具同 dest：copy/copy、copy/append → add 拒絕；append/append → 允許，各工具的行分開記錄，重疊或歸屬不明 → 拒絕；add 與 upgrade 都在任何寫入前檢查（含新版新增 &lt;ns&gt;／dest 的全域撞名）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L4"><g x=20 y=423 w=1520 h=46/></c>
<c id="p3_dest_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1508 y=425 w=30 h=20/></c>
<c id="p3_init_l" v="dist/init.toml（逐字範例；欄位說明在下表）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L4"><g x=20 y=483 w=700 h=28/></c>
<c id="p3_sync_l" v="dist/just/&lt;ns&gt;.just 的 _sync（逐字，行首真 tab）與 label 表" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L4"><g x=790 y=483 w=700 h=28/></c>
<c id="p3_init" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;schema = 1⏎description = &quot;&lt;repo&gt; 的專案範本與 just recipe&quot;⏎⏎[[file]]⏎src = &quot;files/Dockerfile&quot;⏎dest = &quot;Dockerfile&quot;⏎⏎[[file]]⏎src = &quot;files/gitignore.snippet&quot;⏎dest = &quot;.gitignore&quot;⏎strategy = &quot;append&quot;&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=20 y=515 w=750 h=186/></c>
<c id="p3_sync" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;[private]⏎_sync:⏎&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; just vendor_kit sync⏎⏎build: _sync⏎&#9;cd {{quote(justfile_directory())}} &amp;amp;&amp;amp; …&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=790 y=515 w=750 h=108/></c>
<c id="p3_initf_h0" v="欄位" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=711 w=170 h=30/></c>
<c id="p3_initf_h1" v="型別／必填" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=190 y=711 w=110 h=30/></c>
<c id="p3_initf_h2" v="說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=300 y=711 w=470 h=30/></c>
<c id="p3_initf_r0c0" v="schema" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=741 w=170 h=26/></c>
<c id="p3_initf_r0c1" v="integer／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=190 y=741 w=110 h=26/></c>
<c id="p3_initf_r0c2" v="建置期契約（同 image 內讀寫），不進執行期矩陣" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=300 y=741 w=470 h=26/></c>
<c id="p3_initf_r1c0" v="description" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=767 w=170 h=42/></c>
<c id="p3_initf_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=158 y=769 w=30 h=20/></c>
<c id="p3_initf_r1c1" v="string／否" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=190 y=767 w=110 h=42/></c>
<c id="p3_initf_r1c2" v="頂層、單行（含換行 → --dist 失敗）；寫成 gen/tools.just mod? 上方 # &lt;description&gt;；缺則 &lt;repo&gt; &lt;tag&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=300 y=767 w=470 h=42/></c>
<c id="p3_initf_r2c0" v="[[file]].src" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=809 w=170 h=26/></c>
<c id="p3_initf_r2c1" v="string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=190 y=809 w=110 h=26/></c>
<c id="p3_initf_r2c2" v="相對 dist/；正規化、不得越出 dist/" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=300 y=809 w=470 h=26/></c>
<c id="p3_initf_r3c0" v="[[file]].dest" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=835 w=170 h=42/></c>
<c id="p3_initf_r3c1" v="string／是" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=190 y=835 w=110 h=42/></c>
<c id="p3_initf_r3c2" v="相對專案根；正規化、不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；跨工具撞 dest 規則見左" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=300 y=835 w=470 h=42/></c>
<c id="p3_initf_r4c0" v="[[file]].strategy" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=20 y=877 w=170 h=42/></c>
<c id="p3_initf_r4c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=158 y=879 w=30 h=20/></c>
<c id="p3_initf_r4c1" v="string／否" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=190 y=877 w=110 h=42/></c>
<c id="p3_initf_r4c2" v="&quot;copy&quot;（預設）或 &quot;append&quot;，只有這兩值；根 .gitignore／.dockerignore／.editorconfig 類必須用 append" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=300 y=877 w=470 h=42/></c>
<c id="p3_lbl_h0" v="資源" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=790 y=633 w=200 h=30/></c>
<c id="p3_lbl_h1" v="label（鍵前綴 io.github.&lt;org&gt;.vendor_kit）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=990 y=633 w=540 h=30/></c>
<c id="p3_lbl_r0c0" v="啟動器建的容器／network／volume" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=790 y=663 w=200 h=42/></c>
<c id="p3_lbl_r0c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=958 y=665 w=30 h=20/></c>
<c id="p3_lbl_r0c1" v="…=1、….project=&lt;專案根絕對路徑&gt;（專案路徑 label 不加在 image 上）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=990 y=663 w=540 h=42/></c>
<c id="p3_lbl_r1c0" v="引擎 image（build 時）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=790 y=705 w=200 h=26/></c>
<c id="p3_lbl_r1c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=958 y=707 w=30 h=20/></c>
<c id="p3_lbl_r1c1" v="…=1、….protocol=&lt;floor_P&gt;-&lt;current_P&gt;、….schema=&lt;N&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=990 y=705 w=540 h=26/></c>
<c id="p3_lbl_r2c0" v="工具 image（build 時）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=790 y=731 w=200 h=26/></c>
<c id="p3_lbl_r2c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=958 y=733 w=30 h=20/></c>
<c id="p3_lbl_r2c1" v="…=1（Dockerfile.dist 必含）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=990 y=731 w=540 h=26/></c>
<c id="p3_lbl_r3c0" v="prune" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L4"><g x=790 y=757 w=200 h=42/></c>
<c id="p3_lbl_r3c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=958 y=759 w=30 h=20/></c>
<c id="p3_lbl_r3c1" v="依 label 掃四類資源；image 只刪帶 label 且本專案未引用者；vendor_kit 不建 network／volume（驗收差集為空，故意留的也要能刪）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L4"><g x=990 y=757 w=540 h=42/></c>
<c id="p3_syncr" v="【sync 自動前置（F1 定案）】：每個 dist/just/&lt;ns&gt;.just 必含上列私有 _sync（本體逐字、行首真 tab；justfile_directory() 在模組內 = 專案根；用 quote() 不直接插字串）；工具每個公開 recipe 相依它（例 build: _sync；例外集合：無）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump --dump-format json 檢查：_sync 存在、私有、本體逐字相符、每個公開 recipe 的 dependencies 含 _sync。限制（契約明寫）：just 在執行前已載入所有模組，同一次呼叫內看不到 sync 重建後的新 recipe；cache 缺檔時 mod? 讓 just vendor_kit sync 仍可進入；1.33.0 fixture 通過才算結案" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L4"><g x=20 y=933 w=1520 h=61/></c>
<c id="p3_syncr_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1508 y=935 w=30 h=20/></c>
<c id="p3_con" v="【工具契約（初始檔與 recipe）】：初始檔只能引用穩定入口 just &lt;ns&gt; …、.vendor_kit/ci/check.sh、.vendor_kit/entry.just、.vendor_kit/version.toml；不得寫死 cache 內部路徑（Q14）；rename／格式變更不得以 copy/append 假裝完成；工具的 build 若以專案根當 context，依賴 install 加進根 .dockerignore 的排除，不得再以其他方式繞過 .vendor_kit/；dist 可執行性是工具 repo 責任（check.sh --dist + 自己的測試）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L4"><g x=20 y=1008 w=750 h=92/></c>
<c id="p3_con_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=738 y=1010 w=30 h=20/></c>
<c id="p3_off" v="【離線包（Release 資產；Q26）】：每個平台 tar（docker save）旁附同名 .digest 旁檔：&lt;name&gt;.tar + &lt;name&gt;.tar.digest，內容一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；bootstrap.sh --local &lt;tar&gt;／add --local &lt;tar&gt;：docker load 後讀旁檔寫 version.toml（正式 ref@digest），metadata 記 local_image_id；旁檔缺 → 1。離線可用：啟動器先 docker image inspect，本機有就不 pull；斷網 + 已有 image → sync／build 必須成功；斷網 + 無 image → 1 印 6-31 不 hang；離線 upgrade 不支援" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L4"><g x=790 y=1008 w=750 h=92/></c>
<c id="p3_off_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L4"><g x=1508 y=1010 w=30 h=20/></c>
<c id="p3_lg0" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12"><g x=40 y=1259 w=170 h=40/></c>
<c id="p3_lg1" v="等寬字：檔案內容範例" s="fc=#ffffff;sc=#999999;fs=12"><g x=230 y=1259 w=170 h=40/></c>
<c id="p3_lg2" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=420 y=1259 w=190 h=40/></c>
<c id="p3_lg3" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=630 y=1259 w=110 h=40/></c>
<c id="p3_lg4" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=760 y=1259 w=200 h=40/></c>
<c id="p3_lg5" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=980 y=1259 w=200 h=40/></c>
<c id="p3_lg5_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1148 y=1261 w=30 h=20/></c>
<c id="p3_lgt" v="紫 = image（工具／引擎）⏎淺灰底容器 = 契約③ 全部" s="text;fs=12;sc=none;fc=none"><g x=1200 y=1249 w=300 h=60/></c>
<c id="p3_lg6" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1325 w=220 h=40/></c>
<c id="p3_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1381 w=300 h=28/></c>
<c id="p3_tk0" v="dist/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1415 w=150 h=40/></c>
<c id="p3_tv0" v="工具 repo 出貨的目錄：files/（展開到 cache/&lt;repo&gt;/ 的全部）、init.toml（初始檔清單）、just/&lt;ns&gt;.just（工具自己的 recipe，每檔含 _sync）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1415 w=610 h=40/></c>
<c id="p3_tk1" v="Dockerfile.dist" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1455 w=150 h=55/></c>
<c id="p3_tv1" v="逐字三行：FROM scratch／LABEL io.github.&lt;org&gt;.vendor_kit=1／COPY dist/ /dist/；產出「純資料 image」，沒有程式、不會被執行；缺 LABEL → check.sh --dist 失敗（label 只能 build 時加）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1455 w=610 h=55/></c>
<c id="p3_tk2" v="label" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1510 w=150 h=55/></c>
<c id="p3_tv2" v="docker 資源上的鍵值標籤，鍵前綴 io.github.&lt;org&gt;.vendor_kit：容器／network／volume = 1 + .project=&lt;專案根絕對路徑&gt;；引擎 image = 1 + .protocol=&lt;floor_P&gt;-&lt;current_P&gt; + .schema=&lt;N&gt;；工具 image = 1；prune 依 label 掃" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1510 w=610 h=55/></c>
<c id="p3_tk3" v="dest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1565 w=150 h=55/></c>
<c id="p3_tv3" v="init.toml 每個 [[file]] 要建到專案的目標路徑（相對專案根）；正規化後不得越出 repo、不得指向 .vendor_kit/、父目錄不得經 symlink；copy/copy、copy/append 同 dest 跨工具 → add 拒絕；引擎與 lint 都驗" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1565 w=610 h=55/></c>
<c id="p3_tk4" v="strategy = &quot;append&quot;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1620 w=150 h=55/></c>
<c id="p3_tv4" v="init.toml 每個 [[file]] 的 strategy 欄位（copy | append，預設 copy）；append（.gitignore 類）：檔不存在 → 建；存在 → 問後把幾行加進去，實際插入的行記在 metadata lines；upgrade／remove 只對可辨識的上次插入行提修改（CRLF／LF 等價、其餘精確）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1620 w=610 h=55/></c>
<c id="p3_tk5" v="CRLF／LF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1675 w=150 h=40/></c>
<c id="p3_tv5" v="兩種換行符號（Windows 用 CRLF、Linux 用 LF）；比對 append 行時視為等價，其餘字元要精確相同；dist 文字檔一律 LF [#29]" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1675 w=610 h=40/></c>
<c id="p3_tk6" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1715 w=150 h=40/></c>
<c id="p3_tv6" v="指向另一個路徑的捷徑檔；dev 時 cache/&lt;repo&gt;/ 就是指向 &lt;dir&gt;/dist 的 symlink（唯讀性只在容器 mount 上成立）；工具 dist/files/ 裡第一版禁止" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1715 w=610 h=40/></c>
<c id="p3_tk7" v="_sync recipe（F1）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1755 w=150 h=55/></c>
<c id="p3_tv7" v="每個 dist/just/&lt;ns&gt;.just 必含的私有 recipe（逐字：[private] / _sync: / \tcd {{quote(justfile_directory())}} &amp;&amp; just vendor_kit sync）；工具每個公開 recipe 相依它（build: _sync）；vendor_kit 自身動詞不前置；check.sh --dist 以 just --dump 檢查" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1755 w=610 h=55/></c>
<c id="p3_tk8" v="just 的兩個目錄函式" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1415 w=150 h=55/></c>
<c id="p3_tv8" v="justfile_directory()（該 justfile 所在目錄；模組內 = 專案根，工具 recipe 用 cd {{quote(justfile_directory())}} 回專案根）與 invocation_directory()（你打指令時所在目錄）；vendor_kit recipe 用兩者相等檢查「只准在專案根執行」" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1415 w=610 h=55/></c>
<c id="p3_tk9" v="buildx" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1470 w=150 h=28/></c>
<c id="p3_tv9" v="docker 的多架構建置工具：同一次 build 同時產 amd64 + arm64 兩份，合成一個多架構 index" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1470 w=610 h=28/></c>
<c id="p3_tk10" v="多架構 index／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1498 w=150 h=40/></c>
<c id="p3_tv10" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1498 w=610 h=40/></c>
<c id="p3_tk11" v="check.sh --dist" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1538 w=150 h=55/></c>
<c id="p3_tv11" v="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1538 w=610 h=55/></c>
<c id="p3_tk12" v=".digest 旁檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1593 w=150 h=55/></c>
<c id="p3_tv12" v="離線包 &lt;name&gt;.tar 旁的 &lt;name&gt;.tar.digest：一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；--local 用它寫 version.toml（正式 ref@digest），metadata 記 local_image_id 對照；旁檔缺 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1593 w=610 h=55/></c>
<c id="p3_tk13" v="離線可用（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1648 w=150 h=40/></c>
<c id="p3_tv13" v="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1648 w=610 h=40/></c>
<c id="p3_tk14" v="deploy" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1688 w=150 h=40/></c>
<c id="p3_tv14" v="把專案交付物部署到執行環境；工具契約一句：交付物執行期不得依賴 .vendor_kit/、version.toml、GHCR（vendor_kit 不檢查）；version.toml 公開格式可供來源紀錄" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1688 w=610 h=40/></c>
<c id="p3_tk15" v="命名空間" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1728 w=150 h=40/></c>
<c id="p3_tv15" v="just &lt;ns&gt; &lt;recipe&gt; 前面那個 &lt;ns&gt;；每個工具的 just/&lt;ns&gt;.just 一檔一個命名空間；與其他工具、根 justfile 既有 recipe／module、保留名 vendor_kit 撞名 → add 拒絕（撞名整個 just 會掛）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1728 w=610 h=40/></c>
<c id="p3_tk16" v="SemVer／正式版" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1768 w=150 h=40/></c>
<c id="p3_tv16" v="版本號 major.minor.patch；update 取 tags/list 中 SemVer 最大的正式版（預發行如 -rc 排除）；major = 提高 floor 或需手動步驟" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1768 w=610 h=40/></c>
</diagram>
<diagram id="v1p3b" name="契約 v2：啟動器 ↔ 引擎契約④"><c id="title" v="契約④ 啟動器 ↔ 引擎（interface_spec §3、§5；resolve → 主機 docker → apply；主機只需 docker + sh + just）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p3b_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p3b_pend" v="【本頁無待拍板】⏎vk-resolve/1 文法（Q24）；主機命令白名單（16 條必修）；規則框逐條對應 interface_spec §3、§5，皆已定" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=65/></c>
<c id="p3L2" v="契約④ 啟動器 ↔ 引擎（每格一件事；① 啟動器 grep → ② resolve → ③ 主機 docker → ④ apply；規則框 = §3、§5 逐條）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=96 w=1560 h=1725.5/></c>
<c id="s1" v="① 以正規行 regex grep 引擎 ref⏎（version.local.toml 覆寫優先；命中 ≠ 1 → 1）⏎下一格 install／upgrade vendor_kit 跳過" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L2"><g x=30 y=60.5 w=190 h=108/></c>
<c id="d1" v="gen/.stamp⏎= 引擎 ref？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=14;fs=12" parent="p3L2"><g x=244 y=56.5 w=180 h=116/></c>
<c id="d1_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s1" target="d1"></c>
<c id="g2" v="② docker run 引擎 resolve &lt;動詞&gt;（只讀、不寫檔、無 TTY；診斷走 stderr）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12;fst=1" parent="p3L2"><g x=448 y=50.0 w=650 h=103/></c>
<c id="s2a" v="讀 version.toml／local⏎（CI 為真 → frozen）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g2"><g x=8 y=34.0 w=160 h=61/></c>
<c id="s2b" v="查 registry 最新 tag／digest⏎（frozen／@&lt;tag&gt; 不查）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g2"><g x=184 y=34.0 w=180 h=61/></c>
<c id="s2c" v="stdout vk-resolve/1⏎（pull／extract／mount／engine／fingerprint／apply／end）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g2"><g x=380 y=34.0 w=250 h=61/></c>
<c id="s2a_e" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d1" target="s2a"></c>
<c id="s2b_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s2a" target="s2b"></c>
<c id="s2c_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s2b" target="s2c"></c>
<c id="p3_err" v="否 → 1 印 6-1⏎（請 upgrade vendor_kit；不重寫薄殼）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L2"><g x=204.0 y=212.5 w=260 h=84/></c>
<c id="p3_err_e" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d1" target="p3_err"></c>
<c id="d2" v="apply|yes？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=14;fs=12" parent="p3L2"><g x=488.0 y=250.0 w=180 h=85/></c>
<c id="g3" v="③ 主機 docker（每筆 pull／extract；不帶 --platform；先收完 vk-resolve 驗文法才動）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12;fst=1" parent="p3L2"><g x=692.0 y=212.5 w=622 h=134/></c>
<c id="s3a" v="docker image inspect⏎（有 → 不 pull）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g3"><g x=8 y=41.5 w=110 h=77/></c>
<c id="s3b" v="docker pull⏎（逾時 → 1 印 6-31）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g3"><g x=134 y=49.5 w=100 h=61/></c>
<c id="s3c" v="docker create⏎（帶 label）&lt;ref&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g3"><g x=250 y=41.5 w=100 h=77/></c>
<c id="s3d" v="docker cp c:/dist/.⏎→ .tmp.dist.&lt;id&gt;/⏎&lt;repo&gt;/" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g3"><g x=366 y=34.0 w=130 h=92/></c>
<c id="s3e" v="docker rm⏎（trap 也清）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="g3"><g x=512 y=49.5 w=90 h=61/></c>
<c id="s4" v="④ docker run 引擎⏎apply &lt;動詞&gt;（掛 /dist:ro）⏎→ 結束碼 0／1／2／3 回 just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L2"><g x=1338.0 y=246.5 w=180 h=92/></c>
<c id="s3b_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s3a" target="s3b"></c>
<c id="s3c_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s3b" target="s3c"></c>
<c id="s3d_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s3c" target="s3d"></c>
<c id="s3e_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s3d" target="s3e"></c>
<c id="s4_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s3e" target="s4"></c>
<c id="d2_e" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d2" target="s3a"></c>
<c id="d2_in" v="③" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2c" target="d2"><g pts=993.0,288.5;618.0,288.5/></c>
<c id="p3_ok" v="否（apply|no）→ 0 快路徑⏎不起第二個容器" s="ellipse;fc=#d5e8d4;sc=#000000;fs=14;fs=12" parent="p3L2"><g x=448.0 y=370.5 w=260 h=62/></c>
<c id="p3_ok_e" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d2" target="p3_ok"></c>
<c id="p3_sh" v="【主機命令白名單（16 條必修；lint 擋清單外）】：sh（含內建 printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files。啟動器 = POSIX sh（vendor.just 內的 recipe 殼）：不裝 python、不解析 TOML、不 eval；路徑含空白、$、非 ASCII 一律引號" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=456.5 w=750 h=92/></c>
<c id="p3_sh_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=748 y=458.5 w=30 h=20/></c>
<c id="p3_uf" v="【使用者旗標（rootless 不加 -u／Podman keep-id）】：docker info --format &#x27;{{.SecurityOptions}}&#x27; 含 name=rootless → rootless，不加 -u；docker --version 含 podman → 加 --userns=keep-id、不加 -u；其餘（rootful docker）加 -u &quot;$(id -u):$(id -g)&quot;" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=790 y=456.5 w=750 h=92/></c>
<c id="p3_uf_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=458.5 w=30 h=20/></c>
<c id="p3_run" v="【docker run 參數】：docker run --rm [&lt;使用者旗標&gt;] -v &quot;&lt;專案根&gt;:/repo&quot; -w /repo [-v &quot;&lt;專案根&gt;/.vendor_kit/.tmp.dist.&lt;id&gt;:/dist:ro&quot;] [-v &quot;&lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro&quot;]… [-v &quot;&lt;TOKEN_FILE&gt;:/run/vk-token:ro&quot; -e VENDOR_KIT_REGISTRY_TOKEN_FILE=/run/vk-token] [-e CI] [-e VENDOR_KIT_NO_LOCK] [-e VENDOR_KIT_REGISTRY_TOKEN -e VENDOR_KIT_REGISTRY_USER] [-it] --label io.github.&lt;org&gt;.vendor_kit=1 --label io.github.&lt;org&gt;.vendor_kit.project=&lt;專案根絕對路徑&gt; &lt;引擎 ref&gt; --protocol P &lt;子命令&gt; [args]。--protocol P 一律在子命令之前；-w /repo 必給；-it 只在 apply 且互動（有 tty、無 -y、非 frozen），resolve 永不 -t；trap … EXIT INT TERM 清容器與 .tmp.dist.&lt;id&gt;/" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=562.5 w=750 h=124/></c>
<c id="p3_run_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=748 y=564.5 w=30 h=20/></c>
<c id="p3_envw" v="【環境變數與 -e 白名單（§5）】：轉發 CI（照原值；真值規則：非空且不為 0／false → frozen）、VENDOR_KIT_NO_LOCK（=1 跳過 flock）；VENDOR_KIT_REGISTRY_TOKEN／_USER 只在 update／upgrade 的 resolve 階段以 -e 傳（不寫 log／檔、不傳給工具、dry-run 不印）；VENDOR_KIT_REGISTRY_TOKEN_FILE 改為 -v &lt;主機檔&gt;:/run/vk-token:ro 並以 -e …_TOKEN_FILE=/run/vk-token 傳容器內路徑（與 _TOKEN 同設 → 1「只能擇一」）；啟動器自讀不轉發：VENDOR_KIT_PULL_TIMEOUT（預設 300，--timeout 優先）；其餘一律不轉發（HTTP_PROXY 等 → v2）；README 列出全部 VENDOR_KIT_* 與 CI，lint 擋未列者；引擎容器內 LC_ALL=C.UTF-8、TZ=UTC、HOME=&lt;容器內暫存&gt;" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=790 y=562.5 w=750 h=124/></c>
<c id="p3_envw_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=564.5 w=30 h=20/></c>
<c id="p3_img" v="【引擎 image 取得】：一律先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（離線可用）；無 → docker pull &lt;ref&gt;（逾時）。local 覆寫時：docker image inspect &lt;tag&gt; 的 .Id 必須 == version.local.toml vendor_kit_image_id，否則 1；不 pull（不用 docker run 的 pull 旗標：docker 19.03 沒有）。【引擎子命令】：單段 install／update／dev／help／upgrade vendor_kit[@&lt;tag&gt;] = --protocol P &lt;verb&gt; [args]；resolve &lt;verb&gt;（只讀、不詢問、不寫檔、無 TTY）；apply &lt;verb&gt; [--dry-run]；內部 materialize／verify／merge 不對外" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=700.5 w=750 h=139/></c>
<c id="p3_img_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=748 y=702.5 w=30 h=20/></c>
<c id="p3_two" v="【兩段編排的兩個獨立屬性】：需展開 image（docker create/cp）= add／upgrade／sync／undev；兩段（resolve &lt;verb&gt; → 主機 docker → apply &lt;verb&gt;，重驗指紋）= add／remove／upgrade／sync／undev／uninstall／prune；單段 = install／upgrade vendor_kit／update／dev／help。--dry-run = apply --dry-run（也要先拉 image 展開）。【鎖】：鎖在引擎 version 模組（apply 一開始 flock 專案目錄，60 秒逾時失敗印 6-26；VENDOR_KIT_NO_LOCK=1 跳過；啟動器不鎖）。【pull 失敗】：印原文 + 三分類（網路／認證／不存在；daemon 不可用、磁碟滿另列「主機錯誤」）+ 僅 add／bootstrap 提示 6-24 的「離線可用 --local」；【逾時】：VENDOR_KIT_PULL_TIMEOUT／--timeout，預設 300 秒，只收正整數（0 或非數字 → 1）；背景 pull + 每秒輪詢 + kill；逾時 → 1 印 6-31" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=790 y=700.5 w=750 h=139/></c>
<c id="p3_two_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=702.5 w=30 h=20/></c>
<c id="p3_lock" v="【apply 通則（所有動詞）】：讀 /dist/vk-resolve（啟動器把 resolve 原始 stdout 存成 .tmp.dist.&lt;id&gt;/vk-resolve 一起掛入）→ 拿 flock → 重算指紋與計畫中的 fingerprint 比對（不同 → 1 印 6-12）→ 原 argv 與計畫不一致 → 1 → dry-run 分支（唯讀：本機 0；CI 為真需改 tracked → 1 印清單）→ 建進度日誌（第一個寫入前）→ 其後所有寫入（清除衝突狀態、append、baseline、metadata、cache、tools.just；version.toml 最後）→ 最後一步刪日誌（uninstall 在根 justfile 那行之後）；不重新選最新版；詢問後、替換前對目標檔再查一次前像；所有合併在暫存完成 → 逐檔原子替換；失敗明列已完成／未完成" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=853.5 w=1510 h=61/></c>
<c id="p3_lock_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=855.5 w=30 h=20/></c>
<c id="p3_vk_l" v="vk-resolve/1 stdout 文法（Q24；P=1）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L2"><g x=30 y=928.5 w=700 h=28/></c>
<c id="p3_vkt_l" v="kind 一覽（啟動器動作）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L2"><g x=790 y=928.5 w=700 h=28/></c>
<c id="p3_vk" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;vk-resolve/&lt;P&gt;⏎&lt;kind&gt;|&lt;f1&gt;[|&lt;f2&gt;…]⏎end|&lt;N&gt;⏎⏎vk-resolve/1⏎extract|&lt;repo&gt;|ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist:v2.3.0@sha256:bbbb…⏎fingerprint|1c0e…77⏎apply|yes⏎end|3⏎⏎vk-resolve/1⏎mount|&lt;repo&gt;|/home/me/my\0040tools⏎fingerprint|9a2f…c1⏎apply|yes⏎end|3&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=30 y=960.5 w=750 h=248/></c>
<c id="p3_vk_n" v="上段 = 文法骨架：第一行 vk-resolve/&lt;P&gt;（P = 呼叫方 --protocol 的值）；每行一筆 &lt;kind&gt;|&lt;f1&gt;[|&lt;f2&gt;…]（欄位以單一 | 分隔；UTF-8；LF；無空行、無註解；禁 CR／NUL／BOM）；最後一行 end|&lt;N&gt;（N = 記錄行數，之後立即 EOF）⏎中段範例 = sync，&lt;repo&gt; 的 cache 過期（extract）；下段範例 = sync，&lt;repo&gt; 在 dev 覆寫中（mount；路徑含空白 → \0040）。範例工具名一律 &lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=14;fs=12" parent="p3L2"><g x=30 y=1216.5 w=750 h=77/></c>
<c id="p3_vkt_h0" v="kind" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=960.5 w=100 h=30/></c>
<c id="p3_vkt_h1" v="欄位" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=890 y=960.5 w=180 h=30/></c>
<c id="p3_vkt_h2" v="筆數" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=1070 y=960.5 w=50 h=30/></c>
<c id="p3_vkt_h3" v="啟動器動作" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=1120 y=960.5 w=420 h=30/></c>
<c id="p3_vkt_r0c0" v="pull" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=990.5 w=100 h=42/></c>
<c id="p3_vkt_r0c1" v="&lt;name&gt;|&lt;ref&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=990.5 w=180 h=42/></c>
<c id="p3_vkt_r0c2" v="0..n" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=990.5 w=50 h=42/></c>
<c id="p3_vkt_r0c3" v="docker image inspect 有則略，否則 docker pull &lt;ref&gt;（逾時／失敗 → 6-24／6-31）；name = vendor_kit 或 &lt;repo&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=990.5 w=420 h=42/></c>
<c id="p3_vkt_r1c0" v="extract" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1032.5 w=100 h=57/></c>
<c id="p3_vkt_r1c1" v="&lt;repo&gt;|&lt;ref&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1032.5 w=180 h=57/></c>
<c id="p3_vkt_r1c2" v="0..n" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1032.5 w=50 h=57/></c>
<c id="p3_vkt_r1c3" v="同 pull 後 docker create … &lt;ref&gt; /x → docker cp c:/dist/. &quot;.tmp.dist.&lt;id&gt;/&lt;repo&gt;/&quot; → docker rm；同一 repo 不得同時有 extract 與 mount" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1032.5 w=420 h=57/></c>
<c id="p3_vkt_r2c0" v="mount" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1089.5 w=100 h=42/></c>
<c id="p3_vkt_r2c1" v="&lt;repo&gt;|&lt;dir 八進位跳脫&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1089.5 w=180 h=42/></c>
<c id="p3_vkt_r2c2" v="0..n" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1089.5 w=50 h=42/></c>
<c id="p3_vkt_r2c3" v="dev 覆寫：解碼後驗 &lt;dir&gt;/dist/init.toml 存在（缺 → 1）→ -v &quot;&lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro&quot;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1089.5 w=420 h=42/></c>
<c id="p3_vkt_r3c0" v="engine" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1131.5 w=100 h=57/></c>
<c id="p3_vkt_r3c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=858 y=1133.5 w=30 h=20/></c>
<c id="p3_vkt_r3c1" v="&lt;ref&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1131.5 w=180 h=57/></c>
<c id="p3_vkt_r3c2" v="0..1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1131.5 w=50 h=57/></c>
<c id="p3_vkt_r3c3" v="只在 upgrade（不帶 repo）：apply 會把正規行改成此 ref；啟動器先 pull（或 local 覆寫時 inspect 驗 ID）；有 engine 時本次不得夾帶工具寫入" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1131.5 w=420 h=57/></c>
<c id="p3_vkt_r4c0" v="fingerprint" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1188.5 w=100 h=26/></c>
<c id="p3_vkt_r4c1" v="&lt;sha256 hex64&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1188.5 w=180 h=26/></c>
<c id="p3_vkt_r4c2" v="恰 1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1188.5 w=50 h=26/></c>
<c id="p3_vkt_r4c3" v="不解析，隨檔交給 apply" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1188.5 w=420 h=26/></c>
<c id="p3_vkt_r5c0" v="apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1214.5 w=100 h=57/></c>
<c id="p3_vkt_r5c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=858 y=1216.5 w=30 h=20/></c>
<c id="p3_vkt_r5c1" v="yes | no" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1214.5 w=180 h=57/></c>
<c id="p3_vkt_r5c2" v="恰 1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1214.5 w=50 h=57/></c>
<c id="p3_vkt_r5c3" v="no → 驗完文法後直接 exit 0（sync 快路徑）；no 時不得有 pull／extract／mount／engine；yes → docker 階段後跑 apply &lt;verb&gt; [--dry-run] [args]" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1214.5 w=420 h=57/></c>
<c id="p3_vkt_r6c0" v="keep" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1271.5 w=100 h=42/></c>
<c id="p3_vkt_r6c0_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=858 y=1273.5 w=30 h=20/></c>
<c id="p3_vkt_r6c1" v="&lt;name&gt;|&lt;ref&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1271.5 w=180 h=42/></c>
<c id="p3_vkt_r6c2" v="0..n" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1271.5 w=50 h=42/></c>
<c id="p3_vkt_r6c3" v="只在 prune：本專案引用、不可刪的 image（含 local 覆寫的 &lt;tag&gt;）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1271.5 w=420 h=42/></c>
<c id="p3_vkt_r7c0" v="end" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="p3L2"><g x=790 y=1313.5 w=100 h=26/></c>
<c id="p3_vkt_r7c1" v="&lt;N&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=890 y=1313.5 w=180 h=26/></c>
<c id="p3_vkt_r7c2" v="恰 1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1070 y=1313.5 w=50 h=26/></c>
<c id="p3_vkt_r7c3" v="必為最後一行" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L2"><g x=1120 y=1313.5 w=420 h=26/></c>
<c id="p3_vkr" v="【欄位與驗證】：安全字串 [A-Za-z0-9_.-]+；ref [A-Za-z0-9_.:/@-]+（引擎以 image-reference parser 驗證後才輸出）；自由文字（路徑）凡不在 [A-Za-z0-9_./:@+=,-] 的 byte 一律寫成 \0ooo（例：空白 \0040、| \0174、\ \0134），啟動器一行解碼 dir=$(printf &#x27;%b&#x27; &quot;$f2&quot;)、不 eval、不 source；IFS=&#x27;|&#x27; read -r 直接切欄。啟動器先收完整份存到 .tmp.dist.&lt;id&gt;/vk-resolve、驗文法才動 docker：首行 ≠ vk-resolve/&lt;P&gt;、缺 end、N 不符、end 後仍有資料、未知 kind、欄位數不對、fingerprint／apply 不是恰一筆、no 卻附動作記錄、安全字串含非法字元 → 1 印 6-30；引擎宣稱的 P 真不支援 → 3。resolve 結束碼非 0 → 不讀 stdout、原碼傳出。stderr 一律診斷；apply 的 stdout 不作為協定通道。指紋算法見名詞表" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=1353.5 w=1510 h=77/></c>
<c id="p3_vkr_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=1355.5 w=30 h=20/></c>
<c id="p3_self" v="【自身升級的接手（§3.4）】：「引擎已變」不從 stdout 讀：啟動器在 apply 前後各 grep 一次 version.toml 的 vendor_kit 正規行。apply 結束後 ref 變了（且 == 計畫的 engine）→ 以新 ref（local 覆寫有 vendor_kit= 則用該 image、inspect 驗 ID）跑 docker run … &lt;新 ref&gt; --protocol P upgrade vendor_kit，結束碼原樣傳出（預期 1 印 6-2）；第二次第一行又變、或新引擎拉取／重產失敗 → 1 印 6-2b，不再重跑。【救援路徑（§3.5）】：install、upgrade vendor_kit[@&lt;tag&gt;]、sync 的「薄殼不符 → 1 印 6-1」判定、help = 單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼永遠可經此叫任何引擎重產薄殼" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=1444.5 w=750 h=139/></c>
<c id="p3_self_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=748 y=1446.5 w=30 h=20/></c>
<c id="p3_fast" v="【sync 快路徑（Q22）與 sync --verify】：sync（無參數）啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml vendor_kit ref；[tools] 每個 &lt;repo&gt; 的 digest == gen/&lt;repo&gt;.stamp 第一行（或 local 覆寫的 path:&lt;dir&gt;）；gen/tools.just 存在；無 .tmp.&lt;verb&gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 frozen → 起引擎 resolve sync。每檔 sha256 verify 只在：CI 為真（frozen）、快路徑有差那次（版本變動）、sync --verify（長形）；sync &lt;repo&gt; 一律起引擎驗該範圍。前提：.vendor_kit/.gitignore 明列 cache/、gen/、version.local.toml、.tmp.*；install 把 .vendor_kit/cache/、gen/、.tmp.* 加進根 .dockerignore。【--local 值的判別】：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → 本機 image tag；兩者皆成立 → 1 提示用 ./ 或完整 ref 消歧" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=790 y=1444.5 w=750 h=139/></c>
<c id="p3_fast_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=1446.5 w=30 h=20/></c>
<c id="p3_compat" v="【相容承諾（Q16／Q19／Q23）】：薄殼每次呼叫附 --protocol P（第一版就有），引擎依 P 回應。永久：任何 ≥ floor 的舊薄殼可呼叫新引擎的救援路徑並得正確提示；舊資料永遠可讀可遷（讀任一舊 schema → 直接寫當前 schema，不鏈式）。非永久：舊薄殼跑新 major 一般動詞只保證乾淨回 3 印 6-36 零寫入。floor = 固定 release 常數（v1.0.0、P=1、schema=1），只能經 ADR 提高；引擎 image LABEL …protocol=&lt;floor_P&gt;-&lt;current_P&gt; 讓啟動器不起容器即可判 floor。降版 upgrade vendor_kit@&lt;舊版&gt;：目標引擎（以 P／schema 比）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10；dev vendor_kit -i &lt;舊 image&gt; 禁止重產 tracked 薄殼" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=30 y=1597.5 w=750 h=108/></c>
<c id="p3_compat_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=748 y=1599.5 w=30 h=20/></c>
<c id="p3_env" v="【執行環境（19 條）與主機需求】：docker ≥ 19.03（或 Podman ≥ 4.9）、just ≥ 1.33.0、POSIX sh、git；Linux amd64／arm64、WSL2；armv7、SELinux 不支援；Docker Desktop、proxy、自簽 CA、引擎基底 EOL → issue v2。時間戳 UTC ISO 8601；需詢問但無 tty／EOF → 1 印 6-4；所有 docker 資源帶 vendor_kit label；不建 network／volume；離線 upgrade 不支援；worktree 進驗收；submodule 以實測為生效條件" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L2"><g x=790 y=1597.5 w=750 h=108/></c>
<c id="p3_env_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L2"><g x=1508 y=1599.5 w=30 h=20/></c>
<c id="p3b_lg0" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=1851.5 w=200 h=40/></c>
<c id="p3b_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=14"><g x=260 y=1841.5 w=150 h=66/></c>
<c id="p3b_lg2" v="橙橢圓：需要人動作（1／3 印指令、2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12"><g x=430 y=1843.5 w=400 h=56/></c>
<c id="p3b_lg3" v="綠橢圓：成功終點（exit 0）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=14;fs=12"><g x=850 y=1845.5 w=270 h=52/></c>
<c id="p3b_lg4" v="白：步驟／說明" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=1140 y=1851.5 w=130 h=40/></c>
<c id="p3b_lgt" v="實線 = 執行順序；線上文字 = 條件／接續編號⏎淺灰底容器 = ②③ 的分組（標題 = 該段做的事）" s="text;fs=12;sc=none;fc=none"><g x=1290 y=1841.5 w=300 h=60/></c>
<c id="p3b_lg5" v="等寬字：檔案內容範例" s="fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1917.5 w=170 h=40/></c>
<c id="p3b_lg6" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=230 y=1917.5 w=190 h=40/></c>
<c id="p3b_lg7" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=440 y=1917.5 w=110 h=40/></c>
<c id="p3b_lg8" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=570 y=1917.5 w=200 h=40/></c>
<c id="p3b_lg8_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=738 y=1919.5 w=30 h=20/></c>
<c id="p3b_lg9" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=790 y=1917.5 w=220 h=40/></c>
<c id="p3b_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1973.5 w=300 h=28/></c>
<c id="p3b_tk0" v="啟動器" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2007.5 w=150 h=55/></c>
<c id="p3b_tv0" v=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2007.5 w=610 h=55/></c>
<c id="p3b_tk1" v="主機命令白名單" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2062.5 w=150 h=71/></c>
<c id="p3b_tv1" v="啟動器（POSIX sh）只准用：sh（printf、read、trap、kill、cd）、grep、sed、id、mktemp、rm、sleep、git rev-parse、docker {pull, create, cp, run, rm, inspect, image inspect, image ls, image rm, container ls, network ls, network rm, volume ls, volume rm, load, info}；check.sh 另可用 git ls-files；lint 擋清單外" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2062.5 w=610 h=71/></c>
<c id="p3b_tk2" v="docker image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2133.5 w=150 h=55/></c>
<c id="p3b_tv2" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2133.5 w=610 h=55/></c>
<c id="p3b_tk3" v="docker create／cp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2188.5 w=150 h=55/></c>
<c id="p3b_tv3" v="不執行容器，只建一個容器殼（docker create &lt;ref&gt; /x）再把 /dist 複製出來（docker cp c:/dist/. …）→ docker rm；純資料 image 沒有程式所以不能 docker run；不帶 --platform（daemon 挑原生）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2188.5 w=610 h=55/></c>
<c id="p3b_tk4" v="暫存 .tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2243.5 w=150 h=40/></c>
<c id="p3b_tv4" v="啟動器在專案內 mktemp -d 的暫存（.vendor_kit/.tmp.dist.XXXXXX）：放展開的工具 dist 與 vk-resolve；唯讀掛進引擎當 /dist；trap 刪；自有 .gitignore 的 .tmp.* 擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2243.5 w=610 h=40/></c>
<c id="p3b_tk5" v="使用者旗標（-u）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2007.5 w=150 h=55/></c>
<c id="p3b_tv5" v="rootful docker 加 -u &quot;$(id -u):$(id -g)&quot;（寫出的檔才不會變 root 的）；rootless docker（docker info SecurityOptions 含 name=rootless）不加 -u；Podman（docker --version 含 podman）改加 --userns=keep-id、不加 -u" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2007.5 w=610 h=55/></c>
<c id="p3b_tk6" v="REGISTRY_TOKEN／⏎_TOKEN_FILE" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2062.5 w=150 h=55/></c>
<c id="p3b_tv6" v="私有 registry 查最新 tag 的憑證：_TOKEN 以 -e 傳（只在 update／upgrade 的 resolve 階段）；_TOKEN_FILE = 主機檔，啟動器 -v &lt;file&gt;:/run/vk-token:ro 掛進引擎並傳容器內路徑；兩者同設 → 1；不給就改用 &lt;repo&gt;@&lt;tag&gt; 指定版本（主機 docker pull 走主機認證）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2062.5 w=610 h=55/></c>
<c id="p3b_tk7" v="vk-resolve/1" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2117.5 w=150 h=55/></c>
<c id="p3b_tv7" v="resolve 的 stdout 文法：首行 vk-resolve/&lt;P&gt;、每行 &lt;kind&gt;|&lt;f1&gt;[|&lt;f2&gt;…]（欄位以單一 | 分隔）、末行 end|&lt;N&gt;；kind = pull／extract／mount／engine／fingerprint／apply／keep／end；自由文字用 \0ooo 八進位跳脫（printf &#x27;%b&#x27; 可解）；啟動器先收完整份、驗文法才動 docker" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2117.5 w=610 h=55/></c>
<c id="p3b_tk8" v="輸入指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2172.5 w=150 h=55/></c>
<c id="p3b_tv8" v="resolve 輸出的 sha256：對 version.toml、version.local.toml、每個 metadata、managed／appended 的 dest、gen/*.stamp 第一行、.tmp.* 清單、鎖定 digest、本機引擎 image ID、正規化 argv 串接後算；apply 拿鎖後重算，不同 → 1 印 6-12" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2172.5 w=610 h=55/></c>
</diagram>
<diagram id="v1p3c" name="契約 v2：CI 契約⑤ 與驗收矩陣"><c id="title" v="契約⑤ CI 與驗收矩陣（interface_spec §7；下游 check.sh；工具 repo check.sh --dist；自身分層 + 驗收 28 條）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p3c_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p3c_pend" v="【本頁無待拍板】⏎check.sh 步驟與結束碼 §7.1；Renovate preset §7.3（根目錄 default.json）；驗收矩陣 §7.4 每條一情境" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1260 y=12 w=340 h=81/></c>
<c id="p3L5" v="契約⑤ CI（下游 check.sh 六步 + Renovate；工具 repo check.sh --dist；vendor_kit 自身分層 + 驗收矩陣）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=109 w=1560 h=1547/></c>
<c id="p3_k0" v="下游專案 CI：只呼叫 .vendor_kit/ci/check.sh，一關過才下一關（每格一步）" s="text;fs=12;sc=none;fc=none;fst=1" parent="p3L5"><g x=20 y=50 w=200 h=60/></c>
<c id="k0" v="⓪ version.local.toml 被 git track？" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=240 y=50 w=190 h=60/></c>
<c id="k1" v="① sync（frozen）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=446 y=50 w=120 h=60/></c>
<c id="k1_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k0" target="k1"></c>
<c id="k2" v="② verify（印記 sha256，全部工具）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=582 y=50 w=170 h=60/></c>
<c id="k2_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k1" target="k2"></c>
<c id="k3" v="③ upgrade --dry-run" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=768 y=50 w=150 h=60/></c>
<c id="k3_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k2" target="k3"></c>
<c id="k4" v="④ 工具測試 just &lt;repo&gt; check（若有；不得再呼叫 check.sh）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=934 y=50 w=250 h=60/></c>
<c id="k4_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k3" target="k4"></c>
<c id="k5" v="⑤ 專案測試（just check 若有）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=1200 y=50 w=170 h=60/></c>
<c id="k5_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k4" target="k5"></c>
<c id="k6" v="全部通過 → 0" s="ellipse;fc=#d5e8d4;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=1386 y=50 w=130 h=60/></c>
<c id="k6_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="k5" target="k6"></c>
<c id="k0f" v="命中 → 1 拒絕⏎（請勿把 local 覆寫提交）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=235.0 y=150 w=200 h=84/></c>
<c id="k0f_e" v="命中" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="k0" target="k0f"></c>
<c id="k1f" v="1：薄殼不符（6-1）、未完成接入（6-13）、baseline 落後（6-5）、任何 local 覆寫；3" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=416.0 y=254 w=300 h=84/></c>
<c id="k1f_e" v="升為失敗" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="k1" target="k1f"></c>
<c id="k3f" v="CI 為真且需改 tracked 檔⏎→ 1 印清單（version.toml 不動；與 -y 無關）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=763.0 y=150 w=280 h=84/></c>
<c id="k3f_e" v="需改檔" s="fs=12;exitX=0.5;exitY=1;entryX=0.2857;entryY=0" edge="1" source="k3" target="k3f"></c>
<c id="k3g" v="仍有衝突標記 → 2；印 6-6～6-8 但不紅燈" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=1063.0 y=150 w=260 h=62/></c>
<c id="k3g_e" v="衝突" s="fs=12;exitX=0.9;exitY=1;entryX=0.5;entryY=0" edge="1" source="k3" target="k3g"><g pts=943.0,245;1233.0,245/></c>
<c id="p3_kr" v="【check.sh（§7.1）】：第一行 shebang、第二行自描述、其後第一個動作 export CI=1；GitHub／GitLab 一樣、平台無關；一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（③ 有衝突標記回 2；④⑤ 原碼傳出，1/2/3 語意只對 vendor_kit 自身步驟成立）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L5"><g x=20 y=362 w=1520 h=46/></c>
<c id="p3_kr_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=1508 y=364 w=30 h=20/></c>
<c id="p3_rn_l" v="Renovate 路徑（PR 需合併時；補合併在 PR 分支完成、CI 綠後才 merge）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L5"><g x=20 y=422 w=1000 h=28/></c>
<c id="rn1" v="Renovate PR 改 version.toml 一行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=20 y=454 w=170 h=64/></c>
<c id="rn2" v="PR 的 CI 以新版跑 check.sh 完整流程（一行改動本身不構成通過依據）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=206 y=454 w=260 h=64/></c>
<c id="rn2_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="rn1" target="rn2"></c>
<c id="rn3" v="需合併 → 1 印 6-5" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=482 y=454 w=140 h=64/></c>
<c id="rn3_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="rn2" target="rn3"></c>
<c id="rn4" v="維護者在 PR 分支本機 upgrade &lt;repo&gt; -y → commit → push" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=638 y=454 w=240 h=64/></c>
<c id="rn4_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="rn3" target="rn4"></c>
<c id="rn5" v="CI 全部再跑（Renovate 不動有人推過的分支）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=894 y=454 w=220 h=64/></c>
<c id="rn5_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="rn4" target="rn5"></c>
<c id="rn6" v="綠了才 merge" s="ellipse;fc=#d5e8d4;sc=#000000;fs=14;fs=12" parent="p3L5"><g x=1130 y=454 w=110 h=64/></c>
<c id="rn6_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="rn5" target="rn6"></c>
<c id="p3_c2" v="【Renovate preset（§7.3；下游自選，vendor_kit 不出 bot）】：放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；下游 extends: [&quot;github&gt;ycpss91255-research/vendor_kit&quot;]；regex manager 匹配 **/.vendor_kit/version.toml（monorepo 子專案亦命中；key regex 與正規行契約共用）+ docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR（matchUpdateTypes）；hostRules 依 host 不寫死 ghcr.io；prBodyNotes = 6-25（6-5 的指令 + 「推 commit 後不要勾 rebase/retry」）；不設 gitIgnoredAuthors、不改 rebaseWhen；postUpgradeTasks 不採" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L5"><g x=20 y=534 w=1000 h=155/></c>
<c id="p3_c2_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=988 y=536 w=30 h=20/></c>
<c id="p3_c3" v="【工具 repo 的 CI：check.sh --dist（§7.2）】：dist 佈局（files/、init.toml、just/&lt;repo&gt;.just 存在）、init.toml 合法（schema、description 單行、strategy 只能 copy|append、src／dest 規則、copy 不得指向根 ignore 類檔）、無 symlink／hardlink／特殊檔、文字檔 LF（含 CR 即失敗 [#29]）、以 just 1.33.0 解析每個 &lt;ns&gt;.just（並擋比 1.33 新的功能）、_sync lint（just --dump --dump-format json）、Dockerfile.dist 含 LABEL io.github.&lt;org&gt;.vendor_kit=1、image 可展開、amd64／arm64 內容位元組一致、遷移後實際生效值。不檢查 binary 可執行性" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L5"><g x=1040 y=534 w=500 h=155/></c>
<c id="p3_c3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=1508 y=536 w=30 h=20/></c>
<c id="p3_c0" v="vendor_kit 自身 CI（分層，一關過才下一關；每格一個檢查）" s="text;fs=12;sc=none;fc=none;fst=1" parent="p3L5"><g x=20 y=713 w=180 h=60/></c>
<c id="c_a" v="env-test" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=210 y=713 w=84 h=60/></c>
<c id="c_b" v="test-base" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=310 y=713 w=84 h=60/></c>
<c id="c_b_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_a" target="c_b"></c>
<c id="c_c1" v="lint" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=410 y=713 w=84 h=60/></c>
<c id="c_c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=462 y=715 w=30 h=20/></c>
<c id="c_c1_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_b" target="c_c1"></c>
<c id="c_c2" v="unit" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=510 y=713 w=84 h=60/></c>
<c id="c_c2_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=562 y=715 w=30 h=20/></c>
<c id="c_c2_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_c1" target="c_c2"></c>
<c id="c_c3" v="install" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=610 y=713 w=96 h=60/></c>
<c id="c_c3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=674 y=715 w=30 h=20/></c>
<c id="c_c3_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_c2" target="c_c3"></c>
<c id="c_c4" v="merge" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=722 y=713 w=96 h=60/></c>
<c id="c_c4_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=786 y=715 w=30 h=20/></c>
<c id="c_c4_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_c3" target="c_c4"></c>
<c id="c_d" v="release（image、bootstrap.sh、tar + .digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=834 y=713 w=200 h=60/></c>
<c id="c_d_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=1002 y=715 w=30 h=20/></c>
<c id="c_d_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_c4" target="c_d"></c>
<c id="c_e" v="release-test（amd64、arm64 原生 runner）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=1050 y=713 w=190 h=60/></c>
<c id="c_e_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_d" target="c_e"></c>
<c id="c_f" v="驗收：已釋出版驅動候選 + 乾淨 fixture repo 跑完整流程" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p3L5"><g x=1256 y=713 w=250 h=60/></c>
<c id="c_f_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=1474 y=715 w=30 h=20/></c>
<c id="c_f_e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c_e" target="c_f"></c>
<c id="p3_jm" v="just 矩陣 1.33.0 + latest（latest 非 required）；lint 擋比 1.33 新的功能與白名單外主機命令（ADR 記破壞性變更）；驗收用 dev vendor_kit -i &lt;剛 build 的 tag&gt; 同一機制；每版最低環境（docker 19.03、just 1.33.0）跑完整、其他環境（docker 上界、just latest、arm64、WSL2）按世代；驗收 §7.4 條 1–13 缺任一不得出貨；已釋出 image／Release 資產／fixture 永不刪；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p3L5"><g x=20 y=789 w=1520 h=46/></c>
<c id="p3_jm_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=1508 y=791 w=30 h=20/></c>
<c id="p3_acc_l" v="驗收矩陣（§7.4；每列一個情境；左右兩表接續）" s="text;fs=13;sc=none;fc=none;fst=1" parent="p3L5"><g x=20 y=849 w=900 h=28/></c>
<c id="p3_acc_h0" v="#" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=20 y=881 w=40 h=30/></c>
<c id="p3_acc_h1" v="情境" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=60 y=881 w=150 h=30/></c>
<c id="p3_acc_h2" v="驗什麼" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=210 y=881 w=560 h=30/></c>
<c id="p3_acc_r0c0" v="1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=911 w=40 h=73/></c>
<c id="p3_acc_r0c1" v="已釋出版驅動候選" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=911 w=150 h=73/></c>
<c id="p3_acc_r0c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=913 w=30 h=20/></c>
<c id="p3_acc_r0c2" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 第一行改為候選 C → sync（1 印 6-1、零 tracked 寫入）→ upgrade vendor_kit（1 印 6-2、薄殼重產）→ sync 0 → 工具 recipe → upgrade 全；第二次 upgrade vendor_kit → 0；禁止由候選樹複製 fixture、禁 stub 引擎" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=911 w=560 h=73/></c>
<c id="p3_acc_r1c0" v="2" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=984 w=40 h=42/></c>
<c id="p3_acc_r1c1" v="最低環境 × 世代" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=984 w=150 h=42/></c>
<c id="p3_acc_r1c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=986 w=30 h=20/></c>
<c id="p3_acc_r1c2" v="每個歷史版本在最低環境（docker 19.03、just 1.33.0）跑完整；其他環境按世代覆蓋；成本上限當觸發討論條件" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=984 w=560 h=42/></c>
<c id="p3_acc_r2c0" v="3" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1026 w=40 h=42/></c>
<c id="p3_acc_r2c1" v="升級後 == 全新安裝" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1026 w=150 h=42/></c>
<c id="p3_acc_r2c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1028 w=30 h=20/></c>
<c id="p3_acc_r2c2" v="升級後 .vendor_kit/ tracked 內容 == 用 C 全新 install + add（排除時間戳、digest、written_by）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1026 w=560 h=42/></c>
<c id="p3_acc_r3c0" v="4" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1068 w=40 h=26/></c>
<c id="p3_acc_r3c1" v="連續升級" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1068 w=150 h=26/></c>
<c id="p3_acc_r3c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1070 w=30 h=20/></c>
<c id="p3_acc_r3c2" v="r_i → r_j → C；固定 floor 直接跳升 C" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1068 w=560 h=26/></c>
<c id="p3_acc_r4c0" v="5" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1094 w=40 h=42/></c>
<c id="p3_acc_r4c1" v="降版" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1094 w=150 h=42/></c>
<c id="p3_acc_r4c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1096 w=30 h=20/></c>
<c id="p3_acc_r4c2" v="upgrade vendor_kit@&lt;舊版&gt;：同 P／schema 成功；跨 schema 改檔前拒絕 3 印 6-10、零寫入" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1094 w=560 h=42/></c>
<c id="p3_acc_r5c0" v="6" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1136 w=40 h=42/></c>
<c id="p3_acc_r5c1" v="&lt; floor 太舊" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1136 w=150 h=42/></c>
<c id="p3_acc_r5c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1138 w=30 h=20/></c>
<c id="p3_acc_r5c2" v="唯一可用 synthetic fixture；任一動詞 → 3 印 6-18、零寫入；floor 檢查在任何上網之前（斷網也回 3）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1136 w=560 h=42/></c>
<c id="p3_acc_r6c0" v="7" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1178 w=40 h=57/></c>
<c id="p3_acc_r6c1" v="舊 bootstrap.sh 再跑" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1178 w=150 h=57/></c>
<c id="p3_acc_r6c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1180 w=30 h=20/></c>
<c id="p3_acc_r6c2" v="在已升級 repo 再跑：用 version.toml 指定引擎，不降版" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1178 w=560 h=57/></c>
<c id="p3_acc_r7c0" v="8" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1235 w=40 h=26/></c>
<c id="p3_acc_r7c1" v="舊引擎讀新檔" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1235 w=150 h=26/></c>
<c id="p3_acc_r7c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1237 w=30 h=20/></c>
<c id="p3_acc_r7c2" v="dev vendor_kit -i 舊 image：寫入前拒絕 3 印 6-19；不重產 tracked 薄殼" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1235 w=560 h=26/></c>
<c id="p3_acc_r8c0" v="9" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1261 w=40 h=42/></c>
<c id="p3_acc_r8c1" v="只改第一行後 CI=true sync" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1261 w=150 h=42/></c>
<c id="p3_acc_r8c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1263 w=30 h=20/></c>
<c id="p3_acc_r8c2" v="模擬 Renovate、驗 CI 真值規則 → 1 列薄殼不符、零 tracked 寫入" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1261 w=560 h=42/></c>
<c id="p3_acc_r9c0" v="10" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1303 w=40 h=42/></c>
<c id="p3_acc_r9c1" v="fresh clone 無 gen/" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1303 w=150 h=42/></c>
<c id="p3_acc_r9c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1305 w=30 h=20/></c>
<c id="p3_acc_r9c2" v="just vendor_kit 列出 vendor_kit 命名空間不觸網（工具命名空間 sync 後才出現，mod? 缺檔不擋）；sync 可跑；缺 stamp 不盲寫；缺 gen/.stamp 時相容判定用薄殼首行" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1303 w=560 h=42/></c>
<c id="p3_acc_r10c0" v="11" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1345 w=40 h=42/></c>
<c id="p3_acc_r10c1" v="使用者改薄殼／未納管檔／append" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1345 w=150 h=42/></c>
<c id="p3_acc_r10c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1347 w=30 h=20/></c>
<c id="p3_acc_r10c2" v="不覆蓋、不刪、詢問與結束碼符合契約；append 零／多命中 → 保留 warn" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1345 w=560 h=42/></c>
<c id="p3_acc_r11c0" v="12" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1387 w=40 h=42/></c>
<c id="p3_acc_r11c1" v="中斷與重跑" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1387 w=150 h=42/></c>
<c id="p3_acc_r11c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1389 w=30 h=20/></c>
<c id="p3_acc_r11c2" v="resolve／apply／遷移各階段故障注入；再跑保持原狀或可辨識恢復；唯讀動詞遇未完成交易只印 6-33；disk-full／rename 失敗" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1387 w=560 h=42/></c>
<c id="p3_acc_r12c0" v="13" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1429 w=40 h=42/></c>
<c id="p3_acc_r12c1" v="歷史 parser × 異常 TOML" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1429 w=150 h=42/></c>
<c id="p3_acc_r12c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1431 w=30 h=20/></c>
<c id="p3_acc_r12c2" v="BOM、空白、重複 vendor_kit 行 → 1、schema 位置、local 覆寫、尾端註解" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1429 w=560 h=42/></c>
<c id="p3_acc_r13c0" v="14" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=20 y=1471 w=40 h=26/></c>
<c id="p3_acc_r13c1" v="just 矩陣" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=60 y=1471 w=150 h=26/></c>
<c id="p3_acc_r13c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=178 y=1473 w=30 h=20/></c>
<c id="p3_acc_r13c2" v="1.33.0 + latest（latest 非 required）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=210 y=1471 w=560 h=26/></c>
<c id="p3_accb_h0" v="#" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=790 y=881 w=40 h=30/></c>
<c id="p3_accb_h1" v="情境" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=830 y=881 w=150 h=30/></c>
<c id="p3_accb_h2" v="驗什麼" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="p3L5"><g x=980 y=881 w=560 h=30/></c>
<c id="p3_accb_r0c0" v="15" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=911 w=40 h=42/></c>
<c id="p3_accb_r0c1" v="amd64 與 arm64 原生 runner" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=911 w=150 h=42/></c>
<c id="p3_accb_r0c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=913 w=30 h=20/></c>
<c id="p3_accb_r0c2" v="各跑完整流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；工具 dist 兩平台位元組一致；引擎 image 兩平台 LABEL 一致" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=911 w=560 h=42/></c>
<c id="p3_accb_r1c0" v="16" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=953 w=40 h=57/></c>
<c id="p3_accb_r1c1" v="離線包（Q26）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=953 w=150 h=57/></c>
<c id="p3_accb_r1c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=955 w=30 h=20/></c>
<c id="p3_accb_r1c2" v="無法連 GHCR 的機器用 bootstrap.sh --local &lt;tar&gt;（旁檔 .digest）完成 install → add --local → sync，version.toml 為正式 ref@digest、metadata 有 local_image_id；旁檔缺 → 1；amd64／arm64 各一次" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=953 w=560 h=57/></c>
<c id="p3_accb_r2c0" v="17" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1010 w=40 h=57/></c>
<c id="p3_accb_r2c1" v="離線可用（Q22／Q26）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1010 w=150 h=57/></c>
<c id="p3_accb_r2c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1012 w=30 h=20/></c>
<c id="p3_accb_r2c2" v="本機已有 image 後斷網 → just &lt;ns&gt; build（自動 sync 快路徑）與 just vendor_kit sync 必須成功且不起 pull；斷網 + 無 image → 1 印 6-31 於 --timeout 5 內結束、不 hang" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1010 w=560 h=57/></c>
<c id="p3_accb_r3c0" v="18" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1067 w=40 h=57/></c>
<c id="p3_accb_r3c1" v="私有工具" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1067 w=150 h=57/></c>
<c id="p3_accb_r3c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1069 w=30 h=20/></c>
<c id="p3_accb_r3c2" v="add &lt;repo&gt;@&lt;tag&gt; 可拉；add &lt;repo&gt; 無 token → 1 印 6-3；update 無 token → 1 印 6-3 逐字；錯 token → 1；對 token → 列出；TOKEN_FILE（驗 -v 掛載、容器內路徑）；兩者同設 → 1；所有輸出與 metadata／log grep 不到 token" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1067 w=560 h=57/></c>
<c id="p3_accb_r4c0" v="19" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1124 w=40 h=42/></c>
<c id="p3_accb_r4c1" v="append" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1124 w=150 h=42/></c>
<c id="p3_accb_r4c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1126 w=30 h=20/></c>
<c id="p3_accb_r4c2" v="LF／CRLF／混合檔各跑 add → upgrade → remove；Markdown 尾端兩空格不得視為相同；install 的 .dockerignore 三行 append → uninstall 刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1124 w=560 h=42/></c>
<c id="p3_accb_r5c0" v="20" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1166 w=40 h=42/></c>
<c id="p3_accb_r5c1" v="空白路徑" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1166 w=150 h=42/></c>
<c id="p3_accb_r5c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1168 w=30 h=20/></c>
<c id="p3_accb_r5c2" v="專案根含空白與 $、dev -p &quot;含 空白/路徑&quot;；vk-resolve mount 八進位跳脫往返；just vendor_kit add --help 到引擎" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1166 w=560 h=42/></c>
<c id="p3_accb_r6c0" v="21" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1208 w=40 h=42/></c>
<c id="p3_accb_r6c1" v="worktree／submodule" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1208 w=150 h=42/></c>
<c id="p3_accb_r6c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1210 w=30 h=20/></c>
<c id="p3_accb_r6c2" v="git worktree（.git 是檔）完整流程；submodule（已初始化、有工作樹）作專案根：實測後定（F3）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1208 w=560 h=42/></c>
<c id="p3_accb_r7c0" v="22" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1250 w=40 h=42/></c>
<c id="p3_accb_r7c1" v="rootless docker／Podman" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1250 w=150 h=42/></c>
<c id="p3_accb_r7c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1252 w=30 h=20/></c>
<c id="p3_accb_r7c2" v="setup-docker-action rootless: true（不加 -u、/repo 可寫）與 Podman（Ubuntu 24.04 runner 內建 4.9.3：--userns=keep-id）各跑完整流程；uid 12345 無 passwd 項" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1250 w=560 h=42/></c>
<c id="p3_accb_r8c0" v="23" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1292 w=40 h=57/></c>
<c id="p3_accb_r8c1" v="prune" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1292 w=150 h=57/></c>
<c id="p3_accb_r8c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1294 w=30 h=20/></c>
<c id="p3_accb_r8c2" v="完整流程前後 docker network ls／volume ls 差集為空；故意留一個帶 label 的 network／volume 與殘留容器，prune 後必須消失；未引用舊工具 image 刪、version.toml 引用的與 local 覆寫 tag 保留；--dry-run 零刪除；未恢復的 .tmp.* 不刪" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1292 w=560 h=57/></c>
<c id="p3_accb_r9c0" v="24" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1349 w=40 h=42/></c>
<c id="p3_accb_r9c1" v="多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1349 w=150 h=42/></c>
<c id="p3_accb_r9c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1351 w=30 h=20/></c>
<c id="p3_accb_r9c2" v="兩工具 upgrade 一個衝突 2 一個成功 → 兩個都做完、回 2；一個失敗 1 一個有新版 → update 回 1" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1349 w=560 h=42/></c>
<c id="p3_accb_r10c0" v="25" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1391 w=40 h=42/></c>
<c id="p3_accb_r10c1" v="F1 fixture（just 1.33.0）" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1391 w=150 h=42/></c>
<c id="p3_accb_r10c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1393 w=30 h=20/></c>
<c id="p3_accb_r10c2" v="cache 缺檔時 just vendor_kit sync 可進入（mod?）；just &lt;ns&gt; build 從子目錄執行自動 sync 且不觸發 6-9；--dist lint 擋缺 _sync 的模組" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1391 w=560 h=42/></c>
<c id="p3_accb_r11c0" v="26" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1433 w=40 h=26/></c>
<c id="p3_accb_r11c1" v="無 tty／EOF" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1433 w=150 h=26/></c>
<c id="p3_accb_r11c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1435 w=30 h=20/></c>
<c id="p3_accb_r11c2" v="CI 無 -y 需詢問 → 1 印 6-4；互動中 Ctrl-C → 1、不記 declined、可重跑" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1433 w=560 h=26/></c>
<c id="p3_accb_r12c0" v="27" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1459 w=40 h=42/></c>
<c id="p3_accb_r12c1" v="Renovate 實際 repo" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1459 w=150 h=42/></c>
<c id="p3_accb_r12c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1461 w=30 h=20/></c>
<c id="p3_accb_r12c2" v="人工 commit 後 Renovate 不再動該分支；monorepo 子專案 version.toml 被命中" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1459 w=560 h=42/></c>
<c id="p3_accb_r13c0" v="28" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=790 y=1501 w=40 h=26/></c>
<c id="p3_accb_r13c1" v="驗收動詞集合" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=830 y=1501 w=150 h=26/></c>
<c id="p3_accb_r13c1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p3L5"><g x=948 y=1503 w=30 h=20/></c>
<c id="p3_accb_r13c2" v="由 vendor.just 實際列出推導（含 help、參數轉發、失敗碼）；刪掉受測物必紅" s="fc=#ffffff;sc=#999999;fs=12" parent="p3L5"><g x=980 y=1501 w=560 h=26/></c>
<c id="p3c_lg0" v="橙橢圓：需要人動作（1／3 印指令、2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=14;fs=12"><g x=40 y=1678 w=400 h=56/></c>
<c id="p3c_lg1" v="綠橢圓：成功終點（exit 0）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=14;fs=12"><g x=460 y=1680 w=270 h=52/></c>
<c id="p3c_lg2" v="白：步驟／說明" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=750 y=1686 w=130 h=40/></c>
<c id="p3c_lg3" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=900 y=1686 w=190 h=40/></c>
<c id="p3c_lg4" v="灰底：表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1110 y=1686 w=110 h=40/></c>
<c id="p3c_lgt" v="實線 = 執行順序；線上文字 = 條件⏎驗收表：一列一個情境" s="text;fs=12;sc=none;fc=none"><g x=1240 y=1676 w=300 h=60/></c>
<c id="p3c_lg5" v="淺灰底：分組（無狀態意義）" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=40 y=1752 w=200 h=40/></c>
<c id="p3c_lg6" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=260 y=1752 w=200 h=40/></c>
<c id="p3c_lg6_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=428 y=1754 w=30 h=20/></c>
<c id="p3c_lg7" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=480 y=1752 w=220 h=40/></c>
<c id="p3c_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1808 w=300 h=28/></c>
<c id="p3c_tk0" v="check.sh 六步（⓪–⑤）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1842 w=150 h=55/></c>
<c id="p3c_tv0" v="vendor_kit 出貨、進 git 的腳本（第二行自描述、第一個動作 export CI=1）：⓪ local 被 track → 1；① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；整體結束碼 = 第一個失敗步驟的碼" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1842 w=610 h=55/></c>
<c id="p3c_tk1" v="check.sh --dist" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1897 w=150 h=55/></c>
<c id="p3c_tv1" v="同一支腳本的供應端模式：在工具 repo 的 CI 驗 dist 佈局、init.toml、dest 規則、無 symlink／hardlink、無 CRLF、just 1.33.0 可解析、_sync lint、Dockerfile.dist 含 LABEL、image 可展開、兩平台位元組一致" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1897 w=610 h=55/></c>
<c id="p3c_tk2" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1952 w=150 h=55/></c>
<c id="p3c_tv2" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1952 w=610 h=55/></c>
<c id="p3c_tk3" v="CI／runner" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2007 w=150 h=40/></c>
<c id="p3c_tv3" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2007 w=610 h=40/></c>
<c id="p3c_tk4" v="Renovate preset" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2047 w=150 h=55/></c>
<c id="p3c_tv4" v="放 vendor_kit repo 根目錄 default.json（自身設定用 renovate.json）；regex manager 匹配 **/.vendor_kit/version.toml + docker datasource，同時擷取 currentValue（tag）與 currentDigest；PR 只改一行；major 分開 PR；prBodyNotes = 6-25" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2047 w=610 h=55/></c>
<c id="p3c_tk5" v="Renovate／PR／rebase" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2102 w=150 h=40/></c>
<c id="p3c_tv5" v="Renovate = 下游自選的機器人，只改 version.toml 一行；PR = 請求合併的頁面；rebase = 把分支重接到最新主線（勿勾，會丟掉人補的合併）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2102 w=610 h=40/></c>
<c id="p3c_tk6" v="env-test／test-base" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2142 w=150 h=55/></c>
<c id="p3c_tv6" v="vendor_kit 自身 CI 的前兩個 stage：env-test = smoke（環境檢查先於一切：docker、just 版本、runner 能力）；test-base FROM env-test = 之後 lint／unit／install／merge 各測試 stage 的共同基底，環境不對就沒有任何測試會跑" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2142 w=610 h=55/></c>
<c id="p3c_tk7" v="lint／unit／測試矩陣" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1842 w=150 h=40/></c>
<c id="p3c_tv7" v="lint = 靜態檢查（擋語法、擋比 just 1.33 新的功能、擋白名單外主機命令）；unit = 單元測試；矩陣 = 同一套測試在多個 just 版本各跑一次（1.33.0 + latest，latest 非 required）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1842 w=610 h=40/></c>
<c id="p3c_tk8" v="release／release-test" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1882 w=150 h=40/></c>
<c id="p3c_tv8" v="release = 發佈版本（push 多架構 image、附 bootstrap.sh 與 tar + .digest）；release-test = 對剛發佈的 image 在 amd64、arm64 原生 runner 再測一次" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1882 w=610 h=40/></c>
<c id="p3c_tk9" v="fixture repo" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1922 w=150 h=40/></c>
<c id="p3c_tv9" v="驗收用的乾淨小 git repo：用剛 build 的引擎 image 從 bootstrap 到 uninstall 跑一遍完整流程；禁止由候選樹複製、禁 stub 引擎；fixture 永不刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1922 w=610 h=40/></c>
<c id="p3c_tk10" v="floor" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1962 w=150 h=40/></c>
<c id="p3c_tv10" v="相容承諾的下限：固定 release 常數（第一個正式版 v1.0.0、P=1、schema=1），只能經 ADR 提高；低於 floor → 3 印 6-18 零寫入；floor 檢查在任何上網之前（啟動器可先 inspect 引擎 LABEL）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1962 w=610 h=40/></c>
<c id="p3c_tk11" v="rootless／Podman" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2002 w=150 h=40/></c>
<c id="p3c_tv11" v="rootless = 不用 root 跑的 docker 模式（容器內已是你自己，不加 -u）；Podman = 相容 docker 指令的另一套容器工具（GitHub runner 內建 4.9.3；--userns=keep-id）；兩者都進驗收" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2002 w=610 h=40/></c>
<c id="p3c_tk12" v="worktree／submodule" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2042 w=150 h=40/></c>
<c id="p3c_tv12" v="git worktree = 同一 repo 另開一個工作目錄（.git 是檔）；submodule = repo 裡嵌另一個 repo；前者進驗收、後者以實測通過為契約生效條件（F3）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2042 w=610 h=40/></c>
<c id="p3c_tk13" v="離線可用（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2082 w=150 h=40/></c>
<c id="p3c_tv13" v="啟動器先 docker image inspect，本機有就不 pull；斷網 + 本機已有 image → sync／build 必須成功（驗收）；斷網 + 無 image → 1 印 6-31 不 hang（逾時）；離線 upgrade 不支援" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2082 w=610 h=40/></c>
<c id="p3c_tk14" v="多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2122 w=150 h=40/></c>
<c id="p3c_tv14" v="不帶 repo 的動詞做得完的做完（先完整預檢，任一預檢失敗才整體不動），最後回最需要處理的碼：失敗 1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；update 同時遇 1 與 2 → 1；訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2122 w=610 h=40/></c>
</diagram>
<diagram id="v1p4" name="架構圖 v2"><c id="title" v="架構圖 v2 ── 主機、引擎 8 模組、registry（只畫模組、最小單元、模組間傳的資料）" s="text;fs=18;fst=1"><g x=40 y=20 w=1200 h=34/></c>
<c id="p4_num" v="契約編號：①介面 p1／p1b／p1c｜②專案裡的檔 p2／p2b／p2c｜③工具 repo p3｜④啟動器↔引擎 p3b｜⑤CI p3c｜架構 p4｜流程 p5～；訊息編號 6-N = interface_spec §6 逐字" s="text;fs=12;sc=none;fc=none"><g x=40 y=56 w=1200 h=26/></c>
<c id="p4_np" v="【本頁無待拍板】：本頁只畫模組、最小單元、模組間傳的資料（箭頭只標傳什麼，不標動作；雙箭頭 = 讀寫都有）；載入順序／操作順序／sync 判斷／拉取條件／退出流程一律見流程頁（p5～）。啟動器不算引擎模組（主機側薄殼）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1000 y=12 w=600 h=65/></c>
<c id="p4G" v="GHCR（ghcr.io）── 兩種 image 都多架構；拉取都由主機上的啟動器執行，引擎容器內不呼叫 docker" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#e1d5e7;swfc=#ffffff;sc=#9673a6"><g x=40 y=96 w=1560 h=162/></c>
<c id="g_eng" v="【引擎 image ghcr.io/&lt;org&gt;/vendor_kit:vN（公開）】⏎多架構 amd64 + arm64；LABEL …vendor_kit=1、.protocol、.schema；一個專案用 version.toml 正規行那一版；引擎覆寫 vendor_kit=&lt;tag&gt;（version.local.toml）時啟動器 docker image inspect 驗 ID 後直接用本機 image、不 pull；也出 docker save tar + .digest（#27）；已釋出永不刪" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12" parent="p4G"><g x=20 y=50 w=520 h=92/></c>
<c id="g_eng_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4G"><g x=508 y=52 w=30 h=20/></c>
<c id="g_dist" v="【工具 image ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist:&lt;tag&gt;】⏎多架構 amd64 + arm64（同一次 buildx、COPY-only）；純資料 FROM scratch 只有 /dist；LABEL …vendor_kit=1；version.toml 與印記記 index digest" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12" parent="p4G"><g x=560 y=50 w=500 h=92/></c>
<c id="g_dist_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4G"><g x=1028 y=52 w=30 h=20/></c>
<c id="g_note" v="【registry 模組只查 tag／index digest】（update／add／upgrade 用；私有 registry 用 VENDOR_KIT_REGISTRY_TOKEN 或 TOKEN_FILE（-v 掛 /run/vk-token），或改用 &lt;repo&gt;@&lt;tag&gt;）⏎sync 不查最新版；只拉鎖定版；拉取由主機上的啟動器執行，先 docker image inspect 再 pull（逾時）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12" parent="p4G"><g x=1080 y=50 w=460 h=92/></c>
<c id="g_note_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4G"><g x=1508 y=52 w=30 h=20/></c>
<c id="p4H" v="主機（使用者電腦／CI runner）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=328 w=520 h=1328/></c>
<c id="h0" v="使用者⏎打 just vendor_kit &lt;動詞&gt; …⏎或 just &lt;ns&gt; …" s="ellipse;fc=#FFF4C3;sc=#000000;fs=14;fs=12" parent="p4H"><g x=20 y=50 w=220 h=106/></c>
<c id="h1" v="根 justfile（使用者的，進 git）⏎import &#x27;.vendor_kit/entry.just&#x27;" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4H"><g x=20 y=186 w=220 h=61/></c>
<c id="h1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4H"><g x=208 y=188 w=30 h=20/></c>
<c id="h2" v=".vendor_kit/entry.just（進 git）⏎mod vendor_kit &#x27;vendor.just&#x27;⏎import? &#x27;gen/tools.just&#x27;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4H"><g x=20 y=277 w=220 h=108/></c>
<c id="h3" v=".vendor_kit/vendor.just（進 git）⏎動詞 recipe（一行轉發）⏎+ 啟動器本體（POSIX sh）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4H"><g x=20 y=415 w=220 h=79/></c>
<c id="h3_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4H"><g x=208 y=417 w=30 h=20/></c>
<c id="h4" v="【啟動器】（主機側薄殼，非引擎模組；主機需 docker ≥ 19.03、sh、just ≥ 1.33.0）⏎下列為責任單元；命令步驟見流程頁與 p3b" s="fc=#f8cecc;sc=#b85450;fs=14;fs=12" parent="p4H"><g x=20 y=524 w=220 h=296/></c>
<c id="h4_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4H"><g x=208 y=526 w=30 h=20/></c>
<c id="h4_u0_0" v="讀引擎 ref" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=632 w=72 h=24/></c>
<c id="h4_u0_1" v="取得引擎／工具 image" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=104 y=632 w=124 h=24/></c>
<c id="h4_u1_0" v="展開 /dist 到暫存" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=662 w=110 h=24/></c>
<c id="h4_u1_1" v="起引擎容器" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=142 y=662 w=68 h=24/></c>
<c id="h4_u2_0" v="vk-resolve 驗文法" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=692 w=114 h=24/></c>
<c id="h4_u3_0" v="協定旗標 --protocol" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=722 w=124 h=24/></c>
<c id="h4_u4_0" v="清理（trap）" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=752 w=82 h=24/></c>
<c id="h4_u4_1" v="pull 逾時" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=114 y=752 w=68 h=24/></c>
<c id="h4_u5_0" v="資源 label" s="fc=#ffffff;sc=#666666;fs=10" parent="p4H"><g x=26 y=782 w=74 h=24/></c>
<c id="h_vk" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.vendor_kit/ # 契約② p2，根目錄只多這個⏎├─ version.toml # 進 git：唯一來源⏎├─ version.local.toml # 不進 git：dev 覆寫⏎├─ .gitignore # 進 git：我們自己的⏎├─ entry.just # 進 git：mod + import?⏎├─ vendor.just # 進 git：動詞 + 啟動器⏎├─ ci/check.sh # 進 git：CI 六步（⓪–⑤）⏎├─ baseline/ # 進 git：.gitkeep、&lt;repo&gt;/ 範本 + metadata⏎├─ gen/ # 不進 git：tools.just、.stamp、⏎│ # &lt;repo&gt;.stamp（印記）⏎├─ .tmp.&lt;verb&gt;.&lt;id&gt;.toml # 不進 git：進度日誌⏎├─ .tmp.dist.&lt;id&gt;/ # 不進 git：啟動器暫存⏎└─ cache/&lt;repo&gt;/ # 不進 git：工具檔展開&lt;/pre&gt;" s="fc=#ffffff;sc=#999999;fs=12" parent="p4H"><g x=20 y=840 w=480 h=217/></c>
<c id="tmp" v="暫存 .vendor_kit/⏎.tmp.dist.&lt;id&gt;/（專案內）⏎工具 /dist 展開副本 + vk-resolve⏎（唯讀掛進引擎當 /dist）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4H"><g x=260 y=50 w=200 h=94/></c>
<c id="g1" v=".vendor_kit/gen/tools.just（不進 git）⏎mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/⏎just/&lt;ns&gt;.just&#x27;⏎一行一命名空間" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="p4H"><g x=260 y=277 w=240 h=108/></c>
<c id="g1_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4H"><g x=468 y=279 w=30 h=20/></c>
<c id="g2" v="工具命名空間 just &lt;ns&gt; …⏎= cache/&lt;repo&gt;/just/&lt;ns&gt;.just⏎裡的 recipe" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4H"><g x=260 y=415 w=240 h=79/></c>
<c id="g2_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4H"><g x=468 y=417 w=30 h=20/></c>
<c id="p4E" v="引擎容器 vendor_kit:vN（8 個模組；每個模組列最小單元，一格一個）" s="swimlane;startSize=38;fst=1;fs=16;container=1;fc=#e1d5e7;swfc=#ffffff;sc=#9673a6"><g x=600 y=328 w=560 h=1328/></c>
<c id="m_reg" v="【registry】：查 GHCR" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=290 y=164 w=250 h=128/></c>
<c id="m_reg_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=508 y=166 w=30 h=20/></c>
<c id="m_reg_u0_0" v="查 tag（SemVer 最大正式版）" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=194 w=164 h=24/></c>
<c id="m_reg_u1_0" v="查 index digest" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=224 w=106 h=24/></c>
<c id="m_reg_u1_1" v="token／token file" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=408 y=224 w=118 h=24/></c>
<c id="m_reg_u2_0" v="逾時" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=254 w=38 h=24/></c>
<c id="m_ver" v="【version】：version.toml／local 讀寫" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=290 y=314 w=250 h=144/></c>
<c id="m_ver_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=508 y=316 w=30 h=20/></c>
<c id="m_ver_u0_0" v="讀 toml（正規行）" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=360 w=108 h=24/></c>
<c id="m_ver_u0_1" v="寫 toml" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=410 y=360 w=58 h=24/></c>
<c id="m_ver_u1_0" v="schema 轉換" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=390 w=80 h=24/></c>
<c id="m_ver_u1_1" v="flock" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=382 y=390 w=48 h=24/></c>
<c id="m_ver_u1_2" v="指紋" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=436 y=390 w=38 h=24/></c>
<c id="m_ver_u2_0" v="進度日誌" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=420 w=58 h=24/></c>
<c id="m_ver_u2_1" v="label／keep" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=360 y=420 w=82 h=24/></c>
<c id="m_mat" v="【materialize】：/dist → cache/&lt;repo&gt;/" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=290 y=480 w=250 h=158/></c>
<c id="m_mat_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=508 y=482 w=30 h=20/></c>
<c id="m_mat_u0_0" v="展開 /dist" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=526 w=74 h=24/></c>
<c id="m_mat_u0_1" v="路徑驗證" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=376 y=526 w=58 h=24/></c>
<c id="m_mat_u1_0" v="印記 gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=556 w=140 h=24/></c>
<c id="m_mat_u2_0" v="verify sha256" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=586 w=96 h=24/></c>
<c id="m_bl" v="【baseline】：baseline/&lt;repo&gt;/ + metadata" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=290 y=660 w=250 h=114/></c>
<c id="m_bl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=508 y=662 w=30 h=20/></c>
<c id="m_bl_u0_0" v="範本副本" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=706 w=58 h=24/></c>
<c id="m_bl_u0_1" v="metadata" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=360 y=706 w=66 h=24/></c>
<c id="m_bl_u0_2" v="五態 state" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=432 y=706 w=74 h=24/></c>
<c id="m_bl_u1_0" v="declined_hash" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=736 w=96 h=24/></c>
<c id="m_bl_u1_1" v="conflicts" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=398 y=736 w=72 h=24/></c>
<c id="m_lg" v="【launcher-gen】：薄殼、gen/、根 justfile 一行、根 .dockerignore 三行" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=290 y=952 w=250 h=354/></c>
<c id="m_lg_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=508 y=954 w=30 h=20/></c>
<c id="m_lg_u0_0" v="薄殼四檔" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=1013 w=58 h=24/></c>
<c id="m_lg_u0_1" v="自描述首行" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=360 y=1013 w=68 h=24/></c>
<c id="m_lg_u1_0" v="tools.just（mod?）" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=1043 w=122 h=24/></c>
<c id="m_lg_u1_1" v="check.sh" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=424 y=1043 w=66 h=24/></c>
<c id="m_lg_u2_0" v=".stamp" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=296 y=1073 w=54 h=24/></c>
<c id="m_lg_u2_1" v="justfile 四行" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=356 y=1073 w=92 h=24/></c>
<c id="m_mg" v="【merge】：逐檔合併" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=296 y=806 w=116 h=114/></c>
<c id="m_mg_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=380 y=808 w=30 h=20/></c>
<c id="m_mg_u0_0" v="狀態機" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=302 y=852 w=48 h=24/></c>
<c id="m_mg_u1_0" v="merge-file" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=302 y=882 w=78 h=24/></c>
<c id="m_init" v="【init】：初始檔" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=422 y=806 w=116 h=114/></c>
<c id="m_init_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4E"><g x=506 y=808 w=30 h=20/></c>
<c id="m_init_u0_0" v="建檔" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=428 y=852 w=38 h=24/></c>
<c id="m_init_u0_1" v="append" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=472 y=852 w=54 h=24/></c>
<c id="m_init_u1_0" v="新檔詢問" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=428 y=882 w=58 h=24/></c>
<c id="grp_im" s="fc=none;sc=#666666;dashed=1;dashPattern=1 3" parent="p4E"><g x=290 y=796 w=250 h=134/></c>
<c id="m_cli" v="【cli】" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12" parent="p4E"><g x=20 y=50 w=140 h=1256/></c>
<c id="m_cli_u0" v="子命令解析" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=80 w=120 h=24/></c>
<c id="m_cli_u1" v="--protocol P" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=110 w=120 h=24/></c>
<c id="m_cli_u2" v="resolve／apply" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=140 w=120 h=24/></c>
<c id="m_cli_u3" v="詢問／-y／tty" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=170 w=120 h=24/></c>
<c id="m_cli_u4" v="結束碼 0/1/2/3" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=200 w=120 h=24/></c>
<c id="m_cli_u5" v="呼叫其他模組" s="fc=#ffffff;sc=#666666;fs=10" parent="p4E"><g x=30 y=230 w=120 h=24/></c>
<c id="d_reg" v="tag, index digest" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.1417;startArrow=block;startFill=1" edge="1" source="m_reg" target="m_cli"></c>
<c id="d_ver" v="version.toml 內容⏎指紋" s="fs=12;exitX=1;exitY=0.2675;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_cli" target="m_ver"></c>
<c id="d_mat" v="/dist 路徑、&lt;repo&gt;" s="fs=12;exitX=1;exitY=0.4053;entryX=0;entryY=0.5" edge="1" source="m_cli" target="m_mat"></c>
<c id="d_bl" v="metadata" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5311;startArrow=block;startFill=1" edge="1" source="m_bl" target="m_cli"></c>
<c id="d_im" v="檔案清單⏎逐檔決定" s="fs=12;exitX=1;exitY=0.6473;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_cli" target="grp_im"></c>
<c id="d_lg" v="引擎 ref、動詞清單" s="fs=12;exitX=1;exitY=0.8591;entryX=0;entryY=0.5" edge="1" source="m_cli" target="m_lg"></c>
<c id="d_mat_bl" v="cache 路徑、印記" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m_mat" target="m_bl"></c>
<c id="d_im_bl" v="檔案清單、逐檔決定" s="fs=12;exitX=0.5;exitY=0;entryX=0.5;entryY=1" edge="1" source="grp_im" target="m_bl"></c>
<c id="p4P" v="專案根（掛載為 /repo）" s="swimlane;startSize=38;fst=1;fs=18;container=1;fc=#d5e8d4;swfc=#ffffff;sc=#000000"><g x=1320 y=328 w=280 h=1328/></c>
<c id="f_note" v="整個專案根 -v &lt;專案根&gt;:/repo -w /repo 掛進引擎（可寫）；引擎只寫箭頭指到的路徑；工具檔另從 .tmp.dist.&lt;id&gt;/ 唯讀掛 /dist/&lt;repo&gt;" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="p4P"><g x=15 y=50 w=240 h=94/></c>
<c id="f_ver" v="version.toml（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4P"><g x=15 y=314 w=240 h=36/></c>
<c id="f_ver_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=316 w=30 h=20/></c>
<c id="f_vl" v="version.local.toml（dev 覆寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="p4P"><g x=15 y=358 w=240 h=36/></c>
<c id="f_vl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=360 w=30 h=20/></c>
<c id="f_repo" v="cache/&lt;repo&gt;/（不進 git，不可改）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333;fst=1" parent="p4P"><g x=15 y=480 w=240 h=118/></c>
<c id="f_repo_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=482 w=30 h=20/></c>
<c id="f_repo_f0" v="files/…" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="f_repo"><g x=10 y=30 w=210 h=24/></c>
<c id="f_repo_f1" v="init.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="f_repo"><g x=10 y=58 w=210 h=24/></c>
<c id="f_repo_f2" v="just/&lt;ns&gt;.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="f_repo"><g x=10 y=86 w=210 h=24/></c>
<c id="f_stamp" v="gen/&lt;repo&gt;.stamp（印記）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="p4P"><g x=15 y=606 w=240 h=32/></c>
<c id="f_stamp_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=608 w=30 h=20/></c>
<c id="f_bl" v="baseline/&lt;repo&gt;/（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366;fst=1" parent="p4P"><g x=15 y=660 w=240 h=90/></c>
<c id="f_bl_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=662 w=30 h=20/></c>
<c id="f_bl_f0" v="範本副本（上次合併的）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_bl"><g x=10 y=30 w=210 h=24/></c>
<c id="f_bl_f1" v="metadata .vendor_kit.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_bl"><g x=10 y=58 w=210 h=24/></c>
<c id="f_user" v="初始檔（使用者的，進 git；永不刪、永不覆蓋）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366;fst=1" parent="p4P"><g x=15 y=796 w=240 h=90/></c>
<c id="f_user_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=798 w=30 h=20/></c>
<c id="f_user_f0" v="Dockerfile 等（copy）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_user"><g x=10 y=30 w=210 h=24/></c>
<c id="f_user_f1" v="根 .gitignore 幾行（append）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_user"><g x=10 y=58 w=210 h=24/></c>
<c id="f_just" v="根 justfile（使用者的，進 git）⏎import 一行；新檔另有 default 兩行" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4P"><g x=15 y=952 w=240 h=50/></c>
<c id="f_just_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=954 w=30 h=20/></c>
<c id="f_di" v="根 .dockerignore（使用者的）⏎三行（問後 append）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="p4P"><g x=15 y=1010 w=240 h=44/></c>
<c id="f_di_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=1012 w=30 h=20/></c>
<c id="f_shell" v="自有薄殼（進 git；首行自描述）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366;fst=1" parent="p4P"><g x=15 y=1062 w=240 h=146/></c>
<c id="f_shell_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=1064 w=30 h=20/></c>
<c id="f_shell_f0" v="entry.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_shell"><g x=10 y=30 w=210 h=24/></c>
<c id="f_shell_f1" v="vendor.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_shell"><g x=10 y=58 w=210 h=24/></c>
<c id="f_shell_f2" v=".gitignore" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_shell"><g x=10 y=86 w=210 h=24/></c>
<c id="f_shell_f3" v="ci/check.sh" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366" parent="f_shell"><g x=10 y=114 w=210 h=24/></c>
<c id="f_gen" v="gen/（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333;fst=1" parent="p4P"><g x=15 y=1216 w=240 h=90/></c>
<c id="f_gen_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1" parent="p4P"><g x=223 y=1218 w=30 h=20/></c>
<c id="f_gen_f0" v="tools.just（mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="f_gen"><g x=10 y=30 w=210 h=24/></c>
<c id="f_gen_f1" v=".stamp（只記引擎 ref）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333" parent="f_gen"><g x=10 y=58 w=210 h=24/></c>
<c id="w_ver" v="version.toml 內容" s="fs=12;exitX=1;exitY=0.125;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_ver" target="f_ver"></c>
<c id="w_vl" v="覆寫行（path:／⏎tag + image ID）" s="fs=12;exitX=1;exitY=0.4306;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_ver" target="f_vl"></c>
<c id="w_repo" v="展開的工具檔⏎（整批替換）" s="fs=12;exitX=1;exitY=0.3734;entryX=0;entryY=0.5" edge="1" source="m_mat" target="f_repo"></c>
<c id="w_stamp" v="index digest⏎+ 每檔 sha256" s="fs=12;exitX=1;exitY=0.8987;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_mat" target="f_stamp"></c>
<c id="w_bl" v="範本副本、metadata" s="fs=12;exitX=1;exitY=0.3947;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_bl" target="f_bl"></c>
<c id="w_user" v="初始檔內容⏎（現況／結果）" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.7444;startArrow=block;startFill=1" edge="1" source="grp_im" target="f_user"></c>
<c id="w_just" v="import 那一行" s="fs=12;exitX=1;exitY=0.0706;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_lg" target="f_just"></c>
<c id="w_di" v=".dockerignore⏎三行" s="fs=12;exitX=1;exitY=0.226;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_lg" target="f_di"></c>
<c id="w_shell" v="薄殼四檔內容⏎（首行／模板）" s="fs=12;exitX=1;exitY=0.5169;entryX=0;entryY=0.5;startArrow=block;startFill=1" edge="1" source="m_lg" target="f_shell"></c>
<c id="w_gen" v="tools.just、⏎.stamp 內容" s="fs=12;exitX=1;exitY=0.8729;entryX=0;entryY=0.5" edge="1" source="m_lg" target="f_gen"></c>
<c id="run_cli" v="動詞、參數、--protocol P →⏎← 結束碼、vk-resolve 清單" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.4952;startArrow=block;startFill=1" edge="1" source="h4" target="m_cli"><g x=-0.5/></c>
<c id="mount_dist" v="/dist/&lt;repo&gt;⏎（唯讀）" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.073" edge="1" source="tmp" target="p4E"><g x=-0.5/></c>
<c id="pull_eng" v="引擎 image⏎（覆寫時本機 image）" s="fs=12;exitX=0.5;exitY=1;entryX=0.5385;entryY=0" edge="1" source="g_eng" target="p4H"></c>
<c id="pull_dist" v="工具 image 的 /dist 層⏎→ .tmp.dist.&lt;id&gt;/" s="fs=12;exitX=0.2;exitY=1;entryX=0.8269;entryY=0" edge="1" source="g_dist" target="p4H"><g x=0.3 pts=700,314;470,314/></c>
<c id="q_reg" v="tag、index digest" s="fs=12;exitX=0.7411;exitY=0;entryX=0.83;entryY=1;startArrow=block;startFill=1" edge="1" source="p4E" target="g_dist"></c>
<c id="p4_lg0" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=14;fs=12"><g x=40 y=1696 w=170 h=40/></c>
<c id="p4_lg1" v="紅：引擎模組" s="fc=#f8cecc;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=230 y=1696 w=130 h=40/></c>
<c id="p4_lg2" v="白小框：最小單元" s="fc=#ffffff;sc=#666666;fs=10"><g x=380 y=1696 w=140 h=40/></c>
<c id="p4_lg3" v="紅底紅粗框：啟動器（主機側薄殼）" s="fc=#f8cecc;sc=#b85450;fs=14;fs=12"><g x=540 y=1696 w=240 h=40/></c>
<c id="p4_lg4" v="淺灰底：主機分組" s="fc=#f5f5f5;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=800 y=1696 w=150 h=40/></c>
<c id="p4_lg5" v="綠底：專案目錄分組" s="fc=#d5e8d4;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=970 y=1696 w=160 h=40/></c>
<c id="p4_lgt" v="實線 = 資料流（線上文字 = 傳什麼）⏎雙箭頭 = 讀寫／來回都有；黃橢圓 = 使用者；載入／執行順序與判斷見流程頁" s="text;fs=12;sc=none;fc=none"><g x=1150 y=1686 w=300 h=60/></c>
<c id="p4_lg6" v="淺橘底：規則／摘要（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=14;fs=12"><g x=40 y=1762 w=190 h=40/></c>
<c id="p4_lg7" v="綠框：進 git" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=250 y=1762 w=120 h=40/></c>
<c id="p4_lg8" v="灰虛線：不進 git（可重建）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12;dashed=1;sc=#999999;fco=#333333"><g x=390 y=1762 w=200 h=40/></c>
<c id="p4_lg9" v="黃底綠框：使用者的檔（進 git）" s="fc=#FFF4C3;sc=light-dark(#000000,#9577A3);fs=14;fs=12;sc=#82b366"><g x=610 y=1762 w=230 h=40/></c>
<c id="p4_lg10" v="等寬字：檔案內容範例" s="fc=#ffffff;sc=#999999;fs=12"><g x=860 y=1762 w=170 h=40/></c>
<c id="p4_lg11" v="右上角綠標籤：v2 改" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=1050 y=1762 w=200 h=40/></c>
<c id="p4_lg11_v2" v="v2" s="fc=#00b050;sc=#00b050;fco=#ffffff;fs=9;fst=1"><g x=1218 y=1764 w=30 h=20/></c>
<c id="p4_lg12" v="點線框：init／merge 共用箭頭" s="fc=none;sc=#666666;dashed=1;dashPattern=1 3;fs=12"><g x=40 y=1828 w=200 h=40/></c>
<c id="p4_lg13" v="白底黑框：主機上的目錄／命名空間（不是檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=14;fs=12"><g x=260 y=1828 w=300 h=40/></c>
<c id="p4_lg14" v="便條：說明（含「本頁無待拍板」）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=580 y=1828 w=220 h=40/></c>
<c id="p4_th" v="本頁名詞（只列本頁用到的）" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1884 w=300 h=28/></c>
<c id="p4_tk0" v="引擎" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1918 w=150 h=40/></c>
<c id="p4_tv0" v="vendor_kit 的程式本體：只以 image 存在（公開、多架構）、只在容器內跑；8 個模組見紫色容器；一個專案用 version.toml 正規行那一版（version.local.toml 可覆寫成本機 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1918 w=610 h=40/></c>
<c id="p4_tk1" v="啟動器" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1958 w=150 h=55/></c>
<c id="p4_tv1" v=".vendor_kit/vendor.just 裡的 POSIX sh 薄殼，在主機跑：grep version.toml、docker image inspect／pull／create／cp 抓工具檔、docker run 起引擎 resolve／apply；不算引擎模組；最小單元見紅粗框" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1958 w=610 h=55/></c>
<c id="p4_tk2" v="模組／最小單元" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2013 w=150 h=40/></c>
<c id="p4_tv2" v="模組 = 引擎裡一塊獨立責任的程式（紅框）；最小單元 = 模組裡可以單獨測的最小功能（白小框，一格一個）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2013 w=610 h=40/></c>
<c id="p4_tk3" v="cli" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2053 w=150 h=40/></c>
<c id="p4_tv3" v="引擎的入口模組：解析子命令與參數（含 --protocol P）、負責所有詢問（-y 免問；無 tty → 1）、決定結束碼 0／1／2／3，並呼叫其他模組" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2053 w=610 h=40/></c>
<c id="p4_tk4" v="version" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2093 w=150 h=40/></c>
<c id="p4_tv4" v="讀寫 version.toml／version.local.toml（schema 轉換）；apply 拿 flock；產生／重驗輸入指紋；寫 metadata [progress]；算 docker 資源 label（prune 用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2093 w=610 h=40/></c>
<c id="p4_tk5" v="registry" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2133 w=150 h=40/></c>
<c id="p4_tv5" v="查 GHCR 的 tag 與 index digest（update／add／upgrade 用；私有 registry 用 TOKEN／TOKEN_FILE；查詢有逾時）；sync 不查最新版，只拉鎖定版" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2133 w=610 h=40/></c>
<c id="p4_tk6" v="materialize" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2173 w=150 h=40/></c>
<c id="p4_tv6" v="引擎內部步驟（不對外）：把主機掛進來的 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/、寫印記 gen/&lt;repo&gt;.stamp、verify sha256；在 apply 決定套用之後才做" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2173 w=610 h=40/></c>
<c id="p4_tk7" v="init／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2213 w=150 h=40/></c>
<c id="p4_tv7" v="init 建初始檔、append 幾行或問「要建 X 嗎」；merge 在 upgrade 時對每個檔跑狀態機（D==B → 問後換、三者皆異 → 問後三方合併）+ git merge-file；兩者都把檔案清單與逐檔決定交給 baseline" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2213 w=610 h=40/></c>
<c id="p4_tk8" v="baseline（模組）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2253 w=150 h=40/></c>
<c id="p4_tv8" v="維護 baseline/&lt;repo&gt;/ 範本副本與 .vendor_kit.toml metadata（complete、五態、declined_hash、lines、conflicts、[progress]）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2253 w=610 h=40/></c>
<c id="p4_tk9" v="launcher-gen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1918 w=150 h=55/></c>
<c id="p4_tv9" v="產生 .vendor_kit/ 自有薄殼四檔（含自描述首行）、gen/tools.just（mod? 行）、gen/.stamp、根 justfile 那一行（新檔時四行）、根 .dockerignore 三行；薄殼與 gen/.stamp 只由 install／upgrade vendor_kit 重產（先比首行 hash）；tools.just 由 sync／add／remove／upgrade 重生" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1918 w=610 h=55/></c>
<c id="p4_tk10" v="多架構 index／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1973 w=150 h=40/></c>
<c id="p4_tv10" v="同一 tag 下 amd64 + arm64 兩份 manifest 的清單；docker 不帶 --platform 就挑原生；version.toml 與印記記清單的 digest（不記單平台 digest）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1973 w=610 h=40/></c>
<c id="p4_tk11" v="暫存目錄 &lt;tmp&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2013 w=150 h=40/></c>
<c id="p4_tv11" v="啟動器把工具 image 的 /dist 抓到專案內 .vendor_kit/.tmp.dist.&lt;id&gt;/，再唯讀掛進引擎當 /dist/&lt;repo&gt;（逐檔判斷讀這裡，不是 cache）；dev 時改掛 &lt;dir&gt;/dist；trap 清掉" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2013 w=610 h=40/></c>
<c id="p4_tk12" v="掛載（-v）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2053 w=150 h=40/></c>
<c id="p4_tv12" v="docker run -v：把主機目錄接進容器；/repo = 專案根（可寫，-w /repo）；/dist = 暫存工具檔（唯讀）；/dist/&lt;repo&gt; = dev 覆寫的 &lt;dir&gt;/dist（唯讀）；/run/vk-token = TOKEN_FILE（唯讀）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2053 w=610 h=40/></c>
<c id="p4_tk13" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2093 w=150 h=40/></c>
<c id="p4_tv13" v="動詞的兩段：resolve 只讀、算要拉哪些 image、輸出 vk-resolve/1 清單 + 指紋（不寫檔）→ 主機 docker 拉到暫存 → apply 拿鎖、重驗指紋、建進度日誌、寫檔、最後刪日誌；細節 p3b 契約④" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2093 w=610 h=40/></c>
<c id="p4_tk14" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2133 w=150 h=55/></c>
<c id="p4_tv14" v="CI 真值規則：環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen；check.sh 自己 export CI=1。frozen = 不寫任何 tracked 檔、不查最新版；仍拉鎖定版 image、仍寫 cache/、gen/；需要寫 tracked 檔 → 1 印清單，與 -y 無關（-y 不解除 frozen）；update 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2133 w=610 h=55/></c>
<c id="p4_tk15" v="CI／runner" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2188 w=150 h=40/></c>
<c id="p4_tv15" v="CI = GitHub／GitLab 上每次 push 自動跑的檢查（兩者都設環境變數 CI=true → 依真值規則進 frozen）；runner = 跑 CI 的機器（amd64、arm64 原生 runner = 兩種晶片各一台真機）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2188 w=610 h=40/></c>
<c id="p4_tk16" v="docker image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2228 w=150 h=55/></c>
<c id="p4_tv16" v="問本機 daemon「這個 image 在不在、ID 是什麼」的指令（docker 19.03 就有）；啟動器一律先 inspect：有 → 不 pull（離線可用）；無 → docker pull；本機覆寫時 ID 不符 → 1（不用 docker run 的 pull 旗標：19.03 沒有）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2228 w=610 h=55/></c>
</diagram>
<diagram id="v1p5" name="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install"><c id="title" v="流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install（§2／§3、v2.2 B／C、Q17／Q18、v2.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=108/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=128 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=128 w=460 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=760 y=128 w=260 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1040 y=128 w=180 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=128 w=360 h=28/></c>
<c id="bA" v="5a bootstrap.sh 前半：檢查 git／just → 決定引擎 ref（Q18：不退回內嵌）→ --local 三分支（檔案先驗存在；既是檔又是 tag → 1 + 6-37；v2.8 §4）→ inspect → 無才 pull → install（失敗即中止）；後半見「bootstrap.sh（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=172 w=1600 h=1478/></c>
<c id="bA_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=1556 y=5 w=30 h=20/></c>
<c id="a0" v="執行 bootstrap.sh -t &lt;repo&gt;[@&lt;tag&gt;]…" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bA"><g x=20 y=36 w=220 h=58/></c>
<c id="a2" v="1：請先 git init（不代做）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bA"><g x=20 y=126 w=220 h=58/></c>
<c id="a1" v="是 git repo？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=390 y=114 w=200 h=81/></c>
<c id="a4" v="1：印 just 下載＋安裝指令" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bA"><g x=20 y=226 w=220 h=58/></c>
<c id="a3" v="just ≥ 1.33.0？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=390 y=215 w=200 h=81/></c>
<c id="a1v" v="專案已有 version.toml？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=370 y=316 w=240 h=81/></c>
<c id="a1v_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=586 y=306 w=30 h=20/></c>
<c id="a1r" v="Q18（v2.4 §5）：舊 bootstrap.sh 在已裝過的 repo 再跑 → 用 version.toml 第一行的引擎跑 install（不降版、不用內嵌）；該引擎拉不到 → 1 失敗，不得退回內嵌；只有第一次接入才用內嵌 ref" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bA"><g x=1220 y=317 w=360 h=79/></c>
<c id="a1r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=1556 y=307 w=30 h=20/></c>
<c id="a1vy" v="是：引擎 ref = version.toml 第一行（拉不到 → 1，不退回內嵌）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=260 y=417 w=200 h=63/></c>
<c id="a1vy_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=436 y=407 w=30 h=20/></c>
<c id="a1vn" v="否：引擎 ref = 內嵌引擎 ref（第一次接入）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=520 y=424 w=200 h=48/></c>
<c id="a1vn_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=696 y=414 w=30 h=20/></c>
<c id="a5" v="--local？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=420 y=500 w=140 h=81/></c>
<c id="a8q" v="是：值含 / 或以 .tar 結尾？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=260 y=601 w=230 h=81/></c>
<c id="a8q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=591 w=30 h=20/></c>
<c id="a6i" v="否：docker image inspect &lt;引擎 ref&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=520 y=618 w=200 h=48/></c>
<c id="a6i_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=696 y=608 w=30 h=20/></c>
<c id="a8ex" v="否 → 1：--local 指定的檔案不存在（請檢查路徑）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bA"><g x=20 y=702 w=220 h=80/></c>
<c id="a8ex_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=216 y=692 w=30 h=20/></c>
<c id="a8e" v="是：該檔案存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=260 y=717 w=230 h=50/></c>
<c id="a8e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=707 w=30 h=20/></c>
<c id="a6q" v="本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=540 y=717 w=160 h=50/></c>
<c id="a6q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=676 y=707 w=30 h=20/></c>
<c id="a8tx" v="是 → 1：印 6-37（值既是既存檔案也可解讀為本機 image tag，請消歧）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bA"><g x=20 y=802 w=220 h=102/></c>
<c id="a8tx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=216 y=792 w=30 h=20/></c>
<c id="a8t" v="是：本機也有同名 image tag？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=260 y=812 w=230 h=81/></c>
<c id="a8t_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=802 w=30 h=20/></c>
<c id="a6p" v="無：docker pull &lt;引擎 ref&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=550 y=829 w=170 h=48/></c>
<c id="a6p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=696 y=819 w=30 h=20/></c>
<c id="a7" v="ghcr.io/…/vendor_kit:vN⏎（引擎 image；多架構 amd64+arm64）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bA"><g x=1019 y=824 w=182 h=57/></c>
<c id="a8l" v="否：docker load &lt;tar&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=260 y=924 w=230 h=40/></c>
<c id="a8l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=914 w=30 h=20/></c>
<c id="a8i" v="docker image inspect 取 image ID（否：值 = 本機 image tag）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=260 y=984 w=230 h=48/></c>
<c id="a8i_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=974 w=30 h=20/></c>
<c id="a8d" v="讀同名 .digest 旁檔 = 正式 index digest（旁檔缺 → 1）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=260 y=1052 w=230 h=48/></c>
<c id="a8d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=466 y=1042 w=30 h=20/></c>
<c id="a9" v="docker run &lt;引擎&gt; install（-y 轉發；本機 image 直接 run）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA"><g x=340 y=1190 w=300 h=48/></c>
<c id="a9_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=616 y=1180 w=30 h=20/></c>
<c id="a9e" v="install（見「install（1）（2）」頁）：建／重寫 .vendor_kit/ 薄殼、根 justfile、根 .dockerignore" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bA"><g x=740 y=1186 w=260 h=57/></c>
<c id="a9f" v="install 寫（見「install（1）（2）」頁）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bA"><g x=1220 y=1120 w=360 h=189/></c>
<c id="a9f_0" v=".vendor_kit/ 薄殼四檔（首行自描述）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=8 y=26 w=169 h=42/></c>
<c id="a9f_1" v="version.toml 第一行（引擎 ref）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=183 y=26 w=169 h=42/></c>
<c id="a9f_2" v="gen/.stamp（引擎 ref）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=8 y=74 w=169 h=26/></c>
<c id="a9f_3" v="baseline/.gitkeep" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=183 y=74 w=169 h=26/></c>
<c id="a9f_4" v="根 justfile（無 → import 行 + default recipe；有 → 加 import 一行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=8 y=106 w=169 h=73/></c>
<c id="a9f_5" v="根 .dockerignore 三行（有 → 問後加）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a9f"><g x=183 y=106 w=169 h=73/></c>
<c id="a9x" v="是 → 1：中止（第一次不留半成品；--local 檔未寫）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bA"><g x=20 y=1330 w=220 h=80/></c>
<c id="a9x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA"><g x=216 y=1320 w=30 h=20/></c>
<c id="a9q" v="install 失敗？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA"><g x=390 y=1329 w=200 h=81/></c>
<c id="a9z" v="否 ↓ 續「bootstrap.sh（2）」頁：--local 記錄 → 對每個 -t 呼叫 add → 彙總" s="text;fs=12;sc=none;fc=none;fst=1" parent="bA"><g x=260 y=1430 w=460 h=42/></c>
<c id="ae1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a0" target="a1"><g x=0.00 pts=150,276;510,276/></c>
<c id="ae2" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a1" target="a2"></c>
<c id="ae3" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1" target="a3"><g x=-0.6/></c>
<c id="ae4" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a3" target="a4"></c>
<c id="ae5" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a3" target="a1v"><g x=-0.6/></c>
<c id="ae5y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1v" target="a1vy"><g x=0.00 pts=510,579;380,579/></c>
<c id="ae5n" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1v" target="a1vn"><g x=-0.05 pts=510,579;640,579/></c>
<c id="ae5a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1vy" target="a5"><g x=0.00 pts=380,662;510,662/></c>
<c id="ae5b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1vn" target="a5"><g x=0.05 pts=640,662;510,662/></c>
<c id="ae6" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a5" target="a8q"><g x=0.00 pts=510,763;395,763/></c>
<c id="ae7" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a5" target="a6i"><g x=-0.10 pts=510,763;640,763/></c>
<c id="ae8" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8q" target="a8e"><g x=-0.6/></c>
<c id="ae8n" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0.8;entryY=0" edge="1" source="a8q" target="a8i"><g x=-0.86 pts=525,814;525,1146;464,1146/></c>
<c id="ae8e" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a8e" target="a8ex"></c>
<c id="ae8ey" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8e" target="a8t"><g x=-0.6/></c>
<c id="ae8t" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a8t" target="a8tx"></c>
<c id="ae8tn" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8t" target="a8l"><g x=-0.6/></c>
<c id="ae9" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8l" target="a8i"></c>
<c id="ae9d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8i" target="a8d"></c>
<c id="ae6q" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a6i" target="a6q"></c>
<c id="ae6p" v="無" s="fs=12;exitX=0.5;exitY=1;entryX=0.412;entryY=0" edge="1" source="a6q" target="a6p"><g x=-0.6/></c>
<c id="ae10" v="拉" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a7" target="a6p"></c>
<c id="ae6y" v="有" s="fs=12;exitX=0;exitY=0.5;entryX=0.617;entryY=0" edge="1" source="a6q" target="a9"><g x=-0.87 pts=545,914/></c>
<c id="ae11" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8d" target="a9"><g x=-0.34 pts=395,1282;510,1282/></c>
<c id="ae11b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a6p" target="a9"><g x=0.33 pts=655,1282;510,1282/></c>
<c id="ae12" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a9" target="a9e"></c>
<c id="ae12f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a9e" target="a9f"></c>
<c id="ae13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a9" target="a9q"></c>
<c id="ae14" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a9q" target="a9x"></c>
<c id="ae15" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a9q" target="a9z"><g x=-0.6/></c>
<c id="p5_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1666 w=200 h=60/></c>
<c id="p5_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1666 w=140 h=64/></c>
<c id="p5_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1674 w=140 h=44/></c>
<c id="p5_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1668 w=190 h=56/></c>
<c id="p5_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1668 w=210 h=56/></c>
<c id="p5_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1676 w=88 h=40/></c>
<c id="p5_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1676 w=170 h=40/></c>
<c id="p5_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1666 w=300 h=60/></c>
<c id="p5_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1734 w=120 h=36/></c>
<c id="p5_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1734 w=150 h=36/></c>
<c id="p5_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1734 w=190 h=36/></c>
<c id="p5_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1734 w=170 h=36/></c>
<c id="p5_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1734 w=170 h=36/></c>
<c id="p5_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1734 w=200 h=36/></c>
<c id="p5_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1724 w=30 h=20/></c>
<c id="p5_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1772 w=200 h=28/></c>
<c id="p5_tk0" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1806 w=150 h=71/></c>
<c id="p5_tv0" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 呼叫 add；再跑 = install" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1806 w=610 h=71/></c>
<c id="p5_tk1" v="release／tar／.digest／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1877 w=150 h=55/></c>
<c id="p5_tv1" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1877 w=610 h=55/></c>
<c id="p5_tk2" v="--local &lt;image tag 或 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1932 w=150 h=55/></c>
<c id="p5_tv2" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；version.toml 仍寫正式 ref（digest 由 .digest 取得），version.local.toml 記 tag + image ID" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1932 w=610 h=55/></c>
<c id="p5_tk3" v="GHCR／image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1987 w=150 h=40/></c>
<c id="p5_tv3" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1987 w=610 h=40/></c>
<c id="p5_tk4" v="docker image inspect／image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2027 w=150 h=71/></c>
<c id="p5_tv4" v="啟動器每次 docker run 前先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2027 w=610 h=71/></c>
<c id="p5_tk5" v="install／uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2098 w=150 h=55/></c>
<c id="p5_tv5" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2098 w=610 h=55/></c>
<c id="p5_tk6" v="冪等" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2153 w=150 h=40/></c>
<c id="p5_tv6" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2153 w=610 h=40/></c>
<c id="p5_tk7" v="薄殼 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2193 w=150 h=55/></c>
<c id="p5_tv7" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2193 w=610 h=55/></c>
<c id="p5_tk8" v="薄殼首行自描述（Q17）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2248 w=150 h=55/></c>
<c id="p5_tv8" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 LF 正規化 hash&gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2248 w=610 h=55/></c>
<c id="p5_tk9" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1806 w=150 h=40/></c>
<c id="p5_tv9" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1806 w=610 h=40/></c>
<c id="p5_tk10" v="暫存目錄／原子替換" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1846 w=150 h=40/></c>
<c id="p5_tv10" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1846 w=610 h=40/></c>
<c id="p5_tk11" v="version.toml／version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1886 w=150 h=55/></c>
<c id="p5_tv11" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&lt;dir&gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1886 w=610 h=55/></c>
<c id="p5_tk12" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1941 w=150 h=40/></c>
<c id="p5_tv12" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1941 w=610 h=40/></c>
<c id="p5_tk13" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1981 w=150 h=55/></c>
<c id="p5_tv13" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1981 w=610 h=55/></c>
<c id="p5_tk14" v="just／recipe／import／default" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2036 w=150 h=55/></c>
<c id="p5_tv14" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2036 w=610 h=55/></c>
<c id="p5_tk15" v="docker pull／run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2091 w=150 h=40/></c>
<c id="p5_tv15" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2091 w=610 h=40/></c>
<c id="p5_tk16" v="flock／-y" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2131 w=150 h=40/></c>
<c id="p5_tv16" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2131 w=610 h=40/></c>
<c id="p5_tk17" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2171 w=150 h=55/></c>
<c id="p5_tv17" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2171 w=610 h=55/></c>
</diagram>
<diagram id="v1p5ccc" name="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add"><c id="title" v="流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add → 彙總（§2、v2.2 C、v2.5 §8、v2.6 Q26／Q27）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=108/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=128 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=128 w=460 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=760 y=128 w=260 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1040 y=128 w=180 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=128 w=360 h=28/></c>
<c id="bA2" v="5a′ bootstrap.sh 後半（承「bootstrap.sh（1）」頁：install 成功）：--local → 寫 version.local.toml → 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 呼叫 add（resolve → docker → apply；一個失敗即中止）→ 彙總結束碼；不自刪" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=172 w=1600 h=941/></c>
<c id="bA2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=1556 y=5 w=30 h=20/></c>
<c id="a9e2" v="來自「bootstrap.sh（1）」頁：install 成功（薄殼、version.toml、gen/.stamp 已寫）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bA2"><g x=340 y=36 w=300 h=102/></c>
<c id="a8q2" v="--local？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA2"><g x=410 y=158 w=160 h=50/></c>
<c id="a8q2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=546 y=148 w=30 h=20/></c>
<c id="a8b" v="是：寫 version.local.toml：vendor_kit = &quot;&lt;tag&gt;&quot;＋vendor_kit_image_id（install 成功後才寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA2"><g x=520 y=228 w=200 h=79/></c>
<c id="a8b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=696 y=218 w=30 h=20/></c>
<c id="a8f" v="＋version.local.toml（不進 git；引擎覆寫：image tag + image ID；離線包 Q26）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bA2"><g x=1220 y=246 w=360 h=42/></c>
<c id="a10" v="呼叫 add &lt;repo&gt;[@&lt;tag&gt;]（-y 轉發）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA2"><g x=340 y=336 w=300 h=40/></c>
<c id="a10l" v="← 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 重複；一個失敗即中止" s="text;fs=12;sc=none;fc=none;fst=1" parent="bA2"><g x=1020 y=327 w=180 h=57/></c>
<c id="a10r" v="docker run &lt;引擎&gt; resolve add &lt;repo&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA2"><g x=340 y=405 w=300 h=40/></c>
<c id="a10r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=616 y=395 w=30 h=20/></c>
<c id="a10re" v="resolve add（不寫任何檔；見「add（1）」頁）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bA2"><g x=740 y=404 w=260 h=42/></c>
<c id="a10d" v="啟動器 docker 段：拉工具 image、展開 /dist 到暫存（步驟見「add（1）」頁）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA2"><g x=340 y=466 w=300 h=48/></c>
<c id="a10d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=616 y=456 w=30 h=20/></c>
<c id="a10g" v="&lt;repo&gt;-dist@digest⏎（工具 image）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bA2"><g x=1020 y=469 w=180 h=42/></c>
<c id="a10a" v="docker run &lt;引擎&gt; apply add &lt;repo&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bA2"><g x=340 y=625 w=300 h=40/></c>
<c id="a10a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=616 y=615 w=30 h=20/></c>
<c id="a10ae" v="apply add（拿鎖、重驗、建日誌後寫入；見「add（2）」頁）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bA2"><g x=740 y=624 w=260 h=42/></c>
<c id="a10f" v="add 寫（每個工具；見「add（2）」頁）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bA2"><g x=1220 y=534 w=360 h=222/></c>
<c id="a10f_0" v="version.toml [tools] 行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=26 w=344 h=26/></c>
<c id="a10f_1" v="cache/&lt;repo&gt;/" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=58 w=344 h=26/></c>
<c id="a10f_2" v="gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=90 w=344 h=26/></c>
<c id="a10f_3" v="初始檔（init.toml 的 dest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=122 w=344 h=26/></c>
<c id="a10f_4" v="baseline/&lt;repo&gt;/ + .vendor_kit.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=154 w=344 h=26/></c>
<c id="a10f_5" v="gen/tools.just（重生，mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="a10f"><g x=8 y=186 w=344 h=26/></c>
<c id="a12" v="是 → 1：明列已完成／未完成（多工具彙總：1 &gt; 2 &gt; 0）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bA2"><g x=20 y=776 w=220 h=80/></c>
<c id="a12_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bA2"><g x=216 y=766 w=30 h=20/></c>
<c id="a11" v="任一 add 失敗？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bA2"><g x=390 y=776 w=200 h=81/></c>
<c id="a13" v="0：印摘要與要 git add 的清單" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bA2"><g x=20 y=877 w=220 h=58/></c>
<c id="ae16" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a9e2" target="a8q2"></c>
<c id="ae17" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8q2" target="a8b"><g x=0.00 pts=510,390;640,390/></c>
<c id="ae17f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a8b" target="a8f"></c>
<c id="ae17n" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.067;entryY=0" edge="1" source="a8q2" target="a10"><g x=-0.37 pts=380,355/></c>
<c id="ae18" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a8b" target="a10"><g x=-0.05 pts=640,489;510,489/></c>
<c id="ae19" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a10" target="a10r"></c>
<c id="ae19e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a10r" target="a10re"></c>
<c id="ae20" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a10r" target="a10d"></c>
<c id="ae20g" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a10g" target="a10d"></c>
<c id="ae21" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a10d" target="a10a"></c>
<c id="ae21e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a10a" target="a10ae"></c>
<c id="ae21f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a10ae" target="a10f"></c>
<c id="ae22" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a10a" target="a11"></c>
<c id="ae23" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a11" target="a12"></c>
<c id="ae24" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="a11" target="a13"><g x=-0.84 pts=510,1078/></c>
<c id="p5d_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1129 w=200 h=60/></c>
<c id="p5d_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1129 w=140 h=64/></c>
<c id="p5d_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1137 w=140 h=44/></c>
<c id="p5d_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1131 w=190 h=56/></c>
<c id="p5d_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1131 w=210 h=56/></c>
<c id="p5d_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1139 w=88 h=40/></c>
<c id="p5d_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1139 w=170 h=40/></c>
<c id="p5d_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1129 w=300 h=60/></c>
<c id="p5d_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1197 w=200 h=36/></c>
<c id="p5d_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1197 w=120 h=36/></c>
<c id="p5d_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1197 w=190 h=36/></c>
<c id="p5d_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1197 w=170 h=36/></c>
<c id="p5d_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1197 w=170 h=36/></c>
<c id="p5d_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1197 w=200 h=36/></c>
<c id="p5d_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1187 w=30 h=20/></c>
<c id="p5d_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1235 w=200 h=28/></c>
<c id="p5d_tk0" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1269 w=150 h=71/></c>
<c id="p5d_tv0" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 呼叫 add；再跑 = install" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1269 w=610 h=71/></c>
<c id="p5d_tk1" v="release／tar／.digest／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1340 w=150 h=55/></c>
<c id="p5d_tv1" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1340 w=610 h=55/></c>
<c id="p5d_tk2" v="--local &lt;image tag 或 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1395 w=150 h=55/></c>
<c id="p5d_tv2" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；version.toml 仍寫正式 ref（digest 由 .digest 取得），version.local.toml 記 tag + image ID" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1395 w=610 h=55/></c>
<c id="p5d_tk3" v="GHCR／image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1450 w=150 h=40/></c>
<c id="p5d_tv3" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1450 w=610 h=40/></c>
<c id="p5d_tk4" v="docker image inspect／image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1490 w=150 h=71/></c>
<c id="p5d_tv4" v="啟動器每次 docker run 前先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1490 w=610 h=71/></c>
<c id="p5d_tk5" v="install／uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1561 w=150 h=55/></c>
<c id="p5d_tv5" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1561 w=610 h=55/></c>
<c id="p5d_tk6" v="冪等" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1616 w=150 h=40/></c>
<c id="p5d_tv6" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1616 w=610 h=40/></c>
<c id="p5d_tk7" v="薄殼 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1656 w=150 h=55/></c>
<c id="p5d_tv7" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1656 w=610 h=55/></c>
<c id="p5d_tk8" v="薄殼首行自描述（Q17）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1711 w=150 h=55/></c>
<c id="p5d_tv8" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 LF 正規化 hash&gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1711 w=610 h=55/></c>
<c id="p5d_tk9" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1269 w=150 h=40/></c>
<c id="p5d_tv9" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1269 w=610 h=40/></c>
<c id="p5d_tk10" v="暫存目錄／原子替換" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1309 w=150 h=40/></c>
<c id="p5d_tv10" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1309 w=610 h=40/></c>
<c id="p5d_tk11" v="version.toml／version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1349 w=150 h=55/></c>
<c id="p5d_tv11" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&lt;dir&gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1349 w=610 h=55/></c>
<c id="p5d_tk12" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1404 w=150 h=40/></c>
<c id="p5d_tv12" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1404 w=610 h=40/></c>
<c id="p5d_tk13" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1444 w=150 h=55/></c>
<c id="p5d_tv13" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1444 w=610 h=55/></c>
<c id="p5d_tk14" v="just／recipe／import／default" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1499 w=150 h=55/></c>
<c id="p5d_tv14" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1499 w=610 h=55/></c>
<c id="p5d_tk15" v="docker pull／run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1554 w=150 h=40/></c>
<c id="p5d_tv15" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1554 w=610 h=40/></c>
<c id="p5d_tk16" v="flock／-y" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1594 w=150 h=40/></c>
<c id="p5d_tv16" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1594 w=610 h=40/></c>
<c id="p5d_tk17" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1634 w=150 h=55/></c>
<c id="p5d_tv17" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1634 w=610 h=55/></c>
</diagram>
<diagram id="v1p5c" name="流程 v2：install（1）薄殼"><c id="title" v="流程 v2：install ── 專案層動詞（§2／§3、v2.2 A／C、v2.4 Q17／Q20、v2.5 §8、v2.6 §4／§11／Q22 補）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=108/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=128 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=128 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=128 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=128 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=128 w=360 h=28/></c>
<c id="bI" v="5a′ install：專案層動詞（bootstrap.sh 代打，也可自己打）；再跑 = 引擎重寫薄殼（先比對首行自描述 hash）= 冪等修復；第一次不建日誌、修復型建 .tmp.install.&lt;id&gt;.toml（v2.8 §2）；禁止巢狀（Q20）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=172 w=1600 h=1466/></c>
<c id="bI_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=1556 y=5 w=30 h=20/></c>
<c id="i0" v="just vendor_kit install（-y、--no-justfile）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bI"><g x=20 y=36 w=220 h=80/></c>
<c id="i1" v="docker run &lt;引擎&gt; install …⏎（啟動器不鎖；鎖在引擎）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI"><g x=260 y=55 w=280 h=42/></c>
<c id="i3" v="1：請先 git init（不代做）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bI"><g x=20 y=136 w=220 h=58/></c>
<c id="i2" v="是 git repo？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI"><g x=560 y=140 w=220 h=50/></c>
<c id="i2x" v="是 → 1：&lt;dir&gt; 已有 .vendor_kit/，不允許巢狀；請到該目錄執行或先 uninstall" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bI"><g x=20 y=219 w=220 h=102/></c>
<c id="i2x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=216 y=209 w=30 h=20/></c>
<c id="i2n" v="上層或下層已有 .vendor_kit/？（禁止巢狀，Q20）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI"><g x=560 y=214 w=300 h=112/></c>
<c id="i2n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=836 y=204 w=30 h=20/></c>
<c id="i4a" v="否：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=346 w=400 h=40/></c>
<c id="i4a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=336 w=30 h=20/></c>
<c id="i4" v="產 .gitignore 到暫存（首行自描述）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=438 w=400 h=40/></c>
<c id="i4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=428 w=30 h=20/></c>
<c id="i4n" v="第一次 install（薄殼不存在）：不建進度日誌，任一步失敗 → 丟棄暫存、移除已寫到正式位置的檔，專案不留任何檔 → 1（「不留半成品」只對第一次成立，v2.2 C）；修復型 install：建 .vendor_kit/.tmp.install.&lt;id&gt;.toml 進度日誌（第一個寫入前），失敗 → 1 列已完成／未完成，收尾（install（2））後刪（v2.8 §2）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bI"><g x=1220 y=406 w=360 h=104/></c>
<c id="i4_2" v="產 entry.just 到暫存（首行自描述）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=530 w=400 h=40/></c>
<c id="i4_2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=520 w=30 h=20/></c>
<c id="i4_3" v="產 vendor.just 到暫存（首行自描述）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=590 w=400 h=40/></c>
<c id="i4_3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=580 w=30 h=20/></c>
<c id="i4_4" v="產 ci/check.sh 到暫存（自描述在第二行）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=650 w=400 h=40/></c>
<c id="i4_4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=640 w=30 h=20/></c>
<c id="i4e" v="薄殼已存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI"><g x=560 y=710 w=240 h=50/></c>
<c id="i4e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=776 y=700 w=30 h=20/></c>
<c id="i4en" v="否：第一次 = 全新建" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI"><g x=830 y=711 w=130 h=48/></c>
<c id="i4en_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=701 w=30 h=20/></c>
<c id="i4x" v="否 → 1：被改過，列差異不動（git checkout 還原後再跑）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bI"><g x=20 y=796 w=220 h=80/></c>
<c id="i4x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=216 y=786 w=30 h=20/></c>
<c id="i4q" v="薄殼 == 上次產物？（首行自描述 hash）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI"><g x=560 y=780 w=240 h=112/></c>
<c id="i4q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=776 y=770 w=30 h=20/></c>
<c id="i4qn" v="自描述（Q17）：薄殼每檔首行 # vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 LF 正規化 hash&gt;；引擎重算 + 對 image 內模板二次比對；不用 gen/.stamp（不進 git，重新 clone 後也不存在）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bI"><g x=1220 y=796 w=360 h=79/></c>
<c id="i4qn_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=1556 y=786 w=30 h=20/></c>
<c id="i4ld" v="第一次 install（薄殼原本不存在）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI"><g x=560 y=912 w=240 h=112/></c>
<c id="i4ld_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=776 y=902 w=30 h=20/></c>
<c id="i4l" v="否（修復型）：建進度日誌 .tmp.install.&lt;id&gt;.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI"><g x=785 y=944 w=175 h=48/></c>
<c id="i4l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=934 w=30 h=20/></c>
<c id="i4lf" v="＋.vendor_kit/.tmp.install.&lt;id&gt;.toml（進度日誌，不進 git；修復型才有，收尾後刪；第一次 install 不建，失敗整包丟棄）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI"><g x=1220 y=936 w=360 h=63/></c>
<c id="i4lf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=1556 y=926 w=30 h=20/></c>
<c id="i4b" v="是：薄殼四檔逐檔原子替換（暫存 → 正式位置）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=1103 w=400 h=40/></c>
<c id="i4b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=1093 w=30 h=20/></c>
<c id="i4f" v="＋薄殼四檔（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bI"><g x=1220 y=1044 w=360 h=158/></c>
<c id="i4f_0" v=".vendor_kit/.gitignore" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="i4f"><g x=8 y=26 w=344 h=26/></c>
<c id="i4f_1" v=".vendor_kit/entry.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="i4f"><g x=8 y=58 w=344 h=26/></c>
<c id="i4f_2" v=".vendor_kit/vendor.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="i4f"><g x=8 y=90 w=344 h=26/></c>
<c id="i4f_3" v=".vendor_kit/ci/check.sh" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="i4f"><g x=8 y=122 w=344 h=26/></c>
<c id="i4c" v="寫 version.toml：第一行 = 引擎 ref（＋schema、written_by；已有則不動）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=1222 w=400 h=48/></c>
<c id="i4c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=1212 w=30 h=20/></c>
<c id="i4cf" v="＋version.toml（第一行引擎 ref、schema、written_by；進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI"><g x=1220 y=1225 w=360 h=42/></c>
<c id="i4d" v="寫 gen/.stamp（只記引擎 ref）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=1290 w=400 h=40/></c>
<c id="i4d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=1280 w=30 h=20/></c>
<c id="i4df" v="＋gen/.stamp（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI"><g x=1220 y=1290 w=360 h=40/></c>
<c id="i4g" v="建 baseline/.gitkeep（git 不追蹤空目錄；metadata 到 add 才建）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI"><g x=560 y=1350 w=400 h=48/></c>
<c id="i4g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI"><g x=936 y=1340 w=30 h=20/></c>
<c id="i4gf" v="＋baseline/.gitkeep（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI"><g x=1220 y=1354 w=360 h=40/></c>
<c id="i5z" v="↓ 續「install（2）」頁：根 justfile 與根 .dockerignore" s="text;fs=12;sc=none;fc=none;fst=1" parent="bI"><g x=560 y=1418 w=300 h=42/></c>
<c id="ie1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i0" target="i1"></c>
<c id="ie2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i1" target="i2"><g x=0.05 pts=420,298;690,298/></c>
<c id="ie3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="i2" target="i3"></c>
<c id="ie2n" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i2" target="i2n"><g x=0.06 pts=690,376;730,376/></c>
<c id="ie2x" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="i2n" target="i2x"></c>
<c id="ie4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.375;entryY=0" edge="1" source="i2n" target="i4a"><g x=-0.6/></c>
<c id="ie4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4a" target="i4"></c>
<c id="ie4c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4" target="i4_2"></c>
<c id="ie4d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4_2" target="i4_3"></c>
<c id="ie4e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4_3" target="i4_4"></c>
<c id="ie5" s="fs=12;exitX=0.3;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4_4" target="i4e"></c>
<c id="ie5n" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4e" target="i4en"></c>
<c id="ie5y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4e" target="i4q"><g x=-0.6/></c>
<c id="ie5x" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="i4q" target="i4x"></c>
<c id="ie6" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4q" target="i4ld"><g x=-0.6/></c>
<c id="ie6n" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4en" target="i4ld"><g x=0.36 pts=915,1074;700,1074/></c>
<c id="ie6l" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4ld" target="i4l"></c>
<c id="ie6lf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4l" target="i4lf"></c>
<c id="ie6ly" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="i4ld" target="i4b"><g x=-0.6/></c>
<c id="ie6ln" s="fs=12;exitX=0.5;exitY=1;entryX=0.781;entryY=0" edge="1" source="i4l" target="i4b"></c>
<c id="ie6f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4b" target="i4f"></c>
<c id="ie6c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4b" target="i4c"></c>
<c id="ie6cf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4c" target="i4cf"></c>
<c id="ie6d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4c" target="i4d"></c>
<c id="ie6df" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4d" target="i4df"></c>
<c id="ie6g" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i4d" target="i4g"></c>
<c id="ie6gf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i4g" target="i4gf"></c>
<c id="ie7" s="fs=12;exitX=0.5;exitY=1;entryX=0.667;entryY=0" edge="1" source="i4g" target="i5z"></c>
<c id="p5c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1654 w=200 h=60/></c>
<c id="p5c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1654 w=140 h=64/></c>
<c id="p5c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1662 w=140 h=44/></c>
<c id="p5c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1656 w=190 h=56/></c>
<c id="p5c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1656 w=210 h=56/></c>
<c id="p5c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1664 w=88 h=40/></c>
<c id="p5c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1664 w=170 h=40/></c>
<c id="p5c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1654 w=300 h=60/></c>
<c id="p5c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1722 w=120 h=36/></c>
<c id="p5c_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1722 w=190 h=36/></c>
<c id="p5c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1722 w=170 h=36/></c>
<c id="p5c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1722 w=170 h=36/></c>
<c id="p5c_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1722 w=200 h=36/></c>
<c id="p5c_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1712 w=30 h=20/></c>
<c id="p5c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1760 w=200 h=28/></c>
<c id="p5c_tk0" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1794 w=150 h=71/></c>
<c id="p5c_tv0" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 呼叫 add；再跑 = install" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1794 w=610 h=71/></c>
<c id="p5c_tk1" v="release／tar／.digest／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1865 w=150 h=55/></c>
<c id="p5c_tv1" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1865 w=610 h=55/></c>
<c id="p5c_tk2" v="--local &lt;image tag 或 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1920 w=150 h=55/></c>
<c id="p5c_tv2" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；version.toml 仍寫正式 ref（digest 由 .digest 取得），version.local.toml 記 tag + image ID" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1920 w=610 h=55/></c>
<c id="p5c_tk3" v="GHCR／image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1975 w=150 h=40/></c>
<c id="p5c_tv3" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1975 w=610 h=40/></c>
<c id="p5c_tk4" v="docker image inspect／image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2015 w=150 h=71/></c>
<c id="p5c_tv4" v="啟動器每次 docker run 前先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2015 w=610 h=71/></c>
<c id="p5c_tk5" v="install／uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2086 w=150 h=55/></c>
<c id="p5c_tv5" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2086 w=610 h=55/></c>
<c id="p5c_tk6" v="冪等" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2141 w=150 h=40/></c>
<c id="p5c_tv6" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2141 w=610 h=40/></c>
<c id="p5c_tk7" v="薄殼 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2181 w=150 h=55/></c>
<c id="p5c_tv7" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2181 w=610 h=55/></c>
<c id="p5c_tk8" v="薄殼首行自描述（Q17）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2236 w=150 h=55/></c>
<c id="p5c_tv8" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 LF 正規化 hash&gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2236 w=610 h=55/></c>
<c id="p5c_tk9" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1794 w=150 h=40/></c>
<c id="p5c_tv9" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1794 w=610 h=40/></c>
<c id="p5c_tk10" v="暫存目錄／原子替換" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1834 w=150 h=40/></c>
<c id="p5c_tv10" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1834 w=610 h=40/></c>
<c id="p5c_tk11" v="version.toml／version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1874 w=150 h=55/></c>
<c id="p5c_tv11" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&lt;dir&gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1874 w=610 h=55/></c>
<c id="p5c_tk12" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1929 w=150 h=40/></c>
<c id="p5c_tv12" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1929 w=610 h=40/></c>
<c id="p5c_tk13" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1969 w=150 h=55/></c>
<c id="p5c_tv13" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1969 w=610 h=55/></c>
<c id="p5c_tk14" v="just／recipe／import／default" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2024 w=150 h=55/></c>
<c id="p5c_tv14" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2024 w=610 h=55/></c>
<c id="p5c_tk15" v="docker pull／run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2079 w=150 h=40/></c>
<c id="p5c_tv15" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2079 w=610 h=40/></c>
<c id="p5c_tk16" v="flock／-y" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2119 w=150 h=40/></c>
<c id="p5c_tv16" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2119 w=610 h=40/></c>
<c id="p5c_tk17" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2159 w=150 h=55/></c>
<c id="p5c_tv17" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2159 w=610 h=55/></c>
</diagram>
<diagram id="v1p5cc" name="流程 v2：install（2）根 justfile 與 .dockerignore"><c id="title" v="流程 v2：install（2）根 justfile 與根 .dockerignore（§2、v2.6 §4、v2.7 §9、Q22 補）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.4 Q17／Q18、v2.5 §8、v2.6）：install 第一次／修復判定用薄殼首行自描述，不用 gen/.stamp（只記引擎 ref）；專案已有 version.toml → bootstrap.sh 用該行引擎、拉不到即失敗、不得退回內嵌；--local 的 version.local.toml 在 install 成功後才寫、失敗不留；install 建 baseline/.gitkeep、不建 metadata（add 時才建）；引擎 image 一律先 docker image inspect，本機有就不 pull（不用 --pull never）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=108/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=128 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=128 w=140 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=440 y=128 w=560 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1020 y=128 w=200 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=128 w=360 h=28/></c>
<c id="bI2" v="5a″ install 收尾（承「install（1）」頁：薄殼、version.toml、gen/.stamp、baseline/.gitkeep 已寫）：根 justfile（無 → 新建 import 行 + default recipe；有 → 問後加一行）→ 根 .dockerignore（無 → 建三行；有 → 問後 append）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=172 w=1600 h=1270/></c>
<c id="bI2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=5 w=30 h=20/></c>
<c id="i5e" v="來自「install（1）」頁：薄殼與 .vendor_kit/ 各檔已寫" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bI2"><g x=420 y=70 w=300 h=58/></c>
<c id="i5" v="--no-justfile？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=148 w=300 h=50/></c>
<c id="i5_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=696 y=138 w=30 h=20/></c>
<c id="i6" v="否 → 有根 justfile？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=224 w=300 h=81/></c>
<c id="i7" v="無：建 justfile（四行，逐字見右）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI2"><g x=860 y=236 w=120 h=57/></c>
<c id="i7f" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋justfile（新建，逐字四行；recipe 本體以 tab 縮排）⏎import &#x27;.vendor_kit/entry.just&#x27;⏎⏎default:⏎&#9;@just --list&lt;/pre&gt;" s="fc=#ffffff;sc=#666666;dashed=1;fs=12" parent="bI2"><g x=1220 y=218 w=360 h=94/></c>
<c id="i7f_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=208 w=30 h=20/></c>
<c id="i8" v="有 → 已含 import 那行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=332 w=300 h=81/></c>
<c id="i8_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=696 y=322 w=30 h=20/></c>
<c id="i12" v="否 → 問「要在 justfile 加這一行嗎」同意？（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=433 w=300 h=112/></c>
<c id="i11" v="是：append 那一行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI2"><g x=860 y=468 w=120 h=42/></c>
<c id="i11f" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;justfile（尾端＋一行）：⏎import &#x27;.vendor_kit/entry.just&#x27;&lt;/pre&gt;" s="fc=#ffffff;sc=#666666;dashed=1;fs=12" parent="bI2"><g x=1220 y=465 w=360 h=48/></c>
<c id="i11f_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=455 w=30 h=20/></c>
<c id="im" v="印 justfile 結果（建了／加了一行／跳過／已含不再加／拒絕不動）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI2"><g x=360 y=565 w=360 h=42/></c>
<c id="ig" v="有根 .dockerignore？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=627 w=250 h=81/></c>
<c id="ig_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=646 y=617 w=30 h=20/></c>
<c id="ign" v="無：建 .dockerignore（三行，逐字見右）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI2"><g x=860 y=628 w=120 h=79/></c>
<c id="ign_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=956 y=618 w=30 h=20/></c>
<c id="ignf" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;＋.dockerignore（新建，三行）：⏎.vendor_kit/cache/⏎.vendor_kit/gen/⏎.vendor_kit/.tmp.*&lt;/pre&gt;" s="fc=#ffffff;sc=#666666;dashed=1;fs=12" parent="bI2"><g x=1220 y=628 w=360 h=79/></c>
<c id="ignf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=618 w=30 h=20/></c>
<c id="igx" v="否 → 0：不寫 .dockerignore、印指示（含 justfile 結果；修復型先刪進度日誌）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bI2"><g x=20 y=764 w=220 h=102/></c>
<c id="igx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=216 y=754 w=30 h=20/></c>
<c id="igq" v="有 → 問「要在 .dockerignore 加這三行嗎」同意？（-y 免問；已含則跳過）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bI2"><g x=420 y=728 w=250 h=174/></c>
<c id="igq_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=646 y=718 w=30 h=20/></c>
<c id="igz" v="0：印建立了什麼（含 justfile 結果；修復型先刪進度日誌）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bI2"><g x=860 y=742 w=120 h=146/></c>
<c id="igz_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=956 y=732 w=30 h=20/></c>
<c id="igy" v="是：append 三行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bI2"><g x=420 y=942 w=250 h=40/></c>
<c id="igy_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=646 y=932 w=30 h=20/></c>
<c id="igyf" v="&lt;pre style=&quot;margin:0;font-family:inherit;font-size:inherit;line-height:inherit;tab-size:8;&quot;&gt;.dockerignore（尾端＋三行；Q22 補）：⏎.vendor_kit/cache/⏎.vendor_kit/gen/⏎.vendor_kit/.tmp.*&lt;/pre&gt;" s="fc=#ffffff;sc=#666666;dashed=1;fs=12" parent="bI2"><g x=1220 y=922 w=360 h=79/></c>
<c id="igyf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=912 w=30 h=20/></c>
<c id="igm" v="插入的行記在 baseline/.vendor_kit.toml（lines）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI2"><g x=420 y=1021 w=250 h=63/></c>
<c id="igm_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=646 y=1011 w=30 h=20/></c>
<c id="igmf" v="baseline/.vendor_kit.toml（記 .dockerignore 的 append 行；進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI2"><g x=1220 y=1028 w=360 h=48/></c>
<c id="igmf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=1018 w=30 h=20/></c>
<c id="idl" v="刪進度日誌 .tmp.install.&lt;id&gt;.toml（修復型才有；最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bI2"><g x=420 y=1104 w=250 h=48/></c>
<c id="idl_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=646 y=1094 w=30 h=20/></c>
<c id="idlf" v="－.vendor_kit/.tmp.install.&lt;id&gt;.toml（修復型才有）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bI2"><g x=1220 y=1108 w=360 h=40/></c>
<c id="idlf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bI2"><g x=1556 y=1098 w=30 h=20/></c>
<c id="iz" v="0：印建立／修改了什麼（含加的行）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bI2"><g x=20 y=1172 w=220 h=58/></c>
<c id="ie7" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i5e" target="i5"></c>
<c id="ie8" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=0.106;entryY=0" edge="1" source="i5" target="im"><g x=-0.83 pts=418,345/></c>
<c id="ie9" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i5" target="i6"><g x=-0.6/></c>
<c id="ie10" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i6" target="i7"></c>
<c id="ie11" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i7" target="i7f"></c>
<c id="ie12" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i6" target="i8"><g x=-0.6/></c>
<c id="ie13" s="fs=12;exitX=0.5;exitY=0;entryX=0;entryY=0.5" edge="1" source="i7" target="im"><g pts=940,232;370,232;370,758/></c>
<c id="ie13b" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=0.144;entryY=0" edge="1" source="i8" target="im"><g x=-0.78 pts=432,544/></c>
<c id="ie14" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="i8" target="i12"><g x=-0.6/></c>
<c id="ie17" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i12" target="i11"></c>
<c id="ie18" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.583;entryY=0" edge="1" source="i12" target="im"><g x=-0.6/></c>
<c id="ie16f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="i11" target="i11f"></c>
<c id="ie19d" s="fs=12;exitX=0.5;exitY=1;entryX=0.9;entryY=0" edge="1" source="i11" target="im"><g x=0.12 pts=940,727;704,727/></c>
<c id="ie19" s="fs=12;exitX=0.514;exitY=1;entryX=0.5;entryY=0" edge="1" source="im" target="ig"></c>
<c id="ie20" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="ig" target="ign"></c>
<c id="ie20f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="ign" target="ignf"></c>
<c id="ie21" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="ig" target="igq"><g x=-0.6/></c>
<c id="ie20z" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="ign" target="igz"></c>
<c id="ie22" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="igq" target="igx"></c>
<c id="ie23" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="igq" target="igy"><g x=-0.6/></c>
<c id="ie23f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="igy" target="igyf"></c>
<c id="ie23m" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="igy" target="igm"></c>
<c id="ie23mf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="igm" target="igmf"></c>
<c id="ie24" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="igm" target="idl"></c>
<c id="ie24f" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="idl" target="idlf"></c>
<c id="ie25" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="idl" target="iz"><g x=-0.86 pts=565,1373/></c>
<c id="p5cc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1458 w=200 h=60/></c>
<c id="p5cc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1458 w=140 h=64/></c>
<c id="p5cc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1466 w=140 h=44/></c>
<c id="p5cc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1460 w=190 h=56/></c>
<c id="p5cc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1460 w=210 h=56/></c>
<c id="p5cc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1468 w=88 h=40/></c>
<c id="p5cc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1468 w=170 h=40/></c>
<c id="p5cc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1458 w=300 h=60/></c>
<c id="p5cc_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1526 w=200 h=36/></c>
<c id="p5cc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1526 w=120 h=36/></c>
<c id="p5cc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1526 w=190 h=36/></c>
<c id="p5cc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1526 w=170 h=36/></c>
<c id="p5cc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1526 w=170 h=36/></c>
<c id="p5cc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1526 w=200 h=36/></c>
<c id="p5cc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1516 w=30 h=20/></c>
<c id="p5cc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1564 w=200 h=28/></c>
<c id="p5cc_tk0" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1598 w=150 h=71/></c>
<c id="p5cc_tv0" v="release 附的 POSIX sh 薄層：檢查 git repo／just ≥ 1.33.0 → 決定引擎 ref（專案已有 version.toml → 用該行引擎，不用內嵌；拉不到即失敗、不得退回內嵌，Q18；只有第一次接入才用內嵌 ref）→ docker image inspect 本機有就不 pull（--local：docker load 後驗 image ID）→ 呼叫 install（失敗即中止）→ 對每個 -t &lt;repo&gt;[@&lt;tag&gt;] 呼叫 add；再跑 = install" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1598 w=610 h=71/></c>
<c id="p5cc_tk1" v="release／tar／.digest／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1669 w=150 h=55/></c>
<c id="p5cc_tv1" v="release = GitHub 上發布的一版（附 bootstrap.sh）；tar = 離線包（docker save 存的 image 檔），每個 tar 附同名 .digest 旁檔 = 正式 index digest（Q26；旁檔缺 → 1）；docker load = 把 tar 讀進本機 docker" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1669 w=610 h=55/></c>
<c id="p5cc_tk2" v="--local &lt;image tag 或 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1724 w=150 h=55/></c>
<c id="p5cc_tv2" v="離線接入：值含 / 或以 .tar 結尾 → 檔案路徑（必須存在），其餘 → 本機 image tag；兩者皆成立 → 1 消歧；version.toml 仍寫正式 ref（digest 由 .digest 取得），version.local.toml 記 tag + image ID" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1724 w=610 h=55/></c>
<c id="p5cc_tk3" v="GHCR／image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1779 w=150 h=40/></c>
<c id="p5cc_tv3" v="GHCR = GitHub 的容器倉庫；image = 打包好的檔案集；引擎 ref = version.toml 第一行指到的引擎 image（ghcr.io/…/vendor_kit:vN@sha256:…）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1779 w=610 h=40/></c>
<c id="p5cc_tk4" v="docker image inspect／image ID" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1819 w=150 h=71/></c>
<c id="p5cc_tv4" v="啟動器每次 docker run 前先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（離線可用）；無 → docker pull；--local／dev 覆寫時 inspect 的 .Id 必須等於 version.local.toml 記的 image ID（同一個 tag 重新 build 過才會被發現），否則 1；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1819 w=610 h=71/></c>
<c id="p5cc_tk5" v="install／uninstall" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1890 w=150 h=55/></c>
<c id="p5cc_tv5" v="專案層一對（vendor_kit 自己）：把 vendor_kit 裝進這個 git repo（建 .vendor_kit/ 各檔＋根 justfile：無 → 新建 import 行 + default recipe，有 → 問後加一行；根 .dockerignore 三行問後加）／全部拆掉；再跑 install = 修復（用引擎重寫薄殼，不是只補缺）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1890 w=610 h=55/></c>
<c id="p5cc_tk6" v="冪等" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1945 w=150 h=40/></c>
<c id="p5cc_tv6" v="同一指令跑幾次結果都一樣：再跑 bootstrap.sh／install 不會重複加行、不會覆蓋你改過的東西（薄殼被改過 → 1 列差異不動）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1945 w=610 h=40/></c>
<c id="p5cc_tk7" v="薄殼 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1985 w=150 h=55/></c>
<c id="p5cc_tv7" v=".gitignore、entry.just、vendor.just、ci/check.sh（進 git；vendor_kit 自己的檔，人不改）＋ version.toml、baseline/（進 git）＋ cache/、gen/、version.local.toml、.tmp.*（不進 git）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1985 w=610 h=55/></c>
<c id="p5cc_tk8" v="薄殼首行自描述（Q17）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2040 w=150 h=55/></c>
<c id="p5cc_tv8" v="薄殼每檔第一行（check.sh 第二行）：# vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 LF 正規化 hash&gt;；install 用它判定「第一次／修復可重產／被改過 → 1」，不用 gen/.stamp（不進 git，重新 clone 後不存在）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2040 w=610 h=55/></c>
<c id="p5cc_tk9" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1598 w=150 h=40/></c>
<c id="p5cc_tv9" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1598 w=610 h=40/></c>
<c id="p5cc_tk10" v="暫存目錄／原子替換" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1638 w=150 h=40/></c>
<c id="p5cc_tv10" v="先寫到暫存目錄，確認沒問題再逐檔一次換上；第一次 install 失敗 → 丟棄暫存、移除已寫的檔，專案不留任何檔（只對第一次 install 成立）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1638 w=610 h=40/></c>
<c id="p5cc_tk11" v="version.toml／version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1678 w=150 h=55/></c>
<c id="p5cc_tv11" v="version.toml 唯一來源（進 git）：第一行引擎 ref（＋schema、written_by）、[tools] 每工具一行 tag@digest；local 不進 git：dev 覆寫（工具 path:&lt;dir&gt;，或引擎 image tag + image ID）；--local 的 local 檔在 install 成功後才寫" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1678 w=610 h=55/></c>
<c id="p5cc_tk12" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1733 w=150 h=40/></c>
<c id="p5cc_tv12" v="會動 image 的動詞分兩段：resolve 只讀只算（查版本、算要拉哪些 image，不寫檔）→ 啟動器 docker 拉 image → apply 才寫檔（拿鎖、重驗後）；見「add（1）」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1733 w=610 h=40/></c>
<c id="p5cc_tk13" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1773 w=150 h=55/></c>
<c id="p5cc_tv13" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git）；metadata = 其中的 .vendor_kit.toml，記來源版本、完成標記、append 過的行；install 只建 baseline/.gitkeep（git 不追蹤空目錄），metadata 到 add 才建" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1773 w=610 h=55/></c>
<c id="p5cc_tk14" v="just／recipe／import／default" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1828 w=150 h=55/></c>
<c id="p5cc_tv14" v="just = 跑指令的工具（像 make）；recipe = justfile 裡的一條指令；import = 把另一個 just 檔載進根 justfile 的那一行；新建根 justfile 還有 default recipe（default: ＋ 下一行縮排的 @just --list；寫成一行是語法錯誤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1828 w=610 h=55/></c>
<c id="p5cc_tk15" v="docker pull／run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1883 w=150 h=40/></c>
<c id="p5cc_tv15" v="pull = 從 GHCR 下載 image（本機已有則不拉）；run = 用 image 起容器跑引擎（預設不 pull）；多架構 image 由主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1883 w=610 h=40/></c>
<c id="p5cc_tk16" v="flock／-y" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1923 w=150 h=40/></c>
<c id="p5cc_tv16" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖；-y = 免問（§1：對使用者的檔可建、要改先問、永不刪、永不覆蓋；不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1923 w=610 h=40/></c>
<c id="p5cc_tk17" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1963 w=150 h=55/></c>
<c id="p5cc_tv17" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1963 w=610 h=55/></c>
</diagram>
<diagram id="v1p5b" name="流程 v2：add（1）resolve → docker"><c id="title" v="流程 v2：add &lt;repo&gt;（1）resolve → 啟動器 docker（§2／§5、v2.2 C／E、v2.5 §2／§3／§5）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&lt;repo&gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="bB" v="5b add &lt;repo&gt;[@&lt;tag&gt;]（bootstrap.sh 對每個 -t 呼叫；平時使用者也直接打）= 引擎 resolve（不寫）→ 啟動器 docker（inspect → 無才 pull → create → cp → rm）；apply 前置見「add（1′）」頁、寫入段見「add（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1135/></c>
<c id="bB_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=1556 y=5 w=30 h=20/></c>
<c id="c0" v="just vendor_kit add &lt;repo&gt;[@&lt;tag&gt;]（-y、--dry-run…）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bB"><g x=20 y=36 w=220 h=80/></c>
<c id="c1" v="docker run &lt;引擎&gt; resolve add &lt;repo&gt;（--local：tar 先 docker load，讀同名 .digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=260 y=44 w=280 h=63/></c>
<c id="c1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=516 y=34 w=30 h=20/></c>
<c id="c2a" v="resolve（不寫任何檔）：讀 version.toml" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB"><g x=560 y=56 w=400 h=40/></c>
<c id="c2a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=936 y=46 w=30 h=20/></c>
<c id="c2b" v="查 tag（預設最新正式版／@&lt;tag&gt;）與 index digest（--source 改來源）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB"><g x=560 y=140 w=400 h=48/></c>
<c id="c2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=936 y=130 w=30 h=20/></c>
<c id="c3" v="ghcr.io/&lt;org&gt;/&lt;repo&gt;-dist⏎（工具 image；多架構 index digest）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bB"><g x=980 y=136 w=220 h=57/></c>
<c id="c4" v="已接入 &lt;repo&gt;？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB"><g x=560 y=213 w=310 h=50/></c>
<c id="c5" v="metadata 有完成標記？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB"><g x=560 y=283 w=310 h=50/></c>
<c id="c6x" v="是 → 1：@&lt;tag&gt; 與鎖定不同，請改用 upgrade" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bB"><g x=20 y=364 w=220 h=58/></c>
<c id="c6x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=216 y=354 w=30 h=20/></c>
<c id="c5t" v="@&lt;tag&gt; 與鎖定不同？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB"><g x=605 y=353 w=220 h=81/></c>
<c id="c8" v="否：續作，只做缺的步驟（不補刻意刪的檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=840 y=365 w=120 h=57/></c>
<c id="c6" v="否 → 0：已接入且完成，無變更" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bB"><g x=20 y=454 w=220 h=58/></c>
<c id="c2c" v="resolve 完 → 產生執行計畫（要拉的 image@digest、mount、apply 與否）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB"><g x=560 y=532 w=400 h=48/></c>
<c id="c2c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=936 y=522 w=30 h=20/></c>
<c id="c2d" v="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）→ 計畫＋指紋以 stdout 回啟動器" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB"><g x=560 y=600 w=400 h=48/></c>
<c id="c2d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=936 y=590 w=30 h=20/></c>
<c id="c9a" v="docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB"><g x=260 y=668 w=170 h=143/></c>
<c id="c9a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=406 y=658 w=30 h=20/></c>
<c id="c9p" v="無：docker pull" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=440 y=831 w=100 h=48/></c>
<c id="c9p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=516 y=821 w=30 h=20/></c>
<c id="c9g" v="&lt;repo&gt;-dist@digest⏎（鎖定的那一版）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bB"><g x=980 y=834 w=220 h=42/></c>
<c id="c9b" v="docker create &lt;image&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=260 y=899 w=280 h=40/></c>
<c id="c9b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=516 y=889 w=30 h=20/></c>
<c id="c9c" v="docker cp c:/dist/. &lt;tmp&gt;/&lt;repo&gt;/（主機暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=260 y=959 w=280 h=48/></c>
<c id="c9c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=516 y=949 w=30 h=20/></c>
<c id="c9d" v="docker rm 該容器" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB"><g x=260 y=1027 w=280 h=40/></c>
<c id="c9d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB"><g x=516 y=1017 w=30 h=20/></c>
<c id="c9z" v="↓ 續「add（1′）」頁：docker run 引擎 apply add → 前置檢查" s="text;fs=12;sc=none;fc=none;fst=1" parent="bB"><g x=260 y=1087 w=280 h=42/></c>
<c id="cf_l" v="add 前 → 後（專案目錄，一格一檔；＋ = add 新增）" s="text;fs=12;sc=none;fc=none;fst=1" parent="bB"><g x=1220 y=40 w=340 h=26/></c>
<c id="cf0" v="add 前（install 後）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bB"><g x=1220 y=72 w=170 h=365/></c>
<c id="cf0_0" v="justfile（＋import 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=26 w=154 h=42/></c>
<c id="cf0_1" v=".dockerignore（＋三行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=74 w=154 h=42/></c>
<c id="cf0_2" v="version.toml（vendor_kit 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=122 w=154 h=42/></c>
<c id="cf0_3" v="version.local.toml（--local 時）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=170 w=154 h=42/></c>
<c id="cf0_4" v="薄殼四檔：.gitignore、entry.just、vendor.just、ci/check.sh" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=218 w=154 h=73/></c>
<c id="cf0_5" v="gen/.stamp" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=297 w=154 h=26/></c>
<c id="cf0_6" v="baseline/.gitkeep" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf0"><g x=8 y=329 w=154 h=26/></c>
<c id="cf1" v="add 後（＋ = 新增）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bB"><g x=1410 y=81 w=170 h=347/></c>
<c id="cf1_0" v="＋version.toml [tools] &lt;repo&gt; 行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=26 w=154 h=42/></c>
<c id="cf1_1" v="＋cache/&lt;repo&gt;/（不進 git：files/、init.toml、just/）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=74 w=154 h=57/></c>
<c id="cf1_2" v="＋gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=137 w=154 h=26/></c>
<c id="cf1_3" v="＋初始檔（init.toml 的 dest；append 問後加）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=169 w=154 h=57/></c>
<c id="cf1_4" v="＋baseline/&lt;repo&gt;/ + .vendor_kit.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=232 w=154 h=42/></c>
<c id="cf1_5" v="＋gen/tools.just（每個 &lt;ns&gt;.just 一行 mod?）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="cf1"><g x=8 y=280 w=154 h=57/></c>
<c id="ce1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c0" target="c1"></c>
<c id="ce2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c1" target="c2a"></c>
<c id="ce2b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c2a" target="c2b"></c>
<c id="ce3" v="查" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c2b" target="c3"></c>
<c id="ce4" s="fs=12;exitX=0.388;exitY=1;entryX=0.5;entryY=0" edge="1" source="c2b" target="c4"></c>
<c id="ce5" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c4" target="c5"><g x=-0.6/></c>
<c id="ce7" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c5" target="c5t"><g x=-0.6/></c>
<c id="ce7b" v="否" s="fs=12;exitX=0.7;exitY=1;entryX=0.5;entryY=0" edge="1" source="c5" target="c8"><g x=-0.08 pts=797,484;920,484/></c>
<c id="ce8" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c5t" target="c6x"></c>
<c id="ce9" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="c5t" target="c6"><g x=-0.91 pts=735,624/></c>
<c id="ce10" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0.85;entryY=0" edge="1" source="c4" target="c2c"><g x=-0.51 pts=990,379;990,663;920,663/></c>
<c id="ce11" s="fs=12;exitX=1;exitY=0.5;entryX=0.85;entryY=0" edge="1" source="c8" target="c2c"><g pts=990,534;990,663;920,663/></c>
<c id="ce12" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c2c" target="c2d"></c>
<c id="ce12a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c2d" target="c9a"><g x=0.00 pts=780,799;365,799/></c>
<c id="ce12n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="c9a" target="c9p"><g x=-0.60 pts=510,880/></c>
<c id="ce12g" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c9g" target="c9p"></c>
<c id="ce12y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.304;entryY=0" edge="1" source="c9a" target="c9b"><g x=-0.6/></c>
<c id="ce12p" s="fs=12;exitX=0.5;exitY=1;entryX=0.821;entryY=0" edge="1" source="c9p" target="c9b"></c>
<c id="ce12c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c9b" target="c9c"></c>
<c id="ce12d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c9c" target="c9d"></c>
<c id="ce13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c9d" target="c9z"></c>
<c id="cfe" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="cf0" target="cf1"></c>
<c id="p5b_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1292 w=200 h=60/></c>
<c id="p5b_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1292 w=140 h=64/></c>
<c id="p5b_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1300 w=140 h=44/></c>
<c id="p5b_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1294 w=190 h=56/></c>
<c id="p5b_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1294 w=210 h=56/></c>
<c id="p5b_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1302 w=88 h=40/></c>
<c id="p5b_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1302 w=170 h=40/></c>
<c id="p5b_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1292 w=300 h=60/></c>
<c id="p5b_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1360 w=120 h=36/></c>
<c id="p5b_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1360 w=150 h=36/></c>
<c id="p5b_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1360 w=190 h=36/></c>
<c id="p5b_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1360 w=170 h=36/></c>
<c id="p5b_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1360 w=170 h=36/></c>
<c id="p5b_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1360 w=200 h=36/></c>
<c id="p5b_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1350 w=30 h=20/></c>
<c id="p5b_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1398 w=200 h=28/></c>
<c id="p5b_tk0" v="add &lt;repo&gt;[@&lt;tag&gt;]" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1432 w=150 h=71/></c>
<c id="p5b_tv0" v="接一個工具（@&lt;tag&gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1432 w=610 h=71/></c>
<c id="p5b_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1503 w=150 h=40/></c>
<c id="p5b_tv1" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1503 w=610 h=40/></c>
<c id="p5b_tk2" v="stdout／stderr" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1543 w=150 h=40/></c>
<c id="p5b_tv2" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1543 w=610 h=40/></c>
<c id="p5b_tk3" v="輸入指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1583 w=150 h=40/></c>
<c id="p5b_tv3" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1583 w=610 h=40/></c>
<c id="p5b_tk4" v="GHCR／image／index digest／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1623 w=150 h=55/></c>
<c id="p5b_tv4" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1623 w=610 h=55/></c>
<c id="p5b_tk5" v="--local／tar／.digest（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1678 w=150 h=55/></c>
<c id="p5b_tv5" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1678 w=610 h=55/></c>
<c id="p5b_tk6" v="/dist/&lt;repo&gt;（暫存）／N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1733 w=150 h=40/></c>
<c id="p5b_tv6" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&lt;repo&gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&lt;repo&gt;（v2.5 §2）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1733 w=610 h=40/></c>
<c id="p5b_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1773 w=150 h=40/></c>
<c id="p5b_tv7" v="引擎內部步驟：apply 決定套用後才把 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 = gen/&lt;repo&gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1773 w=610 h=40/></c>
<c id="p5b_tk8" v="初始檔／strategy" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1813 w=150 h=55/></c>
<c id="p5b_tv8" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1813 w=610 h=55/></c>
<c id="p5b_tk9" v="dest 撞名" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1868 w=150 h=40/></c>
<c id="p5b_tv9" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1868 w=610 h=40/></c>
<c id="p5b_tk10" v="命名空間撞名（v2.5 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1432 w=150 h=40/></c>
<c id="p5b_tv10" v="工具 dist/just/&lt;ns&gt;.just 的 &lt;ns&gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1432 w=610 h=40/></c>
<c id="p5b_tk11" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1472 w=150 h=71/></c>
<c id="p5b_tv11" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1472 w=610 h=71/></c>
<c id="p5b_tk12" v="續作" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1543 w=150 h=28/></c>
<c id="p5b_tv12" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1543 w=610 h=28/></c>
<c id="p5b_tk13" v="gen／mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1571 w=150 h=71/></c>
<c id="p5b_tv13" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1571 w=610 h=71/></c>
<c id="p5b_tk14" v="CI 為真／frozen／dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1642 w=150 h=55/></c>
<c id="p5b_tv14" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1642 w=610 h=55/></c>
<c id="p5b_tk15" v="flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1697 w=150 h=28/></c>
<c id="p5b_tv15" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1697 w=610 h=28/></c>
<c id="p5b_tk16" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1725 w=150 h=28/></c>
<c id="p5b_tv16" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1725 w=610 h=28/></c>
<c id="p5b_tk17" v="CRLF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1753 w=150 h=40/></c>
<c id="p5b_tv17" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1753 w=610 h=40/></c>
<c id="p5b_tk18" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1793 w=150 h=55/></c>
<c id="p5b_tv18" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1793 w=610 h=55/></c>
</diagram>
<diagram id="v1p5bcc" name="流程 v2：add（1′）apply 前置"><c id="title" v="流程 v2：add &lt;repo&gt;（1′）apply 前置：拿鎖 → 重驗 → 檢查 → frozen → dry-run（v2.2 E、v2.5 §3／§5）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&lt;repo&gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="bB1" v="5b′ add &lt;repo&gt; 的 apply 前置（承「add（1）」頁：工具 image 已展開到主機暫存）：docker run 引擎 apply → 拿鎖 → 重驗指紋 → dest 合法？→ 命名空間撞名？→ frozen → dry-run 分支；寫入段見「add（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=726/></c>
<c id="bB1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=1556 y=5 w=30 h=20/></c>
<c id="c9e" v="來自「add（1）」頁：/dist/&lt;repo&gt; 已在主機暫存" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bB1"><g x=260 y=36 w=280 h=58/></c>
<c id="c10" v="docker run … -v &lt;tmp&gt;:/dist:ro &lt;引擎&gt; apply add &lt;repo&gt;（--dry-run 原樣轉發）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB1"><g x=260 y=114 w=280 h=48/></c>
<c id="c10_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=516 y=104 w=30 h=20/></c>
<c id="c11a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB1"><g x=560 y=118 w=400 h=40/></c>
<c id="c11a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=936 y=108 w=30 h=20/></c>
<c id="c11b" v="重驗 resolve 的輸入指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB1"><g x=560 y=191 w=240 h=40/></c>
<c id="c11b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=776 y=181 w=30 h=20/></c>
<c id="c11x" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bB1"><g x=820 y=182 w=140 h=58/></c>
<c id="c11x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=936 y=172 w=30 h=20/></c>
<c id="c12x" v="否 → 1：dest 不合法" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bB1"><g x=20 y=280 w=220 h=40/></c>
<c id="c12x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=216 y=270 w=30 h=20/></c>
<c id="c12" v="init.toml 的 dest 全部合法？（任何寫入前檢查）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB1"><g x=560 y=260 w=400 h=81/></c>
<c id="c12_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=936 y=250 w=30 h=20/></c>
<c id="c12r" v="dest 規則（v2.2 E）：兩工具 copy/copy、copy/append 同 dest → 拒絕；append/append 允許（各工具的行分開記；重疊或歸屬不明 → 拒絕）；正規化後不得越出 repo、不得指向 .vendor_kit/；dist 含 symlink → 拒絕" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bB1"><g x=1220 y=261 w=360 h=79/></c>
<c id="c12r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=1556 y=251 w=30 h=20/></c>
<c id="c12bx" v="是 → 1：命名空間撞名" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bB1"><g x=20 y=397 w=220 h=40/></c>
<c id="c12bx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=216 y=387 w=30 h=20/></c>
<c id="c12b" v="just/&lt;ns&gt;.just 的 &lt;ns&gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB1"><g x=560 y=361 w=400 h=112/></c>
<c id="c12b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=936 y=351 w=30 h=20/></c>
<c id="c12br" v="命名空間撞名（v2.5 §5）：&lt;ns&gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → 1 拒絕（撞名整個 just 會掛）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bB1"><g x=1220 y=386 w=360 h=63/></c>
<c id="c12br_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=1556 y=376 w=30 h=20/></c>
<c id="c14x" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bB1"><g x=20 y=494 w=220 h=80/></c>
<c id="c14x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=216 y=484 w=30 h=20/></c>
<c id="c14" v="CI 為真（frozen）且需改 tracked 檔？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB1"><g x=590 y=493 w=340 h=81/></c>
<c id="c14_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=906 y=483 w=30 h=20/></c>
<c id="c13y" v="是 → 0：唯讀預覽（印會建／會問哪些檔；讀 /dist/&lt;repo&gt;）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bB1"><g x=20 y=594 w=220 h=80/></c>
<c id="c13y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB1"><g x=216 y=584 w=30 h=20/></c>
<c id="c13" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB1"><g x=640 y=609 w=240 h=50/></c>
<c id="c13z" v="否 ↓ 續「add（2）」頁：apply 寫入段" s="text;fs=12;sc=none;fc=none;fst=1" parent="bB1"><g x=560 y=694 w=300 h=26/></c>
<c id="ce13e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c9e" target="c10"></c>
<c id="ce14" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c10" target="c11a"></c>
<c id="ce14b" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="c11a" target="c11b"></c>
<c id="ce15" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c11b" target="c11x"></c>
<c id="ce16" s="fs=12;exitX=0.833;exitY=1;entryX=0.5;entryY=0" edge="1" source="c11b" target="c12"></c>
<c id="ce17" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c12" target="c12x"></c>
<c id="ce18" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c12" target="c12b"><g x=-0.6/></c>
<c id="ce18x" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c12b" target="c12bx"></c>
<c id="ce18b" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c12b" target="c14"><g x=-0.6/></c>
<c id="ce19" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c14" target="c14x"></c>
<c id="ce20" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c14" target="c13"><g x=-0.6/></c>
<c id="ce21" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c13" target="c13y"></c>
<c id="ce22" s="fs=12;exitX=0.5;exitY=1;entryX=0.667;entryY=0" edge="1" source="c13" target="c13z"></c>
<c id="p5bp_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=883 w=200 h=60/></c>
<c id="p5bp_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=883 w=140 h=64/></c>
<c id="p5bp_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=891 w=140 h=44/></c>
<c id="p5bp_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=885 w=190 h=56/></c>
<c id="p5bp_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=885 w=210 h=56/></c>
<c id="p5bp_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=893 w=88 h=40/></c>
<c id="p5bp_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=893 w=170 h=40/></c>
<c id="p5bp_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=883 w=300 h=60/></c>
<c id="p5bp_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=951 w=200 h=36/></c>
<c id="p5bp_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=951 w=120 h=36/></c>
<c id="p5bp_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=951 w=150 h=36/></c>
<c id="p5bp_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=570 y=951 w=190 h=36/></c>
<c id="p5bp_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=780 y=951 w=170 h=36/></c>
<c id="p5bp_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=951 w=170 h=36/></c>
<c id="p5bp_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1160 y=951 w=200 h=36/></c>
<c id="p5bp_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1336 y=941 w=30 h=20/></c>
<c id="p5bp_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=989 w=200 h=28/></c>
<c id="p5bp_tk0" v="add &lt;repo&gt;[@&lt;tag&gt;]" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1023 w=150 h=71/></c>
<c id="p5bp_tv0" v="接一個工具（@&lt;tag&gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1023 w=610 h=71/></c>
<c id="p5bp_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1094 w=150 h=40/></c>
<c id="p5bp_tv1" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1094 w=610 h=40/></c>
<c id="p5bp_tk2" v="stdout／stderr" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1134 w=150 h=40/></c>
<c id="p5bp_tv2" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1134 w=610 h=40/></c>
<c id="p5bp_tk3" v="輸入指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1174 w=150 h=40/></c>
<c id="p5bp_tv3" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1174 w=610 h=40/></c>
<c id="p5bp_tk4" v="GHCR／image／index digest／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1214 w=150 h=55/></c>
<c id="p5bp_tv4" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1214 w=610 h=55/></c>
<c id="p5bp_tk5" v="--local／tar／.digest（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1269 w=150 h=55/></c>
<c id="p5bp_tv5" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1269 w=610 h=55/></c>
<c id="p5bp_tk6" v="/dist/&lt;repo&gt;（暫存）／N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1324 w=150 h=40/></c>
<c id="p5bp_tv6" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&lt;repo&gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&lt;repo&gt;（v2.5 §2）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1324 w=610 h=40/></c>
<c id="p5bp_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1364 w=150 h=40/></c>
<c id="p5bp_tv7" v="引擎內部步驟：apply 決定套用後才把 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 = gen/&lt;repo&gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1364 w=610 h=40/></c>
<c id="p5bp_tk8" v="初始檔／strategy" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1404 w=150 h=55/></c>
<c id="p5bp_tv8" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1404 w=610 h=55/></c>
<c id="p5bp_tk9" v="dest 撞名" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1459 w=150 h=40/></c>
<c id="p5bp_tv9" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1459 w=610 h=40/></c>
<c id="p5bp_tk10" v="命名空間撞名（v2.5 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1023 w=150 h=40/></c>
<c id="p5bp_tv10" v="工具 dist/just/&lt;ns&gt;.just 的 &lt;ns&gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1023 w=610 h=40/></c>
<c id="p5bp_tk11" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1063 w=150 h=71/></c>
<c id="p5bp_tv11" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1063 w=610 h=71/></c>
<c id="p5bp_tk12" v="續作" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1134 w=150 h=28/></c>
<c id="p5bp_tv12" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1134 w=610 h=28/></c>
<c id="p5bp_tk13" v="gen／mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1162 w=150 h=71/></c>
<c id="p5bp_tv13" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1162 w=610 h=71/></c>
<c id="p5bp_tk14" v="CI 為真／frozen／dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1233 w=150 h=55/></c>
<c id="p5bp_tv14" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1233 w=610 h=55/></c>
<c id="p5bp_tk15" v="flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1288 w=150 h=28/></c>
<c id="p5bp_tv15" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1288 w=610 h=28/></c>
<c id="p5bp_tk16" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1316 w=150 h=28/></c>
<c id="p5bp_tv16" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1316 w=610 h=28/></c>
<c id="p5bp_tk17" v="CRLF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1344 w=150 h=40/></c>
<c id="p5bp_tv17" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1344 w=610 h=40/></c>
<c id="p5bp_tk18" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1384 w=150 h=55/></c>
<c id="p5bp_tv18" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1384 w=610 h=55/></c>
</diagram>
<diagram id="v1p5bc" name="流程 v2：add（2）apply 寫入段"><c id="title" v="流程 v2：add &lt;repo&gt;（2）apply 寫入段（§5、v2.2 C／E、v2.3 §1／§6、v2.5 §2～§4）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：init.toml 每個 [[file]] 的欄位 strategy = &quot;copy&quot; | &quot;append&quot;（預設 copy）。已定（v2.5 §2／§3／§5）：逐檔判斷讀暫存 /dist/&lt;repo&gt;，materialize 在決定套用後；apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 寫入 → 刪日誌；前置檢查加命名空間撞名。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="bB2" v="5b″ add &lt;repo&gt; 的 apply 寫入段（承「add（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → materialize → 印記 → 初始檔逐檔（每個 [[file]] 迴圈）→ baseline → metadata → tools.just → version.toml → 刪日誌" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1460/></c>
<c id="bB2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=1556 y=5 w=30 h=20/></c>
<c id="c13c" v="來自「add（1′）」頁：apply 檢查通過（非 dry-run）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bB2"><g x=610 y=36 w=300 h=58/></c>
<c id="c15a" v="建進度日誌（metadata state=in-progress；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=115 w=400 h=40/></c>
<c id="c15a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=105 w=30 h=20/></c>
<c id="c15af" v="＋baseline/&lt;repo&gt;/.vendor_kit.toml（state=in-progress）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=114 w=360 h=42/></c>
<c id="c15" v="materialize：/dist/&lt;repo&gt; 複製到暫存目錄" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=176 w=400 h=40/></c>
<c id="c15_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=166 w=30 h=20/></c>
<c id="c15c" v="暫存 → cache/&lt;repo&gt;/（原子替換）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=236 w=400 h=40/></c>
<c id="c15c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=226 w=30 h=20/></c>
<c id="c15f" v="＋cache/&lt;repo&gt;/（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=236 w=360 h=40/></c>
<c id="c15b" v="寫印記 gen/&lt;repo&gt;.stamp（第一行 index digest，之後每檔 sha256）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=296 w=400 h=48/></c>
<c id="c15b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=286 w=30 h=20/></c>
<c id="c15bf" v="＋gen/&lt;repo&gt;.stamp（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=300 w=360 h=40/></c>
<c id="cl" v="↓ 初始檔逐檔（init.toml 每個 [[file]]；範本讀 /dist/&lt;repo&gt;）" s="text;fs=12;sc=none;fc=none;fst=1" parent="bB2"><g x=680 y=364 w=280 h=42/></c>
<c id="c16" v="初始檔已存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB2"><g x=560 y=440 w=200 h=50/></c>
<c id="c17" v="無：建該檔（state=managed）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB2"><g x=810 y=444 w=150 h=42/></c>
<c id="cr" v="復原（v2.2 C、v2.5 §3）：進度日誌在第一個寫入前建立、最後一步刪除；合併全在暫存完成 → 逐檔原子替換；失敗 → 1 明列已完成／未完成，下次可寫動詞先恢復（唯讀動詞只提示重跑）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bB2"><g x=1220 y=426 w=360 h=79/></c>
<c id="cr_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=1556 y=416 w=30 h=20/></c>
<c id="c18" v="strategy = append？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB2"><g x=560 y=525 w=200 h=81/></c>
<c id="c18_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=736 y=515 w=30 h=20/></c>
<c id="c19" v="否：不納管（state=unmanaged）、不覆蓋，印「已存在，範本在 cache」" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB2"><g x=780 y=529 w=180 h=73/></c>
<c id="c20q" v="問「要在 X 加這幾行嗎」？（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB2"><g x=560 y=626 w=320 h=81/></c>
<c id="c20q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=856 y=616 w=30 h=20/></c>
<c id="c20n" v="否：不寫；state=unmanaged 只記 declined_hash" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB2"><g x=560 y=727 w=150 h=63/></c>
<c id="c20n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=686 y=717 w=30 h=20/></c>
<c id="c20" v="是：append 那幾行（state=appended；實際插入的行之後記進 metadata）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bB2"><g x=750 y=730 w=210 h=57/></c>
<c id="c20l" v="還有下一個 [[file]]？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bB2"><g x=610 y=810 w=300 h=81/></c>
<c id="c20l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=886 y=800 w=30 h=20/></c>
<c id="c21" v="否：寫 baseline/&lt;repo&gt;/（範本副本）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=911 w=400 h=40/></c>
<c id="c21f" v="＋baseline/&lt;repo&gt;/（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=911 w=360 h=40/></c>
<c id="c21b" v="寫 metadata：來源 ref@digest、最後合併版本（--local 另記 local_image_id）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=971 w=400 h=48/></c>
<c id="c21b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=961 w=30 h=20/></c>
<c id="c21bf" v="＋baseline/&lt;repo&gt;/.vendor_kit.toml（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=975 w=360 h=40/></c>
<c id="c21c" v="寫 metadata：每個 dest 的 state（managed／appended／unmanaged；新檔被拒才 declined）、declined_hash、append 行（lines）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=1039 w=400 h=63/></c>
<c id="c21c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=1029 w=30 h=20/></c>
<c id="c21cf" v=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=1050 w=360 h=42/></c>
<c id="c21d" v="寫 metadata：完成標記（complete）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=1122 w=400 h=40/></c>
<c id="c21d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=1112 w=30 h=20/></c>
<c id="c21df" v=".vendor_kit.toml（complete = true）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=1122 w=360 h=40/></c>
<c id="c22" v="重生 gen/tools.just（每個 &lt;ns&gt;.just 一行 mod?；一工具可多行）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=1182 w=400 h=48/></c>
<c id="c22_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=1172 w=30 h=20/></c>
<c id="c22f" v="gen/tools.just（不進 git；mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=1186 w=360 h=40/></c>
<c id="c23" v="最後寫 version.toml [tools]：&lt;repo&gt; = &quot;…:&lt;tag&gt;@sha256:…&quot;" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=1250 w=400 h=48/></c>
<c id="c23_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=1240 w=30 h=20/></c>
<c id="c23f" v="＋version.toml [tools] 行（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bB2"><g x=1220 y=1254 w=360 h=40/></c>
<c id="c23x" v="失敗 → 1：明列已完成／未完成" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bB2"><g x=20 y=1318 w=220 h=58/></c>
<c id="c23x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=216 y=1308 w=30 h=20/></c>
<c id="c23b" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bB2"><g x=560 y=1327 w=400 h=40/></c>
<c id="c23b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bB2"><g x=936 y=1317 w=30 h=20/></c>
<c id="c24" v="成功 → 0：印摘要，提示 git add" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bB2"><g x=20 y=1396 w=220 h=58/></c>
<c id="ce23a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c13c" target="c15a"></c>
<c id="ce23b" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c15a" target="c15af"></c>
<c id="ce23c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c15a" target="c15"></c>
<c id="ce23cc" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c15" target="c15c"></c>
<c id="ce23" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c15c" target="c15f"></c>
<c id="ce23d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c15c" target="c15b"></c>
<c id="ce23e" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c15b" target="c15bf"></c>
<c id="ce24" s="fs=12;exitX=0.25;exitY=1;entryX=0.5;entryY=0" edge="1" source="c15b" target="c16"></c>
<c id="ce25" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c16" target="c17"></c>
<c id="ce26" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c16" target="c18"><g x=-0.6/></c>
<c id="ce27" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c18" target="c19"></c>
<c id="ce28" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c18" target="c20q"><g x=0.00 pts=680,757;740,757/></c>
<c id="ce28n" v="否" s="fs=12;exitX=0.25;exitY=1;entryX=0.533;entryY=0" edge="1" source="c20q" target="c20n"><g x=0.5/></c>
<c id="ce28y" v="是" s="fs=12;exitX=0.8;exitY=1;entryX=0.314;entryY=0" edge="1" source="c20q" target="c20"><g x=0.5/></c>
<c id="ce29" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="c17" target="c20l"><g pts=990,606;990,941;780,941/></c>
<c id="ce30" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="c19" target="c20l"><g pts=990,706;990,941;780,941/></c>
<c id="ce31" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c20" target="c20l"><g x=0.03 pts=875,941;780,941/></c>
<c id="ce31n" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c20n" target="c20l"><g x=0.00 pts=655,941;780,941/></c>
<c id="ce31y" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c20l" target="c16"><g x=-0.66 pts=565,992;565,606/></c>
<c id="ce31l" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c20l" target="c21"><g x=-0.6/></c>
<c id="ce32" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c21" target="c21f"></c>
<c id="ce32b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c21" target="c21b"></c>
<c id="ce32f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c21b" target="c21bf"></c>
<c id="ce32c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c21b" target="c21c"></c>
<c id="ce32cf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c21c" target="c21cf"></c>
<c id="ce32d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c21c" target="c21d"></c>
<c id="ce32df" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c21d" target="c21df"></c>
<c id="ce33" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c21d" target="c22"></c>
<c id="ce34" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c22" target="c22f"></c>
<c id="ce35" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="c22" target="c23"></c>
<c id="ce36" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="c23" target="c23f"></c>
<c id="ce37" v="成功" s="fs=12;exitX=0.6;exitY=1;entryX=0.6;entryY=0" edge="1" source="c23" target="c23b"><g x=-0.6/></c>
<c id="ce38" v="失敗" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="c23" target="c23x"><g x=0.00 pts=660,1449;150,1449/></c>
<c id="ce39" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="c23b" target="c24"><g x=-0.90 pts=780,1566/></c>
<c id="p5bc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1617 w=200 h=60/></c>
<c id="p5bc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1617 w=140 h=64/></c>
<c id="p5bc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1625 w=140 h=44/></c>
<c id="p5bc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1619 w=190 h=56/></c>
<c id="p5bc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1619 w=210 h=56/></c>
<c id="p5bc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1627 w=88 h=40/></c>
<c id="p5bc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1627 w=170 h=40/></c>
<c id="p5bc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1617 w=300 h=60/></c>
<c id="p5bc_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1685 w=200 h=36/></c>
<c id="p5bc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1685 w=120 h=36/></c>
<c id="p5bc_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=1685 w=150 h=36/></c>
<c id="p5bc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=570 y=1685 w=190 h=36/></c>
<c id="p5bc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=780 y=1685 w=170 h=36/></c>
<c id="p5bc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=1685 w=170 h=36/></c>
<c id="p5bc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1160 y=1685 w=200 h=36/></c>
<c id="p5bc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1336 y=1675 w=30 h=20/></c>
<c id="p5bc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1723 w=200 h=28/></c>
<c id="p5bc_tk0" v="add &lt;repo&gt;[@&lt;tag&gt;]" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1757 w=150 h=71/></c>
<c id="p5bc_tv0" v="接一個工具（@&lt;tag&gt; 省略 = 最新正式版；沒有 --tag）：resolve 查 tag/digest → 啟動器拉 image → apply：拿鎖、重驗、檢查、dry-run 分支 → 建日誌 → materialize → 印記 → 初始檔逐檔 → baseline → metadata → 重生 gen/tools.just → 最後寫 version.toml → 刪日誌；已接入且完成 → 0" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1757 w=610 h=71/></c>
<c id="p5bc_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1828 w=150 h=40/></c>
<c id="p5bc_tv1" v="同一動詞分兩段：resolve 只讀只算，不寫任何檔；apply 才寫（拿 flock、重驗指紋後；v2.5 §3 順序）；--dry-run（無短形）= apply 的唯讀預覽（也要先拉 image 才知道會問哪些檔）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1828 w=610 h=40/></c>
<c id="p5bc_tk2" v="stdout／stderr" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1868 w=150 h=40/></c>
<c id="p5bc_tv2" v="resolve 回給啟動器的結果走 stdout（第一行 vk-resolve/1，之後一行一項，只有固定欄位）；給人看的診斷訊息一律走 stderr；啟動器只逐行讀，不把內容當指令執行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1868 w=610 h=40/></c>
<c id="p5bc_tk3" v="輸入指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1908 w=150 h=40/></c>
<c id="p5bc_tv3" v="resolve 把它讀過的 version.toml、metadata、要動的使用者檔的 hash＋鎖定 digest 一起輸出；apply 拿到 flock 後重驗，不同（中間有人改了）→ 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1908 w=610 h=40/></c>
<c id="p5bc_tk4" v="GHCR／image／index digest／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1948 w=150 h=55/></c>
<c id="p5bc_tv4" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；多架構 image 的總目錄叫 index，其 digest（sha256）= 鎖定用的唯一 ID；啟動器每個 image 先 docker image inspect，本機有就不 pull（離線可用）；docker create 不帶 --platform，主機 docker 挑原生平台" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1948 w=610 h=55/></c>
<c id="p5bc_tk5" v="--local／tar／.digest（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2003 w=150 h=55/></c>
<c id="p5bc_tv5" v="值含 / 或以 .tar 結尾 → tar 路徑（docker save 存的工具 image 檔）先 docker load；其餘 → 本機 image tag；每個 tar 附同名 .digest 旁檔 = 正式 index digest，寫進 version.toml；metadata 記 image ID ↔ digest 對照供離線驗證；只涵蓋 install／add --local" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2003 w=610 h=55/></c>
<c id="p5bc_tk6" v="/dist/&lt;repo&gt;（暫存）／N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2058 w=150 h=40/></c>
<c id="p5bc_tv6" v="啟動器把目標版 image 的 dist/ 展開到主機暫存目錄，掛進引擎 /dist/&lt;repo&gt;:ro；逐檔判斷與 dry-run 都讀它（不是 cache）；N = 目標版範本 = 暫存 /dist/&lt;repo&gt;（v2.5 §2）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2058 w=610 h=40/></c>
<c id="p5bc_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2098 w=150 h=40/></c>
<c id="p5bc_tv7" v="引擎內部步驟：apply 決定套用後才把 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 = gen/&lt;repo&gt;.stamp，第一行 index digest，之後每檔 sha256（用來驗 cache 有沒有被改）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2098 w=610 h=40/></c>
<c id="p5bc_tk8" v="初始檔／strategy" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2138 w=150 h=55/></c>
<c id="p5bc_tv8" v="init.toml [[file]] src/dest，strategy = copy（預設）或 append：copy 無→建、有→不納管；append（.gitignore 類）無→建、有→問「要加這幾行嗎」→ 同意加入並記 metadata（state=appended）；拒絕 → 不寫、state=unmanaged 只記 declined_hash（新版再變才再問）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2138 w=610 h=55/></c>
<c id="p5bc_tk9" v="dest 撞名" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2193 w=150 h=40/></c>
<c id="p5bc_tv9" v="兩工具的 dest 指到同一路徑：copy/copy、copy/append → 拒絕；append/append → 允許（各工具的行分開記，重疊或歸屬不明 → 拒絕）；不得越出 repo、不得指向 .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2193 w=610 h=40/></c>
<c id="p5bc_tk10" v="命名空間撞名（v2.5 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1757 w=150 h=40/></c>
<c id="p5bc_tv10" v="工具 dist/just/&lt;ns&gt;.just 的 &lt;ns&gt; 與 (a) 其他已接工具 (b) 根 justfile 既有 recipe／module (c) 保留名 vendor_kit 相同 → add 回 1 拒絕（撞名整個 just 會掛）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1757 w=610 h=40/></c>
<c id="p5bc_tk11" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1797 w=150 h=71/></c>
<c id="p5bc_tv11" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（歷史狀態，進 git）；metadata = 其中的 .vendor_kit.toml，記來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）、append 過的行、declined_hash、進度日誌（state=in-progress）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1797 w=610 h=71/></c>
<c id="p5bc_tk12" v="續作" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1868 w=150 h=28/></c>
<c id="p5bc_tv12" v="add 對已接入工具只補「metadata 無完成標記」的未完成接入；不補使用者刻意刪的檔" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1868 w=610 h=28/></c>
<c id="p5bc_tk13" v="gen／mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1896 w=150 h=71/></c>
<c id="p5bc_tv13" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? &lt;ns&gt; &#x27;../cache/&lt;repo&gt;/just/&lt;ns&gt;.just&#x27; = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）；mod?（帶問號）= 檔不在也不掛、其他 recipe 仍可跑；recipe = justfile 裡的一條指令；gen 檔裡沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1896 w=610 h=71/></c>
<c id="p5bc_tk14" v="CI 為真／frozen／dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1967 w=150 h=55/></c>
<c id="p5bc_tv14" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除 frozen（-y 只在本機免詢問）；dry-run = 只預覽不動檔（本機 → 0）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1967 w=610 h=55/></c>
<c id="p5bc_tk15" v="flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2022 w=150 h=28/></c>
<c id="p5bc_tv15" v="專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎，啟動器不鎖" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2022 w=610 h=28/></c>
<c id="p5bc_tk16" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2050 w=150 h=28/></c>
<c id="p5bc_tv16" v="指向另一個路徑的捷徑；工具的 dist/ 第一版禁止含 symlink，引擎展開時驗到就拒絕" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2050 w=610 h=28/></c>
<c id="p5bc_tk17" v="CRLF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2078 w=150 h=40/></c>
<c id="p5bc_tv17" v="Windows 換行（\r\n）；append 行比對時 CRLF／LF 視為相同，其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2078 w=610 h=40/></c>
<c id="p5bc_tk18" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2118 w=150 h=55/></c>
<c id="p5bc_tv18" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2118 w=610 h=55/></c>
</diagram>
<diagram id="v1p6" name="流程 v2：sync（1）啟動器快路徑"><c id="title" v="流程 v2：sync（1）啟動器：gen/.stamp 比對 → 快路徑（Q22）→ 起引擎（§6、v2.3 §2、v2.5 §9、v2.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify 或 CI 為真才做。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="eA" v="sync（工具 recipe 的自動前置；CI 為真 → frozen）：第 1 段 = 啟動器比對 gen/.stamp（install／upgrade vendor_kit 跳過）→ 快路徑 grep 全相符 → 0 不起容器；有差 → docker image inspect → 引擎 resolve sync（見「sync（1′）」頁）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=841/></c>
<c id="eA_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=1556 y=5 w=30 h=20/></c>
<c id="n0" v="打工具 recipe（_sync 自動前置）或 just vendor_kit sync" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="eA"><g x=20 y=51 w=220 h=80/></c>
<c id="n1" v="grep version.toml 第一行取引擎 ref（version.local.toml 的 vendor_kit 覆寫優先）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA"><g x=260 y=60 w=280 h=63/></c>
<c id="n1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=516 y=50 w=30 h=20/></c>
<c id="n2" v="讀" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="eA"><g x=1220 y=36 w=360 h=110/></c>
<c id="n2_0" v=".vendor_kit/version.toml（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="n2"><g x=8 y=26 w=344 h=26/></c>
<c id="n2_1" v=".vendor_kit/version.local.toml（不進 git，dev 用）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="n2"><g x=8 y=58 w=344 h=42/></c>
<c id="n3n" v="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="eA"><g x=20 y=166 w=220 h=124/></c>
<c id="n3n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=216 y=156 w=30 h=20/></c>
<c id="n3" v="gen/.stamp 的引擎 ref ＝ 第一行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA"><g x=260 y=172 w=260 h=112/></c>
<c id="n3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=496 y=162 w=30 h=20/></c>
<c id="n6" v="統一提示（Q10 (2)、v2.3 §2）：啟動器發現 gen/.stamp ≠ 引擎 ref → 退出 1 印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」；不自動重寫、不自動續跑；install／upgrade vendor_kit 不受此關" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="eA"><g x=1220 y=181 w=360 h=94/></c>
<c id="n6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=1556 y=171 w=30 h=20/></c>
<c id="nq0" v="是 → 0：不起容器，接著跑原本的 recipe（快路徑）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="eA"><g x=20 y=317 w=220 h=80/></c>
<c id="nq0_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=216 y=307 w=30 h=20/></c>
<c id="nq" v="快路徑：grep 全相符且非 frozen？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA"><g x=260 y=316 w=260 h=81/></c>
<c id="nq_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=496 y=306 w=30 h=20/></c>
<c id="nqr" v="快路徑（Q22）：啟動器只 grep：[tools] 每行 digest == gen/&lt;repo&gt;.stamp 第一行（或 path:&lt;dir&gt;）；gen/tools.just 存在；無 .tmp.&lt;verb&gt;.*.toml；CI 不為真；sync 無參數。全相符 → 0；否則起引擎；每檔 sha256 只在 sync --verify 或 CI 為真才做" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="eA"><g x=1220 y=310 w=360 h=94/></c>
<c id="nqr_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=1556 y=300 w=30 h=20/></c>
<c id="n1i" v="docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA"><g x=280 y=424 w=220 h=112/></c>
<c id="n1i_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=476 y=414 w=30 h=20/></c>
<c id="n6b" v="薄殼重產（v2.2 A、Q10 (2)、Q17）：只由 install 與 upgrade vendor_kit 做；做之前比對現內容 == 上次產物（首行自描述 hash），相同 → 重產，被改過 → 1 列差異不動；sync 永不寫薄殼" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="eA"><g x=1220 y=440 w=360 h=79/></c>
<c id="n6b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=1556 y=430 w=30 h=20/></c>
<c id="n1p" v="無：docker pull &lt;引擎 ref&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA"><g x=460 y=556 w=80 h=79/></c>
<c id="n1p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=516 y=546 w=30 h=20/></c>
<c id="n1g" v="vendor_kit:vN@sha256:…⏎（引擎 image）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="eA"><g x=980 y=574 w=220 h=42/></c>
<c id="n1v" v="覆寫中且 .Id ≠ 記的 image ID？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA"><g x=280 y=655 w=220 h=112/></c>
<c id="n1v_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=476 y=645 w=30 h=20/></c>
<c id="n1x" v="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="eA"><g x=560 y=671 w=240 h=80/></c>
<c id="n1x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=776 y=661 w=30 h=20/></c>
<c id="n1b" v="否：docker run &lt;引擎&gt; resolve sync（永不 -t）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA"><g x=260 y=787 w=280 h=48/></c>
<c id="n1b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA"><g x=516 y=777 w=30 h=20/></c>
<c id="n1z" v="→ 續「sync（1′）」頁：引擎 resolve sync（逐工具）" s="text;fs=12;sc=none;fc=none;fst=1" parent="eA"><g x=560 y=790 w=300 h=42/></c>
<c id="ne1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="n0" target="n1"></c>
<c id="ne2" v="讀" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="n1" target="n2"></c>
<c id="ne3" s="fs=12;exitX=0.464;exitY=1;entryX=0.5;entryY=0" edge="1" source="n1" target="n3"></c>
<c id="ne4" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="n3" target="n3n"></c>
<c id="ne5" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="n3" target="nq"><g x=-0.6/></c>
<c id="ne5q" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="nq" target="nq0"></c>
<c id="ne5n" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="nq" target="n1i"><g x=-0.6/></c>
<c id="ne5p" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="n1i" target="n1p"><g x=-0.68 pts=520,636/></c>
<c id="ne5g" v="拉" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="n1g" target="n1p"></c>
<c id="ne5v" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="n1i" target="n1v"><g x=-0.6/></c>
<c id="ne5pv" s="fs=12;exitX=0.25;exitY=1;entryX=0.5;entryY=0" edge="1" source="n1p" target="n1v"><g x=0.00 pts=500,801;410,801/></c>
<c id="ne5x" v="失敗" s="fs=12;exitX=0.75;exitY=1;entryX=0;entryY=0.5" edge="1" source="n1p" target="n1x"><g x=-0.34 pts=540,867/></c>
<c id="ne5y" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="n1v" target="n1x"></c>
<c id="ne5i" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.464;entryY=0" edge="1" source="n1v" target="n1b"><g x=-0.6/></c>
<c id="ne6" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="n1b" target="n1z"></c>
<c id="p6_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1013 w=200 h=60/></c>
<c id="p6_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1013 w=140 h=64/></c>
<c id="p6_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1021 w=140 h=44/></c>
<c id="p6_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1015 w=190 h=56/></c>
<c id="p6_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1015 w=210 h=56/></c>
<c id="p6_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1023 w=88 h=40/></c>
<c id="p6_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1023 w=170 h=40/></c>
<c id="p6_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1013 w=300 h=60/></c>
<c id="p6_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1081 w=120 h=36/></c>
<c id="p6_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1081 w=150 h=36/></c>
<c id="p6_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1081 w=190 h=36/></c>
<c id="p6_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1081 w=170 h=36/></c>
<c id="p6_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1081 w=170 h=36/></c>
<c id="p6_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1081 w=200 h=36/></c>
<c id="p6_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1071 w=30 h=20/></c>
<c id="p6_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1119 w=200 h=28/></c>
<c id="p6_tk0" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1153 w=150 h=55/></c>
<c id="p6_tv0" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1153 w=610 h=55/></c>
<c id="p6_tk1" v="快路徑（Q22）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1208 w=150 h=71/></c>
<c id="p6_tv1" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &lt;repo&gt; 的 digest == gen/&lt;repo&gt;.stamp 第一行（或 local 覆寫的 path:&lt;dir&gt;）；gen/tools.just 存在；無 .tmp.&lt;verb&gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1208 w=610 h=71/></c>
<c id="p6_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1279 w=150 h=55/></c>
<c id="p6_tv2" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1279 w=610 h=55/></c>
<c id="p6_tk3" v="stdout／stderr／指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1334 w=150 h=40/></c>
<c id="p6_tv3" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1334 w=610 h=40/></c>
<c id="p6_tk4" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1374 w=150 h=71/></c>
<c id="p6_tv4" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1374 w=610 h=71/></c>
<c id="p6_tk5" v="統一提示（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1445 w=150 h=55/></c>
<c id="p6_tv5" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1445 w=610 h=55/></c>
<c id="p6_tk6" v="薄殼／引擎 ref／hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1500 w=150 h=55/></c>
<c id="p6_tv6" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1500 w=610 h=55/></c>
<c id="p6_tk7" v="gen/ 三種檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1555 w=150 h=55/></c>
<c id="p6_tv7" v="gen/tools.just：每個 &lt;ns&gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&lt;repo&gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1555 w=610 h=55/></c>
<c id="p6_tk8" v="materialize／印記／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1610 w=150 h=55/></c>
<c id="p6_tv8" v="把啟動器 docker create/cp 取來的 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 gen/&lt;repo&gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&lt;dir&gt;）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1610 w=610 h=55/></c>
<c id="p6_tk9" v="image tag／digest／image ID／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1153 w=150 h=71/></c>
<c id="p6_tv9" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1153 w=610 h=71/></c>
<c id="p6_tk10" v="verify／sha256" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1224 w=150 h=55/></c>
<c id="p6_tv10" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&lt;repo&gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1224 w=610 h=55/></c>
<c id="p6_tk11" v="metadata／完成標記／落後" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1279 w=150 h=55/></c>
<c id="p6_tv11" v="baseline/&lt;repo&gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&lt;repo&gt; 未完成接入，請執行：just vendor_kit add &lt;repo&gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1279 w=610 h=55/></c>
<c id="p6_tk12" v="mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1334 w=150 h=55/></c>
<c id="p6_tv12" v="mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1334 w=610 h=55/></c>
<c id="p6_tk13" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1389 w=150 h=40/></c>
<c id="p6_tv13" v="指向另一個路徑的捷徑；dev 中的工具 cache/&lt;repo&gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1389 w=610 h=40/></c>
<c id="p6_tk14" v="覆寫兩種（v2.1 B／v2.2 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1429 w=150 h=55/></c>
<c id="p6_tv14" v="引擎覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; → cache 是 symlink，仍查 metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1429 w=610 h=55/></c>
<c id="p6_tk15" v="GHCR／image／daemon／flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1484 w=150 h=40/></c>
<c id="p6_tv15" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1484 w=610 h=40/></c>
<c id="p6_tk16" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1524 w=150 h=55/></c>
<c id="p6_tv16" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1524 w=610 h=55/></c>
</diagram>
<diagram id="v1p6cc" name="流程 v2：sync（1′）引擎 resolve"><c id="title" v="流程 v2：sync（1′）引擎 resolve sync（逐工具；§6、v2.2 A／B／E、v2.3 §3／§4、v2.5 §9、v2.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify 或 CI 為真才做。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="eA2" v="sync 第 1 段續（承「sync（1）」頁）：引擎 resolve sync 不寫任何檔 → 逐工具算待辦 → 無待辦（apply|no）→ 0；有待辦 → 第 2 段見「sync（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=1523/></c>
<c id="eA2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=1556 y=5 w=30 h=20/></c>
<c id="n1e" v="來自「sync（1）」頁：docker run &lt;引擎&gt; resolve sync" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="eA2"><g x=610 y=36 w=300 h=58/></c>
<c id="ncx" v="是 → 1：CI 拒絕本機覆寫（frozen；請先 undev 或勿在 CI 用 local 覆寫）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="eA2"><g x=20 y=114 w=220 h=102/></c>
<c id="ncx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=216 y=104 w=30 h=20/></c>
<c id="nc" v="CI 為真（frozen）且有 local 覆寫？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=124 w=330 h=81/></c>
<c id="nc_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=866 y=114 w=30 h=20/></c>
<c id="nf" v="frozen（CI 為真 = CI 非空且不為 0／false；v2.6 §2）= 只准寫 cache/、gen/；不查最新版；仍拉鎖定版 image；任何需要寫 tracked 檔 → 1（-y 不解除）；升為失敗的警告：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="eA2"><g x=1220 y=126 w=360 h=79/></c>
<c id="nf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=1556 y=116 w=30 h=20/></c>
<c id="nl" v="← 對每個工具重複⏎（範圍 = 全部；先比印記，便宜）" s="text;fs=12;sc=none;fc=none;fst=1" parent="eA2"><g x=980 y=262 w=220 h=42/></c>
<c id="t0" v="path 覆寫（dev 中）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=242 w=250 h=81/></c>
<c id="t0_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=786 y=232 w=30 h=20/></c>
<c id="t0s" v="是：跳過 materialize／verify，仍查 metadata、baseline ↓" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=830 y=236 w=130 h=94/></c>
<c id="t0s_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=226 w=30 h=20/></c>
<c id="t0r" v="覆寫兩種（v2.1 B）：引擎 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID → 啟動器 inspect 驗 ID 後用該本機 image；工具 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; → cache/&lt;repo&gt;/ 是 symlink，跳過 materialize／verify" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="eA2"><g x=1220 y=244 w=360 h=79/></c>
<c id="t0r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=1556 y=234 w=30 h=20/></c>
<c id="t1" v="cache 缺或印記 ≠ 鎖定 digest？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=350 w=250 h=81/></c>
<c id="t1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=786 y=340 w=30 h=20/></c>
<c id="t1y" v="是：列待辦「materialize 鎖定版」（不 verify 舊 cache）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=830 y=351 w=130 h=79/></c>
<c id="t1y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=341 w=30 h=20/></c>
<c id="t2q" v="否 → sync --verify 或 CI 為真？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=451 w=250 h=112/></c>
<c id="t2q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=786 y=441 w=30 h=20/></c>
<c id="t2qn" v="否：不逐檔驗（快）↓" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=830 y=483 w=130 h=48/></c>
<c id="t2qn_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=473 w=30 h=20/></c>
<c id="t2" v="是 → verify：每檔 sha256 ＝ 印記？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=583 w=250 h=112/></c>
<c id="t2n" v="否：列待辦「重裝 + warn（cache 被改過）」" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=830 y=610 w=130 h=57/></c>
<c id="t3a" v="否 → 1：「&lt;repo&gt; 未完成接入，請執行：just vendor_kit add &lt;repo&gt;」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="eA2"><g x=20 y=715 w=220 h=102/></c>
<c id="t3" v="metadata 有完成標記？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=726 w=250 h=81/></c>
<c id="t3r" v="不變量（v2.1 A、v2.5 §9）：自動化不碰使用者的檔 —— sync 不寫 version.toml、初始檔、baseline、薄殼、gen/.stamp；只寫 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp" s="fc=#ffffff;sc=#b85450;fs=12;fst=1" parent="eA2"><g x=1220 y=726 w=360 h=79/></c>
<c id="t3r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=1556 y=716 w=30 h=20/></c>
<c id="t4" v="最後合併版本 ＝ version.toml？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=837 w=250 h=81/></c>
<c id="t4r" v="是 → 1：baseline 落後，印「請在本機執行 just vendor_kit upgrade &lt;repo&gt; -y 後 commit 並 push」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="eA2"><g x=20 y=938 w=220 h=124/></c>
<c id="t4c" v="否（落後）→ CI 為真（frozen）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=960 w=250 h=81/></c>
<c id="t5" v="否：warn「baseline 落後，請 just vendor_kit upgrade &lt;repo&gt;」（繼續）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=560 y=1082 w=300 h=42/></c>
<c id="t6" v="gen/tools.just 缺或與工具清單不符？（全部工具看完後）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eA2"><g x=560 y=1144 w=270 h=143/></c>
<c id="t6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=806 y=1134 w=30 h=20/></c>
<c id="t6y" v="是：列待辦「重生 gen/tools.just」" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eA2"><g x=843 y=1184 w=117 h=63/></c>
<c id="t6y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=1174 w=30 h=20/></c>
<c id="z0" v="resolve 完：產生待辦清單（要拉的 image、要重裝、要重生 gen/tools.just）→ 空 = apply|no" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eA2"><g x=560 y=1307 w=400 h=48/></c>
<c id="z0_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=1297 w=30 h=20/></c>
<c id="z2" v="無待辦（apply|no）→ 0：不起第二個容器 → 接著跑原本的 recipe" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="eA2"><g x=20 y=1375 w=220 h=80/></c>
<c id="z2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=216 y=1365 w=30 h=20/></c>
<c id="z1" v="產生輸入指紋（version.toml、metadata、印記 hash）→ 清單＋指紋＋apply|yes／no 以 stdout 回啟動器" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eA2"><g x=560 y=1391 w=400 h=48/></c>
<c id="z1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eA2"><g x=936 y=1381 w=30 h=20/></c>
<c id="mb" v="有待辦 ↓ 續「sync（2）」頁：啟動器 docker → 引擎 apply sync" s="text;fs=12;sc=none;fc=none;fst=1" parent="eA2"><g x=560 y=1475 w=400 h=42/></c>
<c id="ne6" s="fs=12;exitX=0.383;exitY=1;entryX=0.5;entryY=0" edge="1" source="n1e" target="nc"></c>
<c id="ne7" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="nc" target="ncx"></c>
<c id="ne8" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="nc" target="t0"><g x=0.05 pts=745,382;705,382/></c>
<c id="te0" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t0" target="t0s"></c>
<c id="te1" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t0" target="t1"><g x=-0.6/></c>
<c id="te2" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="t0s" target="t3"><g pts=990,439;990,861;705,861/></c>
<c id="te3" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t1" target="t1y"></c>
<c id="te4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t1" target="t2q"><g x=-0.6/></c>
<c id="te5" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="t1y" target="t3"><g pts=990,546;990,861;705,861/></c>
<c id="te3q" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t2q" target="t2qn"></c>
<c id="te4q" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t2q" target="t2"><g x=-0.6/></c>
<c id="te5q" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="t2qn" target="t3"><g pts=990,663;990,861;705,861/></c>
<c id="te6" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t2" target="t2n"></c>
<c id="te7" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t2" target="t3"><g x=-0.6/></c>
<c id="te8" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="t2n" target="t3"><g pts=990,795;990,861;705,861/></c>
<c id="te9" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="t3" target="t3a"></c>
<c id="te10" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t3" target="t4"><g x=-0.6/></c>
<c id="te11" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t4" target="t4c"><g x=-0.6/></c>
<c id="te12" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="t4c" target="t4r"></c>
<c id="te13" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.417;entryY=0" edge="1" source="t4c" target="t5"><g x=-0.6/></c>
<c id="te14" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0.8;entryY=0" edge="1" source="t4" target="t6"><g pts=990,1034;990,1290;796,1290/></c>
<c id="te15" s="fs=12;exitX=0.45;exitY=1;entryX=0.5;entryY=0" edge="1" source="t5" target="t6"></c>
<c id="te16" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t6" target="t6y"></c>
<c id="te17" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.338;entryY=0" edge="1" source="t6" target="z0"><g x=-0.6/></c>
<c id="te18" s="fs=12;exitX=0.5;exitY=1;entryX=0.854;entryY=0" edge="1" source="t6y" target="z0"></c>
<c id="ze0" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="z0" target="z1"></c>
<c id="ze1" v="無待辦" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="z1" target="z2"></c>
<c id="ze2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="z1" target="mb"></c>
<c id="p6r_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1695 w=200 h=60/></c>
<c id="p6r_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1695 w=140 h=64/></c>
<c id="p6r_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1703 w=140 h=44/></c>
<c id="p6r_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1697 w=190 h=56/></c>
<c id="p6r_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1697 w=210 h=56/></c>
<c id="p6r_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1705 w=88 h=40/></c>
<c id="p6r_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1705 w=170 h=40/></c>
<c id="p6r_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1695 w=300 h=60/></c>
<c id="p6r_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1763 w=200 h=36/></c>
<c id="p6r_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1763 w=120 h=36/></c>
<c id="p6r_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=1763 w=150 h=36/></c>
<c id="p6r_lgx_inv" v="紅粗框：不變量" s="fc=#ffffff;sc=#b85450;fs=12;fst=1"><g x=570 y=1763 w=130 h=36/></c>
<c id="p6r_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=720 y=1763 w=190 h=36/></c>
<c id="p6r_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=930 y=1763 w=170 h=36/></c>
<c id="p6r_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=1763 w=170 h=36/></c>
<c id="p6r_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1310 y=1763 w=200 h=36/></c>
<c id="p6r_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1486 y=1753 w=30 h=20/></c>
<c id="p6r_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1801 w=200 h=28/></c>
<c id="p6r_tk0" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1835 w=150 h=55/></c>
<c id="p6r_tv0" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1835 w=610 h=55/></c>
<c id="p6r_tk1" v="快路徑（Q22）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1890 w=150 h=71/></c>
<c id="p6r_tv1" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &lt;repo&gt; 的 digest == gen/&lt;repo&gt;.stamp 第一行（或 local 覆寫的 path:&lt;dir&gt;）；gen/tools.just 存在；無 .tmp.&lt;verb&gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1890 w=610 h=71/></c>
<c id="p6r_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1961 w=150 h=55/></c>
<c id="p6r_tv2" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1961 w=610 h=55/></c>
<c id="p6r_tk3" v="stdout／stderr／指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2016 w=150 h=40/></c>
<c id="p6r_tv3" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2016 w=610 h=40/></c>
<c id="p6r_tk4" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2056 w=150 h=71/></c>
<c id="p6r_tv4" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2056 w=610 h=71/></c>
<c id="p6r_tk5" v="統一提示（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2127 w=150 h=55/></c>
<c id="p6r_tv5" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2127 w=610 h=55/></c>
<c id="p6r_tk6" v="薄殼／引擎 ref／hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2182 w=150 h=55/></c>
<c id="p6r_tv6" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2182 w=610 h=55/></c>
<c id="p6r_tk7" v="gen/ 三種檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2237 w=150 h=55/></c>
<c id="p6r_tv7" v="gen/tools.just：每個 &lt;ns&gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&lt;repo&gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2237 w=610 h=55/></c>
<c id="p6r_tk8" v="materialize／印記／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2292 w=150 h=55/></c>
<c id="p6r_tv8" v="把啟動器 docker create/cp 取來的 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 gen/&lt;repo&gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&lt;dir&gt;）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2292 w=610 h=55/></c>
<c id="p6r_tk9" v="image tag／digest／image ID／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1835 w=150 h=71/></c>
<c id="p6r_tv9" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1835 w=610 h=71/></c>
<c id="p6r_tk10" v="verify／sha256" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1906 w=150 h=55/></c>
<c id="p6r_tv10" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&lt;repo&gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1906 w=610 h=55/></c>
<c id="p6r_tk11" v="metadata／完成標記／落後" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1961 w=150 h=55/></c>
<c id="p6r_tv11" v="baseline/&lt;repo&gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&lt;repo&gt; 未完成接入，請執行：just vendor_kit add &lt;repo&gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1961 w=610 h=55/></c>
<c id="p6r_tk12" v="mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2016 w=150 h=55/></c>
<c id="p6r_tv12" v="mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2016 w=610 h=55/></c>
<c id="p6r_tk13" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2071 w=150 h=40/></c>
<c id="p6r_tv13" v="指向另一個路徑的捷徑；dev 中的工具 cache/&lt;repo&gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2071 w=610 h=40/></c>
<c id="p6r_tk14" v="覆寫兩種（v2.1 B／v2.2 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2111 w=150 h=55/></c>
<c id="p6r_tv14" v="引擎覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; → cache 是 symlink，仍查 metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2111 w=610 h=55/></c>
<c id="p6r_tk15" v="GHCR／image／daemon／flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2166 w=150 h=40/></c>
<c id="p6r_tv15" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2166 w=610 h=40/></c>
<c id="p6r_tk16" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2206 w=150 h=55/></c>
<c id="p6r_tv16" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2206 w=610 h=55/></c>
</diagram>
<diagram id="v1p6c" name="流程 v2：sync（2）apply"><c id="title" v="流程 v2：sync（2）第 2 段 apply（§6、v2.3 §3／§4、v2.5 §9）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q10 (2)、v2.3 §2）：薄殼／gen 與 version.toml 引擎不符 → 啟動器只回 1 提示 just vendor_kit upgrade vendor_kit（需要人動作）；install／upgrade vendor_kit 跳過這關。已定（v2.5 §9、Q22）：sync 可寫範圍 = cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp；啟動器先 grep 快路徑（全相符不起容器）；每檔 sha256 只在 sync --verify 或 CI 為真才做。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="eB" v="sync 第 2 段（承「sync（1′）」頁：有待辦才跑）：啟動器對每個要拉的 image inspect → 無才 pull → create → cp → rm → docker run 引擎 apply sync；只寫 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=1024/></c>
<c id="eB_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=1556 y=5 w=30 h=20/></c>
<c id="m00" v="來自「sync（1′）」頁：有待辦（resolve 的 stdout 清單，apply|yes）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="eB"><g x=260 y=36 w=280 h=80/></c>
<c id="m0a" v="對每個要拉的 image：docker image inspect 本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="eB"><g x=260 y=136 w=170 h=206/></c>
<c id="m0a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=406 y=126 w=30 h=20/></c>
<c id="m0p" v="無：docker pull" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eB"><g x=440 y=362 w=100 h=48/></c>
<c id="m0p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=516 y=352 w=30 h=20/></c>
<c id="m0g" v="&lt;repo&gt;-dist@digest⏎（鎖定版；多架構 index）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="eB"><g x=980 y=365 w=220 h=42/></c>
<c id="m0b" v="docker create &lt;img&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eB"><g x=260 y=430 w=280 h=40/></c>
<c id="m0b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=516 y=420 w=30 h=20/></c>
<c id="m0c" v="docker cp c:/dist/. &lt;tmp&gt;/&lt;repo&gt;/（主機暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eB"><g x=260 y=490 w=280 h=48/></c>
<c id="m0c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=516 y=480 w=30 h=20/></c>
<c id="m0d" v="docker rm 該容器" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eB"><g x=260 y=558 w=280 h=40/></c>
<c id="m0d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=516 y=548 w=30 h=20/></c>
<c id="m1" v="docker run … -v &lt;tmp&gt;:/dist:ro &lt;引擎&gt; apply sync" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="eB"><g x=260 y=618 w=280 h=48/></c>
<c id="m1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=516 y=608 w=30 h=20/></c>
<c id="m2a" v="apply：flock 專案目錄（60 秒；VENDOR_KIT_NO_LOCK=1 可關）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=622 w=400 h=40/></c>
<c id="m2a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=612 w=30 h=20/></c>
<c id="m2b" v="重驗 resolve 的輸入指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=695 w=240 h=40/></c>
<c id="m2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=776 y=685 w=30 h=20/></c>
<c id="m2x" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="eB"><g x=820 y=686 w=140 h=58/></c>
<c id="m2x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=676 w=30 h=20/></c>
<c id="m3" v="materialize／重裝（每個待辦工具）：/dist/&lt;repo&gt; 展開到暫存目錄" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=764 w=400 h=48/></c>
<c id="m3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=754 w=30 h=20/></c>
<c id="m3c" v="暫存 → cache/&lt;repo&gt;/（原子替換）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=832 w=400 h=40/></c>
<c id="m3c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=822 w=30 h=20/></c>
<c id="m3f" v="cache/&lt;repo&gt;/（重寫，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="eB"><g x=1220 y=832 w=360 h=40/></c>
<c id="m3b" v="寫印記 gen/&lt;repo&gt;.stamp（第一行 index digest，之後每檔 sha256）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=892 w=400 h=48/></c>
<c id="m3b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=882 w=30 h=20/></c>
<c id="m3bf" v="gen/&lt;repo&gt;.stamp（重寫，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="eB"><g x=1220 y=896 w=360 h=40/></c>
<c id="m7" v="0：接著跑原本的 recipe" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="eB"><g x=20 y=960 w=220 h=58/></c>
<c id="m5" v="重生 gen/tools.just（待辦有它時；每個 &lt;ns&gt;.just 一行 mod?）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="eB"><g x=560 y=965 w=400 h=48/></c>
<c id="m5_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="eB"><g x=936 y=955 w=30 h=20/></c>
<c id="m5f" v="gen/tools.just（不進 git；gen/.stamp 不動）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="eB"><g x=1220 y=969 w=360 h=40/></c>
<c id="me0" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m00" target="m0a"><g x=0.00 pts=420,282;365,282/></c>
<c id="me0n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="m0a" target="m0p"><g x=-0.67 pts=510,395/></c>
<c id="me0g" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m0g" target="m0p"></c>
<c id="me0y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.304;entryY=0" edge="1" source="m0a" target="m0b"><g x=-0.6/></c>
<c id="me0p" s="fs=12;exitX=0.5;exitY=1;entryX=0.821;entryY=0" edge="1" source="m0p" target="m0b"></c>
<c id="me0c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m0b" target="m0c"></c>
<c id="me0d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m0c" target="m0d"></c>
<c id="me1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m0d" target="m1"></c>
<c id="me2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m1" target="m2a"></c>
<c id="me2b" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="m2a" target="m2b"></c>
<c id="me2x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m2b" target="m2x"></c>
<c id="me3" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="m2b" target="m3"></c>
<c id="me3c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m3" target="m3c"></c>
<c id="me4" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m3c" target="m3f"></c>
<c id="me4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m3c" target="m3b"></c>
<c id="me4f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m3b" target="m3bf"></c>
<c id="me5" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m3b" target="m5"></c>
<c id="me12" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m5" target="m5f"></c>
<c id="me15" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m5" target="m7"></c>
<c id="p6c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1196 w=200 h=60/></c>
<c id="p6c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1196 w=140 h=64/></c>
<c id="p6c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1204 w=140 h=44/></c>
<c id="p6c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1198 w=190 h=56/></c>
<c id="p6c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1198 w=210 h=56/></c>
<c id="p6c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1206 w=88 h=40/></c>
<c id="p6c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1206 w=170 h=40/></c>
<c id="p6c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1196 w=300 h=60/></c>
<c id="p6c_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1264 w=200 h=36/></c>
<c id="p6c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1264 w=120 h=36/></c>
<c id="p6c_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1264 w=190 h=36/></c>
<c id="p6c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1264 w=170 h=36/></c>
<c id="p6c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1264 w=170 h=36/></c>
<c id="p6c_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1264 w=200 h=36/></c>
<c id="p6c_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1254 w=30 h=20/></c>
<c id="p6c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1302 w=200 h=28/></c>
<c id="p6c_tk0" v="sync" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1336 w=150 h=55/></c>
<c id="p6c_tv0" v="工具 recipe 的前置（工具模組內私有 _sync recipe 相依；vendor_kit 自身動詞不前置）：可寫範圍只有 cache/&lt;repo&gt;/、gen/tools.just、gen/&lt;repo&gt;.stamp（永不寫薄殼、永不寫 gen/.stamp）；範圍 = 全部工具；sync（無參數）先走快路徑" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1336 w=610 h=55/></c>
<c id="p6c_tk1" v="快路徑（Q22）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1391 w=150 h=71/></c>
<c id="p6c_tv1" v="啟動器只用 grep 比對：gen/.stamp 第一行 == version.toml 引擎 ref；[tools] 每個 &lt;repo&gt; 的 digest == gen/&lt;repo&gt;.stamp 第一行（或 local 覆寫的 path:&lt;dir&gt;）；gen/tools.just 存在；無 .tmp.&lt;verb&gt;.*.toml；非 frozen。全相符 → 不起容器、0；任一不符或 CI 為真 → 起引擎 resolve sync" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1391 w=610 h=71/></c>
<c id="p6c_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1462 w=150 h=55/></c>
<c id="p6c_tv2" v="同一動詞兩段：resolve 只讀只算，把待辦清單（要拉哪些 image、要重裝什麼、要不要重生 tools.just）＋輸入指紋以 stdout 一行一項回啟動器（vk-resolve/1：| 分隔、末行 end|N）；apply 拿 flock 後重驗指紋才寫；無待辦 → apply|no" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1462 w=610 h=55/></c>
<c id="p6c_tk3" v="stdout／stderr／指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1517 w=150 h=40/></c>
<c id="p6c_tv3" v="stdout = 給啟動器讀的結果（固定欄位）；stderr = 給人看的診斷；指紋 = resolve 讀過的 version.toml、metadata 等的 hash，apply 重驗，不同 → 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1517 w=610 h=40/></c>
<c id="p6c_tk4" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1557 w=150 h=71/></c>
<c id="p6c_tv4" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感；GitHub/GitLab 都設 CI=true；check.sh 自己 export CI=1）。frozen 下只准寫 cache/、gen/；不查最新版（只拉鎖定版）；任何需要寫 tracked 檔的情況 → 1 印清單（-y 不解除）；警告升為失敗：薄殼不符、baseline 落後、未完成接入、任何 version.local.toml 覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1557 w=610 h=71/></c>
<c id="p6c_tk5" v="統一提示（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1628 w=150 h=55/></c>
<c id="p6c_tv5" v="啟動器發現引擎 ref ≠ gen/.stamp → 不重寫，退出 1 固定印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」（需要人動作，橙）；install／upgrade vendor_kit 跳過這關" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1628 w=610 h=55/></c>
<c id="p6c_tk6" v="薄殼／引擎 ref／hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1683 w=150 h=55/></c>
<c id="p6c_tv6" v="薄殼 = .vendor_kit/ 裡 vendor_kit 自己的 tracked 檔（entry.just、vendor.just、.gitignore、ci/check.sh；首行自描述）；引擎 ref = version.toml 第一行的引擎 image 版本；hash = 內容指紋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1683 w=610 h=55/></c>
<c id="p6c_tk7" v="gen/ 三種檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1738 w=150 h=55/></c>
<c id="p6c_tv7" v="gen/tools.just：每個 &lt;ns&gt;.just 一行 mod?，sync／add／remove／upgrade 重生；gen/.stamp：只記引擎 ref，只由 install／upgrade vendor_kit 寫；gen/&lt;repo&gt;.stamp：每工具印記（第一行 index digest 或 path:，之後每檔 sha256）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1738 w=610 h=55/></c>
<c id="p6c_tk8" v="materialize／印記／index digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1793 w=150 h=55/></c>
<c id="p6c_tv8" v="把啟動器 docker create/cp 取來的 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/；印記 gen/&lt;repo&gt;.stamp 第一行 = index digest（多架構 image 總目錄的 sha256 ID；dev 時是 path:&lt;dir&gt;）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1793 w=610 h=55/></c>
<c id="p6c_tk9" v="image tag／digest／image ID／image inspect" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1336 w=150 h=71/></c>
<c id="p6c_tv9" v="tag = 人看的版本名（可重 build 換內容）；digest = 從倉庫拉來的內容 sha256（鎖定用）；image ID = 本機 image 內容的 ID；啟動器每次 docker run 前先 docker image inspect：本機有 → 不 pull；引擎覆寫時 .Id 必須等於 version.local.toml 記的 image ID（同 tag 重 build 才會被發現），否則 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1336 w=610 h=71/></c>
<c id="p6c_tk10" v="verify／sha256" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1407 w=150 h=55/></c>
<c id="p6c_tv10" v="sha256 = 檔案內容算出的指紋；verify 把 cache/&lt;repo&gt;/ 每個檔的 sha256 跟印記比；不符 → 重裝 + warn（使用者不可改 cache/）；只在 sync --verify、CI 為真、或版本變動那次做；cache 缺或印記變了就直接重裝，不 verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1407 w=610 h=55/></c>
<c id="p6c_tk11" v="metadata／完成標記／落後" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1462 w=150 h=55/></c>
<c id="p6c_tv11" v="baseline/&lt;repo&gt;/.vendor_kit.toml：無完成標記 = add 沒做完 → 1「&lt;repo&gt; 未完成接入，請執行：just vendor_kit add &lt;repo&gt;」；最後合併版本 ≠ version.toml = 有人只改了 version.toml → 提示 upgrade（CI 為真 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1462 w=610 h=55/></c>
<c id="p6c_tk12" v="mod?／recipe" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1517 w=150 h=55/></c>
<c id="p6c_tv12" v="mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …）的那一行；帶問號 = 檔不在也不掛、其他 recipe 與修復入口仍可跑（mod 指向缺檔會讓所有 just 呼叫掛掉）；recipe = justfile 裡的一條指令；gen/tools.just 只有 mod? 行、沒有 recipe" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1517 w=610 h=55/></c>
<c id="p6c_tk13" v="symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1572 w=150 h=40/></c>
<c id="p6c_tv13" v="指向另一個路徑的捷徑；dev 中的工具 cache/&lt;repo&gt;/ 不放檔案，而是指到本機工具 repo 的 dist/，所以 sync 跳過它的 materialize／verify" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1572 w=610 h=40/></c>
<c id="p6c_tk14" v="覆寫兩種（v2.1 B／v2.2 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1612 w=150 h=55/></c>
<c id="p6c_tv14" v="引擎覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID → 啟動器 docker image inspect 驗 ID 後用該本機 image（不 pull）；工具覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; → cache 是 symlink，仍查 metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1612 w=610 h=55/></c>
<c id="p6c_tk15" v="GHCR／image／daemon／flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1667 w=150 h=40/></c>
<c id="p6c_tv15" v="GHCR = GitHub 容器倉庫；image = 打包好的 dist/；daemon = 主機的 docker 服務；flock = 專案目錄鎖（60 秒），鎖在引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1667 w=610 h=40/></c>
<c id="p6c_tk16" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1707 w=150 h=55/></c>
<c id="p6c_tv16" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1707 w=610 h=55/></c>
</diagram>
<diagram id="v1p7" name="流程 v2：upgrade ── A. Renovate 路徑"><c id="title" v="流程 v2：upgrade ── A. Renovate 路徑（§2／§7、v2.2 D、v2.3 §7、v2.5 §1／§7）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=97 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=97 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=97 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=97 w=280 h=28/></c>
<c id="uA" v="A. Renovate 路徑（下游自選，vendor_kit 不出 bot）：機器人只改 version.toml 一行；PR 的 CI 以新版跑完整流程；baseline 落後 → PR 紅（需要人補合併）；補合併在 PR 分支上完成、CI 綠後才 merge" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=920/></c>
<c id="uA_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uA"><g x=1556 y=5 w=30 h=20/></c>
<c id="a0" v="Renovate 定期查 GHCR" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uA"><g x=270 y=36 w=160 h=58/></c>
<c id="a1" v="&lt;repo&gt;-dist⏎出新 tag@digest" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="uA"><g x=1100 y=44 w=180 h=42/></c>
<c id="a2" v="開 PR（獨立分支）：只改 version.toml 該工具一行（tag@digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=270 y=114 w=160 h=57/></c>
<c id="a3" v="version.toml（PR 分支）⏎&lt;repo&gt; 行 = 新 tag@digest" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uA"><g x=1300 y=122 w=280 h=42/></c>
<c id="a4a" v="PR 的 CI 呼叫 .vendor_kit/ci/check.sh（以新版跑完整流程）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=191 w=220 h=57/></c>
<c id="a4r" v="一行改動本身不可能出錯，不構成通過依據⏎→ PR 的 CI 必須以新版跑完整流程" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="uA"><g x=720 y=198 w=360 h=42/></c>
<c id="a4b" v="check.sh ①：sync（CI 為真 → frozen；export CI=1）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=268 w=220 h=42/></c>
<c id="a5" v="1 → PR 紅：需要人補合併（印「本機 upgrade &lt;repo&gt; -y 後 push」）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uA"><g x=20 y=330 w=220 h=102/></c>
<c id="a5_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uA"><g x=216 y=320 w=30 h=20/></c>
<c id="a4q" v="baseline 落後？（最後合併版本 ≠ version.toml）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uA"><g x=720 y=340 w=360 h=81/></c>
<c id="a4q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uA"><g x=1056 y=330 w=30 h=20/></c>
<c id="a4c" v="否：check.sh ②：verify" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=452 w=220 h=40/></c>
<c id="a4d" v="check.sh ③：upgrade --dry-run" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=512 w=220 h=42/></c>
<c id="a4e1" v="check.sh ④：工具測試" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=582 w=220 h=40/></c>
<c id="a6a" v="PR 作者本機：切到 PR 分支" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=20 y=582 w=220 h=40/></c>
<c id="a6a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uA"><g x=216 y=572 w=30 h=20/></c>
<c id="a9" v="Renovate 預設不動有人推過的分支；PR body 加警告：勿勾 rebase（會蓋掉人補的合併 commit）。vendor_kit 無 bot。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="uA"><g x=1300 y=574 w=280 h=57/></c>
<c id="a4e2" v="check.sh ⑤：專案測試" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=470 y=662 w=220 h=40/></c>
<c id="a6b" v="upgrade &lt;repo&gt; -y（走「B. 手動路徑（1）」頁，固定補到 PR 鎖定版）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=20 y=651 w=220 h=63/></c>
<c id="a6b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uA"><g x=216 y=641 w=30 h=20/></c>
<c id="a6c" v="commit（合併結果）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=20 y=734 w=220 h=40/></c>
<c id="a6d" v="push 到 PR 分支" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=20 y=795 w=220 h=40/></c>
<c id="a7" v="PR 分支 CI 再跑完整流程（同上）→ 綠" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uA"><g x=460 y=794 w=150 h=42/></c>
<c id="a8" v="merge PR（CI 綠後才 merge）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uA"><g x=260 y=856 w=180 h=58/></c>
<c id="ae1" v="查" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a0" target="a1"></c>
<c id="ae2" v="有新版" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a1" target="a2"><g x=0.01 pts=1210,245;370,245/></c>
<c id="ae3" v="改一行" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a2" target="a3"></c>
<c id="ae4" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a2" target="a4a"><g x=0.00 pts=370,322;600,322/></c>
<c id="ae4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4a" target="a4b"></c>
<c id="ae4q" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4b" target="a4q"><g x=-0.03 pts=600,461;920,461/></c>
<c id="ae5" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="a4q" target="a5"></c>
<c id="ae5n" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4q" target="a4c"><g x=0.03 pts=920,583;600,583/></c>
<c id="ae5c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4c" target="a4d"></c>
<c id="ae5d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4d" target="a4e1"></c>
<c id="ae5e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a4e1" target="a4e2"></c>
<c id="ae6" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a5" target="a6a"></c>
<c id="ae6b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a6a" target="a6b"></c>
<c id="ae6c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a6b" target="a6c"></c>
<c id="ae6d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a6c" target="a6d"></c>
<c id="ae7" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="a6d" target="a7"></c>
<c id="ae8" v="綠" s="fs=12;exitX=0.9;exitY=1;entryX=1;entryY=0.5" edge="1" source="a4e2" target="a8"><g x=-0.56 pts=688,1026/></c>
<c id="ae9" v="綠" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="a7" target="a8"><g x=0.00 pts=555,987;370,987/></c>
<c id="p7_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1077 w=200 h=60/></c>
<c id="p7_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1077 w=140 h=64/></c>
<c id="p7_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1085 w=140 h=44/></c>
<c id="p7_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1079 w=190 h=56/></c>
<c id="p7_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1079 w=210 h=56/></c>
<c id="p7_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1087 w=88 h=40/></c>
<c id="p7_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1087 w=170 h=40/></c>
<c id="p7_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1077 w=300 h=60/></c>
<c id="p7_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1145 w=120 h=36/></c>
<c id="p7_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1145 w=150 h=36/></c>
<c id="p7_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1145 w=190 h=36/></c>
<c id="p7_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1145 w=170 h=36/></c>
<c id="p7_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1145 w=170 h=36/></c>
<c id="p7_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1145 w=200 h=36/></c>
<c id="p7_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1135 w=30 h=20/></c>
<c id="p7_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1183 w=200 h=28/></c>
<c id="p7_tk0" v="Renovate／regex manager" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1217 w=150 h=40/></c>
<c id="p7_tv0" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1217 w=610 h=40/></c>
<c id="p7_tk1" v="PR／commit／push／rebase／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1257 w=150 h=40/></c>
<c id="p7_tv1" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1257 w=610 h=40/></c>
<c id="p7_tk2" v="check.sh／CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1297 w=150 h=55/></c>
<c id="p7_tv2" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1297 w=610 h=55/></c>
<c id="p7_tk3" v="baseline 落後／待合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1352 w=150 h=40/></c>
<c id="p7_tv3" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1352 w=610 h=40/></c>
<c id="p7_tk4" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1392 w=150 h=55/></c>
<c id="p7_tv4" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1392 w=610 h=55/></c>
<c id="p7_tk5" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1447 w=150 h=40/></c>
<c id="p7_tv5" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1447 w=610 h=40/></c>
<c id="p7_tk6" v="dev 覆寫／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1487 w=150 h=40/></c>
<c id="p7_tv6" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &lt;repo&gt;／remove &lt;repo&gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1487 w=610 h=40/></c>
<c id="p7_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1527 w=150 h=40/></c>
<c id="p7_tv7" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/（暫存 → 原子替換）；印記 gen/&lt;repo&gt;.stamp 第一行 index digest，之後每檔 sha256" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1527 w=610 h=40/></c>
<c id="p7_tk8" v="B／D／N、逐檔判斷後詢問" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1567 w=150 h=86/></c>
<c id="p7_tv8" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&lt;repo&gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1567 w=610 h=86/></c>
<c id="p7_tk9" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1217 w=150 h=71/></c>
<c id="p7_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1217 w=610 h=71/></c>
<c id="p7_tk10" v="gen／mod?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1288 w=150 h=40/></c>
<c id="p7_tv10" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1288 w=610 h=40/></c>
<c id="p7_tk11" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1328 w=150 h=55/></c>
<c id="p7_tv11" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1328 w=610 h=55/></c>
<c id="p7_tk12" v="CRLF／append 行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1383 w=150 h=40/></c>
<c id="p7_tv12" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1383 w=610 h=40/></c>
<c id="p7_tk13" v="GHCR／image／tag@digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1423 w=150 h=40/></c>
<c id="p7_tv13" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1423 w=610 h=40/></c>
<c id="p7_tk14" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1463 w=150 h=55/></c>
<c id="p7_tv14" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1463 w=610 h=55/></c>
</diagram>
<diagram id="v1p7c" name="流程 v2：upgrade ── B. 手動路徑（1）resolve → docker"><c id="title" v="流程 v2：upgrade ── B. 手動路徑（1）前置（§2、v2.2 C／D、v2.5 §2／§3／§6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=97 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=97 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=97 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=97 w=280 h=28/></c>
<c id="uB" v="B. 手動路徑：just vendor_kit upgrade [&lt;repo&gt;[@&lt;tag&gt;]]（不帶 repo = 全部含 vendor_kit 自身，先完整預檢再動；@&lt;tag&gt; 限單一 repo）= resolve（不寫）→ 啟動器 docker；apply 前置見「B（1′）」頁、寫入段見「B（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1511/></c>
<c id="uB_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1556 y=5 w=30 h=20/></c>
<c id="b0" v="just vendor_kit upgrade &lt;repo&gt;[@&lt;tag&gt;]（-y、--dry-run）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uB"><g x=20 y=36 w=220 h=102/></c>
<c id="b1" v="docker run &lt;引擎&gt; resolve upgrade &lt;repo&gt;⏎（啟動器不鎖）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=460 y=56 w=240 h=63/></c>
<c id="b1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=676 y=46 w=30 h=20/></c>
<c id="b1x" v="是 → 1：請先 undev &lt;repo&gt;" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB"><g x=20 y=170 w=220 h=58/></c>
<c id="b1x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=216 y=160 w=30 h=20/></c>
<c id="b1q" v="&lt;repo&gt; 在 dev 覆寫中？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=720 y=158 w=280 h=81/></c>
<c id="b1q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=976 y=148 w=30 h=20/></c>
<c id="b2c" v="是 → 2：先解完衝突再重跑" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB"><g x=20 y=266 w=220 h=58/></c>
<c id="b2c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=216 y=256 w=30 h=20/></c>
<c id="b2" v="(0) 衝突檔仍含我們的標籤？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=720 y=270 w=360 h=50/></c>
<c id="b2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1056 y=260 w=30 h=20/></c>
<c id="b2n" v="標籤 = 我們自己產的 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 等；檔案失蹤不算已解；resolve 只偵測，「清除已解的衝突狀態」在 apply 內、建日誌之後（v2.5 §3）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="uB"><g x=1300 y=259 w=280 h=73/></c>
<c id="b5" v="否 → 1：無 baseline，請先 add &lt;repo&gt;" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB"><g x=20 y=352 w=220 h=58/></c>
<c id="b4" v="有 baseline/&lt;repo&gt;/？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=730 y=356 w=340 h=50/></c>
<c id="b6" v="(1) 有待合併？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=720 y=430 w=170 h=81/></c>
<c id="b6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=866 y=420 w=30 h=20/></c>
<c id="b6y" v="是：目標版 = B（version.toml 那版），補到就停，不查最新" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=910 y=531 w=170 h=63/></c>
<c id="b6y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1056 y=521 w=30 h=20/></c>
<c id="b7a" v="否 → @&lt;tag&gt; 指定？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=720 y=614 w=170 h=112/></c>
<c id="b7a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=866 y=604 w=30 h=20/></c>
<c id="b7t" v="是：目標版 = @&lt;tag&gt;（比現版舊 → warn 仍執行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=910 y=646 w=170 h=48/></c>
<c id="b7t_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1056 y=636 w=30 h=20/></c>
<c id="b7b" v="否 → CI 為真（frozen）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=720 y=746 w=170 h=112/></c>
<c id="b7b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=866 y=736 w=30 h=20/></c>
<c id="b7z" v="是：不查最新；目標版 = 鎖定版（無事可做）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=910 y=778 w=170 h=48/></c>
<c id="b7z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1056 y=768 w=30 h=20/></c>
<c id="b7c" v="否：(2) 查 registry 最新正式版 = 目標版" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=720 y=878 w=170 h=48/></c>
<c id="b7c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=866 y=868 w=30 h=20/></c>
<c id="b7s" v="resolve 完 → stdout：目標 tag@digest ＋ 輸入指紋（version.toml、metadata、要動的使用者檔 hash、鎖定 digest）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB"><g x=720 y=946 w=360 h=63/></c>
<c id="b7s_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=1056 y=936 w=30 h=20/></c>
<c id="b8a" v="docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB"><g x=460 y=1029 w=170 h=143/></c>
<c id="b8a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=606 y=1019 w=30 h=20/></c>
<c id="b8p" v="無：docker pull" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=630 y=1192 w=70 h=63/></c>
<c id="b8p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=676 y=1182 w=30 h=20/></c>
<c id="b8g" v="&lt;repo&gt;-dist⏎目標 tag@digest" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="uB"><g x=1100 y=1202 w=180 h=42/></c>
<c id="b8b" v="docker create &lt;img&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=460 y=1275 w=240 h=40/></c>
<c id="b8b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=676 y=1265 w=30 h=20/></c>
<c id="b8c" v="docker cp c:/dist/. &lt;tmp&gt;/&lt;repo&gt;/（主機暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=460 y=1335 w=240 h=48/></c>
<c id="b8c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=676 y=1325 w=30 h=20/></c>
<c id="b8d" v="docker rm 該容器" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB"><g x=460 y=1403 w=240 h=40/></c>
<c id="b8d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB"><g x=676 y=1393 w=30 h=20/></c>
<c id="b8z" v="↓ 續「B（1′）」頁：docker run 引擎 apply upgrade → 前置檢查" s="text;fs=12;sc=none;fc=none;fst=1" parent="uB"><g x=460 y=1463 w=240 h=42/></c>
<c id="be1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b0" target="b1"></c>
<c id="be1q" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b1" target="b1q"><g x=0.06 pts=600,289;880,289/></c>
<c id="be1x" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b1q" target="b1x"></c>
<c id="be2" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b1q" target="b2"><g x=-0.16 pts=880,390;920,390/></c>
<c id="be3" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b2" target="b2c"></c>
<c id="be4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b2" target="b4"><g x=-0.6/></c>
<c id="be5" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b4" target="b5"></c>
<c id="be6" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b4" target="b6"><g x=0.03 pts=920,561;825,561/></c>
<c id="be7" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b6" target="b6y"></c>
<c id="be8" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b6" target="b7a"><g x=-0.6/></c>
<c id="be8t" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b7a" target="b7t"></c>
<c id="be8b" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b7a" target="b7b"><g x=-0.6/></c>
<c id="be8z" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b7b" target="b7z"></c>
<c id="be8c" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b7b" target="b7c"><g x=-0.6/></c>
<c id="be9" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b6y" target="b7s"><g pts=1110,704;1110,1077;1064,1077/></c>
<c id="be9t" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b7t" target="b7s"><g pts=1110,811;1110,1077;1064,1077/></c>
<c id="be9z" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b7z" target="b7s"><g pts=1110,943;1110,1077;1064,1077/></c>
<c id="be10" s="fs=12;exitX=0.5;exitY=1;entryX=0.236;entryY=0" edge="1" source="b7c" target="b7s"></c>
<c id="be11" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b7s" target="b8a"><g x=0.00 pts=920,1160;565,1160/></c>
<c id="be11n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="b8a" target="b8p"><g x=-0.72 pts=685,1242/></c>
<c id="be12" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b8g" target="b8p"></c>
<c id="be11y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.354;entryY=0" edge="1" source="b8a" target="b8b"><g x=-0.6/></c>
<c id="be11p" s="fs=12;exitX=0.5;exitY=1;entryX=0.854;entryY=0" edge="1" source="b8p" target="b8b"></c>
<c id="be12c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b8b" target="b8c"></c>
<c id="be12d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b8c" target="b8d"></c>
<c id="be13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b8d" target="b8z"></c>
<c id="p7c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1668 w=200 h=60/></c>
<c id="p7c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1668 w=140 h=64/></c>
<c id="p7c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1676 w=140 h=44/></c>
<c id="p7c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1670 w=190 h=56/></c>
<c id="p7c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1670 w=210 h=56/></c>
<c id="p7c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1678 w=88 h=40/></c>
<c id="p7c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1678 w=170 h=40/></c>
<c id="p7c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1668 w=300 h=60/></c>
<c id="p7c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1736 w=120 h=36/></c>
<c id="p7c_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1736 w=190 h=36/></c>
<c id="p7c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1736 w=170 h=36/></c>
<c id="p7c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1736 w=170 h=36/></c>
<c id="p7c_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1736 w=200 h=36/></c>
<c id="p7c_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1726 w=30 h=20/></c>
<c id="p7c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1774 w=200 h=28/></c>
<c id="p7c_tk0" v="Renovate／regex manager" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1808 w=150 h=40/></c>
<c id="p7c_tv0" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1808 w=610 h=40/></c>
<c id="p7c_tk1" v="PR／commit／push／rebase／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1848 w=150 h=40/></c>
<c id="p7c_tv1" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1848 w=610 h=40/></c>
<c id="p7c_tk2" v="check.sh／CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1888 w=150 h=55/></c>
<c id="p7c_tv2" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1888 w=610 h=55/></c>
<c id="p7c_tk3" v="baseline 落後／待合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1943 w=150 h=40/></c>
<c id="p7c_tv3" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1943 w=610 h=40/></c>
<c id="p7c_tk4" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1983 w=150 h=55/></c>
<c id="p7c_tv4" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1983 w=610 h=55/></c>
<c id="p7c_tk5" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2038 w=150 h=40/></c>
<c id="p7c_tv5" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2038 w=610 h=40/></c>
<c id="p7c_tk6" v="dev 覆寫／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2078 w=150 h=40/></c>
<c id="p7c_tv6" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &lt;repo&gt;／remove &lt;repo&gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2078 w=610 h=40/></c>
<c id="p7c_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2118 w=150 h=40/></c>
<c id="p7c_tv7" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/（暫存 → 原子替換）；印記 gen/&lt;repo&gt;.stamp 第一行 index digest，之後每檔 sha256" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2118 w=610 h=40/></c>
<c id="p7c_tk8" v="B／D／N、逐檔判斷後詢問" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2158 w=150 h=86/></c>
<c id="p7c_tv8" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&lt;repo&gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2158 w=610 h=86/></c>
<c id="p7c_tk9" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1808 w=150 h=71/></c>
<c id="p7c_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1808 w=610 h=71/></c>
<c id="p7c_tk10" v="gen／mod?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1879 w=150 h=40/></c>
<c id="p7c_tv10" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1879 w=610 h=40/></c>
<c id="p7c_tk11" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1919 w=150 h=55/></c>
<c id="p7c_tv11" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1919 w=610 h=55/></c>
<c id="p7c_tk12" v="CRLF／append 行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1974 w=150 h=40/></c>
<c id="p7c_tv12" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1974 w=610 h=40/></c>
<c id="p7c_tk13" v="GHCR／image／tag@digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2014 w=150 h=40/></c>
<c id="p7c_tv13" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2014 w=610 h=40/></c>
<c id="p7c_tk14" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2054 w=150 h=55/></c>
<c id="p7c_tv14" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2054 w=610 h=55/></c>
</diagram>
<diagram id="v1p7ccc" name="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置"><c id="title" v="流程 v2：upgrade ── B. 手動路徑（1′）apply 前置（§2、v2.2 C／D、v2.5 §2／§3／§5、v2.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=97 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=97 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=97 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=97 w=280 h=28/></c>
<c id="uB1" v="B（1′）apply 前置（承「B（1）」頁：目標版 image 已展開到暫存）：拿鎖 → 重驗指紋 → dest／命名空間檢查 → 逐檔判斷 → frozen → dry-run 分支；寫入段見「B（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=901/></c>
<c id="uB1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1556 y=5 w=30 h=20/></c>
<c id="b8e" v="來自「B（1）」頁：目標版 /dist 已在主機暫存" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="uB1"><g x=460 y=36 w=240 h=58/></c>
<c id="b9" v="docker run … -v &lt;tmp&gt;:/dist:ro &lt;引擎&gt; apply upgrade &lt;repo&gt;（--dry-run 原樣轉發）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB1"><g x=460 y=114 w=240 h=63/></c>
<c id="b9_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=676 y=104 w=30 h=20/></c>
<c id="b10a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB1"><g x=720 y=126 w=360 h=40/></c>
<c id="b10a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1056 y=116 w=30 h=20/></c>
<c id="b10b" v="重驗 resolve 的輸入指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB1"><g x=720 y=206 w=220 h=40/></c>
<c id="b10b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=916 y=196 w=30 h=20/></c>
<c id="b10x" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB1"><g x=950 y=197 w=130 h=58/></c>
<c id="b10x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1056 y=187 w=30 h=20/></c>
<c id="b10dx" v="否 → 1：dest 不合法" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uB1"><g x=20 y=311 w=220 h=40/></c>
<c id="b10dx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=216 y=301 w=30 h=20/></c>
<c id="b10d" v="新版 init.toml 的 dest 全部合法？（任何寫入前；規則同「add（1）」頁）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB1"><g x=720 y=275 w=340 h=112/></c>
<c id="b10d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1036 y=265 w=30 h=20/></c>
<c id="b10nx" v="是 → 1：命名空間撞名" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uB1"><g x=20 y=474 w=220 h=40/></c>
<c id="b10nx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=216 y=464 w=30 h=20/></c>
<c id="b10n" v="是 → 新版 just/&lt;ns&gt;.just 的 &lt;ns&gt; 撞名？（其他工具／根 justfile recipe／保留名 vendor_kit）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB1"><g x=720 y=407 w=340 h=174/></c>
<c id="b10n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1036 y=397 w=30 h=20/></c>
<c id="b10c" v="否 → 逐檔判斷（B baseline／D 現況／N = 暫存 /dist/&lt;repo&gt;，見「逐檔判斷」頁）→ 詢問清單" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB1"><g x=720 y=601 w=360 h=48/></c>
<c id="b10c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1056 y=591 w=30 h=20/></c>
<c id="b12x" v="是 → 1：印需改清單（frozen；請在本機 upgrade &lt;repo&gt; -y 後 commit 並 push）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB1"><g x=20 y=669 w=220 h=102/></c>
<c id="b12x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=216 y=659 w=30 h=20/></c>
<c id="b12" v="CI 為真（frozen）且需改 tracked 檔？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB1"><g x=720 y=680 w=340 h=81/></c>
<c id="b12_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=1036 y=670 w=30 h=20/></c>
<c id="b11y" v="是 → 0：唯讀預覽（印會問哪些檔）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uB1"><g x=20 y=791 w=220 h=58/></c>
<c id="b11y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB1"><g x=216 y=781 w=30 h=20/></c>
<c id="b11" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB1"><g x=720 y=795 w=240 h=50/></c>
<c id="b11z" v="否 ↓ 續「B（2）」頁：apply 寫入段" s="text;fs=12;sc=none;fc=none;fst=1" parent="uB1"><g x=720 y=869 w=300 h=26/></c>
<c id="be13e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b8e" target="b9"></c>
<c id="be14" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b9" target="b10a"></c>
<c id="be15" s="fs=12;exitX=0.5;exitY=1;entryX=0.818;entryY=0" edge="1" source="b10a" target="b10b"></c>
<c id="be15x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b10b" target="b10x"></c>
<c id="be15b" s="fs=12;exitX=0.773;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10b" target="b10d"></c>
<c id="be15d" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b10d" target="b10dx"></c>
<c id="be15n" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10d" target="b10n"><g x=-0.6/></c>
<c id="be15nx" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b10n" target="b10nx"></c>
<c id="be15c" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.472;entryY=0" edge="1" source="b10n" target="b10c"><g x=-0.6/></c>
<c id="be15e" s="fs=12;exitX=0.472;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10c" target="b12"></c>
<c id="be16" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b12" target="b12x"></c>
<c id="be17" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b12" target="b11"><g x=0.08 pts=910,922;860,922/></c>
<c id="be18" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b11" target="b11y"></c>
<c id="be19" s="fs=12;exitX=0.5;exitY=1;entryX=0.4;entryY=0" edge="1" source="b11" target="b11z"></c>
<c id="p7cp_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1058 w=200 h=60/></c>
<c id="p7cp_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1058 w=140 h=64/></c>
<c id="p7cp_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1066 w=140 h=44/></c>
<c id="p7cp_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1060 w=190 h=56/></c>
<c id="p7cp_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1060 w=210 h=56/></c>
<c id="p7cp_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1068 w=88 h=40/></c>
<c id="p7cp_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1068 w=170 h=40/></c>
<c id="p7cp_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1058 w=300 h=60/></c>
<c id="p7cp_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1126 w=200 h=36/></c>
<c id="p7cp_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1126 w=120 h=36/></c>
<c id="p7cp_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1126 w=190 h=36/></c>
<c id="p7cp_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1126 w=170 h=36/></c>
<c id="p7cp_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1126 w=170 h=36/></c>
<c id="p7cp_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1126 w=200 h=36/></c>
<c id="p7cp_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1116 w=30 h=20/></c>
<c id="p7cp_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1164 w=200 h=28/></c>
<c id="p7cp_tk0" v="Renovate／regex manager" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1198 w=150 h=40/></c>
<c id="p7cp_tv0" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1198 w=610 h=40/></c>
<c id="p7cp_tk1" v="PR／commit／push／rebase／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1238 w=150 h=40/></c>
<c id="p7cp_tv1" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1238 w=610 h=40/></c>
<c id="p7cp_tk2" v="check.sh／CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1278 w=150 h=55/></c>
<c id="p7cp_tv2" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1278 w=610 h=55/></c>
<c id="p7cp_tk3" v="baseline 落後／待合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1333 w=150 h=40/></c>
<c id="p7cp_tv3" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1333 w=610 h=40/></c>
<c id="p7cp_tk4" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1373 w=150 h=55/></c>
<c id="p7cp_tv4" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1373 w=610 h=55/></c>
<c id="p7cp_tk5" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1428 w=150 h=40/></c>
<c id="p7cp_tv5" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1428 w=610 h=40/></c>
<c id="p7cp_tk6" v="dev 覆寫／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1468 w=150 h=40/></c>
<c id="p7cp_tv6" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &lt;repo&gt;／remove &lt;repo&gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1468 w=610 h=40/></c>
<c id="p7cp_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1508 w=150 h=40/></c>
<c id="p7cp_tv7" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/（暫存 → 原子替換）；印記 gen/&lt;repo&gt;.stamp 第一行 index digest，之後每檔 sha256" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1508 w=610 h=40/></c>
<c id="p7cp_tk8" v="B／D／N、逐檔判斷後詢問" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1548 w=150 h=86/></c>
<c id="p7cp_tv8" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&lt;repo&gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1548 w=610 h=86/></c>
<c id="p7cp_tk9" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1198 w=150 h=71/></c>
<c id="p7cp_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1198 w=610 h=71/></c>
<c id="p7cp_tk10" v="gen／mod?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1269 w=150 h=40/></c>
<c id="p7cp_tv10" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1269 w=610 h=40/></c>
<c id="p7cp_tk11" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1309 w=150 h=55/></c>
<c id="p7cp_tv11" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1309 w=610 h=55/></c>
<c id="p7cp_tk12" v="CRLF／append 行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1364 w=150 h=40/></c>
<c id="p7cp_tv12" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1364 w=610 h=40/></c>
<c id="p7cp_tk13" v="GHCR／image／tag@digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1404 w=150 h=40/></c>
<c id="p7cp_tv13" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1404 w=610 h=40/></c>
<c id="p7cp_tk14" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1444 w=150 h=55/></c>
<c id="p7cp_tv14" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1444 w=610 h=55/></c>
</diagram>
<diagram id="v1p7cc" name="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併"><c id="title" v="流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併（§5、v2.2 D、v2.5 §2～§4、v2.6 §8／Q14）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=97 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=97 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=97 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=97 w=280 h=28/></c>
<c id="uB2" v="B（2）apply 寫入段前半（承「B（1′）」頁：已拿鎖、重驗、檢查通過、非 dry-run）：建日誌 → 清除衝突狀態 → materialize → 印記 → 逐檔詢問（四種情況各一問）→ 暫存合併 → 逐檔原子替換；收尾見「B（2′）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1415/></c>
<c id="uB2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1556 y=5 w=30 h=20/></c>
<c id="b10z" v="來自「B（1′）」頁：apply 檢查通過（非 dry-run）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="uB2"><g x=750 y=36 w=300 h=58/></c>
<c id="b10e" v="建進度日誌（metadata state=in-progress；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB2"><g x=720 y=114 w=360 h=48/></c>
<c id="b10e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=104 w=30 h=20/></c>
<c id="b10ef" v="baseline/&lt;repo&gt;/.vendor_kit.toml（state=in-progress）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB2"><g x=1300 y=117 w=280 h=42/></c>
<c id="b10f" v="(0) 判定已解 → 清除 metadata 的衝突狀態（有的話）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB2"><g x=720 y=182 w=360 h=40/></c>
<c id="b10f_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=172 w=30 h=20/></c>
<c id="b10ff" v=".vendor_kit.toml（衝突中檔案清單清空）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB2"><g x=1300 y=182 w=280 h=40/></c>
<c id="b13a" v="materialize 目標版：/dist/&lt;repo&gt; → 暫存 → cache/&lt;repo&gt;/（原子替換）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB2"><g x=720 y=242 w=360 h=48/></c>
<c id="b13a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=232 w=30 h=20/></c>
<c id="b13f" v="cache/&lt;repo&gt;/（目標版，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB2"><g x=1300 y=246 w=280 h=40/></c>
<c id="b13b" v="寫印記 gen/&lt;repo&gt;.stamp（第一行 index digest，之後每檔 sha256）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB2"><g x=720 y=310 w=360 h=48/></c>
<c id="b13b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=300 w=30 h=20/></c>
<c id="b13bf" v="gen/&lt;repo&gt;.stamp（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB2"><g x=1300 y=314 w=280 h=40/></c>
<c id="bl" v="↓ 逐檔（每檔恰一種情況，依「逐檔判斷」頁；不是該情況就看下一格；-y 免問）" s="text;fs=12;sc=none;fc=none;fst=1" parent="uB2"><g x=720 y=378 w=360 h=42/></c>
<c id="b14q1" v="文字檔：你沒改、新版改了 → 問「X 換成新版？」" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB2"><g x=720 y=440 w=240 h=112/></c>
<c id="b14q1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=936 y=430 w=30 h=20/></c>
<c id="b14a" v="是：換新版（在暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=990 y=472 w=90 h=48/></c>
<c id="b14a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=462 w=30 h=20/></c>
<c id="b14q1b" v="二進位／symlink：你沒改、新版改了 → 問「X 是二進位檔，要換成新版嗎？」" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB2"><g x=720 y=572 w=240 h=174/></c>
<c id="b14q1b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=936 y=562 w=30 h=20/></c>
<c id="b14ab" v="是：換新版（在暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=990 y=635 w=90 h=48/></c>
<c id="b14ab_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=625 w=30 h=20/></c>
<c id="b14q2" v="兩邊都改 → 問「你和新版都改了 X，要三方合併嗎？」" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB2"><g x=720 y=766 w=240 h=143/></c>
<c id="b14q2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=936 y=756 w=30 h=20/></c>
<c id="b14b" v="是：git merge-file --diff3（在暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=990 y=798 w=90 h=79/></c>
<c id="b14b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=788 w=30 h=20/></c>
<c id="b14q3" v="append 行找到上次插入的行 → 問「要替換嗎？」" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB2"><g x=720 y=929 w=240 h=112/></c>
<c id="b14q3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=936 y=919 w=30 h=20/></c>
<c id="b14c" v="是：append 行替換（在暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=990 y=954 w=90 h=63/></c>
<c id="b14c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=944 w=30 h=20/></c>
<c id="b14q4" v="新版新增（B 無）→ 問「要建 X 嗎」" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB2"><g x=720 y=1076 w=240 h=112/></c>
<c id="b14q4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=936 y=1066 w=30 h=20/></c>
<c id="b14d" v="是：建新檔（已有同名 → 不納管）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=990 y=1100 w=90 h=63/></c>
<c id="b14d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=1090 w=30 h=20/></c>
<c id="b14r" v="Q14／Q15、v2.7 §3：拒絕 → 已納管檔（managed／appended／二進位）state 不變、只記 declined_hash（目標新版再次更新時再問）；新檔（B 無）被拒 → state=declined 從未建立；之後不再問；dry-run／check.sh 印「有 N 個範本你拒絕過」；dest 在 CI 路徑（.github/workflows/、.gitlab-ci.yml）時訊息醒目" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="uB2"><g x=1300 y=1061 w=280 h=141/></c>
<c id="b14r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1556 y=1051 w=30 h=20/></c>
<c id="b14n" v="否：不動該檔；已納管檔 state 不變只記 declined_hash，新檔被拒 → state=declined（新版再更新時再問）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB2"><g x=620 y=1222 w=280 h=63/></c>
<c id="b14n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=876 y=1212 w=30 h=20/></c>
<c id="b14w" v="逐檔原子替換（暫存 → 正式位置）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB2"><g x=720 y=1306 w=360 h=40/></c>
<c id="b14w_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB2"><g x=1056 y=1296 w=30 h=20/></c>
<c id="b14f" v="初始檔（合併後；衝突留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB2"><g x=1300 y=1305 w=280 h=42/></c>
<c id="b14z" v="↓ 續「B（2′）」頁：baseline → metadata → tools.just → version.toml → 刪日誌" s="text;fs=12;sc=none;fc=none;fst=1" parent="uB2"><g x=720 y=1367 w=360 h=42/></c>
<c id="be20" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10z" target="b10e"></c>
<c id="be20f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b10e" target="b10ef"></c>
<c id="be20b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10e" target="b10f"></c>
<c id="be20ff" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b10f" target="b10ff"></c>
<c id="be21" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b10f" target="b13a"></c>
<c id="be21f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b13a" target="b13f"></c>
<c id="be21b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b13a" target="b13b"></c>
<c id="be21bf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b13b" target="b13bf"></c>
<c id="be22" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b13b" target="bl"></c>
<c id="be22a" s="fs=12;exitX=0.333;exitY=1;entryX=0.5;entryY=0" edge="1" source="bl" target="b14q1"></c>
<c id="be22y1" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14q1" target="b14a"></c>
<c id="be22n1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b14q1" target="b14q1b"></c>
<c id="be22x1" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.214;entryY=0" edge="1" source="b14q1" target="b14n"><g x=-0.95 pts=700,637/></c>
<c id="be22y1b" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14q1b" target="b14ab"></c>
<c id="be22n1b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b14q1b" target="b14q2"></c>
<c id="be22x1b" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.179;entryY=0" edge="1" source="b14q1b" target="b14n"><g x=-0.92 pts=690,800/></c>
<c id="be22y2" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14q2" target="b14b"></c>
<c id="be22n2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b14q2" target="b14q3"></c>
<c id="be22x2" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.143;entryY=0" edge="1" source="b14q2" target="b14n"><g x=-0.87 pts=680,978/></c>
<c id="be22y3" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14q3" target="b14c"></c>
<c id="be22n3" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b14q3" target="b14q4"></c>
<c id="be22x3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.107;entryY=0" edge="1" source="b14q3" target="b14n"><g x=-0.77 pts=670,1126/></c>
<c id="be22y4" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14q4" target="b14d"></c>
<c id="be22x4" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.071;entryY=0" edge="1" source="b14q4" target="b14n"><g x=-0.53 pts=660,1272/></c>
<c id="be23a" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b14a" target="b14w"><g pts=1110,637;1110,1436;1064,1436/></c>
<c id="be23ab" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b14ab" target="b14w"><g pts=1110,800;1110,1436;1064,1436/></c>
<c id="be23b" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b14b" target="b14w"><g pts=1110,978;1110,1436;1064,1436/></c>
<c id="be23c" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b14c" target="b14w"><g pts=1110,1126;1110,1436;1064,1436/></c>
<c id="be23d" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="b14d" target="b14w"><g pts=1110,1272;1110,1436;1064,1436/></c>
<c id="be23n" s="fs=12;exitX=0.5;exitY=1;entryX=0.111;entryY=0" edge="1" source="b14n" target="b14w"></c>
<c id="be22f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b14w" target="b14f"></c>
<c id="be23z" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b14w" target="b14z"></c>
<c id="p7cc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1572 w=200 h=60/></c>
<c id="p7cc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1572 w=140 h=64/></c>
<c id="p7cc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1580 w=140 h=44/></c>
<c id="p7cc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1574 w=190 h=56/></c>
<c id="p7cc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1574 w=210 h=56/></c>
<c id="p7cc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1582 w=88 h=40/></c>
<c id="p7cc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1582 w=170 h=40/></c>
<c id="p7cc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1572 w=300 h=60/></c>
<c id="p7cc_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1640 w=200 h=36/></c>
<c id="p7cc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1640 w=120 h=36/></c>
<c id="p7cc_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=1640 w=150 h=36/></c>
<c id="p7cc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=570 y=1640 w=190 h=36/></c>
<c id="p7cc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=780 y=1640 w=170 h=36/></c>
<c id="p7cc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=1640 w=170 h=36/></c>
<c id="p7cc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1160 y=1640 w=200 h=36/></c>
<c id="p7cc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1336 y=1630 w=30 h=20/></c>
<c id="p7cc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1678 w=200 h=28/></c>
<c id="p7cc_tk0" v="Renovate／regex manager" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1712 w=150 h=40/></c>
<c id="p7cc_tv0" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1712 w=610 h=40/></c>
<c id="p7cc_tk1" v="PR／commit／push／rebase／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1752 w=150 h=40/></c>
<c id="p7cc_tv1" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1752 w=610 h=40/></c>
<c id="p7cc_tk2" v="check.sh／CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1792 w=150 h=55/></c>
<c id="p7cc_tv2" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1792 w=610 h=55/></c>
<c id="p7cc_tk3" v="baseline 落後／待合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1847 w=150 h=40/></c>
<c id="p7cc_tv3" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1847 w=610 h=40/></c>
<c id="p7cc_tk4" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1887 w=150 h=55/></c>
<c id="p7cc_tv4" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1887 w=610 h=55/></c>
<c id="p7cc_tk5" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1942 w=150 h=40/></c>
<c id="p7cc_tv5" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1942 w=610 h=40/></c>
<c id="p7cc_tk6" v="dev 覆寫／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1982 w=150 h=40/></c>
<c id="p7cc_tv6" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &lt;repo&gt;／remove &lt;repo&gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1982 w=610 h=40/></c>
<c id="p7cc_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2022 w=150 h=40/></c>
<c id="p7cc_tv7" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/（暫存 → 原子替換）；印記 gen/&lt;repo&gt;.stamp 第一行 index digest，之後每檔 sha256" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2022 w=610 h=40/></c>
<c id="p7cc_tk8" v="B／D／N、逐檔判斷後詢問" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2062 w=150 h=86/></c>
<c id="p7cc_tv8" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&lt;repo&gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2062 w=610 h=86/></c>
<c id="p7cc_tk9" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1712 w=150 h=71/></c>
<c id="p7cc_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1712 w=610 h=71/></c>
<c id="p7cc_tk10" v="gen／mod?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1783 w=150 h=40/></c>
<c id="p7cc_tv10" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1783 w=610 h=40/></c>
<c id="p7cc_tk11" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1823 w=150 h=55/></c>
<c id="p7cc_tv11" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1823 w=610 h=55/></c>
<c id="p7cc_tk12" v="CRLF／append 行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1878 w=150 h=40/></c>
<c id="p7cc_tv12" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1878 w=610 h=40/></c>
<c id="p7cc_tk13" v="GHCR／image／tag@digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1918 w=150 h=40/></c>
<c id="p7cc_tv13" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1918 w=610 h=40/></c>
<c id="p7cc_tk14" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1958 w=150 h=55/></c>
<c id="p7cc_tv14" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1958 w=610 h=55/></c>
</diagram>
<diagram id="v1p7cccc" name="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入"><c id="title" v="流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入（§5、v2.2 D、v2.5 §3／§4、v2.6 Q27）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行「原文比對」CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.5 §3／§6）：apply 順序 = flock → 重驗 → dry-run 分支 → 建日誌 → 清除衝突狀態與其他寫入 → 刪日誌；目標工具在 dev 覆寫中 → 1 先 undev。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=97 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=97 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=97 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=97 w=280 h=28/></c>
<c id="uB3" v="B（2′）apply 寫入段後半（承「B（2）」頁：初始檔已原子替換）：解析失敗的檔不推 → 推 baseline → metadata（版本／conflicts；state／declined_hash／lines）→ 重生 tools.just → 最後寫 version.toml → 刪日誌 → 有衝突？→ 0／2" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=905/></c>
<c id="uB3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1556 y=5 w=30 h=20/></c>
<c id="b15z" v="來自「B（2）」頁：初始檔已原子替換" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="uB3"><g x=750 y=36 w=300 h=58/></c>
<c id="b15q" v="合併後 TOML／just 類目標重新解析失敗？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB3"><g x=720 y=114 w=220 h=112/></c>
<c id="b15q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=916 y=104 w=30 h=20/></c>
<c id="b15c" v="是：該檔留原檔、dest 記入 conflicts、baseline 不推" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uB3"><g x=970 y=130 w=110 h=79/></c>
<c id="b15c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=120 w=30 h=20/></c>
<c id="b15a" v="否：推 baseline/&lt;repo&gt;/ 到目標版（有衝突也推）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=247 w=360 h=40/></c>
<c id="b15f" v="baseline/&lt;repo&gt;/（目標版範本副本，進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB3"><g x=1300 y=246 w=280 h=42/></c>
<c id="b15b" v="寫 metadata：最後合併版本 = 目標版、衝突中檔案（conflicts）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=308 w=360 h=48/></c>
<c id="b15b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=298 w=30 h=20/></c>
<c id="b15bf" v="baseline/&lt;repo&gt;/.vendor_kit.toml（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB3"><g x=1300 y=311 w=280 h=42/></c>
<c id="b15d" v="寫 metadata：每個 dest 的 state／declined_hash／append 行（lines）—— 已納管檔拒絕 → state 不變只記 declined_hash；新檔被拒 → state=declined" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=376 w=360 h=63/></c>
<c id="b15d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=366 w=30 h=20/></c>
<c id="b15df" v=".vendor_kit.toml（[[file]] 各 dest 的 state／declined_hash／lines）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB3"><g x=1300 y=386 w=280 h=42/></c>
<c id="b15g" v="重生 gen/tools.just（新版的 just/&lt;ns&gt;.just 可能增減；每個一行 mod?）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=459 w=360 h=48/></c>
<c id="b15g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=449 w=30 h=20/></c>
<c id="b15gf" v="gen/tools.just（不進 git；mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB3"><g x=1300 y=463 w=280 h=40/></c>
<c id="b16" v="寫 version.toml &lt;repo&gt; 行 → 目標 tag@digest（待合併：已是 B，不動）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=527 w=360 h=48/></c>
<c id="b16_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=517 w=30 h=20/></c>
<c id="b16f" v="version.toml（&lt;repo&gt; 行，進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uB3"><g x=1300 y=531 w=280 h=40/></c>
<c id="b16x" v="失敗 → 1：明列已完成／未完成" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uB3"><g x=20 y=595 w=220 h=58/></c>
<c id="b16x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=216 y=585 w=30 h=20/></c>
<c id="b16b" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uB3"><g x=720 y=604 w=360 h=40/></c>
<c id="b16b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1056 y=594 w=30 h=20/></c>
<c id="b17" v="否 → 0：印摘要 → commit" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uB3"><g x=20 y=700 w=220 h=58/></c>
<c id="b17_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=216 y=690 w=30 h=20/></c>
<c id="b16q" v="有衝突（conflicts 非空）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uB3"><g x=720 y=673 w=240 h=112/></c>
<c id="b16q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=936 y=663 w=30 h=20/></c>
<c id="b18" v="是 → 2：印衝突檔名（解完再跑直到乾淨；baseline 已在目標版）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uB3"><g x=720 y=823 w=360 h=58/></c>
<c id="b18r" v="多工具彙總（Q27）：不帶 repo 的 upgrade 做得完的做完，最後回最需要處理的碼：失敗 1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；訊息全列；待合併補完後另有新版 → 印「已補齊 &lt;repo&gt; 至 vB；另有新版 vX，再跑一次可升」" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="uB3"><g x=1300 y=805 w=280 h=94/></c>
<c id="b18r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uB3"><g x=1556 y=795 w=30 h=20/></c>
<c id="be23" s="fs=12;exitX=0.267;exitY=1;entryX=0.5;entryY=0" edge="1" source="b15z" target="b15q"></c>
<c id="be23c" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b15q" target="b15c"></c>
<c id="be23a" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.306;entryY=0" edge="1" source="b15q" target="b15a"><g x=-0.6/></c>
<c id="be23cc" s="fs=12;exitX=0.5;exitY=1;entryX=0.847;entryY=0" edge="1" source="b15c" target="b15a"></c>
<c id="be24" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b15a" target="b15f"></c>
<c id="be24b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b15a" target="b15b"></c>
<c id="be24bf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b15b" target="b15bf"></c>
<c id="be24d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b15b" target="b15d"></c>
<c id="be24df" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b15d" target="b15df"></c>
<c id="be25" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b15d" target="b15g"></c>
<c id="be25f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b15g" target="b15gf"></c>
<c id="be25g" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="b15g" target="b16"></c>
<c id="be27" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="b16" target="b16f"></c>
<c id="be26" v="成功" s="fs=12;exitX=0.6;exitY=1;entryX=0.6;entryY=0" edge="1" source="b16" target="b16b"><g x=-0.6/></c>
<c id="be26x" v="失敗" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="b16" target="b16x"><g x=0.00 pts=812,726;150,726/></c>
<c id="be28q" s="fs=12;exitX=0.333;exitY=1;entryX=0.5;entryY=0" edge="1" source="b16b" target="b16q"></c>
<c id="be28" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="b16q" target="b17"></c>
<c id="be29" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.333;entryY=0" edge="1" source="b16q" target="b18"><g x=-0.6/></c>
<c id="p7cq_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1062 w=200 h=60/></c>
<c id="p7cq_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1062 w=140 h=64/></c>
<c id="p7cq_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1070 w=140 h=44/></c>
<c id="p7cq_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1064 w=190 h=56/></c>
<c id="p7cq_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1064 w=210 h=56/></c>
<c id="p7cq_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1072 w=88 h=40/></c>
<c id="p7cq_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1072 w=170 h=40/></c>
<c id="p7cq_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1062 w=300 h=60/></c>
<c id="p7cq_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1130 w=200 h=36/></c>
<c id="p7cq_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1130 w=120 h=36/></c>
<c id="p7cq_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=1130 w=150 h=36/></c>
<c id="p7cq_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=570 y=1130 w=190 h=36/></c>
<c id="p7cq_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=780 y=1130 w=170 h=36/></c>
<c id="p7cq_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=1130 w=170 h=36/></c>
<c id="p7cq_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1160 y=1130 w=200 h=36/></c>
<c id="p7cq_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1336 y=1120 w=30 h=20/></c>
<c id="p7cq_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1168 w=200 h=28/></c>
<c id="p7cq_tk0" v="Renovate／regex manager" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1202 w=150 h=40/></c>
<c id="p7cq_tv0" v="GitHub 上的機器人（下游自選；vendor_kit 不出 bot）：regex manager = 用正規表示式在 version.toml 找版本字串；docker datasource = 去 GHCR 查新 tag；有新版就開 PR 改那一行" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1202 w=610 h=40/></c>
<c id="p7cq_tk1" v="PR／commit／push／rebase／merge" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1242 w=150 h=40/></c>
<c id="p7cq_tv1" v="PR = 提議把分支併進主線（GitHub 上審查）；commit = 記錄一次修改；push = 傳到 GitHub；rebase = 重排分支（會蓋掉人補的 commit）；merge = 併入主線" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1242 w=610 h=40/></c>
<c id="p7cq_tk2" v="check.sh／CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1282 w=150 h=55/></c>
<c id="p7cq_tv2" v="下游 CI 只呼叫 .vendor_kit/ci/check.sh（自己 export CI=1）= sync（frozen：不查最新版、不寫 tracked 檔）→ verify → upgrade --dry-run → 工具測試 → 專案測試；CI 為真 = CI 非空且不為 0／false → frozen：需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1282 w=610 h=55/></c>
<c id="p7cq_tk3" v="baseline 落後／待合併" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1337 w=150 h=40/></c>
<c id="p7cq_tv3" v="最後合併版本 ≠ version.toml：有人只改了 version.toml（如 Renovate）→ CI 1（PR 紅，需要人動作）、本機 warn；upgrade 先只補到那版就停，印「另有新版，再跑一次可升」；補合併衝突也立刻 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1337 w=610 h=40/></c>
<c id="p7cq_tk4" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1377 w=150 h=55/></c>
<c id="p7cq_tv4" v="resolve 只讀只算（查目標版、輸出要拉的 image 與指紋，不寫檔）；啟動器 docker image inspect 有則不拉、無才 pull；apply 拿 flock 後重驗指紋才寫（v2.5 §3 順序）；--dry-run（無短形）= apply --dry-run 唯讀預覽（要先拉 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1377 w=610 h=55/></c>
<c id="p7cq_tk5" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1432 w=150 h=40/></c>
<c id="p7cq_tv5" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 重驗；進度日誌 = metadata state=in-progress，第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1432 w=610 h=40/></c>
<c id="p7cq_tk6" v="dev 覆寫／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1472 w=150 h=40/></c>
<c id="p7cq_tv6" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫 = 用本機 dist/ 取代 image；upgrade &lt;repo&gt;／remove &lt;repo&gt; 都先擋 → 1 提示先 undev（v2.5 §6）；不帶 repo 的 upgrade 預檢也擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1472 w=610 h=40/></c>
<c id="p7cq_tk7" v="materialize／印記" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1512 w=150 h=40/></c>
<c id="p7cq_tv7" v="引擎內部步驟：apply 決定套用後把目標版 /dist/&lt;repo&gt; 展開到 cache/&lt;repo&gt;/（暫存 → 原子替換）；印記 gen/&lt;repo&gt;.stamp 第一行 index digest，之後每檔 sha256" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1512 w=610 h=40/></c>
<c id="p7cq_tk8" v="B／D／N、逐檔判斷後詢問" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1552 w=150 h=86/></c>
<c id="p7cq_tv8" v="B = baseline（上次合併的範本）、D = 現況（你的檔）、N = 目標版範本（啟動器展開到暫存、掛進引擎的 /dist/&lt;repo&gt;，不是 cache）；N 改了才問「換成新版？」，兩邊都改才問「三方合併？」，新版新增問「要建 X 嗎」，二進位問「是二進位檔，要換成新版嗎？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash（新版再變才再問），新檔被拒才 state=declined（v2.7 §3）；細表見「逐檔判斷」頁" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1552 w=610 h=86/></c>
<c id="p7cq_tk9" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1202 w=150 h=71/></c>
<c id="p7cq_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行（實際插入的行）、衝突中檔案清單、進度日誌 state；upgrade 讀它決定待合併與衝突重入，apply 內更新" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1202 w=610 h=71/></c>
<c id="p7cq_tk10" v="gen／mod?" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1273 w=150 h=40/></c>
<c id="p7cq_tv10" v="gen/tools.just（不進 git）每個 &lt;ns&gt;.just 一行 mod? = 把工具的 just 檔掛成一個命名空間（just &lt;ns&gt; …；帶問號 = 檔不在也不掛）；新版的 just/ 可能增減檔，所以 upgrade 重生它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1273 w=610 h=40/></c>
<c id="p7cq_tk11" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1313 w=150 h=55/></c>
<c id="p7cq_tv11" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤，重入時靠它偵測）；回傳衝突數 → 映射為 2（需要人解衝突，橙）；多工具（Q27）最後回最需處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1313 w=610 h=55/></c>
<c id="p7cq_tk12" v="CRLF／append 行" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1368 w=150 h=40/></c>
<c id="p7cq_tv12" v="CRLF = Windows 換行（\r\n）；upgrade 找上次 append 的行時 CRLF／LF 視為相同、其餘精確；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1368 w=610 h=40/></c>
<c id="p7cq_tk13" v="GHCR／image／tag@digest" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1408 w=150 h=40/></c>
<c id="p7cq_tv13" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；tag = 人看的版本名，digest = 內容的 sha256 ID（鎖定用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1408 w=610 h=40/></c>
<c id="p7cq_tk14" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1448 w=150 h=55/></c>
<c id="p7cq_tv14" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1448 w=610 h=55/></c>
</diagram>
<diagram id="v1p7b" name="流程 v2：upgrade ── 逐檔判斷、衝突重入、回退"><c id="title" v="流程 v2：upgrade ── C. 逐檔判斷表、C′ 衝突重入、D. 回退（§5、v2.2 D、v2.3 §1、v2.5 §1／§2／§4）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1）：append 行比對 CRLF／LF 視為相同、其餘精確；找不到或多處 → 保留只 warn。已定（v2.2 E）：dist/files/ 第一版禁止 symlink。已定（v2.5 §2）：N 讀暫存 /dist/&lt;repo&gt;，materialize 在決定套用之後。自身升級見「E. 自身升級」頁。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=61/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=81 w=220 h=28/></c>
<c id="hdr1" v="Renovate（GitHub 上）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=81 w=180 h=28/></c>
<c id="hdr2" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=480 y=81 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=740 y=81 w=360 h=28/></c>
<c id="hdr4" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1120 y=81 w=180 h=28/></c>
<c id="hdr5" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=81 w=280 h=28/></c>
<c id="uC" v="C. 逐檔判斷後詢問（每個 init.toml 檔；引擎 merge 模組；§5 表；在 apply 內、拿到 flock、建日誌後）＋ C′ 衝突重入（v2.2 D (0)、v2.5 §3）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=125 w=1600 h=905/></c>
<c id="uC_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uC"><g x=1556 y=5 w=30 h=20/></c>
<c id="c_in0" v="B = baseline/&lt;repo&gt;/&lt;檔&gt;（上次合併的範本）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uC"><g x=1300 y=50 w=280 h=42/></c>
<c id="c_in1" v="D = 專案裡的 &lt;檔&gt;（現況，你可能改過）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uC"><g x=1300 y=106 w=280 h=40/></c>
<c id="c_in2" v="N = 目標版範本：暫存 /dist/&lt;repo&gt;/&lt;檔&gt;（不是 cache）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uC"><g x=1300 y=162 w=280 h=42/></c>
<c id="c_in2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uC"><g x=1556 y=152 w=30 h=20/></c>
<c id="c_m" v="引擎 merge 模組：三份比對，逐檔判斷（左表）→ 要改的先問（-y 免問；拒絕 → 不動、記 declined_hash；新檔才 state=declined）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uC"><g x=730 y=54 w=340 h=60/></c>
<c id="c_h0" v="情況" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=70 w=170 h=28/></c>
<c id="c_h1" v="做法" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="uC"><g x=190 y=70 w=290 h=28/></c>
<c id="c_h2" v="結果" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1" parent="uC"><g x=480 y=70 w=230 h=28/></c>
<c id="c_r0c0" v="新版沒改／你的檔已等於新版（N==B 或 D==N）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=98 w=170 h=44/></c>
<c id="c_r0c1" v="不動" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=98 w=290 h=44/></c>
<c id="c_r0c2" v="—" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=98 w=230 h=44/></c>
<c id="c_r1c0" v="你刪了已納管的檔（D 缺）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=142 w=170 h=40/></c>
<c id="c_r1c1" v="不問、不重建" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=142 w=290 h=40/></c>
<c id="c_r1c2" v="state=deleted，維持刪除（§4.3）" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=142 w=230 h=40/></c>
<c id="c_r2c0" v="新版改了、你沒改（D==B、N≠B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=182 w=170 h=59/></c>
<c id="c_r2c1" v="問「X 換成新版？」" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=182 w=290 h=59/></c>
<c id="c_r2c2" v="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（目標新版再次更新時再問）" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=182 w=230 h=59/></c>
<c id="c_r3c0" v="兩邊都改（D≠B、N≠B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=241 w=170 h=122/></c>
<c id="c_r3c1" v="問「你和新版都改了 X，要三方合併嗎？」" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=241 w=290 h=122/></c>
<c id="c_r3c2" v="同意 → git merge-file --diff3（在暫存做）：乾淨 → 原子替換寫入；衝突 → 留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記、回 2；baseline 仍推到目標版；解完重跑直到乾淨；拒絕 → 不動、state 不變只記 declined_hash" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=241 w=230 h=122/></c>
<c id="c_r4c0" v="新版新增（B 無）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=363 w=170 h=106/></c>
<c id="c_r4c1" v="問「要建 X 嗎」（-y 建）；已有同名 → 不納管；dest 在 CI 路徑時訊息醒目" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=363 w=290 h=106/></c>
<c id="c_r4c2" v="拒絕 → 不建、state=declined（唯一會用 declined 的情況；之後不再問；目標新版再次更新時重新詢問；dry-run／check.sh 印「有 N 個範本你拒絕過」）；不覆蓋、印「已存在，範本在 cache」" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=363 w=230 h=106/></c>
<c id="c_r5c0" v="新版刪除該檔（N 無）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=469 w=170 h=40/></c>
<c id="c_r5c1" v="不刪，只 warn" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=469 w=290 h=40/></c>
<c id="c_r5c2" v="你的檔留著" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=469 w=230 h=40/></c>
<c id="c_r6c0" v="append 行（strategy=append）" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=509 w=170 h=75/></c>
<c id="c_r6c1" v="找到上次插入的行（CRLF／LF 視為相同，其餘精確）→ 問後替換" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=509 w=290 h=75/></c>
<c id="c_r6c2" v="唯一命中 → 替換；零命中或多處 → 保留只 warn、印新內容；拒絕 → 不動、state 維持 appended 只記 declined_hash" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=509 w=230 h=75/></c>
<c id="c_r7c0" v="二進位／symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=584 w=170 h=59/></c>
<c id="c_r7c1" v="不合併：你未改（D==B）→ 問「X 是二進位檔，要換成新版嗎？」（-y 免問）" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=584 w=290 h=59/></c>
<c id="c_r7c2" v="同意 → 換；拒絕 → 不動、state 不變只記 declined_hash（新版再更新時再問）；改過 → 保留 + warn" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=584 w=230 h=59/></c>
<c id="c_r8c0" v="CI 為真（frozen）且需改 tracked 檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1" parent="uC"><g x=20 y=643 w=170 h=59/></c>
<c id="c_r8c1" v="apply 印清單 → 1（version.toml 未動；-y 不解除 frozen）" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=190 y=643 w=290 h=59/></c>
<c id="c_r8c2" v="--dry-run 也一樣：CI 為真且需改 tracked 檔 → 1；本機 → 0 只印清單" s="fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=480 y=643 w=230 h=59/></c>
<c id="c_note" v="--dry-run = 唯讀預覽，只印會問哪些檔。衝突解完 → 再跑一次 upgrade 直到乾淨（2 = 需要人解衝突，橙）。dest 撞名規則見「add（1）」頁；四種詢問各一格見「B（2）」頁。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="uC"><g x=1300 y=218 w=280 h=73/></c>
<c id="cx_l" v="C′ 衝突重入（解完衝突後再跑 upgrade；v2.2 D (0)）—— 偵測在 resolve，清除在 apply（拿鎖、建日誌後）" s="text;fs=12;sc=none;fc=none;fst=1" parent="uC"><g x=20 y=732 w=700 h=26/></c>
<c id="cx0" v="解完衝突後再跑 upgrade &lt;repo&gt;" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uC"><g x=20 y=772.0 w=220 h=58/></c>
<c id="cx1" v="衝突檔仍含我們的標籤？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uC"><g x=730 y=776.0 w=340 h=50/></c>
<c id="cx1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uC"><g x=1046 y=766 w=30 h=20/></c>
<c id="cx2" v="是 → 2：停（先解完標記再重跑）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uC"><g x=1100 y=772.0 w=200 h=58/></c>
<c id="cx3" v="否：apply 拿鎖、建日誌後清除衝突狀態 → 接「B. 手動路徑（1）」頁的 (1)(2)（version.toml、baseline 已在目標版 → 通常「不動」）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uC"><g x=730 y=842 w=340 h=57/></c>
<c id="cx3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uC"><g x=1046 y=832 w=30 h=20/></c>
<c id="c_e0" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c_in0" target="c_m"><g pts=1296,195;1296,209/></c>
<c id="c_e1" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c_in1" target="c_m"><g pts=1296,251;1296,209/></c>
<c id="c_e2" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c_in2" target="c_m"><g pts=1296,307;1296,209/></c>
<c id="c_e3" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="c_m" target="c_h2"></c>
<c id="cx_e0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="cx0" target="cx1"></c>
<c id="cx_e1" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="cx1" target="cx2"></c>
<c id="cx_e2" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="cx1" target="cx3"><g x=-0.40/></c>
<c id="uD" v="D. 回退 ＝ git revert 該升級 commit（version.toml + 初始檔 + baseline 同一 commit）；下次 just 的 sync 只把 cache/ 換回舊版" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=1046 w=1600 h=615/></c>
<c id="d0" v="git revert 該升級 commit" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uD"><g x=20 y=36 w=220 h=58/></c>
<c id="d1a" v="下次 just：docker run 引擎 resolve sync" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=460 y=44 w=240 h=42/></c>
<c id="d2" v="sync resolve：gen/&lt;repo&gt;.stamp 第一行 ≠ version.toml 鎖定 digest → 待辦「materialize 舊版」" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uD"><g x=720 y=36 w=360 h=57/></c>
<c id="d3b" v="初始檔、baseline/&lt;repo&gt;/、version.toml（由 git revert 還原，不是 sync 寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uD"><g x=20 y=172 w=220 h=57/></c>
<c id="d1b" v="docker image inspect：舊版本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uD"><g x=460 y=114 w=170 h=174/></c>
<c id="d1p" v="無：docker pull" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=630 y=308 w=70 h=57/></c>
<c id="d1g" v="&lt;repo&gt;-dist@digest⏎（version.toml 還原後的舊版）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="uD"><g x=1100 y=308 w=180 h=57/></c>
<c id="d1c" v="docker create &lt;img&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=460 y=385 w=240 h=40/></c>
<c id="d1d" v="docker cp c:/dist/. &lt;tmp&gt;/&lt;repo&gt;/" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=460 y=445 w=240 h=42/></c>
<c id="d1e" v="docker rm 該容器" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=460 y=507 w=240 h=40/></c>
<c id="d1f" v="docker run … -v &lt;tmp&gt;:/dist:ro 引擎 apply sync" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uD"><g x=460 y=567 w=240 h=42/></c>
<c id="d2c" v="materialize 舊版 → cache/&lt;repo&gt;/、寫印記（只寫 cache/、gen/；初始檔與 baseline 不碰）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uD"><g x=720 y=567 w=360 h=42/></c>
<c id="d3" v="cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp（舊版；sync 寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uD"><g x=1300 y=567 w=280 h=42/></c>
<c id="de1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d0" target="d1a"></c>
<c id="de2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d1a" target="d2"></c>
<c id="de2b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d2" target="d1b"><g x=0.00 pts=920,1150;565,1150/></c>
<c id="de2n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="d1b" target="d1p"><g x=-0.75 pts=685,1247/></c>
<c id="de2g" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="d1g" target="d1p"></c>
<c id="de2y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.354;entryY=0" edge="1" source="d1b" target="d1c"><g x=-0.6/></c>
<c id="de2p" s="fs=12;exitX=0.5;exitY=1;entryX=0.854;entryY=0" edge="1" source="d1p" target="d1c"></c>
<c id="de2d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d1c" target="d1d"></c>
<c id="de2e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d1d" target="d1e"></c>
<c id="de2f" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d1e" target="d1f"></c>
<c id="de2h" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d1f" target="d2c"></c>
<c id="de3" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d2c" target="d3"></c>
<c id="de4" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d0" target="d3b"></c>
<c id="p7b_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1677 w=200 h=60/></c>
<c id="p7b_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1677 w=140 h=64/></c>
<c id="p7b_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1685 w=140 h=44/></c>
<c id="p7b_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1679 w=190 h=56/></c>
<c id="p7b_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1679 w=210 h=56/></c>
<c id="p7b_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1687 w=88 h=40/></c>
<c id="p7b_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1687 w=170 h=40/></c>
<c id="p7b_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1677 w=300 h=60/></c>
<c id="p7b_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1745 w=120 h=36/></c>
<c id="p7b_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1745 w=190 h=36/></c>
<c id="p7b_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1745 w=170 h=36/></c>
<c id="p7b_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1745 w=170 h=36/></c>
<c id="p7b_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1745 w=200 h=36/></c>
<c id="p7b_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1735 w=30 h=20/></c>
<c id="p7b_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1783 w=200 h=28/></c>
<c id="p7b_tk0" v="B／D／N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1817 w=150 h=55/></c>
<c id="p7b_tv0" v="B = baseline（上次合併時的範本副本，進 git）；D = 現況（專案裡你的那份檔）；N = 目標版範本 = 啟動器把目標版 image 展開到暫存、掛進引擎的 /dist/&lt;repo&gt;（不是 cache；v2.5 §2）；「D==B」= 你沒改過" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1817 w=610 h=55/></c>
<c id="p7b_tk1" v="逐檔判斷後詢問／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1872 w=150 h=71/></c>
<c id="p7b_tv1" v="apply = 動詞的第二段（拿到 flock、重驗指紋、建日誌後才寫檔）；三份比：N 改了才問「換成新版？」，兩邊都改才問「三方合併？」；-y 免問；拒絕 → 不動：已納管檔 state 不變只記 declined_hash，新檔（B 無）被拒才 state=declined；全部在暫存完成再逐檔原子替換；materialize 到 cache 在決定套用之後" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1872 w=610 h=71/></c>
<c id="p7b_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1943 w=150 h=40/></c>
<c id="p7b_tv2" v="同一動詞兩段：resolve 只讀只算（查目標版、輸出要拉的 image 與輸入指紋，不寫檔）→ 啟動器 docker 拉 image、展開到暫存 → apply 拿 flock 後重驗指紋才寫" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1943 w=610 h=40/></c>
<c id="p7b_tk3" v="flock／指紋" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1983 w=150 h=40/></c>
<c id="p7b_tv3" v="flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎；指紋 = resolve 讀過的檔的 hash＋鎖定 digest，apply 拿鎖後重驗，不同 → 1「請重跑」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1983 w=610 h=40/></c>
<c id="p7b_tk4" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2023 w=150 h=55/></c>
<c id="p7b_tv4" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、每個 dest 的 state（managed／appended／declined／unmanaged／deleted）＋ declined_hash、append 過的行、衝突中檔案清單、進度日誌 state；衝突重入靠它的「衝突中檔案」清單" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2023 w=610 h=55/></c>
<c id="p7b_tk5" v="git merge-file --diff3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2078 w=150 h=40/></c>
<c id="p7b_tv5" v="git 的三方合併指令；衝突時在檔內留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline ||||||| ======= &gt;&gt;&gt;&gt;&gt;&gt;&gt; 標記（我們自己的標籤）；回傳衝突數 → 映射為結束狀態 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2078 w=610 h=40/></c>
<c id="p7b_tk6" v="衝突重入（v2.2 D (0)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2118 w=150 h=40/></c>
<c id="p7b_tv6" v="再跑 upgrade 時 resolve 先看 metadata 的「衝突中檔案」：檔內仍有我們的標籤 → 2 停；檔案失蹤不算已解；都乾淨 → apply 拿鎖、建日誌後清除狀態再往下" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2118 w=610 h=40/></c>
<c id="p7b_tk7" v="--dry-run／CI 為真" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1817 w=150 h=55/></c>
<c id="p7b_tv7" v="apply --dry-run 唯讀預覽：只印會問哪些檔（哪些要換／合併／append 替換；讀 /dist/&lt;repo&gt;），不動任何檔；本機 → 0；CI 為真（CI 非空且不為 0／false = frozen）且需改 tracked 檔 → 1（-y 不解除）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1817 w=610 h=55/></c>
<c id="p7b_tk8" v="append 行／CRLF" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1872 w=150 h=40/></c>
<c id="p7b_tv8" v="strategy=append 的初始檔：upgrade 找上次插入的行（CRLF = Windows 換行 \r\n，與 LF 視為相同；其餘精確）→ 問後替換；零命中或多處 → 保留只 warn" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1872 w=610 h=40/></c>
<c id="p7b_tk9" v="二進位／symlink" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1912 w=150 h=55/></c>
<c id="p7b_tv9" v="二進位 = 不是文字的檔（圖片等）；symlink = 指向另一個路徑的捷徑；兩者不做行內合併：你沒改 → 問「X 是二進位檔，要換成新版嗎？」答應才換（v2.6 §8）；改過保留 + warn；dist/files/ 第一版禁止 symlink" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1912 w=610 h=55/></c>
<c id="p7b_tk10" v="回退／git revert" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1967 w=150 h=40/></c>
<c id="p7b_tv10" v="git revert = 產生一個反向 commit 把那次升級（version.toml、初始檔、baseline 同一 commit）整組退回；下次 just 的 sync 看印記 ≠ version.toml → 只把 cache/&lt;repo&gt;/ 換回舊版" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1967 w=610 h=40/></c>
<c id="p7b_tk11" v="GHCR／image／印記／declined／declined_hash" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2007 w=150 h=71/></c>
<c id="p7b_tv11" v="GHCR = GitHub 的容器倉庫；image = 打包好的 dist/；印記 = gen/&lt;repo&gt;.stamp（第一行 index digest，之後每檔 sha256），sync 拿它跟 version.toml 鎖定 digest 比；state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管檔拒絕本次更新 → state 不變、只記 declined_hash（= 被拒那版 N 的 sha256），N 再變才再問（v2.7 §3）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2007 w=610 h=71/></c>
<c id="p7b_tk12" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2078 w=150 h=55/></c>
<c id="p7b_tv12" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2078 w=610 h=55/></c>
</diagram>
<diagram id="v1p7bc" name="流程 v2：upgrade ── E. 自身升級 (a)(b)"><c id="title" v="流程 v2：upgrade ── E. vendor_kit 自身升級 (a)(b)（v2.2 A／B、v2.3 §2、v2.5 §7、v2.6 §5）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=124/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=144 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=144 w=320 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=620 y=144 w=380 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1020 y=144 w=200 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=144 w=360 h=28/></c>
<c id="uE" v="E. vendor_kit 自身升級（v2.3 §2 統一版、v2.5 §7、v2.6 §5）：(a) upgrade 不帶 repo 當次換新引擎並重產薄殼；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit 見「E(c)」頁；install 修復也走同樣比對" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=188 w=1600 h=1565/></c>
<c id="uE_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=1556 y=5 w=30 h=20/></c>
<c id="s0" v="(a) upgrade 不帶 repo（含 vendor_kit 自身）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE"><g x=20 y=36 w=220 h=80/></c>
<c id="s0_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=26 w=30 h=20/></c>
<c id="s1" v="docker run 舊引擎 resolve upgrade（全部）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE"><g x=280 y=52 w=280 h=48/></c>
<c id="s1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=536 y=42 w=30 h=20/></c>
<c id="s2a" v="resolve：先完整預檢（含 dev 中工具 → 1 提示 undev）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=56 w=360 h=40/></c>
<c id="s2a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=46 w=30 h=20/></c>
<c id="s2n" v="否 → 只升工具（走「B. 手動路徑（1）」頁，對每個工具；Q27 彙總）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE"><g x=20 y=136 w=220 h=80/></c>
<c id="s2n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=126 w=30 h=20/></c>
<c id="s2q" v="引擎有新版？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE"><g x=600 y=151 w=240 h=50/></c>
<c id="s2q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=816 y=141 w=30 h=20/></c>
<c id="s2b" v="是：apply（舊引擎）：flock 專案目錄" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=236 w=360 h=40/></c>
<c id="s2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=226 w=30 h=20/></c>
<c id="s2c" v="重驗指紋（不同 → 1「請重跑」，橙）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=296 w=360 h=40/></c>
<c id="s2c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=286 w=30 h=20/></c>
<c id="s2d" v="建進度日誌（第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=356 w=360 h=40/></c>
<c id="s2d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=346 w=30 h=20/></c>
<c id="s2e" v="只改 version.toml 第一行 → 新引擎 ref（其餘工具等重跑原指令）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=416 w=360 h=48/></c>
<c id="s2e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=406 w=30 h=20/></c>
<c id="s2f" v="version.toml 第一行 = 新引擎 ref" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uE"><g x=1260 y=420 w=280 h=40/></c>
<c id="s2g" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE"><g x=610 y=484 w=360 h=40/></c>
<c id="s2g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=946 y=474 w=30 h=20/></c>
<c id="s2h" v="apply 後再 grep version.toml 第一行（local 覆寫 vendor_kit= 優先；v2.6 §5，不從 stdout 讀）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE"><g x=280 y=544 w=280 h=63/></c>
<c id="s2h_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=536 y=534 w=30 h=20/></c>
<c id="s2hx" v="否 → 1：apply 未改第一行（印 apply 的錯誤）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uE"><g x=20 y=628 w=220 h=80/></c>
<c id="s2hx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=618 w=30 h=20/></c>
<c id="s2h2" v="第一行變了且 == 計畫的 engine？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE"><g x=300 y=627 w=240 h=81/></c>
<c id="s2h2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=516 y=617 w=30 h=20/></c>
<c id="s2ln" v="是 → docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE"><g x=310 y=728 w=220 h=112/></c>
<c id="s2ln_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=506 y=718 w=30 h=20/></c>
<c id="s2lp" v="無：docker pull 新引擎" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE"><g x=500 y=860 w=80 h=79/></c>
<c id="s2lp_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=556 y=850 w=30 h=20/></c>
<c id="s2gi" v="vendor_kit:vY⏎（新引擎）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="uE"><g x=1000 y=878 w=200 h=42/></c>
<c id="s2lv" v="覆寫中且 .Id ≠ 記的 image ID？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE"><g x=310 y=959 w=220 h=112/></c>
<c id="s2lv_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=506 y=949 w=30 h=20/></c>
<c id="s2lx" v="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uE"><g x=600 y=975 w=240 h=80/></c>
<c id="s2lx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=816 y=965 w=30 h=20/></c>
<c id="s4" v="→ 接「E(c) upgrade vendor_kit」頁的「docker run 該引擎」格（同一次指令內；第二次第一行又變 → 1 不再重跑）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE"><g x=20 y=1091 w=220 h=146/></c>
<c id="s4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=1081 w=30 h=20/></c>
<c id="s2r" v="docker run 新引擎 upgrade vendor_kit" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE"><g x=260 y=1144 w=320 h=40/></c>
<c id="s2r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=556 y=1134 w=30 h=20/></c>
<c id="s5" v="(b) 別人 pull 後（第一行已變）打任何 just" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE"><g x=20 y=1257 w=220 h=58/></c>
<c id="s5_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=1247 w=30 h=20/></c>
<c id="s6a" v="啟動器：grep version.toml 第一行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE"><g x=280 y=1266 w=280 h=40/></c>
<c id="s6a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=536 y=1256 w=30 h=20/></c>
<c id="s8" v="否 → 1：印「vendor_kit 已更新 vX → vY，請執行：just vendor_kit upgrade vendor_kit」→ 使用者打 (c)（「E(c)」頁）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE"><g x=20 y=1335 w=220 h=146/></c>
<c id="s8_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=216 y=1325 w=30 h=20/></c>
<c id="s6q" v="gen/.stamp 的引擎 ref == 第一行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE"><g x=300 y=1352 w=240 h=112/></c>
<c id="s6q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE"><g x=516 y=1342 w=30 h=20/></c>
<c id="s6y" v="是 → 正常跑（「sync（1）」頁）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE"><g x=300 y=1501 w=240 h=58/></c>
<c id="se1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s0" target="s1"></c>
<c id="se2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s1" target="s2a"></c>
<c id="se2q" s="fs=12;exitX=0.306;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2a" target="s2q"></c>
<c id="se2n" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s2q" target="s2n"></c>
<c id="se3" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.306;entryY=0" edge="1" source="s2q" target="s2b"><g x=-0.6/></c>
<c id="se3c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2b" target="s2c"></c>
<c id="se3d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2c" target="s2d"></c>
<c id="se3e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2d" target="s2e"></c>
<c id="se4" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s2e" target="s2f"></c>
<c id="se3g" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2e" target="s2g"></c>
<c id="se5" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2g" target="s2h"><g x=0.00 pts=702,722;440,722/></c>
<c id="se5h" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2h" target="s2h2"></c>
<c id="se5x" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s2h2" target="s2hx"></c>
<c id="se5l" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2h2" target="s2ln"><g x=-0.6/></c>
<c id="se6p" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="s2ln" target="s2lp"><g x=-0.49 pts=560,972/></c>
<c id="se6" v="拉" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s2gi" target="s2lp"></c>
<c id="se6y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2ln" target="s2lv"><g x=-0.6/></c>
<c id="se6pv" s="fs=12;exitX=0.25;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2lp" target="s2lv"><g x=0.00 pts=540,1137;440,1137/></c>
<c id="se6px" v="失敗" s="fs=12;exitX=0.75;exitY=1;entryX=0;entryY=0.5" edge="1" source="s2lp" target="s2lx"><g x=-0.34 pts=580,1203/></c>
<c id="se6vx" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s2lv" target="s2lx"></c>
<c id="se6vr" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s2lv" target="s2r"><g x=-0.6/></c>
<c id="se7" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s2r" target="s4"></c>
<c id="se8" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s5" target="s6a"></c>
<c id="se8q" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s6a" target="s6q"></c>
<c id="se9" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s6q" target="s8"></c>
<c id="se9y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s6q" target="s6y"><g x=-0.6/></c>
<c id="p7bc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1769 w=200 h=60/></c>
<c id="p7bc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1769 w=140 h=64/></c>
<c id="p7bc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1777 w=140 h=44/></c>
<c id="p7bc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1771 w=190 h=56/></c>
<c id="p7bc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1771 w=210 h=56/></c>
<c id="p7bc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1779 w=88 h=40/></c>
<c id="p7bc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1779 w=170 h=40/></c>
<c id="p7bc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1769 w=300 h=60/></c>
<c id="p7bc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1837 w=120 h=36/></c>
<c id="p7bc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1837 w=190 h=36/></c>
<c id="p7bc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1837 w=170 h=36/></c>
<c id="p7bc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1837 w=170 h=36/></c>
<c id="p7bc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1837 w=200 h=36/></c>
<c id="p7bc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1827 w=30 h=20/></c>
<c id="p7bc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1875 w=200 h=28/></c>
<c id="p7bc_tk0" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1909 w=150 h=86/></c>
<c id="p7bc_tv0" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&lt;tag&gt;]：查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1909 w=610 h=86/></c>
<c id="p7bc_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1995 w=150 h=55/></c>
<c id="p7bc_tv1" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1995 w=610 h=55/></c>
<c id="p7bc_tk2" v="薄殼首行自描述（Q17）／上次產物／相符" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2050 w=150 h=55/></c>
<c id="p7bc_tv2" v="薄殼每檔首行 # vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 hash&gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2050 w=610 h=55/></c>
<c id="p7bc_tk3" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2105 w=150 h=40/></c>
<c id="p7bc_tv3" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2105 w=610 h=40/></c>
<c id="p7bc_tk4" v="GHCR／registry／引擎 image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2145 w=150 h=55/></c>
<c id="p7bc_tv4" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&lt;tag&gt; 不查）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2145 w=610 h=55/></c>
<c id="p7bc_tk5" v="image ID／docker image inspect／local 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2200 w=150 h=55/></c>
<c id="p7bc_tv5" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2200 w=610 h=55/></c>
<c id="p7bc_tk6" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1909 w=150 h=55/></c>
<c id="p7bc_tv6" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1909 w=610 h=55/></c>
<c id="p7bc_tk7" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1964 w=150 h=40/></c>
<c id="p7bc_tv7" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1964 w=610 h=40/></c>
<c id="p7bc_tk8" v="dev 覆寫／undev／多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2004 w=150 h=40/></c>
<c id="p7bc_tv8" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2004 w=610 h=40/></c>
<c id="p7bc_tk9" v="--protocol P／降版（Q19）／結束碼 3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2044 w=150 h=71/></c>
<c id="p7bc_tv9" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&lt;舊版&gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2044 w=610 h=71/></c>
<c id="p7bc_tk10" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2115 w=150 h=55/></c>
<c id="p7bc_tv10" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2115 w=610 h=55/></c>
</diagram>
<diagram id="v1p7bcc" name="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）"><c id="title" v="流程 v2：upgrade ── E(c) upgrade vendor_kit（1）啟動器 → 查 registry → 改第一行（v2.7 §5）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=124/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=144 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=144 w=320 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=620 y=144 w=380 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1020 y=144 w=200 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=144 w=360 h=28/></c>
<c id="uE2" v="E(c)（1）upgrade vendor_kit[@&lt;tag&gt;]（單段救援）：grep 第一行 → inspect → 無才 pull → 拿鎖、重驗 → 薄殼 == 上次產物？（否 → 1 零寫入，v2.8 §3）→ @舊版無法無損讀 → 3 → 查 registry → 有新版 → 改第一行 → 用新引擎再跑；否則見「E(c)（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=188 w=1600 h=1442/></c>
<c id="uE2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=1556 y=5 w=30 h=20/></c>
<c id="s10" v="(c) just vendor_kit upgrade vendor_kit[@&lt;tag&gt;]（(b) 提示後由使用者打；也可直接打）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE2"><g x=20 y=36 w=220 h=124/></c>
<c id="s10_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=216 y=26 w=30 h=20/></c>
<c id="s11a" v="grep version.toml 第一行取引擎 ref（local 覆寫 vendor_kit= 優先；跳過 gen/.stamp 比對）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE2"><g x=280 y=66 w=280 h=63/></c>
<c id="s11a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=536 y=56 w=30 h=20/></c>
<c id="s11n" v="docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=280 y=180 w=220 h=112/></c>
<c id="s11n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=476 y=170 w=30 h=20/></c>
<c id="s11p" v="無：docker pull 該引擎" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE2"><g x=500 y=312 w=80 h=79/></c>
<c id="s11p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=556 y=302 w=30 h=20/></c>
<c id="s11g" v="vendor_kit:vN⏎（第一行指到的引擎）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="uE2"><g x=1000 y=330 w=200 h=42/></c>
<c id="s11v" v="覆寫中且 .Id ≠ 記的 image ID？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=280 y=411 w=220 h=112/></c>
<c id="s11v_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=476 y=401 w=30 h=20/></c>
<c id="s11x" v="拉不到／image ID 不符（同 tag 重 build）→ 1：印原因" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="uE2"><g x=600 y=427 w=240 h=80/></c>
<c id="s11x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=816 y=417 w=30 h=20/></c>
<c id="s10a" v="來自「E. 自身升級 (a)(b)」頁：(a) 啟動器已用新引擎 ref（不再走 grep／inspect）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="uE2"><g x=20 y=543 w=220 h=102/></c>
<c id="s11r" v="否：docker run 該引擎 upgrade vendor_kit" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE2"><g x=260 y=574 w=320 h=40/></c>
<c id="s11r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=556 y=564 w=30 h=20/></c>
<c id="s12a" v="flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE2"><g x=610 y=574 w=360 h=40/></c>
<c id="s12a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=946 y=564 w=30 h=20/></c>
<c id="s12b" v="重驗指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE2"><g x=600 y=674 w=220 h=40/></c>
<c id="s12b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=796 y=664 w=30 h=20/></c>
<c id="s12bx" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE2"><g x=850 y=665 w=130 h=58/></c>
<c id="s12bx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=956 y=655 w=30 h=20/></c>
<c id="s12sx" v="否 → 1：偵測到薄殼被修改，列差異不動（零寫入；git checkout 還原後再跑）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE2"><g x=20 y=748 w=220 h=102/></c>
<c id="s12sx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=216 y=738 w=30 h=20/></c>
<c id="s12s" v="薄殼 == 上次產物？（首行自描述 hash、未被改）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=600 y=743 w=260 h=112/></c>
<c id="s12s_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=836 y=733 w=30 h=20/></c>
<c id="s12sn" v="「上次產物」= 薄殼首行自描述的 sha256 與其餘內容相符（Q17）；同一判斷 install 頁也用；在拿鎖重驗之後、任何寫入（含改第一行）之前檢查，不符 → 1 列差異、零寫入（v2.8 §3）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="uE2"><g x=1220 y=760 w=360 h=79/></c>
<c id="s12sn_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=1556 y=750 w=30 h=20/></c>
<c id="s12dx" v="是 → 3：印 6-10「目標引擎無法無損讀取現有檔；未修改任何檔；要退回請 git revert」（零寫入）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE2"><g x=20 y=875 w=220 h=124/></c>
<c id="s12dx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=216 y=865 w=30 h=20/></c>
<c id="s12d" v="是 → @&lt;tag&gt; 為舊版且無法無損讀現有檔（P／schema）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=600 y=881 w=260 h=112/></c>
<c id="s12d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=836 y=871 w=30 h=20/></c>
<c id="s12t" v="否 → @&lt;tag&gt; 指定或 CI 為真（frozen）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=600 y=1019 w=260 h=112/></c>
<c id="s12t_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=836 y=1009 w=30 h=20/></c>
<c id="s12tn" v="是：不查 registry" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE2"><g x=880 y=1051 w=100 h=48/></c>
<c id="s12tn_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=956 y=1041 w=30 h=20/></c>
<c id="s12u" v="否：查 registry（GHCR）取引擎最新正式版" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE2"><g x=600 y=1151 w=260 h=48/></c>
<c id="s12u_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=836 y=1141 w=30 h=20/></c>
<c id="s12v" v="有新版？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE2"><g x=600 y=1230 w=200 h=50/></c>
<c id="s12v_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=776 y=1220 w=30 h=20/></c>
<c id="s12vz" v="否／不查 → 續「E(c)（2）」頁：薄殼比對與重產" s="text;fs=12;sc=none;fc=none;fst=1" parent="uE2"><g x=870 y=1219 w=110 h=73/></c>
<c id="s12hz" v="→ 用新引擎從本頁「docker run 該引擎」格再跑一次（同一次指令內；第二次第一行又變 → 1 印 6-2b）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE2"><g x=20 y=1312 w=220 h=124/></c>
<c id="s12hz_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=216 y=1302 w=30 h=20/></c>
<c id="s12h" v="啟動器：apply 前後 grep 第一行 → 變了 → 用新引擎再跑 upgrade vendor_kit（接手邏輯同「E(a)(b)」頁）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="uE2"><g x=270 y=1342 w=300 h=63/></c>
<c id="s12h_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=546 y=1332 w=30 h=20/></c>
<c id="s12w" v="是：改 version.toml 第一行 = 新引擎 ref（其餘不動）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE2"><g x=600 y=1350 w=260 h=48/></c>
<c id="s12w_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE2"><g x=836 y=1340 w=30 h=20/></c>
<c id="s12wf" v="version.toml 第一行 = 新引擎 ref（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uE2"><g x=1220 y=1354 w=360 h=40/></c>
<c id="se11" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s10" target="s11a"></c>
<c id="se11q" s="fs=12;exitX=0.393;exitY=1;entryX=0.5;entryY=0" edge="1" source="s11a" target="s11n"></c>
<c id="se11p" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="s11n" target="s11p"><g x=-0.66 pts=560,424/></c>
<c id="se11g" v="拉" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s11g" target="s11p"></c>
<c id="se11v" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s11n" target="s11v"><g x=-0.6/></c>
<c id="se11pv" s="fs=12;exitX=0.25;exitY=1;entryX=0.5;entryY=0" edge="1" source="s11p" target="s11v"><g x=0.00 pts=540,589;410,589/></c>
<c id="se11px" v="失敗" s="fs=12;exitX=0.75;exitY=1;entryX=0;entryY=0.5" edge="1" source="s11p" target="s11x"><g x=-0.34 pts=580,655/></c>
<c id="se11vx" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s11v" target="s11x"></c>
<c id="se11vr" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.406;entryY=0" edge="1" source="s11v" target="s11r"><g x=-0.6/></c>
<c id="se11e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s10a" target="s11r"></c>
<c id="se12" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s11r" target="s12a"></c>
<c id="se12b" s="fs=12;exitX=0.5;exitY=1;entryX=0.864;entryY=0" edge="1" source="s12a" target="s12b"></c>
<c id="se12x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s12b" target="s12bx"></c>
<c id="se12s" s="fs=12;exitX=0.591;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12b" target="s12s"></c>
<c id="se12sx" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s12s" target="s12sx"></c>
<c id="se12d" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12s" target="s12d"><g x=-0.6/></c>
<c id="se12dx" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s12d" target="s12dx"></c>
<c id="se12t" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12d" target="s12t"><g x=-0.6/></c>
<c id="se12tn" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s12t" target="s12tn"></c>
<c id="se12u" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12t" target="s12u"><g x=-0.6/></c>
<c id="se12v" s="fs=12;exitX=0.385;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12u" target="s12v"></c>
<c id="se12vn" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s12v" target="s12vz"></c>
<c id="se12tv" s="fs=12;exitX=0.5;exitY=1;entryX=0.545;entryY=0" edge="1" source="s12tn" target="s12vz"></c>
<c id="se12w" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.385;entryY=0" edge="1" source="s12v" target="s12w"><g x=-0.6/></c>
<c id="se12wf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s12w" target="s12wf"></c>
<c id="se12wh" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s12w" target="s12h"></c>
<c id="se12hz" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s12h" target="s12hz"></c>
<c id="p7bcc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1646 w=200 h=60/></c>
<c id="p7bcc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1646 w=140 h=64/></c>
<c id="p7bcc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1654 w=140 h=44/></c>
<c id="p7bcc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1648 w=190 h=56/></c>
<c id="p7bcc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1648 w=210 h=56/></c>
<c id="p7bcc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1656 w=88 h=40/></c>
<c id="p7bcc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1656 w=170 h=40/></c>
<c id="p7bcc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1646 w=300 h=60/></c>
<c id="p7bcc_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1714 w=200 h=36/></c>
<c id="p7bcc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1714 w=120 h=36/></c>
<c id="p7bcc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1714 w=190 h=36/></c>
<c id="p7bcc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1714 w=170 h=36/></c>
<c id="p7bcc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1714 w=170 h=36/></c>
<c id="p7bcc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1714 w=200 h=36/></c>
<c id="p7bcc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1704 w=30 h=20/></c>
<c id="p7bcc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1752 w=200 h=28/></c>
<c id="p7bcc_tk0" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1786 w=150 h=86/></c>
<c id="p7bcc_tv0" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&lt;tag&gt;]：查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1786 w=610 h=86/></c>
<c id="p7bcc_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1872 w=150 h=55/></c>
<c id="p7bcc_tv1" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1872 w=610 h=55/></c>
<c id="p7bcc_tk2" v="薄殼首行自描述（Q17）／上次產物／相符" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1927 w=150 h=55/></c>
<c id="p7bcc_tv2" v="薄殼每檔首行 # vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 hash&gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1927 w=610 h=55/></c>
<c id="p7bcc_tk3" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1982 w=150 h=40/></c>
<c id="p7bcc_tv3" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1982 w=610 h=40/></c>
<c id="p7bcc_tk4" v="GHCR／registry／引擎 image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2022 w=150 h=55/></c>
<c id="p7bcc_tv4" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&lt;tag&gt; 不查）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2022 w=610 h=55/></c>
<c id="p7bcc_tk5" v="image ID／docker image inspect／local 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2077 w=150 h=55/></c>
<c id="p7bcc_tv5" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2077 w=610 h=55/></c>
<c id="p7bcc_tk6" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1786 w=150 h=55/></c>
<c id="p7bcc_tv6" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1786 w=610 h=55/></c>
<c id="p7bcc_tk7" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1841 w=150 h=40/></c>
<c id="p7bcc_tv7" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1841 w=610 h=40/></c>
<c id="p7bcc_tk8" v="dev 覆寫／undev／多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1881 w=150 h=40/></c>
<c id="p7bcc_tv8" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1881 w=610 h=40/></c>
<c id="p7bcc_tk9" v="--protocol P／降版（Q19）／結束碼 3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1921 w=150 h=71/></c>
<c id="p7bcc_tv9" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&lt;舊版&gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1921 w=610 h=71/></c>
<c id="p7bcc_tk10" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1992 w=150 h=55/></c>
<c id="p7bcc_tv10" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1992 w=610 h=55/></c>
</diagram>
<diagram id="v1p7bccc" name="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）"><c id="title" v="流程 v2：upgrade ── E(c) upgrade vendor_kit（2）薄殼比對 → 重產（v2.2 A、v2.3 §2、Q17、v2.7 §5）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §2、v2.5 §7、v2.6 §1／§5、v2.7 §5）：自身升級統一版 —— (a) 不帶 repo：resolve 先判斷「引擎有新版？」，否 → 只升工具；是 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行：變了 → local 覆寫有 vendor_kit= → docker image inspect 驗 image ID 用該 image，否則 inspect 有則不拉、無才 pull 新引擎 → 新引擎 upgrade vendor_kit；(c) 先查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版／只重產／無變更三種結果；結束 1 = 需要人動作（橙）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=124/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=144 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=144 w=320 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=620 y=144 w=380 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1020 y=144 w=200 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=144 w=360 h=28/></c>
<c id="uE3" v="E(c)（2）薄殼比對與重產（承「E(c)（1）」頁：無新版或不查，第一行未變；薄殼 == 上次產物已在 (1) 拿鎖重驗後驗過，v2.8 §3）：已是本引擎產物？→ 是 → 0 無變更；否 → 建日誌 → 重產薄殼四檔 + gen/.stamp + tools.just → 刪日誌 → 1" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=188 w=1600 h=900/></c>
<c id="uE3_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=1556 y=5 w=30 h=20/></c>
<c id="s12z0" v="來自「E(c)（1）」頁：無新版／不查（第一行未變；已拿鎖、重驗，且薄殼 == 上次產物）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="uE3"><g x=610 y=36 w=360 h=80/></c>
<c id="s12n" v="「薄殼 == 上次產物」（首行自描述 sha256 與其餘內容相符，Q17）已在「E(c)（1）」頁拿鎖重驗後、任何寫入前驗過（v2.8 §3）；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 0 無變更（v2.7 §5）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="uE3"><g x=1220 y=152 w=360 h=79/></c>
<c id="s12n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=1556 y=142 w=30 h=20/></c>
<c id="s12z" v="是 → 0：無變更（薄殼相符，已是本引擎產物）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="uE3"><g x=20 y=163 w=220 h=58/></c>
<c id="s12z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=216 y=153 w=30 h=20/></c>
<c id="s12e" v="首行 engine == 本引擎且 gen/.stamp 相符？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="uE3"><g x=600 y=136 w=300 h=112/></c>
<c id="s12e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=876 y=126 w=30 h=20/></c>
<c id="s12l" v="否：建進度日誌（第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE3"><g x=610 y=268 w=360 h=40/></c>
<c id="s12l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=946 y=258 w=30 h=20/></c>
<c id="s13" v="重產薄殼四檔（暫存 → 原子替換）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE3"><g x=610 y=387 w=360 h=40/></c>
<c id="s13_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=946 y=377 w=30 h=20/></c>
<c id="s13f" v="薄殼四檔（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="uE3"><g x=1220 y=328 w=360 h=158/></c>
<c id="s13f_0" v=".vendor_kit/.gitignore" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="s13f"><g x=8 y=26 w=344 h=26/></c>
<c id="s13f_1" v=".vendor_kit/entry.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="s13f"><g x=8 y=58 w=344 h=26/></c>
<c id="s13f_2" v=".vendor_kit/vendor.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="s13f"><g x=8 y=90 w=344 h=26/></c>
<c id="s13f_3" v=".vendor_kit/ci/check.sh" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="s13f"><g x=8 y=122 w=344 h=26/></c>
<c id="s13b" v="寫 gen/.stamp（本引擎 ref）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE3"><g x=610 y=506 w=360 h=40/></c>
<c id="s13b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=946 y=496 w=30 h=20/></c>
<c id="s13bf" v="gen/.stamp（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uE3"><g x=1220 y=506 w=360 h=40/></c>
<c id="s13c" v="重生 gen/tools.just（用本引擎的規則；mod? 行）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE3"><g x=610 y=566 w=360 h=40/></c>
<c id="s13c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=946 y=556 w=30 h=20/></c>
<c id="s13cf" v="gen/tools.just（不進 git；mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="uE3"><g x=1220 y=566 w=360 h=40/></c>
<c id="s13x" v="失敗 → 1：「引擎版本已鎖定為 vY，但薄殼尚未重產；請排除上述錯誤後執行：just vendor_kit upgrade vendor_kit」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE3"><g x=20 y=626 w=220 h=146/></c>
<c id="s13x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=216 y=616 w=30 h=20/></c>
<c id="s13d" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="uE3"><g x=610 y=679 w=360 h=40/></c>
<c id="s13d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=946 y=669 w=30 h=20/></c>
<c id="s14" v="1：印「已升級引擎 vX → vY 並重產薄殼，請 commit .vendor_kit/ 並再跑原指令」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="uE3"><g x=20 y=792 w=220 h=102/></c>
<c id="s14_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="uE3"><g x=216 y=782 w=30 h=20/></c>
<c id="se13" s="fs=12;exitX=0.389;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12z0" target="s12e"></c>
<c id="se15z" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="s12e" target="s12z"></c>
<c id="se15l" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.389;entryY=0" edge="1" source="s12e" target="s12l"><g x=-0.6/></c>
<c id="se15s" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s12l" target="s13"></c>
<c id="se16" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s13" target="s13f"></c>
<c id="se17" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s13" target="s13b"></c>
<c id="se18" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s13b" target="s13bf"></c>
<c id="se18b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s13b" target="s13c"></c>
<c id="se18c" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="s13c" target="s13cf"></c>
<c id="se18d" v="成功" s="fs=12;exitX=0.6;exitY=1;entryX=0.6;entryY=0" edge="1" source="s13c" target="s13d"><g x=-0.6/></c>
<c id="se18x" v="失敗" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="s13c" target="s13x"><g x=0.00 pts=702,804;150,804/></c>
<c id="se19" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="s13d" target="s14"><g x=-0.82 pts=810,1031/></c>
<c id="p7bcd_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1104 w=200 h=60/></c>
<c id="p7bcd_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1104 w=140 h=64/></c>
<c id="p7bcd_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1112 w=140 h=44/></c>
<c id="p7bcd_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1106 w=190 h=56/></c>
<c id="p7bcd_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1106 w=210 h=56/></c>
<c id="p7bcd_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1114 w=88 h=40/></c>
<c id="p7bcd_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1114 w=170 h=40/></c>
<c id="p7bcd_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1104 w=300 h=60/></c>
<c id="p7bcd_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1172 w=200 h=36/></c>
<c id="p7bcd_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1172 w=120 h=36/></c>
<c id="p7bcd_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1172 w=190 h=36/></c>
<c id="p7bcd_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1172 w=170 h=36/></c>
<c id="p7bcd_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1172 w=170 h=36/></c>
<c id="p7bcd_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1172 w=200 h=36/></c>
<c id="p7bcd_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1162 w=30 h=20/></c>
<c id="p7bcd_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1210 w=200 h=28/></c>
<c id="p7bcd_tk0" v="自身升級（v2.3 §2、v2.5 §7、v2.6 §5、v2.7 §5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1244 w=150 h=86/></c>
<c id="p7bcd_tv0" v="(a) 不帶 repo：resolve 先判斷引擎有沒有新版；有 → 舊引擎 apply（拿鎖、重驗、建日誌）只改第一行 → 啟動器 apply 前後 grep 第一行比對、變了就同一次指令內用新引擎跑 upgrade vendor_kit → 1；(b) 別人 pull 後只回 1 提示；(c) upgrade vendor_kit[@&lt;tag&gt;]：查 registry（@&lt;tag&gt;／frozen 不查）→ 有新版 → 改第一行、用新引擎重產 → 1；無新版 → 薄殼相符 → 0 無變更、否則重產 → 1；@舊版無法無損讀 → 3" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1244 w=610 h=86/></c>
<c id="p7bcd_tk1" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1330 w=150 h=55/></c>
<c id="p7bcd_tv1" v="同一動詞兩段：resolve 只讀只算（預檢、查引擎最新版、輸出指紋）；apply 拿 flock、重驗指紋、建日誌後才寫；舊引擎的 apply 只改 version.toml 第一行；upgrade vendor_kit 本身是單段（一次 docker run）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1330 w=610 h=55/></c>
<c id="p7bcd_tk2" v="薄殼首行自描述（Q17）／上次產物／相符" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1385 w=150 h=55/></c>
<c id="p7bcd_tv2" v="薄殼每檔首行 # vendor_kit-shell/&lt;P&gt; engine=&lt;vX&gt; sha256=&lt;其餘內容 hash&gt;；「薄殼 == 上次產物」= 首行 hash 與內容相符（引擎重算 + 對 image 內模板二次比對），被改過 → 1 列差異不動；「薄殼相符」= 首行 engine 已是本引擎且 gen/.stamp 相符 → 不用重產 → 0 無變更" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1385 w=610 h=55/></c>
<c id="p7bcd_tk3" v="gen/.stamp" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1440 w=150 h=40/></c>
<c id="p7bcd_tv3" v="不進 git；只記引擎 ref（v2.4 Q17）；只由 install／upgrade vendor_kit 寫；啟動器每次 just 拿它跟 version.toml 第一行比，不符 → 1 提示 upgrade vendor_kit（需要人動作）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1440 w=610 h=40/></c>
<c id="p7bcd_tk4" v="GHCR／registry／引擎 image／引擎 ref" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1480 w=150 h=55/></c>
<c id="p7bcd_tv4" v="GHCR = GitHub 的容器倉庫（registry）；引擎 image = ghcr.io/…/vendor_kit:vN；引擎 ref = version.toml 第一行指到的那一個（tag@digest）；查 registry = 列 tags 取最新正式版（frozen 或 @&lt;tag&gt; 不查）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1480 w=610 h=55/></c>
<c id="p7bcd_tk5" v="image ID／docker image inspect／local 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1535 w=150 h=55/></c>
<c id="p7bcd_tv5" v="本機引擎覆寫（dev vendor_kit -i）在 version.local.toml 記 tag + image ID；啟動器每次先 docker image inspect：本機有就不 pull（覆寫時 .Id 必須 == 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1535 w=610 h=55/></c>
<c id="p7bcd_tk6" v="metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1244 w=150 h=55/></c>
<c id="p7bcd_tv6" v="baseline/&lt;repo&gt;/.vendor_kit.toml：來源、最後合併版本、完成標記、append 行、每個 dest 的 state 與 declined_hash、進度日誌 state；不帶 repo 的 upgrade 預檢會讀每個工具的 metadata；schema 遷移由 upgrade vendor_kit 做並在 dry-run 明列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1244 w=610 h=55/></c>
<c id="p7bcd_tk7" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1299 w=150 h=40/></c>
<c id="p7bcd_tv7" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗，不同 → 1「請重跑」；進度日誌 = 第一個寫入前建、最後一步刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1299 w=610 h=40/></c>
<c id="p7bcd_tk8" v="dev 覆寫／undev／多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1339 w=150 h=40/></c>
<c id="p7bcd_tv8" v="工具在 version.local.toml 有 path:&lt;dir&gt; 覆寫；不帶 repo 的 upgrade 預檢遇到 → 1 提示先 undev（v2.5 §6）；多工具做得完的做完，最後回最需要處理的碼：1 &gt; 2 &gt; 0，訊息全列" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1339 w=610 h=40/></c>
<c id="p7bcd_tk9" v="--protocol P／降版（Q19）／結束碼 3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1379 w=150 h=71/></c>
<c id="p7bcd_tv9" v="薄殼每次呼叫附 --protocol P（v2.4 Q16）；舊薄殼跑新 major 引擎的一般動詞 → 乾淨回 3 提示先 upgrade vendor_kit；upgrade vendor_kit@&lt;舊版&gt;：目標引擎（以 image LABEL 的 P／schema 判）能無損讀現有檔才做，否則改檔前拒絕 3 印 6-10（零寫入；要退回請 git revert）；救援路徑（install／upgrade vendor_kit／sync 不符提示）永久可用" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1379 w=610 h=71/></c>
<c id="p7bcd_tk10" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1450 w=150 h=55/></c>
<c id="p7bcd_tv10" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1450 w=610 h=55/></c>
</diagram>
<diagram id="v1p8" name="流程 v2：dev &lt;repo&gt;"><c id="title" v="流程 v2：dev &lt;repo&gt;（§2 dev 列；v2.1 B、v2.2 B、v2.3 §3；&lt;repo&gt; = 工具 repo 名）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&lt;repo&gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="vA" v="dev &lt;repo&gt; -p &lt;dir&gt;：工具 path 覆寫（v2.1 B）—— 用本機工具 repo 的 dist/ 取代 image（不進 git；CI 拒絕；工具必須已在 version.toml；不經 docker create/cp）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=872/></c>
<c id="vA_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=1556 y=5 w=30 h=20/></c>
<c id="d0" v="just vendor_kit dev &lt;repo&gt; -p &lt;dir&gt;" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vA"><g x=20 y=48 w=220 h=58/></c>
<c id="d1q" v="&lt;dir&gt;/dist/init.toml 存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vA"><g x=220 y=36 w=320 h=81/></c>
<c id="d1q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=516 y=26 w=30 h=20/></c>
<c id="d1x" v="否 → 1：&lt;dir&gt;/dist/init.toml 不存在" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vA"><g x=16 y=137 w=227 h=80/></c>
<c id="d1x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=219 y=127 w=30 h=20/></c>
<c id="d1m" v="是：準備掛載 -v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro（唯讀）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vA"><g x=336 y=146 w=204 h=63/></c>
<c id="d1m_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=516 y=136 w=30 h=20/></c>
<c id="d1" v="docker run 引擎 dev &lt;repo&gt; -p &lt;dir&gt;（不經 docker create/cp）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vA"><g x=340 y=237 w=200 h=63/></c>
<c id="d1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=516 y=227 w=30 h=20/></c>
<c id="d3a" v="是 → 1：CI 拒絕 dev" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vA"><g x=20 y=340 w=220 h=40/></c>
<c id="d2a" v="CI 為真？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vA"><g x=560 y=320 w=130 h=81/></c>
<c id="d2b" v="已接入 &lt;repo&gt;？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vA"><g x=720 y=336 w=240 h=50/></c>
<c id="d3c" v="否 → 1：dist/ 或 init.toml 不合法" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vA"><g x=20 y=421 w=220 h=58/></c>
<c id="d2c" v="dist 合法？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vA"><g x=560 y=425 w=180 h=50/></c>
<c id="d3b" v="否 → 1：未接入，請先 add &lt;repo&gt;" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vA"><g x=770 y=421 w=190 h=58/></c>
<c id="d6a" v="是：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vA"><g x=560 y=499 w=400 h=40/></c>
<c id="d6a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=936 y=489 w=30 h=20/></c>
<c id="d6" v="寫 version.local.toml：&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;（.vendor_kit/.gitignore 已排除它；不碰 .git/info/exclude）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vA"><g x=560 y=559 w=400 h=63/></c>
<c id="d6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=936 y=549 w=30 h=20/></c>
<c id="d6f" v="＋version.local.toml（不進 git）：&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vA"><g x=1220 y=570 w=360 h=42/></c>
<c id="d7" v="cache/&lt;repo&gt;/ 改為 symlink → &lt;dir&gt;/dist（本機工具 repo 的 dist/，唯讀）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vA"><g x=560 y=642 w=400 h=42/></c>
<c id="d7f" v="cache/&lt;repo&gt;/ → &lt;dir&gt;/dist（symlink，內容不複製）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vA"><g x=1220 y=643 w=360 h=40/></c>
<c id="d7b" v="寫印記 gen/&lt;repo&gt;.stamp 第一行 = path:&lt;dir&gt;（印記不放在 symlink 裡）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vA"><g x=560 y=704 w=400 h=48/></c>
<c id="d7b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=936 y=694 w=30 h=20/></c>
<c id="d7bf" v="gen/&lt;repo&gt;.stamp 第一行：path:&lt;dir&gt;（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vA"><g x=1220 y=708 w=360 h=40/></c>
<c id="d8" v="0：之後每次 just 用 &lt;dir&gt;" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vA"><g x=20 y=790 w=220 h=58/></c>
<c id="d8_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=216 y=780 w=30 h=20/></c>
<c id="d9" v="dev 中的工具：sync 跳過它的 materialize／verify，仍檢查 metadata／baseline；upgrade &lt;repo&gt;／remove &lt;repo&gt; → 1 提示先 undev（v2.1 B、v2.5 §6）；不帶 repo 的 upgrade 預檢也會擋" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="vA"><g x=660 y=772 w=300 h=94/></c>
<c id="d9_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vA"><g x=936 y=762 w=30 h=20/></c>
<c id="de1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d0" target="d1q"></c>
<c id="de1x" v="否" s="fs=12;exitX=0.15;exitY=1;entryX=1;entryY=0.5" edge="1" source="d1q" target="d1x"><g x=0.03 pts=288,333/></c>
<c id="de1y" v="是" s="fs=12;exitX=0.65;exitY=1;entryX=0.451;entryY=0" edge="1" source="d1q" target="d1m"><g x=0.18819188191881908/></c>
<c id="de1m" s="fs=12;exitX=0.5;exitY=1;entryX=0.49;entryY=0" edge="1" source="d1m" target="d1"></c>
<c id="de2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d1" target="d2a"><g x=0.00 pts=460,466;645,466/></c>
<c id="de3" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="d2a" target="d3a"></c>
<c id="de4" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d2a" target="d2b"></c>
<c id="de5" v="是" s="fs=12;exitX=0.3;exitY=1;entryX=0.5;entryY=0" edge="1" source="d2b" target="d2c"><g x=0.06 pts=812,567;670,567/></c>
<c id="de6" v="否" s="fs=12;exitX=0.7;exitY=1;entryX=0.621;entryY=0" edge="1" source="d2b" target="d3b"><g x=-0.03296703296703296/></c>
<c id="de7" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="d2c" target="d3c"></c>
<c id="de8" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.225;entryY=0" edge="1" source="d2c" target="d6a"><g x=-0.6/></c>
<c id="de8b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d6a" target="d6"></c>
<c id="de9" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d6" target="d6f"></c>
<c id="de10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d6" target="d7"></c>
<c id="de11" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d7" target="d7f"></c>
<c id="de12" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="d7" target="d7b"></c>
<c id="de13" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="d7b" target="d7bf"></c>
<c id="de14" s="fs=12;exitX=0.1;exitY=1;entryX=1;entryY=0.5" edge="1" source="d7b" target="d8"><g x=-0.84 pts=620,975/></c>
<c id="p8_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1044 w=200 h=60/></c>
<c id="p8_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1044 w=140 h=64/></c>
<c id="p8_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1052 w=140 h=44/></c>
<c id="p8_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1046 w=190 h=56/></c>
<c id="p8_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1046 w=210 h=56/></c>
<c id="p8_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1054 w=88 h=40/></c>
<c id="p8_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1054 w=170 h=40/></c>
<c id="p8_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1044 w=300 h=60/></c>
<c id="p8_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1112 w=120 h=36/></c>
<c id="p8_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1112 w=150 h=36/></c>
<c id="p8_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1112 w=190 h=36/></c>
<c id="p8_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1112 w=170 h=36/></c>
<c id="p8_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1112 w=170 h=36/></c>
<c id="p8_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1112 w=200 h=36/></c>
<c id="p8_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1102 w=30 h=20/></c>
<c id="p8_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1150 w=200 h=28/></c>
<c id="p8_tk0" v="dev／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1184 w=150 h=40/></c>
<c id="p8_tv0" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1184 w=610 h=40/></c>
<c id="p8_tk1" v="覆寫兩種（v2.1 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1224 w=150 h=55/></c>
<c id="p8_tv1" v="工具 path 覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;：cache/&lt;repo&gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID：啟動器改用該本機 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1224 w=610 h=55/></c>
<c id="p8_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1279 w=150 h=40/></c>
<c id="p8_tv2" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1279 w=610 h=40/></c>
<c id="p8_tk3" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1319 w=150 h=55/></c>
<c id="p8_tv3" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + image ID（成對，undev 一起撤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1319 w=610 h=55/></c>
<c id="p8_tk4" v="symlink／印記／materialize" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1374 w=150 h=55/></c>
<c id="p8_tv4" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&lt;repo&gt;/ 不放檔案，而是指到 &lt;dir&gt;/dist；印記 gen/&lt;repo&gt;.stamp 在 symlink 外，第一行 path:&lt;dir&gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1374 w=610 h=55/></c>
<c id="p8_tk5" v="image tag／image ID／RepoDigests" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1429 w=150 h=55/></c>
<c id="p8_tv5" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1429 w=610 h=55/></c>
<c id="p8_tk6" v="GHCR／tar／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1184 w=150 h=40/></c>
<c id="p8_tv6" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &lt;tag&gt; 指定它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1184 w=610 h=40/></c>
<c id="p8_tk7" v="docker image inspect／掛載 -v" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1224 w=150 h=55/></c>
<c id="p8_tv7" v="啟動器每次 docker run 前先 docker image inspect &lt;ref 或 tag&gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro = 把本機目錄唯讀掛進容器" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1224 w=610 h=55/></c>
<c id="p8_tk8" v="統一提示／gen/.stamp（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1279 w=150 h=55/></c>
<c id="p8_tv8" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1279 w=610 h=55/></c>
<c id="p8_tk9" v="metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1334 w=150 h=40/></c>
<c id="p8_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1334 w=610 h=40/></c>
<c id="p8_tk10" v="flock／指紋／進度日誌／CI 為真" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1374 w=150 h=55/></c>
<c id="p8_tv10" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&lt;id&gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1374 w=610 h=55/></c>
<c id="p8_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1429 w=150 h=55/></c>
<c id="p8_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1429 w=610 h=55/></c>
</diagram>
<diagram id="v1p8ccc" name="流程 v2：dev vendor_kit"><c id="title" v="流程 v2：dev vendor_kit -i（§2 dev 列；v2.1 B、v2.2 B、v2.6 §1）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&lt;repo&gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="vI" v="dev vendor_kit -i &lt;本機 image tag&gt;：引擎 tag 覆寫（v2.1 B／v2.2 B）—— 只能 tag：docker load 後無 RepoDigests（實測），另記 image ID（由啟動器 docker image inspect 取得後交給引擎，v2.8 §6）；驗收測試用同一機制" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=966/></c>
<c id="vI_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=1556 y=5 w=30 h=20/></c>
<c id="v0" v="dev vendor_kit -i &lt;本機 image tag&gt;" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vI"><g x=20 y=38 w=220 h=58/></c>
<c id="v1i" v="docker image inspect &lt;tag&gt; 取 .Id（主機側；本機無此 image → 1；tar 先自己 docker load）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vI"><g x=260 y=36 w=280 h=63/></c>
<c id="v1i_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=516 y=26 w=30 h=20/></c>
<c id="v1" v="docker run 引擎 dev vendor_kit -i &lt;tag&gt;，image ID 一併交給引擎（引擎容器內不呼叫 docker）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vI"><g x=260 y=119 w=280 h=63/></c>
<c id="v1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=516 y=109 w=30 h=20/></c>
<c id="v2x" v="是 → 1：CI 拒絕 dev（請在本機執行）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vI"><g x=20 y=214 w=220 h=58/></c>
<c id="v2x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=216 y=204 w=30 h=20/></c>
<c id="v2q" v="CI 為真？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vI"><g x=560 y=202 w=130 h=81/></c>
<c id="v2a" v="否：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vI"><g x=560 y=303 w=400 h=40/></c>
<c id="v2a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=936 y=293 w=30 h=20/></c>
<c id="v2b" v="寫 version.local.toml：vendor_kit = &quot;&lt;tag&gt;&quot;（不動薄殼）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vI"><g x=560 y=364 w=400 h=40/></c>
<c id="v2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=936 y=354 w=30 h=20/></c>
<c id="v3" v="＋version.local.toml：vendor_kit = &quot;&lt;tag&gt;&quot;（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vI"><g x=1220 y=363 w=360 h=42/></c>
<c id="v2c" v="寫 version.local.toml：vendor_kit_image_id = 啟動器交來的 image ID" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vI"><g x=560 y=430 w=400 h=48/></c>
<c id="v2c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=936 y=420 w=30 h=20/></c>
<c id="v3c" v="version.local.toml：＋vendor_kit_image_id 行（同 tag 重 build 才會被發現）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vI"><g x=1220 y=433 w=360 h=42/></c>
<c id="v2z" v="0：之後每次 just 用該本機 image" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vI"><g x=20 y=425 w=220 h=58/></c>
<c id="v2z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=216 y=415 w=30 h=20/></c>
<c id="v5" v="下次打任何 just" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vI"><g x=20 y=553 w=220 h=40/></c>
<c id="v6a" v="grep 引擎 ref：version.local.toml 覆寫優先 → 該 tag" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vI"><g x=260 y=549 w=280 h=48/></c>
<c id="v6a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=516 y=539 w=30 h=20/></c>
<c id="vb" v="═══ 下次 just（改用該本機 image；啟動器先比對 gen/.stamp 再起容器）═══" s="text;fs=12;sc=none;fc=none;fst=1" parent="vI"><g x=260 y=503 w=560 h=26/></c>
<c id="v8" v="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vI"><g x=20 y=617 w=220 h=102/></c>
<c id="v8_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=216 y=607 w=30 h=20/></c>
<c id="v7" v="gen/.stamp 的引擎 ref == 該 tag？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vI"><g x=265 y=628 w=270 h=81/></c>
<c id="v7_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=511 y=618 w=30 h=20/></c>
<c id="v9" v="→ 打 upgrade vendor_kit（「E(c) upgrade vendor_kit」頁）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vI"><g x=20 y=760 w=220 h=102/></c>
<c id="v9_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=216 y=750 w=30 h=20/></c>
<c id="v6b" v="是：docker image inspect &lt;tag&gt; 的 .Id == 記的 image ID？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vI"><g x=265 y=739 w=270 h=143/></c>
<c id="v6b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=511 y=729 w=30 h=20/></c>
<c id="v6x" v="否 → 1：本機 image 已變（同 tag 重 build）或不存在" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vI"><g x=560 y=770 w=240 h=80/></c>
<c id="v6x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=776 y=760 w=30 h=20/></c>
<c id="v6c" v="是：docker run &lt;tag&gt; resolve sync（不 pull）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vI"><g x=260 y=907 w=280 h=48/></c>
<c id="v6c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vI"><g x=516 y=897 w=30 h=20/></c>
<c id="v10" v="0：正常跑（用該本機 image）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vI"><g x=560 y=902 w=240 h=58/></c>
<c id="ve1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v0" target="v1i"></c>
<c id="ve1i" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v1i" target="v1"></c>
<c id="ve2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v1" target="v2q"><g x=0.00 pts=420,348;645,348/></c>
<c id="ve3" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="v2q" target="v2x"></c>
<c id="ve4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.163;entryY=0" edge="1" source="v2q" target="v2a"><g x=-0.6/></c>
<c id="ve4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v2a" target="v2b"></c>
<c id="ve5" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v2b" target="v3"></c>
<c id="ve5c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v2b" target="v2c"></c>
<c id="ve5cf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v2c" target="v3c"></c>
<c id="ve6" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="v2c" target="v2z"></c>
<c id="ve7" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v5" target="v6a"></c>
<c id="ve8" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v6a" target="v7"></c>
<c id="ve9" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="v7" target="v8"></c>
<c id="ve10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v8" target="v9"></c>
<c id="ve11" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v7" target="v6b"><g x=-0.6/></c>
<c id="ve11x" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v6b" target="v6x"></c>
<c id="ve11c" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v6b" target="v6c"><g x=-0.6/></c>
<c id="ve12" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v6c" target="v10"></c>
<c id="p8v_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1138 w=200 h=60/></c>
<c id="p8v_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1138 w=140 h=64/></c>
<c id="p8v_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1146 w=140 h=44/></c>
<c id="p8v_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1140 w=190 h=56/></c>
<c id="p8v_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1140 w=210 h=56/></c>
<c id="p8v_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1148 w=88 h=40/></c>
<c id="p8v_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1148 w=170 h=40/></c>
<c id="p8v_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1138 w=300 h=60/></c>
<c id="p8v_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1206 w=120 h=36/></c>
<c id="p8v_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1206 w=190 h=36/></c>
<c id="p8v_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1206 w=170 h=36/></c>
<c id="p8v_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1206 w=170 h=36/></c>
<c id="p8v_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1206 w=200 h=36/></c>
<c id="p8v_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1196 w=30 h=20/></c>
<c id="p8v_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1244 w=200 h=28/></c>
<c id="p8v_tk0" v="dev／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1278 w=150 h=40/></c>
<c id="p8v_tv0" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1278 w=610 h=40/></c>
<c id="p8v_tk1" v="覆寫兩種（v2.1 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1318 w=150 h=55/></c>
<c id="p8v_tv1" v="工具 path 覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;：cache/&lt;repo&gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID：啟動器改用該本機 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1318 w=610 h=55/></c>
<c id="p8v_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1373 w=150 h=40/></c>
<c id="p8v_tv2" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1373 w=610 h=40/></c>
<c id="p8v_tk3" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1413 w=150 h=55/></c>
<c id="p8v_tv3" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + image ID（成對，undev 一起撤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1413 w=610 h=55/></c>
<c id="p8v_tk4" v="symlink／印記／materialize" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1468 w=150 h=55/></c>
<c id="p8v_tv4" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&lt;repo&gt;/ 不放檔案，而是指到 &lt;dir&gt;/dist；印記 gen/&lt;repo&gt;.stamp 在 symlink 外，第一行 path:&lt;dir&gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1468 w=610 h=55/></c>
<c id="p8v_tk5" v="image tag／image ID／RepoDigests" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1523 w=150 h=55/></c>
<c id="p8v_tv5" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1523 w=610 h=55/></c>
<c id="p8v_tk6" v="GHCR／tar／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1278 w=150 h=40/></c>
<c id="p8v_tv6" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &lt;tag&gt; 指定它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1278 w=610 h=40/></c>
<c id="p8v_tk7" v="docker image inspect／掛載 -v" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1318 w=150 h=55/></c>
<c id="p8v_tv7" v="啟動器每次 docker run 前先 docker image inspect &lt;ref 或 tag&gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro = 把本機目錄唯讀掛進容器" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1318 w=610 h=55/></c>
<c id="p8v_tk8" v="統一提示／gen/.stamp（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1373 w=150 h=55/></c>
<c id="p8v_tv8" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1373 w=610 h=55/></c>
<c id="p8v_tk9" v="metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1428 w=150 h=40/></c>
<c id="p8v_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1428 w=610 h=40/></c>
<c id="p8v_tk10" v="flock／指紋／進度日誌／CI 為真" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1468 w=150 h=55/></c>
<c id="p8v_tv10" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&lt;id&gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1468 w=610 h=55/></c>
<c id="p8v_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1523 w=150 h=55/></c>
<c id="p8v_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1523 w=610 h=55/></c>
</diagram>
<diagram id="v1p8c" name="流程 v2：undev &lt;repo&gt;"><c id="title" v="流程 v2：undev（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §3／§10；&lt;repo&gt; = 工具 repo 名）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&lt;repo&gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="vB" v="undev &lt;repo&gt;：回到 version.toml 鎖定版 = resolve → docker → apply（要重新 materialize，v2.3 §5；建日誌後才動，v2.5 §10；失敗 → 1 保留可恢復狀態，v2.2 B）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=1292/></c>
<c id="vB_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=1556 y=5 w=30 h=20/></c>
<c id="u0" v="just vendor_kit undev &lt;repo&gt;" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB"><g x=20 y=36 w=220 h=58/></c>
<c id="u1" v="docker run 引擎 resolve undev &lt;repo&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=260 y=45 w=280 h=40/></c>
<c id="u3" v="否 → 0：未啟用 dev（提示）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB"><g x=20 y=116 w=220 h=58/></c>
<c id="u2" v="有 path 覆寫？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB"><g x=560 y=120 w=220 h=50/></c>
<c id="u4" v="是：resolve：要拉 &lt;repo&gt;-dist@digest（鎖定版）；輸出指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=800 y=114 w=160 h=63/></c>
<c id="u4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=104 w=30 h=20/></c>
<c id="u5a" v="docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB"><g x=260 y=197 w=170 h=143/></c>
<c id="u5a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=406 y=187 w=30 h=20/></c>
<c id="u5p" v="無：docker pull" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=440 y=360 w=100 h=48/></c>
<c id="u5p_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=516 y=350 w=30 h=20/></c>
<c id="u5g" v="&lt;repo&gt;-dist@digest（鎖定版）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="vB"><g x=980 y=364 w=220 h=40/></c>
<c id="u5b" v="docker create &lt;img&gt; /x" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=260 y=428 w=280 h=40/></c>
<c id="u5b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=516 y=418 w=30 h=20/></c>
<c id="u5c" v="docker cp c:/dist/. &lt;tmp&gt;/&lt;repo&gt;/（主機暫存）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=260 y=488 w=280 h=48/></c>
<c id="u5c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=516 y=478 w=30 h=20/></c>
<c id="u5d" v="docker rm 該容器" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=260 y=556 w=280 h=40/></c>
<c id="u5d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=516 y=546 w=30 h=20/></c>
<c id="u5r" v="docker run … -v &lt;tmp&gt;:/dist:ro 引擎 apply undev &lt;repo&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB"><g x=260 y=616 w=280 h=48/></c>
<c id="u5r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=516 y=606 w=30 h=20/></c>
<c id="u6a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=620 w=400 h=40/></c>
<c id="u6a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=610 w=30 h=20/></c>
<c id="u6b" v="重驗指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=693 w=240 h=40/></c>
<c id="u6b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=776 y=683 w=30 h=20/></c>
<c id="u6bx" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vB"><g x=820 y=684 w=140 h=58/></c>
<c id="u6bx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=674 w=30 h=20/></c>
<c id="u6l" v="建進度日誌（.vendor_kit/.tmp.undev.&lt;id&gt;.toml；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=762 w=400 h=48/></c>
<c id="u6l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=752 w=30 h=20/></c>
<c id="u6lf" v="＋.vendor_kit/.tmp.undev.&lt;id&gt;.toml（進度日誌，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB"><g x=1220 y=765 w=360 h=42/></c>
<c id="u6c" v="刪 version.local.toml 該行（&lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；最後一個覆寫 → 刪整個檔）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=830 w=400 h=48/></c>
<c id="u6c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=820 w=30 h=20/></c>
<c id="u6cf" v="version.local.toml（少一行；空了就刪檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB"><g x=1220 y=834 w=360 h=40/></c>
<c id="u6d" v="拆掉 cache/&lt;repo&gt;/ 的 symlink" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=898 w=400 h=40/></c>
<c id="u6d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=888 w=30 h=20/></c>
<c id="u6df" v="cache/&lt;repo&gt;/（不再是 symlink）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB"><g x=1220 y=898 w=360 h=40/></c>
<c id="u6e" v="materialize 鎖定版：/dist/&lt;repo&gt; 展開到暫存目錄" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=958 w=400 h=40/></c>
<c id="u6e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=948 w=30 h=20/></c>
<c id="u6e2" v="暫存 → cache/&lt;repo&gt;/（原子替換）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=1018 w=400 h=40/></c>
<c id="u6e2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=1008 w=30 h=20/></c>
<c id="u6ef" v="cache/&lt;repo&gt;/（重新展開）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB"><g x=1220 y=1018 w=360 h=40/></c>
<c id="u6f" v="寫 gen/&lt;repo&gt;.stamp（第一行 index digest，之後每檔 sha256）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=1078 w=400 h=48/></c>
<c id="u6f_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=1068 w=30 h=20/></c>
<c id="u6ff" v="gen/&lt;repo&gt;.stamp（第一行 index digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB"><g x=1220 y=1082 w=360 h=40/></c>
<c id="u6x" v="失敗（任一步）→ 1：保留可恢復狀態（下次任何動詞先恢復）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vB"><g x=20 y=1146 w=220 h=80/></c>
<c id="u6x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=216 y=1136 w=30 h=20/></c>
<c id="u6g" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB"><g x=560 y=1166 w=400 h=40/></c>
<c id="u6g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB"><g x=936 y=1156 w=30 h=20/></c>
<c id="u7" v="成功 → 0" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB"><g x=20 y=1246 w=220 h=40/></c>
<c id="ue1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u0" target="u1"></c>
<c id="ue2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u1" target="u2"><g x=0.01 pts=420,260;690,260/></c>
<c id="ue3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="u2" target="u3"></c>
<c id="ue4" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u2" target="u4"></c>
<c id="ue5" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u4" target="u5a"><g x=0.00 pts=900,343;365,343/></c>
<c id="ue5n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="u5a" target="u5p"><g x=-0.60 pts=510,424/></c>
<c id="ue6" v="拉 /dist" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="u5g" target="u5p"></c>
<c id="ue5y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.304;entryY=0" edge="1" source="u5a" target="u5b"><g x=-0.6/></c>
<c id="ue5p" s="fs=12;exitX=0.5;exitY=1;entryX=0.821;entryY=0" edge="1" source="u5p" target="u5b"></c>
<c id="ue5c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u5b" target="u5c"></c>
<c id="ue5d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u5c" target="u5d"></c>
<c id="ue7" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u5d" target="u5r"></c>
<c id="ue8" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u5r" target="u6a"></c>
<c id="ue8b" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="u6a" target="u6b"></c>
<c id="ue8x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6b" target="u6bx"></c>
<c id="ue9" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="u6b" target="u6l"></c>
<c id="ue9f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6l" target="u6lf"></c>
<c id="ue10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6l" target="u6c"></c>
<c id="ue10f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6c" target="u6cf"></c>
<c id="ue11" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6c" target="u6d"></c>
<c id="ue11f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6d" target="u6df"></c>
<c id="ue12" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6d" target="u6e"></c>
<c id="ue12b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6e" target="u6e2"></c>
<c id="ue12f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6e2" target="u6ef"></c>
<c id="ue13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6e2" target="u6f"></c>
<c id="ue13f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6f" target="u6ff"></c>
<c id="ue14" v="成功" s="fs=12;exitX=0.6;exitY=1;entryX=0.6;entryY=0" edge="1" source="u6f" target="u6g"><g x=-0.6/></c>
<c id="ue14x" v="失敗" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="u6f" target="u6x"><g x=0.00 pts=660,1292;150,1292/></c>
<c id="ue15" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="u6g" target="u7"><g x=-0.90 pts=780,1422/></c>
<c id="p8c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1464 w=200 h=60/></c>
<c id="p8c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1464 w=140 h=64/></c>
<c id="p8c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1472 w=140 h=44/></c>
<c id="p8c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1466 w=190 h=56/></c>
<c id="p8c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1466 w=210 h=56/></c>
<c id="p8c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1474 w=88 h=40/></c>
<c id="p8c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1474 w=170 h=40/></c>
<c id="p8c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1464 w=300 h=60/></c>
<c id="p8c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1532 w=120 h=36/></c>
<c id="p8c_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1532 w=190 h=36/></c>
<c id="p8c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1532 w=170 h=36/></c>
<c id="p8c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1532 w=170 h=36/></c>
<c id="p8c_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1532 w=200 h=36/></c>
<c id="p8c_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1522 w=30 h=20/></c>
<c id="p8c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1570 w=200 h=28/></c>
<c id="p8c_tk0" v="dev／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1604 w=150 h=40/></c>
<c id="p8c_tv0" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1604 w=610 h=40/></c>
<c id="p8c_tk1" v="覆寫兩種（v2.1 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1644 w=150 h=55/></c>
<c id="p8c_tv1" v="工具 path 覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;：cache/&lt;repo&gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID：啟動器改用該本機 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1644 w=610 h=55/></c>
<c id="p8c_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1699 w=150 h=40/></c>
<c id="p8c_tv2" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1699 w=610 h=40/></c>
<c id="p8c_tk3" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1739 w=150 h=55/></c>
<c id="p8c_tv3" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + image ID（成對，undev 一起撤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1739 w=610 h=55/></c>
<c id="p8c_tk4" v="symlink／印記／materialize" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1794 w=150 h=55/></c>
<c id="p8c_tv4" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&lt;repo&gt;/ 不放檔案，而是指到 &lt;dir&gt;/dist；印記 gen/&lt;repo&gt;.stamp 在 symlink 外，第一行 path:&lt;dir&gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1794 w=610 h=55/></c>
<c id="p8c_tk5" v="image tag／image ID／RepoDigests" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1849 w=150 h=55/></c>
<c id="p8c_tv5" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1849 w=610 h=55/></c>
<c id="p8c_tk6" v="GHCR／tar／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1604 w=150 h=40/></c>
<c id="p8c_tv6" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &lt;tag&gt; 指定它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1604 w=610 h=40/></c>
<c id="p8c_tk7" v="docker image inspect／掛載 -v" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1644 w=150 h=55/></c>
<c id="p8c_tv7" v="啟動器每次 docker run 前先 docker image inspect &lt;ref 或 tag&gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro = 把本機目錄唯讀掛進容器" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1644 w=610 h=55/></c>
<c id="p8c_tk8" v="統一提示／gen/.stamp（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1699 w=150 h=55/></c>
<c id="p8c_tv8" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1699 w=610 h=55/></c>
<c id="p8c_tk9" v="metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1754 w=150 h=40/></c>
<c id="p8c_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1754 w=610 h=40/></c>
<c id="p8c_tk10" v="flock／指紋／進度日誌／CI 為真" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1794 w=150 h=55/></c>
<c id="p8c_tv10" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&lt;id&gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1794 w=610 h=55/></c>
<c id="p8c_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1849 w=150 h=55/></c>
<c id="p8c_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1849 w=610 h=55/></c>
</diagram>
<diagram id="v1p8cc" name="流程 v2：undev vendor_kit"><c id="title" v="流程 v2：undev vendor_kit（§2 undev 列；v2.2 B、v2.3 §5、v2.5 §10、v2.6 §1、v2.7 §6；Q10 (2)）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定：工具 path 覆寫與引擎 tag 覆寫分開處理（v2.1 B）；引擎覆寫記 tag + image ID，啟動器 docker image inspect 驗 ID 後直接 run、不 pull（v2.6 §1，不用 --pull never）；每工具印記在 gen/&lt;repo&gt;.stamp，不放在 symlink 內（v2.3 §3）；undev 走 resolve → docker → apply，撤覆寫行含 image ID、建日誌後才動（v2.5 §10）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=112 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=112 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=112 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=112 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=112 w=360 h=28/></c>
<c id="vB′" v="undev vendor_kit = resolve → apply（無 image 要拉）：建 .tmp.undev.&lt;id&gt;.toml 日誌後才撤 vendor_kit 行（含 image ID）；最後一個覆寫撤掉 → 刪整個 version.local.toml；下次 just：gen/.stamp 不符 → 只回 1 提示（Q10 (2)）" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=156 w=1600 h=1436/></c>
<c id="vB′_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=1556 y=5 w=30 h=20/></c>
<c id="w0" v="just vendor_kit undev vendor_kit" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB′"><g x=20 y=36 w=220 h=58/></c>
<c id="w1" v="docker run 引擎 resolve undev vendor_kit" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=260 y=41 w=280 h=48/></c>
<c id="w1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=516 y=31 w=30 h=20/></c>
<c id="w3" v="否 → 0：未啟用（提示）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB′"><g x=20 y=134 w=220 h=40/></c>
<c id="w2q" v="version.local.toml 有 vendor_kit 行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB′"><g x=560 y=114 w=300 h=81/></c>
<c id="w2q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=836 y=104 w=30 h=20/></c>
<c id="w2s" v="是：resolve（不寫）：無 image 要拉；輸出輸入指紋（version.local.toml hash）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=215 w=400 h=48/></c>
<c id="w2s_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=205 w=30 h=20/></c>
<c id="w1b" v="docker run 引擎 apply undev vendor_kit" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=260 y=283 w=280 h=48/></c>
<c id="w1b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=516 y=273 w=30 h=20/></c>
<c id="w2a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=287 w=400 h=40/></c>
<c id="w2a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=277 w=30 h=20/></c>
<c id="w2b" v="重驗指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=360 w=240 h=40/></c>
<c id="w2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=776 y=350 w=30 h=20/></c>
<c id="w2bx" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vB′"><g x=820 y=351 w=140 h=58/></c>
<c id="w2bx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=341 w=30 h=20/></c>
<c id="w2l" v="建進度日誌（.vendor_kit/.tmp.undev.&lt;id&gt;.toml；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=429 w=400 h=48/></c>
<c id="w2l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=419 w=30 h=20/></c>
<c id="w2lf" v="＋.vendor_kit/.tmp.undev.&lt;id&gt;.toml（進度日誌，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB′"><g x=1220 y=432 w=360 h=42/></c>
<c id="w2x" v="失敗 → 1：保留可恢復狀態（下次可寫動詞先恢復）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vB′"><g x=20 y=497 w=220 h=80/></c>
<c id="w2x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=216 y=487 w=30 h=20/></c>
<c id="w2" v="刪 version.local.toml 的 vendor_kit 行（tag＋vendor_kit_image_id 一起撤）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=513 w=400 h=48/></c>
<c id="w2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=503 w=30 h=20/></c>
<c id="w2f" v="version.local.toml（少 vendor_kit 行與 vendor_kit_image_id 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB′"><g x=1220 y=516 w=360 h=42/></c>
<c id="w2e" v="還有其他覆寫行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB′"><g x=560 y=597 w=200 h=81/></c>
<c id="w2e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=736 y=587 w=30 h=20/></c>
<c id="w2ed" v="否：刪整個 version.local.toml（最後一個覆寫已撤）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=790 y=606 w=170 h=63/></c>
<c id="w2ed_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=596 w=30 h=20/></c>
<c id="w2edf" v="－version.local.toml（整個檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vB′"><g x=1220 y=618 w=360 h=40/></c>
<c id="w2edf_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=1556 y=608 w=30 h=20/></c>
<c id="w2g" v="是／已刪：刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vB′"><g x=560 y=698 w=400 h=40/></c>
<c id="w2g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=936 y=688 w=30 h=20/></c>
<c id="w2z" v="0：本次結束（下次 just 用 version.toml 的引擎）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB′"><g x=20 y=758 w=220 h=80/></c>
<c id="w2z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=216 y=748 w=30 h=20/></c>
<c id="wb" v="═══ 下次 just（改用 version.toml 的引擎；啟動器先比對 gen/.stamp 再起容器）═══" s="text;fs=12;sc=none;fc=none;fst=1" parent="vB′"><g x=260 y=858 w=560 h=26/></c>
<c id="w4" v="下次打任何 just" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB′"><g x=20 y=908 w=220 h=40/></c>
<c id="w5a" v="grep version.toml 第一行取引擎 ref（local 已無覆寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=260 y=904 w=280 h=48/></c>
<c id="w5a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=516 y=894 w=30 h=20/></c>
<c id="w7" v="否 → 1：「vendor_kit 已更新，請執行：just vendor_kit upgrade vendor_kit」（不重寫）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vB′"><g x=20 y=972 w=220 h=124/></c>
<c id="w7_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=216 y=962 w=30 h=20/></c>
<c id="w6" v="gen/.stamp 的引擎 ref == 第一行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB′"><g x=260 y=994 w=270 h=81/></c>
<c id="w6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=506 y=984 w=30 h=20/></c>
<c id="w5b" v="是 → docker image inspect：本機有？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vB′"><g x=260 y=1116 w=170 h=174/></c>
<c id="w5b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vB′"><g x=406 y=1106 w=30 h=20/></c>
<c id="w5p" v="無：docker pull 該引擎" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=440 y=1310 w=100 h=42/></c>
<c id="w5g" v="vendor_kit:vN（version.toml 的引擎）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="vB′"><g x=980 y=1310 w=220 h=42/></c>
<c id="w5c" v="docker run 該引擎 resolve sync" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vB′"><g x=260 y=1381 w=280 h=40/></c>
<c id="w9" v="0：正常跑（「sync（1）」頁）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vB′"><g x=560 y=1372 w=200 h=58/></c>
<c id="we1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w0" target="w1"></c>
<c id="we2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="w1" target="w2q"><g x=0.01 pts=420,260;730,260/></c>
<c id="we2n" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="w2q" target="w3"></c>
<c id="we2y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.375;entryY=0" edge="1" source="w2q" target="w2s"><g x=-0.6/></c>
<c id="we2s" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="w2s" target="w1b"><g x=0.00 pts=660,429;420,429/></c>
<c id="we2a" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w1b" target="w2a"></c>
<c id="we2b" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="w2a" target="w2b"></c>
<c id="we2bx" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w2b" target="w2bx"></c>
<c id="we2l" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="w2b" target="w2l"></c>
<c id="we2lf" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w2l" target="w2lf"></c>
<c id="we2w" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="w2l" target="w2"></c>
<c id="we3" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w2" target="w2f"></c>
<c id="we3x" v="失敗" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="w2" target="w2x"></c>
<c id="we2e" s="fs=12;exitX=0.25;exitY=1;entryX=0.5;entryY=0" edge="1" source="w2" target="w2e"></c>
<c id="we2ed" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w2e" target="w2ed"></c>
<c id="we2edf" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w2ed" target="w2edf"></c>
<c id="we2g" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.25;entryY=0" edge="1" source="w2e" target="w2g"><g x=-0.6/></c>
<c id="we2gd" s="fs=12;exitX=0.5;exitY=1;entryX=0.787;entryY=0" edge="1" source="w2ed" target="w2g"></c>
<c id="we4" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="w2g" target="w2z"><g x=-0.90 pts=780,954/></c>
<c id="we5" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w4" target="w5a"></c>
<c id="we6" s="fs=12;exitX=0.482;exitY=1;entryX=0.5;entryY=0" edge="1" source="w5a" target="w6"></c>
<c id="we7" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="w6" target="w7"></c>
<c id="we8" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="w6" target="w5b"><g x=0.23 pts=415,1262;365,1262/></c>
<c id="we8n" v="無" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="w5b" target="w5p"><g x=-0.64 pts=510,1359/></c>
<c id="we8g" v="拉" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="w5g" target="w5p"></c>
<c id="we8y" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.304;entryY=0" edge="1" source="w5b" target="w5c"><g x=-0.6/></c>
<c id="we8p" s="fs=12;exitX=0.5;exitY=1;entryX=0.821;entryY=0" edge="1" source="w5p" target="w5c"></c>
<c id="we10" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w5c" target="w9"></c>
<c id="p8cc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1608 w=200 h=60/></c>
<c id="p8cc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1608 w=140 h=64/></c>
<c id="p8cc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1616 w=140 h=44/></c>
<c id="p8cc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1610 w=190 h=56/></c>
<c id="p8cc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1610 w=210 h=56/></c>
<c id="p8cc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1618 w=88 h=40/></c>
<c id="p8cc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1618 w=170 h=40/></c>
<c id="p8cc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1608 w=300 h=60/></c>
<c id="p8cc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1676 w=120 h=36/></c>
<c id="p8cc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1676 w=190 h=36/></c>
<c id="p8cc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1676 w=170 h=36/></c>
<c id="p8cc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1676 w=170 h=36/></c>
<c id="p8cc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1676 w=200 h=36/></c>
<c id="p8cc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1666 w=30 h=20/></c>
<c id="p8cc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1714 w=200 h=28/></c>
<c id="p8cc_tk0" v="dev／undev" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1748 w=150 h=40/></c>
<c id="p8cc_tv0" v="用本機工具 repo 的 dist/ 取代 image（開發工具本身用；工具必須已在 version.toml）／回到 version.toml 鎖定版；dev 自身則是換引擎 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1748 w=610 h=40/></c>
<c id="p8cc_tk1" v="覆寫兩種（v2.1 B）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1788 w=150 h=55/></c>
<c id="p8cc_tv1" v="工具 path 覆寫 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;：cache/&lt;repo&gt;/ 變 symlink，sync 跳過該工具 materialize／verify 但仍檢查 metadata、baseline；引擎 tag 覆寫 vendor_kit = &quot;&lt;tag&gt;&quot;＋image ID：啟動器改用該本機 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1788 w=610 h=55/></c>
<c id="p8cc_tk2" v="resolve／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1843 w=150 h=40/></c>
<c id="p8cc_tv2" v="undev 分兩段：resolve 只讀只算（列要拉的鎖定版 image、輸出指紋，不寫檔）→ 啟動器拉 image → apply 拿 flock、重驗指紋、建日誌後才刪覆寫、拆 symlink、重新 materialize；dev 不拉 image" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1843 w=610 h=40/></c>
<c id="p8cc_tk3" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1883 w=150 h=55/></c>
<c id="p8cc_tv3" v=".vendor_kit/version.local.toml，不進 git（.vendor_kit/.gitignore 排除；不碰 .git/info/exclude）；記 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot; 或 vendor_kit = &quot;&lt;tag&gt;&quot; + image ID（成對，undev 一起撤）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1883 w=610 h=55/></c>
<c id="p8cc_tk4" v="symlink／印記／materialize" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1938 w=150 h=55/></c>
<c id="p8cc_tv4" v="symlink = 指向另一個路徑的捷徑：dev 時 cache/&lt;repo&gt;/ 不放檔案，而是指到 &lt;dir&gt;/dist；印記 gen/&lt;repo&gt;.stamp 在 symlink 外，第一行 path:&lt;dir&gt; 或 index digest（多架構 image 的 sha256 ID）；materialize = 把 image 的 /dist 展開到 cache/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1938 w=610 h=55/></c>
<c id="p8cc_tk5" v="image tag／image ID／RepoDigests" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1993 w=150 h=55/></c>
<c id="p8cc_tv5" v="tag = 人取的版本名（可重 build 換內容）；image ID = 本機 image 內容的 ID（同 tag 重 build 才會被發現）；RepoDigests = 從倉庫拉來才有的 digest，docker load 的 tar 沒有 → 自身 dev 只能用 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1993 w=610 h=55/></c>
<c id="p8cc_tk6" v="GHCR／tar／docker load" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1748 w=150 h=40/></c>
<c id="p8cc_tv6" v="GHCR = GitHub 的容器倉庫（正常情況引擎 image 從這裡 pull）；tar = 離線包（docker save 存的 image 檔）；docker load = 把 tar 讀進本機 docker，之後才能用 -i &lt;tag&gt; 指定它" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1748 w=610 h=40/></c>
<c id="p8cc_tk7" v="docker image inspect／掛載 -v" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1788 w=150 h=55/></c>
<c id="p8cc_tv7" v="啟動器每次 docker run 前先 docker image inspect &lt;ref 或 tag&gt;：本機有 → 不 pull（覆寫時 .Id 必須 == version.local.toml 記的 image ID，否則 1）；不用 --pull never（docker 19.03 無此旗標）；-v &lt;dir&gt;/dist:/dist/&lt;repo&gt;:ro = 把本機目錄唯讀掛進容器" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1788 w=610 h=55/></c>
<c id="p8cc_tk8" v="統一提示／gen/.stamp（Q10 (2)）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1843 w=150 h=55/></c>
<c id="p8cc_tv8" v="gen/.stamp 只記引擎 ref（或本機 tag）；啟動器先比對它 ≠ 現在要用的引擎 → 不起容器、只退出 1 印「請 just vendor_kit upgrade vendor_kit」（需要人動作，橙）；upgrade vendor_kit 比對薄殼首行自描述才重產薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1843 w=610 h=55/></c>
<c id="p8cc_tk9" v="metadata／baseline" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1898 w=150 h=40/></c>
<c id="p8cc_tv9" v="baseline/&lt;repo&gt;/.vendor_kit.toml：完成標記、最後合併版本等；dev 中 sync 仍檢查這兩項（未完成接入 → 1；baseline 落後 → warn／CI 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1898 w=610 h=40/></c>
<c id="p8cc_tk10" v="flock／指紋／進度日誌／CI 為真" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1938 w=150 h=55/></c>
<c id="p8cc_tv10" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗；進度日誌（undev 用 .vendor_kit/.tmp.undev.&lt;id&gt;.toml）第一個寫入前建、最後刪；CI 為真 = CI 非空且不為 0／false → frozen：dev 一律拒絕、sync 看到任何覆寫 → 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1938 w=610 h=55/></c>
<c id="p8cc_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1993 w=150 h=55/></c>
<c id="p8cc_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1993 w=610 h=55/></c>
</diagram>
<diagram id="v1p8b" name="流程 v2：remove（1）resolve → apply 前置"><c id="title" v="流程 v2：remove（1）resolve → apply 前置（§2、§5；v2.2 C／E、v2.3 §5、v2.5 §3／§11）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="vC" v="remove &lt;repo&gt;（1）：拆掉一個工具（初始檔永不刪、印清單，要刪用 git rm）= resolve（讀 metadata → 刪除清單 → 詢問清單 → 計畫＋指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；無 image 要拉；寫入段見「remove（2）」頁" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=928/></c>
<c id="vC_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=1556 y=5 w=30 h=20/></c>
<c id="m0" v="just vendor_kit remove &lt;repo&gt;（-y、--dry-run）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vC"><g x=20 y=36 w=220 h=80/></c>
<c id="m1" v="docker run &lt;引擎&gt; resolve remove &lt;repo&gt;（不經 docker create/cp）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC"><g x=260 y=52 w=280 h=48/></c>
<c id="m1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=516 y=42 w=30 h=20/></c>
<c id="m3" v="否 → 0：未接入（提示）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vC"><g x=20 y=141 w=220 h=40/></c>
<c id="m2" v="已接入 &lt;repo&gt;？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC"><g x=560 y=136 w=280 h=50/></c>
<c id="m5" v="是 → 1：請先 undev &lt;repo&gt;（v2.1 B）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vC"><g x=20 y=206 w=220 h=58/></c>
<c id="m4" v="有 dev path 覆寫？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC"><g x=560 y=210 w=280 h=50/></c>
<c id="m6" v="否：resolve（不寫）：讀 metadata（append 過的行、完成標記）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=284 w=400 h=40/></c>
<c id="m6_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=274 w=30 h=20/></c>
<c id="m6b" v="產生刪除清單：version.toml 行、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp、baseline/&lt;repo&gt;/、gen/tools.just 的 mod? 行" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=344 w=400 h=63/></c>
<c id="m6b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=334 w=30 h=20/></c>
<c id="m6c" v="產生詢問清單：metadata 記的 append 行（有才問）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=427 w=400 h=40/></c>
<c id="m6c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=417 w=30 h=20/></c>
<c id="m6d" v="產生輸入指紋（version.toml、metadata、要動的使用者檔 hash）→ 計畫＋指紋以 stdout 回啟動器" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=487 w=400 h=48/></c>
<c id="m6d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=477 w=30 h=20/></c>
<c id="m8" v="docker run &lt;引擎&gt; apply remove &lt;repo&gt;（--dry-run 原樣轉發）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC"><g x=260 y=555 w=280 h=48/></c>
<c id="m8_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=516 y=545 w=30 h=20/></c>
<c id="m9a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=559 w=400 h=40/></c>
<c id="m9a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=549 w=30 h=20/></c>
<c id="m9b" v="重驗指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC"><g x=560 y=632 w=240 h=40/></c>
<c id="m9b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=776 y=622 w=30 h=20/></c>
<c id="m9x" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vC"><g x=820 y=623 w=140 h=58/></c>
<c id="m9x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=936 y=613 w=30 h=20/></c>
<c id="m7cx" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vC"><g x=20 y=702 w=220 h=80/></c>
<c id="m7cx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=216 y=692 w=30 h=20/></c>
<c id="m7c" v="CI 為真（frozen）且需改 tracked 檔？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC"><g x=560 y=701 w=340 h=81/></c>
<c id="m7c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=876 y=691 w=30 h=20/></c>
<c id="m7y" v="是 → 0：只印清單（會刪什麼、會問什麼）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vC"><g x=20 y=802 w=220 h=58/></c>
<c id="m7y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC"><g x=216 y=792 w=30 h=20/></c>
<c id="m7" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC"><g x=610 y=806 w=240 h=50/></c>
<c id="m7z" v="否 ↓ 續「remove（2）」頁：建日誌 → 問 append 行 → 刪檔 → 刪日誌" s="text;fs=12;sc=none;fc=none;fst=1" parent="vC"><g x=560 y=880 w=400 h=42/></c>
<c id="me1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m0" target="m1"></c>
<c id="me2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m1" target="m2"><g x=0.05 pts=420,267;720,267/></c>
<c id="me3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m2" target="m3"></c>
<c id="me4" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m2" target="m4"><g x=-0.6/></c>
<c id="me5" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m4" target="m5"></c>
<c id="me6" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.35;entryY=0" edge="1" source="m4" target="m6"><g x=-0.6/></c>
<c id="me6b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m6" target="m6b"></c>
<c id="me6c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m6b" target="m6c"></c>
<c id="me6d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m6c" target="m6d"></c>
<c id="me7" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="m6d" target="m8"><g x=0.00 pts=660,686;420,686/></c>
<c id="me8" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m8" target="m9a"></c>
<c id="me8b" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="m9a" target="m9b"></c>
<c id="me8x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m9b" target="m9x"></c>
<c id="me9" s="fs=12;exitX=0.708;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9b" target="m7c"></c>
<c id="me9x" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m7c" target="m7cx"></c>
<c id="me9c" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m7c" target="m7"><g x=-0.6/></c>
<c id="me10" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m7" target="m7y"></c>
<c id="me11" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.425;entryY=0" edge="1" source="m7" target="m7z"><g x=-0.6/></c>
<c id="p8b_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1085 w=200 h=60/></c>
<c id="p8b_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1085 w=140 h=64/></c>
<c id="p8b_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1093 w=140 h=44/></c>
<c id="p8b_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1087 w=190 h=56/></c>
<c id="p8b_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1087 w=210 h=56/></c>
<c id="p8b_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1095 w=88 h=40/></c>
<c id="p8b_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1095 w=170 h=40/></c>
<c id="p8b_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1085 w=300 h=60/></c>
<c id="p8b_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1153 w=120 h=36/></c>
<c id="p8b_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1153 w=190 h=36/></c>
<c id="p8b_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=390 y=1153 w=170 h=36/></c>
<c id="p8b_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=1153 w=170 h=36/></c>
<c id="p8b_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=770 y=1153 w=200 h=36/></c>
<c id="p8b_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=946 y=1143 w=30 h=20/></c>
<c id="p8b_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1191 w=200 h=28/></c>
<c id="p8b_tk0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1225 w=150 h=55/></c>
<c id="p8b_tv0" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&lt;repo&gt;/、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1225 w=610 h=55/></c>
<c id="p8b_tk1" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1280 w=150 h=71/></c>
<c id="p8b_tv1" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1280 w=610 h=71/></c>
<c id="p8b_tk2" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1351 w=150 h=55/></c>
<c id="p8b_tv2" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1351 w=610 h=55/></c>
<c id="p8b_tk3" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1406 w=150 h=71/></c>
<c id="p8b_tv3" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml，因 metadata 會被刪）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1406 w=610 h=71/></c>
<c id="p8b_tk4" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1477 w=150 h=55/></c>
<c id="p8b_tv4" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1477 w=610 h=55/></c>
<c id="p8b_tk5" v="append 行／CRLF／三分支" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1532 w=150 h=55/></c>
<c id="p8b_tv5" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1532 w=610 h=55/></c>
<c id="p8b_tk6" v="初始檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1225 w=150 h=40/></c>
<c id="p8b_tv6" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1225 w=610 h=40/></c>
<c id="p8b_tk7" v="保護清單／保護模式" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1265 w=150 h=40/></c>
<c id="p8b_tv7" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1265 w=610 h=40/></c>
<c id="p8b_tk8" v="dev 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1305 w=150 h=40/></c>
<c id="p8b_tv8" v="version.local.toml 的 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1305 w=610 h=40/></c>
<c id="p8b_tk9" v="gen／mod?／import" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1345 w=150 h=71/></c>
<c id="p8b_tv9" v="gen/tools.just 每個 &lt;ns&gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1345 w=610 h=71/></c>
<c id="p8b_tk10" v="CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1416 w=150 h=55/></c>
<c id="p8b_tv10" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1416 w=610 h=55/></c>
<c id="p8b_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1471 w=150 h=55/></c>
<c id="p8b_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1471 w=610 h=55/></c>
</diagram>
<diagram id="v1p8bccc" name="流程 v2：remove（2）寫入段"><c id="title" v="流程 v2：remove（2）apply 寫入段（§2、§5；v2.2 C／E、v2.3 §1／§5、v2.5 §3／§11）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="vC2" v="remove &lt;repo&gt;（2）寫入段（承「remove（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 問 append 行（找行 → 命中幾處？）→ 刪 baseline/&lt;repo&gt;/、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1128/></c>
<c id="vC2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=1556 y=5 w=30 h=20/></c>
<c id="m9e" v="來自「remove（1）」頁：apply 檢查通過（非 dry-run）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="vC2"><g x=610 y=36 w=300 h=58/></c>
<c id="m9l" v="建進度日誌（.vendor_kit/.tmp.remove.&lt;id&gt;.toml；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=114 w=400 h=48/></c>
<c id="m9l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=104 w=30 h=20/></c>
<c id="m9lf" v="＋.vendor_kit/.tmp.remove.&lt;id&gt;.toml（進度日誌，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=117 w=360 h=42/></c>
<c id="m9h" v="metadata 有 append 過的行？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC2"><g x=590 y=182 w=300 h=81/></c>
<c id="m9h_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=866 y=172 w=30 h=20/></c>
<c id="m9q" v="有 → 問「要刪我們加在 X 的這幾行嗎」同意？（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC2"><g x=590 y=283 w=300 h=112/></c>
<c id="m9q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=866 y=273 w=30 h=20/></c>
<c id="m9s" v="是：找上次插入的行（CRLF／LF 視為相同、其餘精確）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC2"><g x=640 y=415 w=200 h=48/></c>
<c id="m9s_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=816 y=405 w=30 h=20/></c>
<c id="m9mn" v="找行（v2.3 §1）：CRLF／LF 視為相同、其餘精確；唯一命中 → 刪；零命中 → 不刪印清單；多處 → 保留並 warn（Q13）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="vC2"><g x=1220 y=418 w=360 h=42/></c>
<c id="m9z" v="零命中：不刪、印清單" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC2"><g x=560 y=495 w=70 h=57/></c>
<c id="m9m" v="命中幾處？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vC2"><g x=670 y=483 w=140 h=81/></c>
<c id="m9m_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=786 y=473 w=30 h=20/></c>
<c id="m9d" v="唯一：刪那幾行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC2"><g x=860 y=504 w=100 h=40/></c>
<c id="m9f" v="初始檔（只移除我們 append 的行；其餘不動；永不刪檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=504 w=360 h=40/></c>
<c id="m9w" v="多處：保留＋warn" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vC2"><g x=670 y=604 w=140 h=40/></c>
<c id="m9w_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=786 y=594 w=30 h=20/></c>
<c id="m10a" v="刪 baseline/&lt;repo&gt;/（含 metadata）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=530 y=664 w=400 h=40/></c>
<c id="m10a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=906 y=654 w=30 h=20/></c>
<c id="m10af" v="－baseline/&lt;repo&gt;/（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=664 w=360 h=40/></c>
<c id="m10b" v="刪 cache/&lt;repo&gt;/" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=724 w=400 h=40/></c>
<c id="m10b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=714 w=30 h=20/></c>
<c id="m10bf" v="－cache/&lt;repo&gt;/（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=724 w=360 h=40/></c>
<c id="m10c" v="刪 gen/&lt;repo&gt;.stamp" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=784 w=400 h=40/></c>
<c id="m10c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=774 w=30 h=20/></c>
<c id="m10cf" v="－gen/&lt;repo&gt;.stamp（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=784 w=360 h=40/></c>
<c id="m10d" v="重生 gen/tools.just（去掉該工具所有 mod? 行）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=844 w=400 h=40/></c>
<c id="m10d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=834 w=30 h=20/></c>
<c id="m10df" v="gen/tools.just（不進 git；mod? 行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=844 w=360 h=40/></c>
<c id="m10e" v="最後刪 version.toml 該工具那一行" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=904 w=400 h=40/></c>
<c id="m10e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=894 w=30 h=20/></c>
<c id="m10ef" v="－version.toml &lt;repo&gt; 行（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vC2"><g x=1220 y=904 w=360 h=40/></c>
<c id="m10x" v="失敗 → 1：明列已完成／未完成" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vC2"><g x=20 y=964 w=220 h=58/></c>
<c id="m10x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=216 y=954 w=30 h=20/></c>
<c id="m10g" v="刪進度日誌（最後一步）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vC2"><g x=560 y=973 w=400 h=40/></c>
<c id="m10g_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vC2"><g x=936 y=963 w=30 h=20/></c>
<c id="m11" v="0：印「以下初始檔保留，若不需要請 git rm：…」" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vC2"><g x=20 y=1042 w=220 h=80/></c>
<c id="me11e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9e" target="m9l"></c>
<c id="me11f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m9l" target="m9lf"></c>
<c id="me11h" s="fs=12;exitX=0.45;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9l" target="m9h"></c>
<c id="me11hn" v="無" s="fs=12;exitX=0;exitY=0.5;entryX=0.037;entryY=0" edge="1" source="m9h" target="m10a"><g x=-0.76 pts=565,364/></c>
<c id="me11q" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9h" target="m9q"><g x=-0.6/></c>
<c id="me12n" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=0.062;entryY=0" edge="1" source="m9q" target="m10a"><g x=-0.73 pts=575,480/></c>
<c id="me12y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9q" target="m9s"><g x=-0.6/></c>
<c id="me12m" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9s" target="m9m"></c>
<c id="me13z" v="零" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="m9m" target="m9z"></c>
<c id="me13d" v="唯一" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m9m" target="m9d"></c>
<c id="me13w" v="多處" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m9m" target="m9w"><g x=-0.6/></c>
<c id="me13f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m9d" target="m9f"></c>
<c id="me14z" s="fs=12;exitX=0.5;exitY=1;entryX=0.163;entryY=0" edge="1" source="m9z" target="m10a"></c>
<c id="me14w" s="fs=12;exitX=0.5;exitY=1;entryX=0.525;entryY=0" edge="1" source="m9w" target="m10a"></c>
<c id="me14d" s="fs=12;exitX=0.3;exitY=1;entryX=0.9;entryY=0" edge="1" source="m9d" target="m10a"></c>
<c id="me15a" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m10a" target="m10af"></c>
<c id="me15b" s="fs=12;exitX=0.5;exitY=1;entryX=0.425;entryY=0" edge="1" source="m10a" target="m10b"></c>
<c id="me15bf" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m10b" target="m10bf"></c>
<c id="me15c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m10b" target="m10c"></c>
<c id="me15cf" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m10c" target="m10cf"></c>
<c id="me15d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m10c" target="m10d"></c>
<c id="me15df" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m10d" target="m10df"></c>
<c id="me15e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="m10d" target="m10e"></c>
<c id="me15ef" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="m10e" target="m10ef"></c>
<c id="me16" v="成功" s="fs=12;exitX=0.6;exitY=1;entryX=0.6;entryY=0" edge="1" source="m10e" target="m10g"><g x=-0.6/></c>
<c id="me16x" v="失敗" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="m10e" target="m10x"><g x=0.00 pts=660,1095;150,1095/></c>
<c id="me17" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="m10g" target="m11"><g x=-0.88 pts=780,1223/></c>
<c id="p8b2_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1285 w=200 h=60/></c>
<c id="p8b2_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1285 w=140 h=64/></c>
<c id="p8b2_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1293 w=140 h=44/></c>
<c id="p8b2_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1287 w=190 h=56/></c>
<c id="p8b2_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1287 w=210 h=56/></c>
<c id="p8b2_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1295 w=88 h=40/></c>
<c id="p8b2_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1295 w=170 h=40/></c>
<c id="p8b2_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1285 w=300 h=60/></c>
<c id="p8b2_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1353 w=200 h=36/></c>
<c id="p8b2_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1353 w=120 h=36/></c>
<c id="p8b2_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=400 y=1353 w=190 h=36/></c>
<c id="p8b2_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=610 y=1353 w=170 h=36/></c>
<c id="p8b2_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=1353 w=170 h=36/></c>
<c id="p8b2_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=990 y=1353 w=200 h=36/></c>
<c id="p8b2_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1166 y=1343 w=30 h=20/></c>
<c id="p8b2_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1391 w=200 h=28/></c>
<c id="p8b2_tk0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1425 w=150 h=55/></c>
<c id="p8b2_tv0" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&lt;repo&gt;/、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1425 w=610 h=55/></c>
<c id="p8b2_tk1" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1480 w=150 h=71/></c>
<c id="p8b2_tv1" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1480 w=610 h=71/></c>
<c id="p8b2_tk2" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1551 w=150 h=55/></c>
<c id="p8b2_tv2" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1551 w=610 h=55/></c>
<c id="p8b2_tk3" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1606 w=150 h=71/></c>
<c id="p8b2_tv3" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml，因 metadata 會被刪）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1606 w=610 h=71/></c>
<c id="p8b2_tk4" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1677 w=150 h=55/></c>
<c id="p8b2_tv4" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1677 w=610 h=55/></c>
<c id="p8b2_tk5" v="append 行／CRLF／三分支" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1732 w=150 h=55/></c>
<c id="p8b2_tv5" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1732 w=610 h=55/></c>
<c id="p8b2_tk6" v="初始檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1425 w=150 h=40/></c>
<c id="p8b2_tv6" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1425 w=610 h=40/></c>
<c id="p8b2_tk7" v="保護清單／保護模式" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1465 w=150 h=40/></c>
<c id="p8b2_tv7" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1465 w=610 h=40/></c>
<c id="p8b2_tk8" v="dev 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1505 w=150 h=40/></c>
<c id="p8b2_tv8" v="version.local.toml 的 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1505 w=610 h=40/></c>
<c id="p8b2_tk9" v="gen／mod?／import" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1545 w=150 h=71/></c>
<c id="p8b2_tv9" v="gen/tools.just 每個 &lt;ns&gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1545 w=610 h=71/></c>
<c id="p8b2_tk10" v="CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1616 w=150 h=55/></c>
<c id="p8b2_tv10" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1616 w=610 h=55/></c>
<c id="p8b2_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1671 w=150 h=55/></c>
<c id="p8b2_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1671 w=610 h=55/></c>
</diagram>
<diagram id="v1p8bc" name="流程 v2：uninstall（1）resolve → apply 前置"><c id="title" v="流程 v2：uninstall（1）resolve → apply 前置（§2；v2.2 E、v2.3 §6、v2.5 §3／§10）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="vD" v="uninstall（1）：全部拆掉（install 的反向；bootstrap.sh 的反向也是它）= resolve（預檢 → hash → 保護清單 → 計畫 → 詢問清單 → 指紋）→ apply 前置（拿鎖、重驗、frozen、dry-run）；寫入段見「uninstall（2）」頁；不 rm -rf .vendor_kit/" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=941/></c>
<c id="vD_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=1556 y=5 w=30 h=20/></c>
<c id="x0" v="just vendor_kit uninstall（-y、--dry-run）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vD"><g x=20 y=36 w=220 h=80/></c>
<c id="x1" v="docker run &lt;引擎&gt; resolve uninstall（不經 docker create/cp）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD"><g x=260 y=52 w=280 h=48/></c>
<c id="x1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=516 y=42 w=30 h=20/></c>
<c id="x2x" v="否 → 1：預檢失敗（dev 中 → 請先 undev；未完成接入 → 請先 add）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vD"><g x=20 y=136 w=220 h=80/></c>
<c id="x2x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=216 y=126 w=30 h=20/></c>
<c id="x2" v="預檢全部工具通過？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD"><g x=560 y=151 w=250 h=50/></c>
<c id="x2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=786 y=141 w=30 h=20/></c>
<c id="x2b" v="是：算每個自產檔的 hash（薄殼、version.toml、gen/、cache/、baseline/；不動任何東西）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=236 w=400 h=48/></c>
<c id="x2b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=226 w=30 h=20/></c>
<c id="x2bb" v="分類：hash 相符 → 可刪清單；未知或被改的 → 保護清單（之後一律保留並回報）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=304 w=400 h=48/></c>
<c id="x2bb_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=294 w=30 h=20/></c>
<c id="x2r" v="保護清單在任何 remove 之前生效（v2.5 §10）；逐工具 remove 走保護模式：清單內的檔跳過" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="vD"><g x=1220 y=304 w=360 h=48/></c>
<c id="x2r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=1556 y=294 w=30 h=20/></c>
<c id="x2c" v="產生執行計畫：可刪清單＋保護清單（逐工具 remove 的順序）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=372 w=400 h=40/></c>
<c id="x2c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=362 w=30 h=20/></c>
<c id="x2d" v="產生詢問清單：append 行、根 justfile 那行、根 .dockerignore 三行" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=432 w=400 h=48/></c>
<c id="x2d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=422 w=30 h=20/></c>
<c id="x2e" v="產生輸入指紋（version.toml、各 metadata、要動的使用者檔 hash）→ 計畫＋詢問清單＋指紋以 stdout 回啟動器" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=500 w=400 h=48/></c>
<c id="x2e_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=490 w=30 h=20/></c>
<c id="x1b" v="docker run &lt;引擎&gt; apply uninstall（--dry-run 原樣轉發）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD"><g x=260 y=568 w=280 h=48/></c>
<c id="x1b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=516 y=558 w=30 h=20/></c>
<c id="x4a" v="apply：flock 專案目錄（60 秒）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=572 w=400 h=40/></c>
<c id="x4a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=562 w=30 h=20/></c>
<c id="x4b" v="重驗指紋" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD"><g x=560 y=645 w=240 h=40/></c>
<c id="x4b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=776 y=635 w=30 h=20/></c>
<c id="x4bx" v="不同 → 1「請重跑」" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vD"><g x=820 y=636 w=140 h=58/></c>
<c id="x4bx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=936 y=626 w=30 h=20/></c>
<c id="x3cx" v="是 → 1：印需改清單（frozen；請在本機執行後 commit 並 push）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="vD"><g x=20 y=714 w=220 h=80/></c>
<c id="x3cx_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=216 y=704 w=30 h=20/></c>
<c id="x3c" v="CI 為真（frozen）且需改 tracked 檔？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD"><g x=560 y=714 w=340 h=81/></c>
<c id="x3c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=876 y=704 w=30 h=20/></c>
<c id="x3y" v="是 → 0：只印會刪什麼、會問什麼" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vD"><g x=20 y=815 w=220 h=58/></c>
<c id="x3y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD"><g x=216 y=805 w=30 h=20/></c>
<c id="x3" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD"><g x=610 y=819 w=240 h=50/></c>
<c id="x4z" v="否 ↓ 續「uninstall（2）」頁：建日誌 → 逐工具 remove → 刪自產檔 → 根 justfile 那行 → 刪日誌" s="text;fs=12;sc=none;fc=none;fst=1" parent="vD"><g x=560 y=893 w=400 h=42/></c>
<c id="xe1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x0" target="x1"></c>
<c id="xe2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x1" target="x2"><g x=0.00 pts=420,267;705,267/></c>
<c id="xe3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x2" target="x2x"></c>
<c id="xe4" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.312;entryY=0" edge="1" source="x2" target="x2b"><g x=-0.6/></c>
<c id="xe4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x2b" target="x2bb"></c>
<c id="xe4c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x2bb" target="x2c"></c>
<c id="xe4d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x2c" target="x2d"></c>
<c id="xe4e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x2d" target="x2e"></c>
<c id="xe5" s="fs=12;exitX=0.2;exitY=1;entryX=0.5;entryY=0" edge="1" source="x2e" target="x1b"><g x=0.00 pts=660,699;420,699/></c>
<c id="xe5b" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x1b" target="x4a"></c>
<c id="xe5c" s="fs=12;exitX=0.5;exitY=1;entryX=0.833;entryY=0" edge="1" source="x4a" target="x4b"></c>
<c id="xe5x" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x4b" target="x4bx"></c>
<c id="xe5d" s="fs=12;exitX=0.708;exitY=1;entryX=0.5;entryY=0" edge="1" source="x4b" target="x3c"></c>
<c id="xe5e" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x3c" target="x3cx"></c>
<c id="xe5f" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x3c" target="x3"><g x=-0.6/></c>
<c id="xe6" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x3" target="x3y"></c>
<c id="xe7" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.425;entryY=0" edge="1" source="x3" target="x4z"><g x=-0.6/></c>
<c id="p8bc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1098 w=200 h=60/></c>
<c id="p8bc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1098 w=140 h=64/></c>
<c id="p8bc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1106 w=140 h=44/></c>
<c id="p8bc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1100 w=190 h=56/></c>
<c id="p8bc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1100 w=210 h=56/></c>
<c id="p8bc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1108 w=88 h=40/></c>
<c id="p8bc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1108 w=170 h=40/></c>
<c id="p8bc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1098 w=300 h=60/></c>
<c id="p8bc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1166 w=120 h=36/></c>
<c id="p8bc_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1166 w=150 h=36/></c>
<c id="p8bc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1166 w=190 h=36/></c>
<c id="p8bc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1166 w=170 h=36/></c>
<c id="p8bc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1166 w=170 h=36/></c>
<c id="p8bc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=940 y=1166 w=200 h=36/></c>
<c id="p8bc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1116 y=1156 w=30 h=20/></c>
<c id="p8bc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1204 w=200 h=28/></c>
<c id="p8bc_tk0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1238 w=150 h=55/></c>
<c id="p8bc_tv0" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&lt;repo&gt;/、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1238 w=610 h=55/></c>
<c id="p8bc_tk1" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1293 w=150 h=71/></c>
<c id="p8bc_tv1" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1293 w=610 h=71/></c>
<c id="p8bc_tk2" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1364 w=150 h=55/></c>
<c id="p8bc_tv2" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1364 w=610 h=55/></c>
<c id="p8bc_tk3" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1419 w=150 h=71/></c>
<c id="p8bc_tv3" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml，因 metadata 會被刪）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1419 w=610 h=71/></c>
<c id="p8bc_tk4" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1490 w=150 h=55/></c>
<c id="p8bc_tv4" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1490 w=610 h=55/></c>
<c id="p8bc_tk5" v="append 行／CRLF／三分支" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1545 w=150 h=55/></c>
<c id="p8bc_tv5" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1545 w=610 h=55/></c>
<c id="p8bc_tk6" v="初始檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1238 w=150 h=40/></c>
<c id="p8bc_tv6" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1238 w=610 h=40/></c>
<c id="p8bc_tk7" v="保護清單／保護模式" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1278 w=150 h=40/></c>
<c id="p8bc_tv7" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1278 w=610 h=40/></c>
<c id="p8bc_tk8" v="dev 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1318 w=150 h=40/></c>
<c id="p8bc_tv8" v="version.local.toml 的 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1318 w=610 h=40/></c>
<c id="p8bc_tk9" v="gen／mod?／import" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1358 w=150 h=71/></c>
<c id="p8bc_tv9" v="gen/tools.just 每個 &lt;ns&gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1358 w=610 h=71/></c>
<c id="p8bc_tk10" v="CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1429 w=150 h=55/></c>
<c id="p8bc_tv10" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1429 w=610 h=55/></c>
<c id="p8bc_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1484 w=150 h=55/></c>
<c id="p8bc_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1484 w=610 h=55/></c>
</diagram>
<diagram id="v1p8bcc" name="流程 v2：uninstall（2）寫入段"><c id="title" v="流程 v2：uninstall（2）apply 寫入段（§2；v2.2 E、v2.3 §6、v2.5 §3／§10、v2.6 Q22 補、v2.8 §1）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.3 §1、v2.5 §11）：remove／uninstall 只刪原文相同的 append 行，比對 CRLF／LF 視為相同、其餘精確；唯一命中 → 刪、零命中 → 不刪印清單、多處 → 保留並 warn。已定（v2.5 §3／§10）：uninstall 也是 resolve → apply 兩段、重驗指紋；保護清單在任何 remove 之前生效；日誌在根 justfile 那行之後才刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=77/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=97 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=97 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=97 w=400 h=28/></c>
<c id="hdr3" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=97 w=220 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1240 y=97 w=360 h=28/></c>
<c id="vD2" v="uninstall（2）寫入段（承「uninstall（1）」頁：已拿鎖、重驗、非 dry-run）：建日誌 → 逐工具 remove（保護模式）→ 只刪 hash 相符的自產檔（含 baseline/ 根檔，v2.8 §1）→ justfile 那行、.dockerignore 三行問後刪 → 刪日誌 → 空才 rmdir" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=141 w=1600 h=1642/></c>
<c id="vD2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=1556 y=5 w=30 h=20/></c>
<c id="x4e" v="來自「uninstall（1）」頁：apply 檢查通過（非 dry-run）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="vD2"><g x=610 y=36 w=300 h=58/></c>
<c id="x4l" v="建進度日誌（.vendor_kit/.tmp.uninstall.&lt;id&gt;.toml；第一個寫入前）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=114 w=400 h=48/></c>
<c id="x4l_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=104 w=30 h=20/></c>
<c id="x4lf" v="＋.vendor_kit/.tmp.uninstall.&lt;id&gt;.toml（進度日誌，不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vD2"><g x=1220 y=117 w=360 h=42/></c>
<c id="x4x" v="任一失敗 → 1 中止，列出已完成部分" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="vD2"><g x=20 y=182 w=220 h=58/></c>
<c id="x4x_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=216 y=172 w=30 h=20/></c>
<c id="x4" v="逐工具 remove（保護模式；步驟同「remove（2）」頁）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=191 w=400 h=40/></c>
<c id="x4_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=181 w=30 h=20/></c>
<c id="x5a" v="全部成功：刪薄殼四檔（hash 相符者）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=287 w=400 h=40/></c>
<c id="x5a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=277 w=30 h=20/></c>
<c id="x5af" v="－.vendor_kit/ 薄殼四檔（保護清單內的保留）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="vD2"><g x=1220 y=260 w=360 h=94/></c>
<c id="x5af_0" v=".gitignore" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5af"><g x=8 y=26 w=169 h=26/></c>
<c id="x5af_1" v="entry.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5af"><g x=183 y=26 w=169 h=26/></c>
<c id="x5af_2" v="vendor.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5af"><g x=8 y=58 w=169 h=26/></c>
<c id="x5af_3" v="ci/check.sh" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5af"><g x=183 y=58 w=169 h=26/></c>
<c id="x5b" v="刪 version.toml（hash 相符者）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=374 w=400 h=40/></c>
<c id="x5b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=364 w=30 h=20/></c>
<c id="x5bf" v="－version.toml（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vD2"><g x=1220 y=374 w=360 h=40/></c>
<c id="x5c" v="刪 version.local.toml（有的話；hash 相符者）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=434 w=400 h=40/></c>
<c id="x5c_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=424 w=30 h=20/></c>
<c id="x5cf" v="－version.local.toml（不進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vD2"><g x=1220 y=434 w=360 h=40/></c>
<c id="x5d" v="刪 gen/ 與 baseline/ 內剩下的自產檔（hash 相符者；v2.8 §1）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=517 w=400 h=48/></c>
<c id="x5d_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=507 w=30 h=20/></c>
<c id="x5df" v="－gen/ 兩檔（不進 git）、baseline/ 根檔（進 git）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="vD2"><g x=1220 y=494 w=360 h=94/></c>
<c id="x5df_0" v="gen/.stamp" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5df"><g x=8 y=26 w=140 h=26/></c>
<c id="x5df_1" v="gen/tools.just" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5df"><g x=154 y=26 w=198 h=26/></c>
<c id="x5df_2" v="baseline/.gitkeep" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5df"><g x=8 y=58 w=140 h=26/></c>
<c id="x5df_3" v="baseline/.vendor_kit.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="x5df"><g x=154 y=58 w=198 h=26/></c>
<c id="x5dd" v="刪已空的子目錄 baseline/（gen/、cache/、ci/ 亦同；rmdir，不 rm -rf）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=608 w=400 h=48/></c>
<c id="x5dd_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=598 w=30 h=20/></c>
<c id="x6" v="根 justfile 有我們寫的那一行（完全相同）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=700 y=676 w=260 h=112/></c>
<c id="x5r" v="初始檔留著（永不刪，印清單）；使用者的 .gitignore／.dockerignore 只動我們 append 過且你同意的那幾行（v2.1 A、Q22 補）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="vD2"><g x=1220 y=700 w=360 h=63/></c>
<c id="x5r_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=1556 y=690 w=30 h=20/></c>
<c id="x8" v="無／否：印指示（請自行移除 import 那行）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD2"><g x=560 y=828 w=100 h=73/></c>
<c id="x7" v="有 → 問「要刪這一行嗎」同意？（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=700 y=808 w=260 h=112/></c>
<c id="x7_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=798 w=30 h=20/></c>
<c id="x7y" v="是：只刪那一行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD2"><g x=760 y=941 w=140 h=40/></c>
<c id="x7f" v="justfile（少一行：import &#x27;.vendor_kit/entry.just&#x27;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vD2"><g x=1220 y=940 w=360 h=42/></c>
<c id="x9a" v="根 .dockerignore 存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=680 y=1002 w=260 h=81/></c>
<c id="x9a_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=916 y=992 w=30 h=20/></c>
<c id="x9b" v="有 → 含我們加的三行（原文相同，CRLF／LF 等價）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=680 y=1103 w=260 h=112/></c>
<c id="x9b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=916 y=1093 w=30 h=20/></c>
<c id="x9q" v="有 → 問「要刪這幾行嗎」同意？（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=680 y=1235 w=260 h=112/></c>
<c id="x9q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=916 y=1225 w=30 h=20/></c>
<c id="x9z" v="無／否：不動 .dockerignore" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD2"><g x=560 y=1367 w=110 h=48/></c>
<c id="x9z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=646 y=1357 w=30 h=20/></c>
<c id="x9y" v="是：只刪原文相同的那幾行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="vD2"><g x=730 y=1371 w=230 h=40/></c>
<c id="x9y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=1361 w=30 h=20/></c>
<c id="x9f" v=".dockerignore（少三行；其餘不動）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="vD2"><g x=1220 y=1371 w=360 h=40/></c>
<c id="x9f_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=1556 y=1361 w=30 h=20/></c>
<c id="x5z" v="刪進度日誌（最後一步；根 justfile 那行之後）= 交易完成" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=1435 w=400 h=40/></c>
<c id="x5z_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=1425 w=30 h=20/></c>
<c id="x5n" v="否 → 0：保留目錄與保護清單內的檔並回報；印摘要" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vD2"><g x=20 y=1496 w=220 h=80/></c>
<c id="x5n_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=216 y=1486 w=30 h=20/></c>
<c id="x5q" v=".vendor_kit/ 已空？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="vD2"><g x=560 y=1495 w=205 h=81/></c>
<c id="x5q_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=741 y=1485 w=30 h=20/></c>
<c id="x5y" v="0：印摘要" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="vD2"><g x=20 y=1596 w=220 h=40/></c>
<c id="x5y_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=216 y=1586 w=30 h=20/></c>
<c id="x5t" v="是：刪空目錄（rmdir；不 rm -rf）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="vD2"><g x=560 y=1596 w=400 h=40/></c>
<c id="x5t_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="vD2"><g x=936 y=1586 w=30 h=20/></c>
<c id="xe7" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x4e" target="x4l"></c>
<c id="xe7f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x4l" target="x4lf"></c>
<c id="xe8" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x4l" target="x4"></c>
<c id="xe9" v="失敗" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x4" target="x4x"></c>
<c id="xe10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x4" target="x5a"></c>
<c id="xe10f" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x5a" target="x5af"></c>
<c id="xe10b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5a" target="x5b"></c>
<c id="xe10bf" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x5b" target="x5bf"></c>
<c id="xe10c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5b" target="x5c"></c>
<c id="xe10cf" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x5c" target="x5cf"></c>
<c id="xe10d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5c" target="x5d"></c>
<c id="xe10df" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x5d" target="x5df"></c>
<c id="xe10e" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5d" target="x5dd"></c>
<c id="xe12" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5dd" target="x6"><g x=0.00 pts=780,807;850,807/></c>
<c id="xe13" v="無" s="fs=12;exitX=0;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="x6" target="x8"><g x=0.12 pts=630,873/></c>
<c id="xe14" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x6" target="x7"><g x=-0.6/></c>
<c id="xe14n" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x7" target="x8"></c>
<c id="xe14y" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x7" target="x7y"><g x=-0.6/></c>
<c id="xe15" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x7y" target="x7f"></c>
<c id="xe16z" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x8" target="x9a"><g x=0.27 pts=630,1133;830,1133/></c>
<c id="xe16y" s="fs=12;exitX=0.357;exitY=1;entryX=0.5;entryY=0" edge="1" source="x7y" target="x9a"></c>
<c id="xe16a" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x9a" target="x9b"><g x=-0.6/></c>
<c id="xe16b" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x9b" target="x9q"><g x=-0.6/></c>
<c id="xe16q" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.348;entryY=0" edge="1" source="x9q" target="x9y"><g x=-0.6/></c>
<c id="xe16f" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="x9y" target="x9f"></c>
<c id="xe16an" v="無" s="fs=12;exitX=0;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="x9a" target="x9z"><g x=-0.59 pts=635,1184/></c>
<c id="xe16bn" v="無" s="fs=12;exitX=0;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="x9b" target="x9z"><g x=-0.42 pts=635,1300/></c>
<c id="xe16qn" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="x9q" target="x9z"><g x=0.00 pts=830,1498;635,1498/></c>
<c id="xe16v" s="fs=12;exitX=0.5;exitY=1;entryX=0.713;entryY=0" edge="1" source="x9y" target="x5z"></c>
<c id="xe16w" s="fs=12;exitX=0.5;exitY=1;entryX=0.138;entryY=0" edge="1" source="x9z" target="x5z"></c>
<c id="xe17" s="fs=12;exitX=0.256;exitY=1;entryX=0.5;entryY=0" edge="1" source="x5z" target="x5q"></c>
<c id="xe18" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x5q" target="x5n"></c>
<c id="xe19" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.256;entryY=0" edge="1" source="x5q" target="x5t"><g x=-0.6/></c>
<c id="xe20" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="x5t" target="x5y"></c>
<c id="p8bcc_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1799 w=200 h=60/></c>
<c id="p8bcc_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1799 w=140 h=64/></c>
<c id="p8bcc_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1807 w=140 h=44/></c>
<c id="p8bcc_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1801 w=190 h=56/></c>
<c id="p8bcc_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1801 w=210 h=56/></c>
<c id="p8bcc_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1809 w=88 h=40/></c>
<c id="p8bcc_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1809 w=170 h=40/></c>
<c id="p8bcc_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1799 w=300 h=60/></c>
<c id="p8bcc_lgx_entry" v="虛線橢圓：跨頁入口" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=40 y=1867 w=200 h=36/></c>
<c id="p8bcc_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=260 y=1867 w=120 h=36/></c>
<c id="p8bcc_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=400 y=1867 w=150 h=36/></c>
<c id="p8bcc_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=570 y=1867 w=190 h=36/></c>
<c id="p8bcc_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=780 y=1867 w=170 h=36/></c>
<c id="p8bcc_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=1867 w=170 h=36/></c>
<c id="p8bcc_lgx_v2" v="右上綠標 v2：與 v1 不同處" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1160 y=1867 w=200 h=36/></c>
<c id="p8bcc_lgx_v2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1"><g x=1336 y=1857 w=30 h=20/></c>
<c id="p8bcc_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1905 w=200 h=28/></c>
<c id="p8bcc_tk0" v="remove" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1939 w=150 h=55/></c>
<c id="p8bcc_tv0" v="拆掉一個工具 = resolve（讀 metadata、列清單、輸出指紋）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 問 append 行 → 刪 baseline/&lt;repo&gt;/、cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp → 重生 gen/tools.just → 最後刪 version.toml 行 → 刪日誌）；初始檔永不刪、印清單" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1939 w=610 h=55/></c>
<c id="p8bcc_tk1" v="uninstall（v2.2 E、v2.5 §10、v2.8 §1）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1994 w=150 h=71/></c>
<c id="p8bcc_tv1" v="全部拆掉 = resolve（預檢全部工具、算自產檔 hash 得保護清單）→ apply（flock → 重驗 → dry-run 分支 → 建日誌 → 逐工具 remove 走保護模式 → 只刪 hash 相符的自產檔，含專案層 baseline/.gitkeep、baseline/.vendor_kit.toml，再刪空的 baseline/ → 根 justfile 那行問後刪 → 最後刪日誌 → 目錄空了才 rmdir）；不 rm -rf .vendor_kit/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1994 w=610 h=71/></c>
<c id="p8bcc_tk2" v="resolve／apply／--dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2065 w=150 h=55/></c>
<c id="p8bcc_tv2" v="resolve 只讀只算（讀 metadata、列清單、輸出指紋，不寫檔）；apply 拿 flock、重驗指紋後才刪；--dry-run（無短形）只印會刪什麼、會問什麼，覆蓋所有刪改與詢問（本機 → 0；CI 為真且需改 tracked 檔 → 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2065 w=610 h=55/></c>
<c id="p8bcc_tk3" v="flock／指紋／進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2120 w=150 h=71/></c>
<c id="p8bcc_tv3" v="flock = 專案目錄鎖（60 秒），鎖在引擎；指紋 = resolve 讀過的檔的 hash，apply 重驗（不同 → 1 請重跑，橙）；進度日誌 = 列已完成／未完成，第一個寫入前建、最後一步刪，失敗後下次可寫動詞先恢復、唯讀動詞只提示重跑（remove／uninstall 用 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml，因 metadata 會被刪）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2120 w=610 h=71/></c>
<c id="p8bcc_tk4" v="baseline／metadata" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2191 w=150 h=55/></c>
<c id="p8bcc_tv4" v="baseline/&lt;repo&gt;/ = 上次合併的範本副本（進 git；upgrade 拿它當三方合併的共同祖先）；metadata = 其中的 .vendor_kit.toml：來源 ref@digest、最後合併版本、完成標記、append 過的行；remove 先讀它（append 行）再刪整個 baseline/&lt;repo&gt;/" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2191 w=610 h=55/></c>
<c id="p8bcc_tk5" v="append 行／CRLF／三分支" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2246 w=150 h=55/></c>
<c id="p8bcc_tv5" v="add 時（strategy=append）問後加進使用者檔（.gitignore 類）的行，記在 metadata；remove／uninstall 問後找那些行（CRLF = Windows 換行 \r\n，與 LF 視為相同）：唯一命中 → 刪；零命中 → 不刪、印清單；多處命中 → 保留並 warn（Q13）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2246 w=610 h=55/></c>
<c id="p8bcc_tk6" v="初始檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1939 w=150 h=40/></c>
<c id="p8bcc_tv6" v="init.toml 複製到專案的檔（歸使用者、進 git）；remove／uninstall 都不刪，只印清單（要刪用 git rm）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1939 w=610 h=40/></c>
<c id="p8bcc_tk7" v="保護清單／保護模式" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1979 w=150 h=40/></c>
<c id="p8bcc_tv7" v="uninstall 在任何 remove 之前先算每個自產檔的 hash：內容 == 我們上次產出 → 可刪；未知或被改的 → 進保護清單，一律保留並回報；逐工具 remove 在保護模式下遇到保護清單內的檔也跳過" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1979 w=610 h=40/></c>
<c id="p8bcc_tk8" v="dev 覆寫" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2019 w=150 h=40/></c>
<c id="p8bcc_tv8" v="version.local.toml 的 &lt;repo&gt; = &quot;path:&lt;dir&gt;&quot;；工具在 dev 中 → remove 回 1 提示先 undev；uninstall 預檢時一併擋" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2019 w=610 h=40/></c>
<c id="p8bcc_tk9" v="gen／mod?／import" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2059 w=150 h=71/></c>
<c id="p8bcc_tv9" v="gen/tools.just 每個 &lt;ns&gt;.just 一行 mod?（把工具的 just 檔掛成一個命名空間；帶問號 = 檔不在也不掛）；remove 重生它去掉該工具的 mod? 行；import = 根 justfile 裡載入 .vendor_kit/entry.just 的那一行，uninstall 問後才刪；根 .dockerignore 我們加的三行也問後只刪原文相同的" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2059 w=610 h=71/></c>
<c id="p8bcc_tk10" v="CI 為真／frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2130 w=150 h=55/></c>
<c id="p8bcc_tv10" v="CI 為真 = 環境變數 CI 非空且不為 0／false（大小寫不敏感）→ frozen：任何需要寫 tracked 檔的情況一律 → 1 印清單，-y 不解除（remove／uninstall 都會改 tracked 檔，所以 CI 下只能 dry-run 或回 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2130 w=610 h=55/></c>
<c id="p8bcc_tk11" v="結束狀態 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2185 w=150 h=55/></c>
<c id="p8bcc_tv11" v="0 成功；1 失敗或需要人動作（工具層動詞不動 version.toml；自身升級後「請再跑原指令」也是 1）；2 有合併衝突（留標記、解完重跑）；3 協定不合／版本太舊（薄殼帶 --protocol P，引擎不支援 → 先 upgrade vendor_kit；v2.4 Q16／Q19）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2185 w=610 h=55/></c>
</diagram>
<diagram id="v1p9" name="流程 v2：prune"><c id="title" v="流程 v2：prune ── 依 label 清未引用的 docker 資源（interface_spec §1.2、§3.3 keep、§4.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.4-10、grilling 9 修正／補充、Q24、Q25、interface_spec A1、v2.7-7）：prune 第一版做；所有 vendor_kit 建的 docker 資源帶 label；prune 依 label 掃四類資源、刪 version.toml／local 未引用者；docker 指令由啟動器執行（不掛 socket）；image 只刪帶 label 且本專案未引用者（共享 daemon 提醒）；活躍的 .tmp.* 只列出不刪、不視為未完成交易；需問但無 tty 且無 -y → 1 + 6-4；選項只有 -y 與 --dry-run（無 -n）。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=116/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=136 w=200 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=260 y=136 w=300 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=136 w=340 h=28/></c>
<c id="hdr3" v="docker daemon" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=940 y=136 w=300 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1260 y=136 w=330 h=28/></c>
<c id="bP" v="prune [-y] [--dry-run]：引擎 resolve 算保留清單（不寫）→ 啟動器依 label 列四類資源 → 差集 → 問後逐類刪 → 引擎 apply（flock → 重驗指紋 → 清 .tmp.dist.* → 清殘留 .tmp.*）→ 摘要" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=180 w=1590 h=1541/></c>
<c id="bP_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bP"><g x=1546 y=5 w=30 h=20/></c>
<c id="q0" v="just vendor_kit prune（-y／--dry-run）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bP"><g x=20 y=36 w=200 h=80/></c>
<c id="q1" v="docker run &lt;引擎&gt; resolve prune（永不 -t）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=55 w=300 h=42/></c>
<c id="q2" v="resolve（不寫任何檔）：讀 version.toml、version.local.toml" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=55 w=340 h=42/></c>
<c id="q3" v="算保留清單 keep：引擎 ref、[tools] 每個工具 ref、local 覆寫的 vendor_kit &lt;tag&gt;" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=162 w=340 h=42/></c>
<c id="q3f" v="只讀（不寫）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bP"><g x=1240 y=136 w=330 h=94/></c>
<c id="q3f_0" v="version.toml（引擎 ref、[tools]）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="q3f"><g x=8 y=26 w=314 h=26/></c>
<c id="q3f_1" v="version.local.toml（vendor_kit = &quot;&lt;tag&gt;&quot;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="q3f"><g x=8 y=58 w=314 h=26/></c>
<c id="q4" v="偵測活躍（未恢復）的 .tmp.&lt;verb&gt;.&lt;id&gt;.toml → 只列出、印 6-33（不刪、不視為未完成交易）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=250 w=340 h=42/></c>
<c id="q4f" v=".vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml（活躍交易：保留）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bP"><g x=1240 y=250 w=330 h=42/></c>
<c id="q5" v="stdout vk-resolve/1：keep|&lt;name&gt;|&lt;ref&gt;…、fingerprint、apply|yes、end|N" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=312 w=340 h=42/></c>
<c id="q6" v="收完整份、驗首尾與筆數（不合 → 1 + 6-30，不動 docker）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=374 w=300 h=42/></c>
<c id="q7" v="docker container／image／network／volume ls --filter label=io.github.&lt;org&gt;.vendor_kit=1" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=452 w=300 h=57/></c>
<c id="q7d" v="列出帶 label 的四類資源：容器、image、network、volume" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=920 y=459 w=300 h=42/></c>
<c id="q7n" v="所有 vendor_kit 建的資源都帶 label（容器／network／volume 另加 .project=&lt;專案根&gt;）；不建 network／volume，若意外建立也要能刪（驗收 §7.4-23：故意留一個帶 label 的 network／volume，prune 後必須消失）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bP"><g x=1240 y=436 w=330 h=88/></c>
<c id="q8" v="差集 = 候選 − keep（image：帶 label 且本專案未引用；容器／network／volume：帶 label 者）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=552 w=300 h=57/></c>
<c id="q8n" v="共享 daemon 提醒：image 沒有 .project label，其他專案是否引用同一 image 不可知 → 只刪帶 label 且本專案未引用者；先 --dry-run 看；被刪的 image 下次 sync 會再拉" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bP"><g x=920 y=544 w=300 h=73/></c>
<c id="q9y" v="是 → 0：只列出會刪什麼（零刪除）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bP"><g x=20 y=637 w=200 h=58/></c>
<c id="q9" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bP"><g x=290 y=641 w=200 h=50/></c>
<c id="q10n" v="否 → 0：不刪、印清單" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bP"><g x=20 y=771 w=200 h=40/></c>
<c id="q10" v="問 6-32「要刪除以上 vendor_kit 資源嗎？」（-y 免問）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bP"><g x=240 y=735 w=300 h=112/></c>
<c id="q11l" v="是 ↓ 對四類資源逐類刪（失敗的記下、續刪其餘）" s="text;fs=12;sc=none;fc=none;fst=1" parent="bP"><g x=240 y=867 w=300 h=26/></c>
<c id="q11a" v="docker rm &lt;差集內的容器&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=913 w=300 h=40/></c>
<c id="q11ad" v="容器被刪" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=920 y=913 w=300 h=40/></c>
<c id="q11b" v="docker image rm &lt;差集內的 image&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=973 w=300 h=40/></c>
<c id="q11bd" v="image 被刪（keep 內的 image 保留）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=920 y=973 w=300 h=40/></c>
<c id="q11c" v="docker network rm &lt;差集內的 network&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=1033 w=300 h=40/></c>
<c id="q11cd" v="network 被刪" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=920 y=1033 w=300 h=40/></c>
<c id="q11d" v="docker volume rm &lt;差集內的 volume&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=1093 w=300 h=40/></c>
<c id="q11dd" v="volume 被刪" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=920 y=1093 w=300 h=40/></c>
<c id="q12" v="docker run &lt;引擎&gt; apply prune" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bP"><g x=240 y=1154 w=300 h=40/></c>
<c id="q12a" v="apply prune：拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=1153 w=340 h=42/></c>
<c id="q12b" v="重驗指紋（與 vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=1215 w=340 h=42/></c>
<c id="q12c" v="刪失效的啟動器暫存 .tmp.dist.*／（trap 沒清到的）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=1277 w=340 h=40/></c>
<c id="q12cf" v=".vendor_kit/.tmp.dist.&lt;id&gt;/（刪）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bP"><g x=1240 y=1277 w=330 h=40/></c>
<c id="q12d" v="刪已完成交易殘留的 .tmp.&lt;verb&gt;.&lt;id&gt;.toml（活躍的不刪，只列出）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bP"><g x=560 y=1337 w=340 h=42/></c>
<c id="q12df" v=".vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml（殘留：刪；活躍：保留）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bP"><g x=1240 y=1337 w=330 h=42/></c>
<c id="q13x" v="是 → 1：摘要全列，失敗的標出" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bP"><g x=20 y=1399 w=200 h=58/></c>
<c id="q13" v="有刪除失敗？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bP"><g x=290 y=1403 w=200 h=50/></c>
<c id="q14" v="否 → 0：印刪了什麼、保留什麼（含原因）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bP"><g x=20 y=1477 w=200 h=58/></c>
<c id="qe0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q0" target="q1"></c>
<c id="qe1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q1" target="q2"></c>
<c id="qe2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q2" target="q3"></c>
<c id="qe3" v="讀" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q3" target="q3f"></c>
<c id="qe4" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q3" target="q4"></c>
<c id="qe5" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q4" target="q4f"></c>
<c id="qe6" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q4" target="q5"></c>
<c id="qe7" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="q5" target="q6"><g x=-0.82 pts=750,575/></c>
<c id="qe8" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q6" target="q7"></c>
<c id="qe9" v="ls" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q7" target="q7d"></c>
<c id="qe10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q7" target="q8"></c>
<c id="qe11" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q8" target="q9"></c>
<c id="qe12" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="q9" target="q9y"></c>
<c id="qe13" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q9" target="q10"><g x=-0.6/></c>
<c id="qe14" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="q10" target="q10n"></c>
<c id="qe15" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q10" target="q11l"></c>
<c id="qe15a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q11l" target="q11a"></c>
<c id="qe16a" v="rm" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q11a" target="q11ad"></c>
<c id="qe16b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q11a" target="q11b"></c>
<c id="qe16c" v="rm" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q11b" target="q11bd"></c>
<c id="qe16d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q11b" target="q11c"></c>
<c id="qe16e" v="rm" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q11c" target="q11cd"></c>
<c id="qe16f" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q11c" target="q11d"></c>
<c id="qe16g" v="rm" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q11d" target="q11dd"></c>
<c id="qe17" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q11d" target="q12"></c>
<c id="qe18" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q12" target="q12a"></c>
<c id="qe18a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q12a" target="q12b"></c>
<c id="qe18b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q12b" target="q12c"></c>
<c id="qe19" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q12c" target="q12cf"></c>
<c id="qe18c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q12c" target="q12d"></c>
<c id="qe19d" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="q12d" target="q12df"></c>
<c id="qe20" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="q12" target="q13"></c>
<c id="qe21" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="q13" target="q13x"></c>
<c id="qe22" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="q13" target="q14"><g x=-0.76 pts=410,1686/></c>
<c id="p9_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1737 w=200 h=60/></c>
<c id="p9_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1737 w=140 h=64/></c>
<c id="p9_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1745 w=140 h=44/></c>
<c id="p9_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1739 w=190 h=56/></c>
<c id="p9_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1739 w=210 h=56/></c>
<c id="p9_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1747 w=88 h=40/></c>
<c id="p9_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1747 w=170 h=40/></c>
<c id="p9_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1737 w=280 h=60/></c>
<c id="p9_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1805 w=120 h=36/></c>
<c id="p9_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=180 y=1805 w=190 h=36/></c>
<c id="p9_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=390 y=1805 w=170 h=36/></c>
<c id="p9_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1843 w=200 h=28/></c>
<c id="p9_tk0" v="prune" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1877 w=150 h=55/></c>
<c id="p9_tv0" v="清掉本專案不再引用的 docker 資源與殘留暫存：兩段（resolve prune 出 keep 清單 → 啟動器 docker ls／rm → apply prune 清 .tmp.*）；-y 免問、--dry-run 只列出零刪除（無短形）；結束 0／1／3" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1877 w=610 h=55/></c>
<c id="p9_tk1" v="keep 清單" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1932 w=150 h=40/></c>
<c id="p9_tv1" v="vk-resolve 的 keep|&lt;name&gt;|&lt;ref&gt; 記錄：version.toml 引擎 ref、[tools] 每個工具 ref、version.local.toml 覆寫的 vendor_kit &lt;tag&gt;；這些 image 不可刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1932 w=610 h=40/></c>
<c id="p9_tk2" v="docker label" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1972 w=150 h=55/></c>
<c id="p9_tv2" v="啟動器建的每個 docker 資源都帶 io.github.&lt;org&gt;.vendor_kit=1；容器／network／volume 另加 ….project=&lt;專案根絕對路徑&gt;；工具 image 由 Dockerfile.dist 的 LABEL 帶（check.sh --dist 擋缺 LABEL）；引擎 image 另帶 ….protocol=&lt;floor_P&gt;-&lt;current_P&gt;、….schema=&lt;N&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1972 w=610 h=55/></c>
<c id="p9_tk3" v="差集" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2027 w=150 h=55/></c>
<c id="p9_tv3" v="候選（依 label 列出的四類資源）扣掉 keep：image 只刪「帶 label 且本專案未引用」者；容器／network／volume 依 label 刪；vendor_kit 不建 network／volume，若意外建立也要能刪（驗收 §7.4-23）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2027 w=610 h=55/></c>
<c id="p9_tk4" v="共享 daemon" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2082 w=150 h=40/></c>
<c id="p9_tv4" v="一台 docker daemon 被多個專案共用：image 上沒有 .project label，其他專案是否引用同一 image 不可知 → 文件明寫、先 --dry-run 看；被刪的 image 下次 sync 會再拉（已釋出 image 永不刪）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2082 w=610 h=40/></c>
<c id="p9_tk5" v=".tmp.* 日誌／.tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2122 w=150 h=55/></c>
<c id="p9_tv5" v="前者 = remove／uninstall／undev／prune 的進度日誌，未恢復（活躍）的 prune 不刪、只列出並印 6-33、不視為未完成交易（v2.7-7）；後者 = 啟動器暫存（展開的 dist、vk-resolve），trap 刪，殘留由 apply prune 清" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2122 w=610 h=55/></c>
<c id="p9_tk6" v="resolve／apply（兩段）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1877 w=150 h=55/></c>
<c id="p9_tv6" v="同一動詞分兩段：引擎 resolve 只讀只算，stdout 回 vk-resolve/1 清單（永不 -t）；啟動器先收完整份、驗首尾與筆數才動 docker；apply 拿 flock、重驗指紋後才寫；--dry-run（無短形）= apply 的唯讀預覽" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1877 w=610 h=55/></c>
<c id="p9_tk7" v="指紋／flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1932 w=150 h=55/></c>
<c id="p9_tv7" v="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1932 w=610 h=55/></c>
<c id="p9_tk8" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1987 w=150 h=55/></c>
<c id="p9_tv8" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1987 w=610 h=55/></c>
<c id="p9_tk9" v="docker ls／rm（主機命令白名單）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2042 w=150 h=55/></c>
<c id="p9_tv9" v="啟動器只用白名單命令：docker {container,image,network,volume} ls --filter label=…、docker rm／image rm／network rm／volume rm；逐類資源一次一個命令；不把 docker socket 掛進引擎（引擎不碰 daemon）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2042 w=610 h=55/></c>
<c id="p9_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2097 w=150 h=71/></c>
<c id="p9_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2097 w=610 h=71/></c>
</diagram>
<diagram id="v1p10" name="流程 v2：update"><c id="title" v="流程 v2：update ── 只查版本、不動檔（interface_spec §1.2、§5、6-3／6-15／6-33、Q27）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q11、Q27、v2.6-5、v2.7-8、v2.8-7、interface_spec §1.2 update）：無憑證時不支援需認證的版本列舉，該工具直接記失敗 1 + 6-3（不進 SemVer 解析；需人動作 → 橙），其他工具照查再彙總；token 只在 update／upgrade 的 resolve 階段以 -e 傳（TOKEN_FILE 用 -v 掛）；update 唯讀、不受 frozen 限制；有新版只在 --exit-code 時回 2；末行固定印 6-15。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=100/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=120 w=220 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=120 w=280 h=28/></c>
<c id="hdr2" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=580 y=120 w=400 h=28/></c>
<c id="hdr3" v="registry（GHCR）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1000 y=120 w=290 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1310 y=120 w=280 h=28/></c>
<c id="bU" v="update [&lt;repo&gt;] [--exit-code]：引擎查 registry（公開／有 token → 解析 SemVer；無憑證 → 直接記該目標失敗 6-3）→ 每個目標彙總（Q27）→ 末行 6-15 → 結束碼 0／1／2" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=164 w=1590 h=1255/></c>
<c id="bU_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bU"><g x=1546 y=5 w=30 h=20/></c>
<c id="u0" v="just vendor_kit update [&lt;repo&gt;] [--exit-code]" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bU"><g x=20 y=36 w=220 h=80/></c>
<c id="u1" v="組 docker run 引數：-e VENDOR_KIT_REGISTRY_TOKEN／_USER，或 -v &lt;TOKEN_FILE&gt;:/run/vk-token:ro（只在 update／upgrade 的 resolve 傳）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bU"><g x=260 y=40 w=280 h=73/></c>
<c id="u1r" v="docker run &lt;引擎&gt; update（單段、不經 create/cp）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bU"><g x=260 y=136 w=280 h=42/></c>
<c id="u2" v="update（唯讀；不受 frozen 限制）：讀 version.toml 現版" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bU"><g x=560 y=137 w=400 h=40/></c>
<c id="u2f" v="version.toml（只讀：引擎 ref、[tools]）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bU"><g x=1290 y=137 w=280 h=40/></c>
<c id="u3x" v="是 → 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bU"><g x=20 y=214 w=220 h=80/></c>
<c id="u3" v="有未完成交易（.tmp.&lt;verb&gt;.*.toml／[progress]）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bU"><g x=560 y=198 w=400 h=112/></c>
<c id="u4l" v="否 ↓ 對每個目標（[tools] 每工具 + vendor_kit 自身）查 registry" s="text;fs=12;sc=none;fc=none;fst=1" parent="bU"><g x=560 y=330 w=400 h=42/></c>
<c id="u5" v="registry 不要求認證（公開）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bU"><g x=580 y=392 w=300 h=81/></c>
<c id="u5g" v="是：GET /v2/&lt;name&gt;/tags/list（分頁）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bU"><g x=1110 y=404 w=160 h=57/></c>
<c id="u6" v="有 VENDOR_KIT_REGISTRY_TOKEN／_TOKEN_FILE？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bU"><g x=560 y=513 w=392 h=112/></c>
<c id="u6g" v="是：WWW-Authenticate 換 token → tags/list" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bU"><g x=980 y=532 w=132 h=73/></c>
<c id="u6r" v="已定（Q11）：無憑證時不支援需認證的版本列舉；token 只在 update／upgrade 的 resolve 階段以 -e 傳，不寫 log、不傳給工具；GHCR 已測試，其他 registry 依標準協定可用但未驗證" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bU"><g x=1290 y=525 w=280 h=88/></c>
<c id="u7" v="否：無憑證、不查 → 該目標記「查詢失敗 1 + 6-3」（不進 SemVer 解析）→ 下一目標／彙總" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bU"><g x=560 y=645 w=240 h=57/></c>
<c id="u8a" v="取 SemVer 最大正式版（排除預發行）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bU"><g x=810 y=722 w=150 h=42/></c>
<c id="u8b" v="與現版比較 → 記「現版 → 最新」" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bU"><g x=810 y=784 w=150 h=42/></c>
<c id="u9" v="彙總（Q27）：全部目標查完；每個目標一行（查到的「現版 → 最新」、失敗的 6-3）；訊息全列" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bU"><g x=560 y=846 w=400 h=42/></c>
<c id="u10" v="末行固定印 6-15：「套用：just vendor_kit upgrade」" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bU"><g x=560 y=908 w=400 h=40/></c>
<c id="u11x" v="是 → 1：查詢失敗（6-3：設 token 或指定 &lt;repo&gt;@&lt;tag&gt;；即使另有新版）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bU"><g x=20 y=968 w=220 h=102/></c>
<c id="u11" v="任一目標查詢失敗（1）？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bU"><g x=560 y=978 w=300 h=81/></c>
<c id="u12y" v="是 → 2：有新版（給 CI 用）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bU"><g x=20 y=1102 w=220 h=58/></c>
<c id="u12" v="有新版且 --exit-code？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bU"><g x=560 y=1090 w=300 h=81/></c>
<c id="u13" v="否 → 0：已列出（有新版也 0）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bU"><g x=20 y=1191 w=220 h=58/></c>
<c id="ue0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u0" target="u1"></c>
<c id="ue0b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u1" target="u1r"></c>
<c id="ue1" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u1r" target="u2"></c>
<c id="ue2" v="讀" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u2" target="u2f"></c>
<c id="ue3" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u2" target="u3"></c>
<c id="ue4" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="u3" target="u3x"></c>
<c id="ue5" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u3" target="u4l"></c>
<c id="ue6" s="fs=12;exitX=0.425;exitY=1;entryX=0.5;entryY=0" edge="1" source="u4l" target="u5"></c>
<c id="ue7" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u5" target="u5g"></c>
<c id="ue8" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u5" target="u6"><g x=0.30 pts=750,667;776,667/></c>
<c id="ue9" v="是" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="u6" target="u6g"></c>
<c id="ue10" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.817;entryY=0" edge="1" source="u6" target="u7"><g x=-0.6/></c>
<c id="ue11" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="u5g" target="u8a"><g x=-0.45 pts=1210,907/></c>
<c id="ue12" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="u6g" target="u8a"><g x=-0.38 pts=1066,907/></c>
<c id="ue13" v="記失敗" s="fs=12;exitX=0.5;exitY=1;entryX=0.3;entryY=0" edge="1" source="u7" target="u9"><g x=-0.6/></c>
<c id="ue13b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u8a" target="u8b"></c>
<c id="ue14" s="fs=12;exitX=0.5;exitY=1;entryX=0.812;entryY=0" edge="1" source="u8b" target="u9"></c>
<c id="ue15" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u9" target="u10"></c>
<c id="ue16" s="fs=12;exitX=0.375;exitY=1;entryX=0.5;entryY=0" edge="1" source="u10" target="u11"></c>
<c id="ue17" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="u11" target="u11x"></c>
<c id="ue18" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="u11" target="u12"><g x=-0.6/></c>
<c id="ue19" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="u12" target="u12y"></c>
<c id="ue20" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="u12" target="u13"><g x=-0.91 pts=730,1384/></c>
<c id="p10_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1435 w=200 h=60/></c>
<c id="p10_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1435 w=140 h=64/></c>
<c id="p10_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1443 w=140 h=44/></c>
<c id="p10_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1437 w=190 h=56/></c>
<c id="p10_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1437 w=210 h=56/></c>
<c id="p10_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1445 w=88 h=40/></c>
<c id="p10_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1445 w=170 h=40/></c>
<c id="p10_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1435 w=280 h=60/></c>
<c id="p10_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1503 w=120 h=36/></c>
<c id="p10_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1503 w=150 h=36/></c>
<c id="p10_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1503 w=190 h=36/></c>
<c id="p10_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=560 y=1503 w=170 h=36/></c>
<c id="p10_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1541 w=200 h=28/></c>
<c id="p10_tk0" v="update" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1575 w=150 h=55/></c>
<c id="p10_tv0" v="只查 registry 有沒有新版、不動任何檔（唯讀，不受 frozen 限制）；單段 docker run（不經 docker create/cp）；[&lt;repo&gt;] 省略 = 全部工具 + vendor_kit 自身；--exit-code：有新版回 2（給 CI 用）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1575 w=610 h=55/></c>
<c id="p10_tk1" v="查最新" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1630 w=150 h=55/></c>
<c id="p10_tv1" v="對 registry 走 Docker Registry 標準協定：需要時以 WWW-Authenticate 換 token → GET /v2/&lt;name&gt;/tags/list（分頁）→ 取 SemVer 最大正式版（排除預發行）；契約標「GHCR 已測試，其他 registry 依標準協定可用但未驗證」；查詢步驟畫白格（不是 image）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1630 w=610 h=55/></c>
<c id="p10_tk2" v="registry 憑證（Q11）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1685 w=150 h=55/></c>
<c id="p10_tv2" v="VENDOR_KIT_REGISTRY_TOKEN（+ _USER）或 VENDOR_KIT_REGISTRY_TOKEN_FILE（啟動器 -v &lt;file&gt;:/run/vk-token:ro 掛入；兩者同設 → 1）；只在 update／upgrade 的 resolve 階段以 -e 傳入引擎；不寫 log／檔、不傳給工具、dry-run 不印；不掛 ~/.docker/config.json" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1685 w=610 h=55/></c>
<c id="p10_tk3" v="6-3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1740 w=150 h=55/></c>
<c id="p10_tv3" v="無法列舉 &lt;repo&gt; 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade &lt;repo&gt;@&lt;tag&gt;（拉取使用主機 docker 認證）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1740 w=610 h=55/></c>
<c id="p10_tk4" v="多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1795 w=150 h=40/></c>
<c id="p10_tv4" v="做得完的做完；最後回最需要處理的碼：失敗 1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；update 同時遇 1 與 2 → 1；訊息全列（每個目標一行「現版 → 最新」）；不可同時宣稱「已是最新」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1795 w=610 h=40/></c>
<c id="p10_tk5" v="6-15（末行固定）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1575 w=150 h=28/></c>
<c id="p10_tv5" v="update 最後一行永遠印「套用：just vendor_kit upgrade」" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1575 w=610 h=28/></c>
<c id="p10_tk6" v="未完成交易（6-33）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1603 w=150 h=55/></c>
<c id="p10_tv6" v="唯讀動詞（sync／update／help）偵測到 .tmp.&lt;verb&gt;.*.toml 或 metadata [progress] state=in-progress → 只印「偵測到未完成的 &lt;verb&gt;（&lt;id&gt;）。請先重跑：just vendor_kit &lt;verb&gt; &lt;targets&gt;」，不自動恢復、不寫檔；update 結束 1" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1603 w=610 h=55/></c>
<c id="p10_tk7" v="frozen" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1658 w=150 h=40/></c>
<c id="p10_tv7" v="CI 非空且不為 0／false → frozen：不寫 tracked 檔、不查最新版；update 是唯讀動詞，不受 frozen 影響（CI 裡也能查）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1658 w=610 h=40/></c>
<c id="p10_tk8" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1698 w=150 h=55/></c>
<c id="p10_tv8" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1698 w=610 h=55/></c>
<c id="p10_tk9" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1753 w=150 h=71/></c>
<c id="p10_tv9" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1753 w=610 h=71/></c>
</diagram>
<diagram id="v1p11" name="狀態機 v2：初始檔五態"><c id="title" v="狀態機 v2：初始檔五態 ── metadata [[file]].state 與轉移（interface_spec §4.3、Q14／Q15、v2.7-3）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q14、Q15、v2.6 16 條、v2.7-3、interface_spec §4.3）：metadata 對每個範本記單一 state（五值）+ declined_hash + lines；declined 只用於新檔被拒、從未建立；已納管檔拒絕換版／合併時 state 不變只記 declined_hash（自環）；add 時 append 檔已存在且拒絕 → unmanaged；新版 hash 不同才再問；unmanaged／declined 只在 dry-run／check.sh 提醒、不動檔不紅燈；使用者刪了已納管檔 → deleted、upgrade 維持刪除。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=100/></c>
<c id="bS" v="初始檔五態：每個範本一筆 state；箭頭 = 動詞：條件（自環 = 拒絕但狀態不變，只記 declined_hash）；每格一件事（狀態 → 轉入條件 → upgrade 時 → dry-run／check.sh 印什麼）；remove／uninstall 一律到終點" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=164 w=1590 h=1441/></c>
<c id="bS_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bS"><g x=1546 y=5 w=30 h=20/></c>
<c id="s0" v="起點：範本存在於工具 dist/init.toml 的 [[file]]（src／dest／strategy）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=645 y=36 w=280 h=102/></c>
<c id="st_d" v="deleted⏎使用者刪了已納管檔" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1" parent="bS"><g x=20 y=268 w=160 h=57/></c>
<c id="st_m" v="managed⏎已納管（vendor_kit 建的 copy 檔）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1" parent="bS"><g x=330 y=268 w=160 h=57/></c>
<c id="st_c" v="declined⏎新檔被拒、從未建立" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1" parent="bS"><g x=640 y=268 w=160 h=57/></c>
<c id="st_a" v="appended⏎已插入行（strategy=append）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1" parent="bS"><g x=950 y=268 w=160 h=57/></c>
<c id="st_u" v="unmanaged⏎本來就有、沒納管" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1" parent="bS"><g x=1260 y=268 w=160 h=57/></c>
<c id="in_d" v="轉入：upgrade 逐檔判斷發現 D 缺（使用者刪了已納管檔）→ state=deleted" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=120 y=478 w=190 h=57/></c>
<c id="in_m" v="轉入：add 時 dest 不存在 → 建；upgrade 新版新增檔、問「要建 X 嗎」同意 → 建；declined 再問後同意 → 建" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=430 y=470 w=190 h=73/></c>
<c id="in_c" v="轉入：upgrade 新版新增檔、問「要建 X 嗎」後明確答否（EOF／Ctrl-C 不算）→ 從未建立、記 declined_hash" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=740 y=470 w=190 h=73/></c>
<c id="in_a" v="轉入：add 時 strategy=append 且檔已存在、問「要在 X 加這幾行嗎」同意 → 插入並記 lines（原本就有的相同行不認領）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=1050 y=463 w=190 h=88/></c>
<c id="in_u" v="轉入：add 時 copy 檔已存在 → 不納管、不覆蓋（-y 也不覆蓋），印 6-11；add 時 append 檔已存在、問後拒絕 → 同樣 unmanaged（只記 declined_hash）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=1360 y=455 w=190 h=104/></c>
<c id="up_d" v="upgrade 時：維持刪除（不重建、不合併）；baseline 仍推到 N" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=120 y=712 w=190 h=57/></c>
<c id="up_m" v="upgrade 時（仍 managed）：D==N／B==N 不動；D==B 問後寫 N；皆異問後三方合併（衝突 → 2）；拒絕 → 只記 declined_hash（自環）；baseline 推到 N" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=430 y=689 w=190 h=104/></c>
<c id="up_c" v="upgrade 時：N 的 hash ≠ declined_hash → 再問；相同 → 不問（仍 declined）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=740 y=712 w=190 h=57/></c>
<c id="up_a" v="upgrade 時（仍 appended）：原文比對找 lines：唯一命中 → 問後替換（拒絕 → 只記 declined_hash，自環）；零命中 → 不動只印新內容；多處 → 保留並 warn" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=1050 y=689 w=190 h=104/></c>
<c id="up_u" v="upgrade 時：永遠不動（不合併、不覆蓋）；仍 unmanaged" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bS"><g x=1360 y=720 w=190 h=42/></c>
<c id="pr_d" v="dry-run／check.sh 印：維持刪除（不重建）；不紅燈" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=120 y=946 w=190 h=42/></c>
<c id="pr_m" v="dry-run／check.sh 印：會問哪些檔（換新版／三方合併）；有 declined_hash 且新版相同 → 6-6；CI 需改 tracked 檔 → 1 印清單" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=430 y=923 w=190 h=88/></c>
<c id="pr_c" v="dry-run／check.sh 印：6-6「有 N 個範本你拒絕過」；新版有更新 → 6-8「Y 你拒絕過，vZ 有新版」；不紅燈" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=740 y=930 w=190 h=73/></c>
<c id="pr_a" v="dry-run／check.sh 印：找到 lines → 會問替換；找不到 → 印新內容；多處 → warn" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=1050 y=938 w=190 h=57/></c>
<c id="pr_u" v="dry-run／check.sh 印：6-7「X 沒納管，與範本差 N 行」；不紅燈" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=1360 y=938 w=190 h=57/></c>
<c id="end_d" v="終點：remove &lt;repo&gt;／uninstall → 這筆 state 隨 metadata 消失" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=20 y=1141 w=160 h=124/></c>
<c id="end_m" v="終點：remove &lt;repo&gt;／uninstall → 這筆 state 隨 metadata 消失" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=330 y=1141 w=160 h=124/></c>
<c id="end_c" v="終點：remove &lt;repo&gt;／uninstall → 這筆 state 隨 metadata 消失" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=640 y=1141 w=160 h=124/></c>
<c id="end_a" v="終點：remove &lt;repo&gt;／uninstall → 這筆 state 隨 metadata 消失" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=950 y=1141 w=160 h=124/></c>
<c id="end_u" v="終點：remove &lt;repo&gt;／uninstall → 這筆 state 隨 metadata 消失" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bS"><g x=1260 y=1141 w=160 h=124/></c>
<c id="s_endn" v="終點（任一狀態皆同）：remove &lt;repo&gt;／uninstall → 初始檔保留並印清單（append 行問後只刪原文相同的）；metadata 隨 baseline/&lt;repo&gt;/ 刪除 → 狀態消失；要刪初始檔請自行 git rm" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bS"><g x=20 y=1395 w=1530 h=40/></c>
<c id="sl_m_l" v="upgrade：拒絕換版／三方合併 → 只記 declined_hash（仍 managed）" s="text;fs=12;sc=none;fc=none" parent="bS"><g x=430 y=347.0 w=200 h=57/></c>
<c id="sl_c_l" v="upgrade：再問後仍拒絕 → 更新 declined_hash（仍 declined）" s="text;fs=12;sc=none;fc=none" parent="bS"><g x=740 y=347.0 w=200 h=57/></c>
<c id="sl_a_l" v="upgrade：拒絕替換 lines → 只記 declined_hash（仍 appended）" s="text;fs=12;sc=none;fc=none" parent="bS"><g x=1050 y=347.0 w=200 h=57/></c>
<c id="sl_u_l" v="upgrade：永遠不動（仍 unmanaged）" s="text;fs=12;sc=none;fc=none" parent="bS"><g x=1360 y=347.0 w=200 h=42/></c>
<c id="se_c" v="upgrade：拒絕建新檔" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="s0" target="st_c"><g x=0.00 pts=805,367;740,367/></c>
<c id="se_m" v="add：建；upgrade：新增檔同意建" s="fs=12;exitX=0.1;exitY=1;entryX=0.5;entryY=0" edge="1" source="s0" target="st_m"><g x=0.00 pts=693,367;430,367/></c>
<c id="se_a" v="add：append 檔已存在、同意插入" s="fs=12;exitX=0.65;exitY=1;entryX=0.5;entryY=0" edge="1" source="s0" target="st_a"><g x=0.14 pts=847,391;1050,391/></c>
<c id="se_u" v="add：copy 已存在；append 已存在但拒絕" s="fs=12;exitX=0.9;exitY=1;entryX=0.5;entryY=0" edge="1" source="s0" target="st_u"><g x=-0.08 pts=917,343;1360,343/></c>
<c id="se_md" v="upgrade：D 缺" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="st_m" target="st_d"></c>
<c id="se_cm" v="upgrade：再問→同意建" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="st_c" target="st_m"></c>
<c id="se_end_d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="st_d" target="end_d"></c>
<c id="se_end_m" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="st_m" target="end_m"></c>
<c id="se_end_c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="st_c" target="end_c"></c>
<c id="se_end_a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="st_a" target="end_a"></c>
<c id="se_end_u" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="st_u" target="end_u"></c>
<c id="sl_m" s="fs=12;exitX=1;exitY=0.7;entryX=0.8;entryY=1" edge="1" source="st_m" target="st_m"><g pts=524,472;524,507;478,507/></c>
<c id="sl_c" s="fs=12;exitX=1;exitY=0.7;entryX=0.8;entryY=1" edge="1" source="st_c" target="st_c"><g pts=834,472;834,507;788,507/></c>
<c id="sl_a" s="fs=12;exitX=1;exitY=0.7;entryX=0.8;entryY=1" edge="1" source="st_a" target="st_a"><g pts=1144,472;1144,507;1098,507/></c>
<c id="sl_u" s="fs=12;exitX=1;exitY=0.7;entryX=0.8;entryY=1" edge="1" source="st_u" target="st_u"><g pts=1454,472;1454,507;1408,507/></c>
<c id="p11_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1621 w=200 h=60/></c>
<c id="p11_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1621 w=140 h=64/></c>
<c id="p11_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1629 w=140 h=44/></c>
<c id="p11_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1623 w=190 h=56/></c>
<c id="p11_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1623 w=210 h=56/></c>
<c id="p11_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1631 w=88 h=40/></c>
<c id="p11_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1631 w=170 h=40/></c>
<c id="p11_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1621 w=280 h=60/></c>
<c id="p11_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1689 w=120 h=36/></c>
<c id="p11_lgx_state" v="粗框白格：狀態（state 值）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;fst=1"><g x=180 y=1689 w=200 h=36/></c>
<c id="p11_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1727 w=200 h=28/></c>
<c id="p11_tk0" v="初始檔／範本" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1761 w=150 h=40/></c>
<c id="p11_tv0" v="工具 dist/init.toml 每個 [[file]]（src、dest、strategy = copy｜append）：add 時建到專案（dest）、upgrade 時逐檔判斷；歸使用者、進 git" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1761 w=610 h=40/></c>
<c id="p11_tk1" v="metadata [[file]].state（Q15、16 條）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1801 w=150 h=55/></c>
<c id="p11_tv1" v="baseline/&lt;repo&gt;/.vendor_kit.toml 對每個範本一筆：state 單一列舉 managed／appended／declined／unmanaged／deleted；declined_hash（選填）= 最近一次被拒絕的那版範本 N 的 sha256；lines（只在 appended）= 實際插入的行原文" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1801 w=610 h=55/></c>
<c id="p11_tk2" v="declined 語意（v2.7-3）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1856 w=150 h=55/></c>
<c id="p11_tv2" v="state=declined 只用於「範本要建的新檔被拒、從未建立」；已納管（managed／appended）的檔拒絕本次更新 → state 不變、只記 declined_hash（畫成自環）；add 時 append 檔已存在且拒絕 → unmanaged（本來就有、沒納管）；二進位拒絕同" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1856 w=610 h=55/></c>
<c id="p11_tk3" v="B／D／N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1911 w=150 h=40/></c>
<c id="p11_tv3" v="B = baseline（上次合併的範本副本）、D = 磁碟上使用者的檔、N = 新版範本（讀自暫存 /dist/&lt;repo&gt;，不是 cache）；upgrade 逐檔判斷只對 state=managed 且無待解衝突" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1911 w=610 h=40/></c>
<c id="p11_tk4" v="upgrade 逐檔判斷（managed）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1951 w=150 h=55/></c>
<c id="p11_tv4" v="D 缺 → deleted；D==N 或 B==N → 不動；D==B → 問「X 換成新版？」；三者皆異 → 問後 git merge-file --diff3（衝突 → 2）；不論結果 baseline 推到 N（解析失敗除外）；二進位／symlink 未改 → 問後換、改過保留 + warn；拒絕 → 記 declined_hash、state 維持 managed" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1951 w=610 h=55/></c>
<c id="p11_tk5" v="declined 再問規則（Q14／Q15）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2006 w=150 h=55/></c>
<c id="p11_tv5" v="新版 N 的 hash ≠ declined_hash → 再問一次「要建 X 嗎」（同意 → 建 → managed；拒絕 → 仍 declined、更新 declined_hash）；相同 → 不問，只印 6-6／6-8；EOF／Ctrl-C 不算拒絕、不記 declined" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2006 w=610 h=55/></c>
<c id="p11_tk6" v="append 行（Q6／Q12／Q13）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1761 w=150 h=55/></c>
<c id="p11_tv6" v="strategy=append 的檔已存在 → 問「要在 X 加這幾行嗎」；同意 → 插入並記 lines；upgrade 用原文比對（CRLF／LF 等價）找上次插入的行：唯一命中 → 問後替換、零命中 → 不動只印新內容、多處 → 保留並 warn；remove／uninstall 問後只刪原文相同的行" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1761 w=610 h=55/></c>
<c id="p11_tk7" v="dry-run／check.sh 印什麼" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1816 w=150 h=40/></c>
<c id="p11_tv7" v="upgrade --dry-run 與 ci/check.sh ③ 印 6-6「有 N 個範本你拒絕過」、6-7「X 沒納管，與範本差 N 行」、6-8「Y 你拒絕過，vZ 有新版」；不動檔、不紅燈（CI 需改 tracked 檔才 1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1816 w=610 h=40/></c>
<c id="p11_tk8" v="6-11" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1856 w=150 h=40/></c>
<c id="p11_tv8" v="add 遇 copy 檔已存在：「&lt;X&gt; 已存在，未納管；範本在 .vendor_kit/cache/&lt;repo&gt;/files/ 可自行比對」" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1856 w=610 h=40/></c>
<c id="p11_tk9" v="永不刪" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1896 w=150 h=40/></c>
<c id="p11_tv9" v="不變量：vendor_kit 對使用者的檔可以建、要改先問、永不刪、永不覆蓋；remove／uninstall 只印初始檔清單（要刪用 git rm）；新版刪除的檔（N 缺）只 warn 不刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1896 w=610 h=40/></c>
<c id="p11_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1936 w=150 h=71/></c>
<c id="p11_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1936 w=610 h=71/></c>
</diagram>
<diagram id="v1p12" name="狀態機 v2：交易與進度日誌"><c id="title" v="狀態機 v2：交易與進度日誌（interface_spec §0、§3.2 apply、§4.3 [progress]、§4.6）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（v2.2 C、v2.4-12、v2.5-3、v2.6-9、v2.7-7、v2.8-2、interface_spec §0 進度日誌、§4.3 [progress]、§4.6）：apply 順序 = flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 寫入 → 最後一步刪日誌（uninstall 在根 justfile 那行之後）；中斷 → 1 明列已完成／未完成；下次可寫動詞先恢復（失敗 6-27）、唯讀動詞只提示 6-33 不恢復；prune 特例：活躍日誌只列出不刪、不視為未完成交易；install 例外：第一次 install 不建日誌、失敗整包丟棄，修復型 install 建 .tmp.install.&lt;id&gt;.toml。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=116/></c>
<c id="hdr0" v="使用者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=136 w=240 h=28/></c>
<c id="hdr1" v="引擎容器（apply 段）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=300 y=136 w=480 h=28/></c>
<c id="hdr2" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=800 y=136 w=380 h=28/></c>
<c id="hdr3" v="規則／說明" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1200 y=136 w=390 h=28/></c>
<c id="bT1" v="交易生命週期（所有可寫動詞的 apply 段；第一次 install 例外：不建日誌、失敗整包丟棄）：拿鎖 → 重驗指紋 → dry-run 分支 → 建日誌 → 逐步寫入（每步記 done）→ 刪日誌；中斷 → 1、日誌留著" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=180 w=1590 h=853/></c>
<c id="bT1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bT1"><g x=1546 y=5 w=30 h=20/></c>
<c id="t0" v="來自各動詞頁：resolve → 啟動器 docker 之後，apply &lt;verb&gt;" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bT1"><g x=20 y=36 w=240 h=80/></c>
<c id="t1" v="拿 flock 專案目錄（60 秒；逾時 → 1 + 6-26；VENDOR_KIT_NO_LOCK=1 跳過）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT1"><g x=280 y=55 w=480 h=42/></c>
<c id="t1i" v="不變量：回 3 一律零寫入（無任何例外）；工具層回 1 時 version.toml 不動；日誌在第一個寫入前建、最後一步刪；never fail silently" s="fc=#ffffff;sc=#b85450;fs=12;fst=1" parent="bT1"><g x=1180 y=48 w=390 h=57/></c>
<c id="t2" v="重驗指紋（與 /dist/vk-resolve 的 fingerprint 比；不同 → 1 + 6-12「請重跑」，零寫入）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT1"><g x=280 y=136 w=480 h=42/></c>
<c id="t3y" v="是 → 0：唯讀預覽（CI 為真且需改 tracked 檔 → 1）；不建日誌" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT1"><g x=20 y=198 w=240 h=80/></c>
<c id="t3" v="--dry-run？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT1"><g x=280 y=213 w=200 h=50/></c>
<c id="t4" v="建進度日誌（第一個寫入前）：state=in-progress、verb、id、started、targets、done[]／pending[]、consents" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT1"><g x=280 y=380 w=480 h=42/></c>
<c id="t4f" v="日誌位置（依動詞）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bT1"><g x=780 y=298 w=380 h=206/></c>
<c id="t4f_0" v="add／upgrade：baseline/&lt;repo&gt;/.vendor_kit.toml [progress]" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="t4f"><g x=8 y=26 w=364 h=42/></c>
<c id="t4f_1" v="remove／uninstall／undev／prune：.vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="t4f"><g x=8 y=74 w=364 h=42/></c>
<c id="t4f_2" v="修復型 install：.vendor_kit/.tmp.install.&lt;id&gt;.toml" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="t4f"><g x=8 y=122 w=364 h=42/></c>
<c id="t4f_3" v="第一次 install（薄殼不存在）：不建日誌" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="t4f"><g x=8 y=170 w=364 h=26/></c>
<c id="t4n" v="已定（v2.8-2）install 例外：第一次 install（薄殼不存在）不建日誌，失敗整包丟棄、不留半成品，下次直接重跑；修復型 install（薄殼已存在）建 .tmp.install.&lt;id&gt;.toml，同其他可寫動詞走恢復。其餘兩種位置：remove／uninstall 會刪 metadata、undev／prune 沒有工具 metadata → 放 .vendor_kit/.tmp.*（自有 .gitignore 擋）；&lt;id&gt; = UTC 時間戳 + 隨機" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bT1"><g x=1180 y=341 w=390 h=120/></c>
<c id="t5" v="逐步寫入：每步「暫存 → 原子替換 → 日誌 done += 步驟」（詢問取得的同意也記進 consents）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT1"><g x=280 y=532 w=480 h=42/></c>
<c id="t5f" v="日誌 done[]／pending[] 每步更新（合併也在暫存完成）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bT1"><g x=780 y=532 w=380 h=40/></c>
<c id="t5n" v="順序固定：清除衝突狀態 → append／初始檔 → baseline → metadata → cache → gen/tools.just（最後寫、與 cache 同一 apply 內原子替換）→ version.toml 最後" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bT1"><g x=1180 y=524 w=390 h=57/></c>
<c id="t6x" v="是 → 1：明列已完成／未完成；日誌留著（state 仍 in-progress）；第一次 install：整包丟棄、無日誌" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bT1"><g x=20 y=601 w=240 h=124/></c>
<c id="t6" v="中斷？（寫入失敗／Ctrl-C／斷電）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT1"><g x=280 y=622 w=300 h=81/></c>
<c id="t7" v="否：最後一步刪日誌（uninstall：在根 justfile 那行之後才刪）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT1"><g x=280 y=746 w=480 h=40/></c>
<c id="t7f" v="日誌刪除 = 交易完成（.tmp.&lt;verb&gt;.&lt;id&gt;.toml 刪／[progress] 移除）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bT1"><g x=780 y=745 w=380 h=42/></c>
<c id="t8" v="0（或 2 有衝突）：印摘要" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT1"><g x=20 y=807 w=240 h=40/></c>
<c id="te0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t0" target="t1"></c>
<c id="te1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t1" target="t2"></c>
<c id="te2" s="fs=12;exitX=0.208;exitY=1;entryX=0.5;entryY=0" edge="1" source="t2" target="t3"></c>
<c id="te3" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="t3" target="t3y"></c>
<c id="te4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.208;entryY=0" edge="1" source="t3" target="t4"><g x=-0.6/></c>
<c id="te5" v="建" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t4" target="t4f"></c>
<c id="te6" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="t4" target="t5"></c>
<c id="te7" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t5" target="t5f"></c>
<c id="te8" s="fs=12;exitX=0.312;exitY=1;entryX=0.5;entryY=0" edge="1" source="t5" target="t6"></c>
<c id="te9" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="t6" target="t6x"></c>
<c id="te10" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.312;entryY=0" edge="1" source="t6" target="t7"><g x=-0.6/></c>
<c id="te11" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="t7" target="t7f"></c>
<c id="te12" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="t7" target="t8"><g x=-0.86 pts=540,1007/></c>
<c id="bT2" v="中斷後的下一次執行（任何動詞開始前先偵測未完成交易）：可寫動詞先恢復再繼續；唯讀動詞只提示重跑原動詞；prune 特例只列出" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=1049 w=1590 h=730/></c>
<c id="bT2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bT2"><g x=1546 y=5 w=30 h=20/></c>
<c id="r0" v="打任何 vendor_kit 動詞" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT2"><g x=20 y=37 w=240 h=40/></c>
<c id="r1" v="偵測未完成交易：.vendor_kit/.tmp.&lt;verb&gt;.*.toml（含 .tmp.install.*）或任一 metadata [progress] state=in-progress" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT2"><g x=280 y=36 w=480 h=42/></c>
<c id="r1f" v="讀日誌（verb、id、targets、done／pending、consents）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bT2"><g x=780 y=37 w=380 h=40/></c>
<c id="r2n" v="否 → 正常執行本次動詞" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT2"><g x=20 y=103 w=240 h=40/></c>
<c id="r2" v="有未完成交易？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT2"><g x=370 y=98 w=220 h=50/></c>
<c id="r2px" v="是 → prune 特例：只列出活躍日誌、印 6-33（不刪、不恢復）→ 繼續 prune（接 prune 頁）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT2"><g x=20 y=188 w=240 h=102/></c>
<c id="r2p" v="本動詞是 prune？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT2"><g x=370 y=198 w=220 h=81/></c>
<c id="r2pn" v="已定（v2.7-7）：prune 遇活躍日誌不擋、不恢復、不刪；只列出提示重跑原動詞；差集與 apply prune 照做" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bT2"><g x=1180 y=218 w=390 h=42/></c>
<c id="r3x" v="否（sync／update）→ 1 + 6-33：請先重跑原動詞（不恢復、不寫檔）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bT2"><g x=20 y=346 w=240 h=80/></c>
<c id="r3" v="本動詞可寫？（修復型 install／add／remove／upgrade／undev／uninstall）" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT2"><g x=280 y=330 w=400 h=112/></c>
<c id="r3n" v="已定（v2.6-9）：唯讀動詞遇未完成交易只提示重跑原動詞，不自動恢復；help 不受影響" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bT2"><g x=1180 y=365 w=390 h=42/></c>
<c id="r4" v="是：恢復 = 依日誌把上次交易走完（done 略過；pending 逐步補做；consents 已記的不再問）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT2"><g x=280 y=462 w=480 h=42/></c>
<c id="r4f" v="補做 pending 的寫入（暫存 → 原子替換）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bT2"><g x=780 y=463 w=380 h=40/></c>
<c id="r5x" v="否 → 1 + 6-27「未恢復：&lt;檔名&gt;」逐檔列出；日誌留著" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bT2"><g x=20 y=524 w=240 h=80/></c>
<c id="r5" v="恢復成功？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bT2"><g x=280 y=539 w=220 h=50/></c>
<c id="r6" v="是：刪日誌 → 繼續本次動詞（resolve 會重算指紋）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bT2"><g x=280 y=624 w=480 h=40/></c>
<c id="r6f" v="日誌刪除" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bT2"><g x=780 y=624 w=380 h=40/></c>
<c id="r7" v="→ 繼續本次動詞" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bT2"><g x=20 y=684 w=240 h=40/></c>
<c id="re0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="r0" target="r1"></c>
<c id="re1" v="讀" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="r1" target="r1f"></c>
<c id="re2" s="fs=12;exitX=0.417;exitY=1;entryX=0.5;entryY=0" edge="1" source="r1" target="r2"></c>
<c id="re3" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="r2" target="r2n"></c>
<c id="re4" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="r2" target="r2p"><g x=-0.6/></c>
<c id="re4p" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="r2p" target="r2px"></c>
<c id="re4n" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="r2p" target="r3"><g x=-0.6/></c>
<c id="re5" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="r3" target="r3x"></c>
<c id="re6" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.417;entryY=0" edge="1" source="r3" target="r4"><g x=-0.6/></c>
<c id="re7" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="r4" target="r4f"></c>
<c id="re8" s="fs=12;exitX=0.229;exitY=1;entryX=0.5;entryY=0" edge="1" source="r4" target="r5"></c>
<c id="re9" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="r5" target="r5x"></c>
<c id="re10" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.229;entryY=0" edge="1" source="r5" target="r6"><g x=-0.6/></c>
<c id="re11" v="刪" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="r6" target="r6f"></c>
<c id="re12" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="r6" target="r7"><g x=-0.87 pts=540,1753/></c>
<c id="p12_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1795 w=200 h=60/></c>
<c id="p12_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1795 w=140 h=64/></c>
<c id="p12_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1803 w=140 h=44/></c>
<c id="p12_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1797 w=190 h=56/></c>
<c id="p12_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1797 w=210 h=56/></c>
<c id="p12_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1805 w=88 h=40/></c>
<c id="p12_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1805 w=170 h=40/></c>
<c id="p12_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1795 w=280 h=60/></c>
<c id="p12_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1863 w=120 h=36/></c>
<c id="p12_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1863 w=150 h=36/></c>
<c id="p12_lgx_inv" v="紅粗框：不變量" s="fc=#ffffff;sc=#b85450;fs=12;fst=1"><g x=350 y=1863 w=130 h=36/></c>
<c id="p12_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=500 y=1863 w=190 h=36/></c>
<c id="p12_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=710 y=1863 w=170 h=36/></c>
<c id="p12_lgx_entry" v="虛線橢圓：來自其他頁" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=900 y=1863 w=200 h=36/></c>
<c id="p12_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1901 w=200 h=28/></c>
<c id="p12_tk0" v="交易／apply" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1935 w=150 h=40/></c>
<c id="p12_tv0" v="一次會寫檔的動詞執行 = 一筆交易：apply 拿 flock → 重驗指紋 → dry-run 分支 → 建進度日誌（第一個寫入前）→ 逐步寫入 → 最後一步刪日誌；回 3 一律零寫入；工具層回 1 時 version.toml 不動" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1935 w=610 h=40/></c>
<c id="p12_tk1" v="進度日誌" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1975 w=150 h=40/></c>
<c id="p12_tv1" v="記錄交易進度的 TOML：state=&quot;in-progress&quot;、verb、id、started（UTC ISO 8601）、targets、done／pending（步驟清單）、consents（已取得的同意）；存在 = 上次沒走完" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1975 w=610 h=40/></c>
<c id="p12_tk2" v="兩種位置" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2015 w=150 h=55/></c>
<c id="p12_tv2" v="add／upgrade 記在 metadata baseline/&lt;repo&gt;/.vendor_kit.toml 的 [progress]；remove／uninstall／undev／prune／修復型 install 放 .vendor_kit/.tmp.&lt;verb&gt;.&lt;id&gt;.toml（因為 metadata 會被刪或不存在）；&lt;id&gt; = UTC 時間戳 + 隨機（不用 &lt;repo&gt;，uninstall 多工具才不撞）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2015 w=610 h=55/></c>
<c id="p12_tk3" v="install 的日誌（v2.8-2）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2070 w=150 h=55/></c>
<c id="p12_tv3" v="第一次 install（薄殼不存在）不建日誌：失敗整包丟棄、不留半成品（bootstrap.sh 的 1 失敗不留半成品只對它成立），下次直接重跑；修復型 install（薄殼已存在、冪等修復）建 .vendor_kit/.tmp.install.&lt;id&gt;.toml，與其他可寫動詞一樣走恢復" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2070 w=610 h=55/></c>
<c id="p12_tk4" v="恢復" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2125 w=150 h=55/></c>
<c id="p12_tv4" v="可寫動詞（修復型 install／add／remove／upgrade／undev／uninstall）開始前偵測到未完成交易 → 先依日誌把交易走完（done 略過、pending 補做、consents 不再問）再繼續本次；失敗 → 1 印 6-27「未恢復：&lt;檔名&gt;」逐檔列出、日誌留著；第一次 install 沒有日誌可恢復（整包丟棄後重跑）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2125 w=610 h=55/></c>
<c id="p12_tk5" v="唯讀動詞不恢復" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2180 w=150 h=40/></c>
<c id="p12_tv5" v="sync／update 偵測到未完成交易只印 6-33「偵測到未完成的 &lt;verb&gt;（&lt;id&gt;）。請先重跑：just vendor_kit &lt;verb&gt; &lt;targets&gt;」→ 1，不寫任何檔；help 不受影響" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2180 w=610 h=40/></c>
<c id="p12_tk6" v="prune 特例（v2.7-7）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2220 w=150 h=40/></c>
<c id="p12_tv6" v="prune 遇活躍（未恢復）日誌：只列出並印 6-33、不刪、不視為未完成交易（不擋 prune、不恢復）；prune 自己的日誌 .tmp.prune.&lt;id&gt;.toml 與其他可寫動詞一樣走恢復" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2220 w=610 h=40/></c>
<c id="p12_tk7" v="原子替換／暫存" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1935 w=150 h=40/></c>
<c id="p12_tv7" v="每個寫入先寫到暫存（合併也在暫存完成），確認沒問題再逐檔一次換上（rename）；gen/tools.just 最後寫、與 cache 同一 apply 內原子替換；中斷只會留下「已換上」與「未換上」兩種檔，不留半寫的檔" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1935 w=610 h=40/></c>
<c id="p12_tk8" v=".tmp.dist.&lt;id&gt;/" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1975 w=150 h=40/></c>
<c id="p12_tv8" v="啟動器暫存（展開的工具 dist、vk-resolve）；不是交易日誌；啟動器 trap … EXIT INT TERM 清容器與此目錄；殘留由 prune 清" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1975 w=610 h=40/></c>
<c id="p12_tk9" v="dry-run" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2015 w=150 h=40/></c>
<c id="p12_tv9" v="apply --dry-run：唯讀預覽（本機 → 0；CI 為真且需改 tracked 檔 → 1 印清單）；不建日誌、不寫檔；也要先拉 image 展開才知道會問哪些檔" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2015 w=610 h=40/></c>
<c id="p12_tk10" v="指紋／flock" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2055 w=150 h=55/></c>
<c id="p12_tv10" v="指紋 = resolve 讀過的檔（version.toml、local、metadata、要動的使用者檔、stamp 第一行、.tmp.* 清單、鎖定 digest、argv）的 sha256；apply 拿鎖後重算，不同 → 1 + 6-12「請重跑」；flock = 專案目錄鎖（60 秒；VENDOR_KIT_NO_LOCK=1 可關），鎖在引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2055 w=610 h=55/></c>
<c id="p12_tk11" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2110 w=150 h=55/></c>
<c id="p12_tv11" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2110 w=610 h=55/></c>
<c id="p12_tk12" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2165 w=150 h=71/></c>
<c id="p12_tv12" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2165 w=610 h=71/></c>
</diagram>
<diagram id="v1p13" name="相容性矩陣 v2"><c id="title" v="相容性矩陣 v2：舊薄殼 × 新引擎、舊引擎 × 新檔 → 0／1／3（interface_spec §2、§8；Q16／Q19／Q23）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q16、Q19、Q23、v2.4-3／-6／-7、v2.6 16 條、v2.7-4、interface_spec §2、§4 通則、§8）：相容承諾兩層（永久：救援路徑 + 舊資料可讀可遷；非永久：舊薄殼跑新 major 一般動詞回 3）；floor = 固定 release 常數；新舊以 P／schema 比較不用版本字串；回 3 零寫入、無任何例外（救援路徑亦同）；written_by 純資訊欄、無 min_reader；同 schema 未知欄位讀忽略寫保留。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="l13a" v="(a) 舊薄殼 P × 新引擎（接受 [floor_P, current_P]）：一般動詞／救援路徑各回什麼" s="text;fs=12;sc=none;fc=none;fst=1"><g x=40 y=120 w=900 h=24/></c>
<c id="ta_h0" v="薄殼 P 的情況" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=150 w=330 h=30/></c>
<c id="ta_h1" v="一般動詞（add／remove／upgrade &lt;repo&gt;／sync 寫入／undev／uninstall／prune／dev／update）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=370 y=150 w=640 h=30/></c>
<c id="ta_h2" v="救援路徑（install／upgrade vendor_kit／sync 不符提示／help；單段）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1010 y=150 w=590 h=30/></c>
<c id="ta_r0c0" v="P &lt; floor_P（太舊）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=180 w=330 h=30/></c>
<c id="ta_r0c1" v="3 + 6-18「請以 bootstrap.sh 重建」；零寫入；floor 檢查先於任何上網（斷網也回 3）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=370 y=180 w=640 h=30/></c>
<c id="ta_r0c2" v="3 + 6-18（救援路徑也不接、同樣零寫入；唯一可用 synthetic fixture 驗收）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1010 y=180 w=590 h=30/></c>
<c id="ta_r1c0" v="floor_P ≤ P &lt; 引擎需求（舊薄殼 × 新 major）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=210 w=330 h=42/></c>
<c id="ta_r1c1" v="3 + 6-36「薄殼協定 &lt;P_shell&gt; 低於引擎 &lt;vY&gt; 的一般動詞需求，請先 upgrade vendor_kit」；零寫入" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=370 y=210 w=640 h=42/></c>
<c id="ta_r1c2" v="0／1 正常（永久保證）：install／upgrade vendor_kit 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」；sync 不符 → 1 + 6-1；help → 0" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=1010 y=210 w=590 h=42/></c>
<c id="ta_r2c0" v="同 major（P 在引擎支援範圍內）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=252 w=330 h=42/></c>
<c id="ta_r2c1" v="0／1／2 正常：引擎以呼叫方 P 輸出 vk-resolve/P 與結束碼語意；不輸出呼叫方不認識的 kind、不要求其未提供的 mount／環境變數" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=370 y=252 w=640 h=42/></c>
<c id="ta_r2c2" v="0／1 正常；upgrade vendor_kit 無新版且薄殼相符 → 0 無變更" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=1010 y=252 w=590 h=42/></c>
<c id="ta_r3c0" v="P &gt; current_P（新薄殼 × 舊引擎：降版／dev -i 舊 image）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=294 w=330 h=73/></c>
<c id="ta_r3c1" v="3：P 不在引擎的 [floor_P, current_P]；零寫入" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=370 y=294 w=640 h=73/></c>
<c id="ta_r3c2" v="降版 upgrade vendor_kit@&lt;舊版&gt;：目標引擎能無損讀現有檔（同 P／schema）→ 重產薄殼 → 1 + 6-2「請 commit 並再跑原指令」（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前 3 + 6-10「請 git revert」（零寫入）；dev vendor_kit -i 舊 image 禁止重產 tracked 薄殼 → 3" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1010 y=294 w=590 h=73/></c>
<c id="l13b" v="(b) 舊引擎 × 檔案 schema（每檔各自 schema = N；讀取門檻只看 schema）" s="text;fs=12;sc=none;fc=none;fst=1"><g x=40 y=391 w=900 h=24/></c>
<c id="tb_h0" v="檔 vs 引擎" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=421 w=300 h=30/></c>
<c id="tb_h1" v="讀" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=340 y=421 w=420 h=30/></c>
<c id="tb_h2" v="寫" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=760 y=421 w=560 h=30/></c>
<c id="tb_h3" v="結束碼" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1320 y=421 w=280 h=30/></c>
<c id="tb_r0c0" v="同 schema、有未知欄位" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=451 w=300 h=30/></c>
<c id="tb_r0c1" v="讀時忽略未知欄位" s="sc=#999999;fs=12;fc=#ffffff"><g x=340 y=451 w=420 h=30/></c>
<c id="tb_r0c2" v="寫時保留未知欄位（不能保留 → 拒絕寫）；只拒絕型別錯／重複宣告" s="sc=#999999;fs=12;fc=#ffffff"><g x=760 y=451 w=560 h=30/></c>
<c id="tb_r0c3" v="0（型別錯／重複宣告 → 1）" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=1320 y=451 w=280 h=30/></c>
<c id="tb_r1c0" v="檔 schema &lt; 引擎（舊檔）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=481 w=300 h=42/></c>
<c id="tb_r1c1" v="可讀：記憶體轉換（讀任一舊 schema → 當前 schema，不鏈式）" s="sc=#999999;fs=12;fc=#ffffff"><g x=340 y=481 w=420 h=42/></c>
<c id="tb_r1c2" v="只在本來要寫該檔的明確動作才寫回當前 schema；metadata 遷移由 upgrade vendor_kit 做、dry-run 明列；同一專案短暫混合 schema 合法" s="sc=#999999;fs=12;fc=#ffffff"><g x=760 y=481 w=560 h=42/></c>
<c id="tb_r1c3" v="0" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=1320 y=481 w=280 h=42/></c>
<c id="tb_r2c0" v="檔 schema &gt; 引擎支援上限（新檔）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=523 w=300 h=42/></c>
<c id="tb_r2c1" v="拒絕讀：3 + 6-19「schema &lt;N&gt; 高於本引擎支援的 &lt;M&gt;；寫入者為 vendor_kit &lt;written_by&gt;」" s="sc=#999999;fs=12;fc=#ffffff"><g x=340 y=523 w=420 h=42/></c>
<c id="tb_r2c2" v="任何寫入前退出（零寫入）；dev vendor_kit -i 舊 image 亦同" s="sc=#999999;fs=12;fc=#ffffff"><g x=760 y=523 w=560 h=42/></c>
<c id="tb_r2c3" v="3" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1320 y=523 w=280 h=42/></c>
<c id="tb_r3c0" v="降版目標引擎（upgrade vendor_kit@&lt;舊版&gt;）" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=565 w=300 h=42/></c>
<c id="tb_r3c1" v="以目標 image LABEL 的 P／schema 判：能無損讀現有檔 → 讀" s="sc=#999999;fs=12;fc=#ffffff"><g x=340 y=565 w=420 h=42/></c>
<c id="tb_r3c2" v="無損 → 重產薄殼 → 1 + 6-2（依 upgrade vendor_kit 的 0／1 規則；薄殼已相符才 0）；否則改檔前拒絕 3 + 6-10「請 git revert」" s="sc=#999999;fs=12;fc=#ffffff"><g x=760 y=565 w=560 h=42/></c>
<c id="tb_r3c3" v="1（無損 → 重產薄殼）／3（否則）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1320 y=565 w=280 h=42/></c>
<c id="k13a" v="floor 常數（已定）：第一個正式版 v1.0.0、P=1、schema=1；寫在契約，只能經 ADR + major 提高；引擎 image LABEL ….protocol=&lt;floor_P&gt;-&lt;current_P&gt;、….schema=&lt;N&gt; 讓啟動器不起容器即可判 floor；低於 floor → 3 + 6-18 零寫入" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=40 y=631 w=500 h=57/></c>
<c id="k13b" v="--protocol 協商（已定，Q16）：薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎接受 [floor_P, current_P]，以呼叫方 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1；引擎宣稱的 P 真不支援 → 3" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=560 y=631 w=520 h=73/></c>
<c id="k13c" v="Q16 兩層承諾（已定）：永久 —— 任何 ≥ floor 的舊薄殼可叫新引擎的救援路徑（單段 docker run，不依賴 resolve/apply 與 gen/）並得正確提示；舊資料永遠可讀可遷。非永久 —— 舊薄殼跑新 major 一般動詞只保證乾淨回 3 + 6-36（零寫入）；同 major 內保留已承諾薄殼的一般呼叫" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=1100 y=631 w=490 h=73/></c>
<c id="k13d" v="written_by：每個 vendor_kit 寫的 TOML 都有 written_by = &quot;&lt;vX&gt;&quot;（寫入引擎版本），純資訊欄、不作讀取門檻（無 min_reader）；6-19 印出它供人判斷該用哪個引擎" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=720 w=500 h=57/></c>
<c id="k13e" v="新舊怎麼比：一律以 P／schema 比較，不用 SemVer 版本字串；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1 的情境（印記不符、薄殼被改 6-28、自身升級完成要重跑 6-2）維持 1，不因訊息含 upgrade 而改 3；回 3 零寫入無任何例外（v2.7-4）" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=560 y=720 w=520 h=57/></c>
<c id="k13f" v="驗收（§7.4-1～8）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 驅動候選 C（線性）；連升 r_i → r_j → C；floor 直接跳升；降版同 P／schema 成功（重產薄殼 → 1）、跨 schema 3；&lt; floor 唯一 synthetic；舊引擎讀新檔 3 零寫入；舊 bootstrap.sh 再跑不降版；已釋出 image／資產／fixture 永不刪" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1100 y=720 w=490 h=73/></c>
<c id="p13_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=823 w=200 h=60/></c>
<c id="p13_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=823 w=140 h=64/></c>
<c id="p13_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=831 w=140 h=44/></c>
<c id="p13_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=825 w=190 h=56/></c>
<c id="p13_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=825 w=210 h=56/></c>
<c id="p13_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=833 w=88 h=40/></c>
<c id="p13_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=833 w=170 h=40/></c>
<c id="p13_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=823 w=280 h=60/></c>
<c id="p13_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=891 w=120 h=36/></c>
<c id="p13_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=891 w=150 h=36/></c>
<c id="p13_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=350 y=891 w=170 h=36/></c>
<c id="p13_lgx_c0" v="綠格：結束碼 0" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=540 y=891 w=110 h=36/></c>
<c id="p13_lgx_cx" v="橙格：需要人動作（1／2／3）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=670 y=891 w=190 h=36/></c>
<c id="p13_lgx_cell" v="白格：表格內容" s="sc=#999999;fs=12;fc=#ffffff"><g x=880 y=891 w=110 h=36/></c>
<c id="p13_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=929 w=200 h=28/></c>
<c id="p13_tk0" v="薄殼 P／引擎 [floor_P, current_P]" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=963 w=150 h=55/></c>
<c id="p13_tv0" v="薄殼 = 進 git 的 .vendor_kit/ 四檔（entry.just、vendor.just、.gitignore、ci/check.sh），首行自描述帶協定號 P；引擎 image 接受 [floor_P, current_P]（LABEL ….protocol=&lt;floor_P&gt;-&lt;current_P&gt;，啟動器不起容器即可判 floor）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=963 w=610 h=55/></c>
<c id="p13_tk1" v="--protocol P" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1018 w=150 h=55/></c>
<c id="p13_tv1" v="薄殼每次呼叫附 --protocol P（第一版起 P=1；全域旗標在子命令前）；引擎以呼叫方的 P 輸出 vk-resolve/P 行別與結束碼語意；新增 verb／旗標／記錄種類／欄位／結束碼語意／印記第一行語意 → P+1" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1018 w=610 h=55/></c>
<c id="p13_tk2" v="floor" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1073 w=150 h=40/></c>
<c id="p13_tv2" v="固定 release 常數 = 第一個正式版（v1.0.0、P=1、schema=1）；只能經 ADR + major 提高；低於 floor → 3 + 6-18 零寫入；floor 檢查先於任何上網（斷網也回 3）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1073 w=610 h=40/></c>
<c id="p13_tk3" v="救援路徑（永久）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1113 w=150 h=55/></c>
<c id="p13_tv3" v="install、upgrade vendor_kit[@&lt;tag&gt;]、sync 的「薄殼不符 → 1 + 6-1」判定、help：單段 docker run，不依賴 resolve/apply 與 gen/；任何 ≥ floor 的薄殼都能經此叫任何引擎重產薄殼（反向降版亦然，受 3 (c)(d) 限制）；救援路徑回 3 時同樣零寫入" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1113 w=610 h=55/></c>
<c id="p13_tk4" v="一般動詞（非永久）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1168 w=150 h=55/></c>
<c id="p13_tv4" v="add／remove／upgrade &lt;repo&gt;／sync 寫入／undev／uninstall／prune／dev／update：舊薄殼跑新 major 只保證乾淨回 3 + 6-36 提示先 upgrade vendor_kit（零寫入）；同 major 內保留所有已承諾薄殼的一般呼叫" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1168 w=610 h=55/></c>
<c id="p13_tk5" v="schema N" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1223 w=150 h=55/></c>
<c id="p13_tv5" v="每個 vendor_kit 寫的 TOML（version.toml、version.local.toml、metadata、.tmp.*）有 schema = N（integer）：讀取門檻只看它；同 schema 只加不改；讀時忽略未知欄位、寫時保留（不能保留則拒絕寫）；只拒絕型別錯／重複宣告 → 1；讀任一舊 schema → 直接寫當前 schema（不鏈式）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1223 w=610 h=55/></c>
<c id="p13_tk6" v="written_by" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=963 w=150 h=40/></c>
<c id="p13_tv6" v="寫入引擎版本（string），純資訊欄、不作讀取門檻（無 min_reader）；6-19 訊息印出它供人判斷該用哪個引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=963 w=610 h=40/></c>
<c id="p13_tk7" v="6-18／6-19／6-36／6-10" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1003 w=150 h=55/></c>
<c id="p13_tv7" v="6-18 薄殼／引擎低於 floor「請以 bootstrap.sh 重建」；6-19 schema N 高於本引擎支援的 M；6-36 薄殼協定低於引擎一般動詞需求「請先 upgrade vendor_kit」；6-10 降版目標引擎無法無損讀「請 git revert」；四者皆 3、零寫入" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1003 w=610 h=55/></c>
<c id="p13_tk8" v="降版" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1058 w=150 h=55/></c>
<c id="p13_tv8" v="upgrade vendor_kit@&lt;舊版&gt;：目標引擎（以其 image LABEL 的 P／schema 判）能無損讀現有檔才做（做 = 重產薄殼 → 1 + 6-2），否則改檔前拒絕 3 + 6-10；dev vendor_kit -i &lt;舊 image&gt; 允許但禁止重產 tracked 薄殼" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1058 w=610 h=55/></c>
<c id="p13_tk9" v="驗收（§7.4）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1113 w=150 h=55/></c>
<c id="p13_tv9" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture 驅動候選（線性，非兩兩相乘）；連升 r_i → r_j → C；floor 直接跳升；降版；&lt; floor 用唯一 synthetic；舊引擎讀新檔 3 零寫入；已釋出 image／Release 資產／fixture 永不刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1113 w=610 h=55/></c>
<c id="p13_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1168 w=150 h=71/></c>
<c id="p13_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1168 w=610 h=71/></c>
</diagram>
<diagram id="v1p14" name="結束碼決策表 v2"><c id="title" v="結束碼決策表 v2：動詞 × 情況 → 0／1／2／3（interface_spec §1.2、§2、§7.1；Q23／Q27）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q23、Q27、v2.6-15、v2.7-4／-8、interface_spec §1.2 每動詞結束碼欄、§2 結束碼總表、§7.1）：3 = 版本／協定／schema 不合且零寫入（無任何例外）；既定回 1 的情境維持 1；多工具做得完的做完再回最需要處理的碼；CI 動作：0 過、1 修、2 解衝突、3 換版本；顏色：0 綠、需要人動作 1／2／3 橙（含 update 無憑證 6-3）、失敗 1 紅。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1080 y=12 w=520 h=92/></c>
<c id="te_h0" v="動詞" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=120 w=170 h=30/></c>
<c id="te_h1" v="0 成功（綠）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=210 y=120 w=250 h=30/></c>
<c id="te_h2" v="1 需要人動作（橙：印指令）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=460 y=120 w=420 h=30/></c>
<c id="te_h3" v="1 失敗（紅）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=880 y=120 w=260 h=30/></c>
<c id="te_h4" v="2 衝突／有新版（橙）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1140 y=120 w=240 h=30/></c>
<c id="te_h5" v="3 版本不合（橙；零寫入）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1380 y=120 w=210 h=30/></c>
<c id="te_r0c0" v="bootstrap.sh" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=150 w=170 h=42/></c>
<c id="te_r0c1" v="install 與每個 -t 的 add 都完成" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=150 w=250 h=42/></c>
<c id="te_r0c2" v="非 git repo（6-16）；just &lt; 1.33.0（6-23）；需問但無 tty（6-4）；任一 add 失敗（明列已完成／未完成）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=150 w=420 h=42/></c>
<c id="te_r0c3" v="pull 失敗／逾時（6-24／6-31）；install 失敗（第一次不留半成品）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=150 w=260 h=42/></c>
<c id="te_r0c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=150 w=240 h=42/></c>
<c id="te_r0c5" v="薄殼／引擎 &lt; floor（6-18）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=150 w=210 h=42/></c>
<c id="te_r1c0" v="install" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=192 w=170 h=57/></c>
<c id="te_r1c1" v="建立或修復完成；已含 import 行不再加；--no-justfile 只印指示；問後拒絕加行 → 不動、印指示" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=192 w=250 h=57/></c>
<c id="te_r1c2" v="非 git（6-16）；巢狀（6-35）；install &lt;repo&gt; 誤用（6-17）；薄殼被改（6-28，列差異不動）；無 tty 需問（6-4）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=192 w=420 h=57/></c>
<c id="te_r1c3" v="寫入失敗（第一次不留半成品）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=192 w=260 h=57/></c>
<c id="te_r1c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=192 w=240 h=57/></c>
<c id="te_r1c5" v="P &lt; floor（6-18）；檔 schema 高於支援（6-19）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=192 w=210 h=57/></c>
<c id="te_r2c0" v="uninstall" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=249 w=170 h=42/></c>
<c id="te_r2c1" v="完成（初始檔保留印清單；未知或被改的檔保留並回報）；dry-run 本機" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=249 w=250 h=42/></c>
<c id="te_r2c2" v="任一工具在 dev 覆寫中（先 undev）；CI 需改 tracked 檔；指紋不同（6-12）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=249 w=420 h=42/></c>
<c id="te_r2c3" v="任一工具 remove 失敗 → 中止、列已完成部分" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=249 w=260 h=42/></c>
<c id="te_r2c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=249 w=240 h=42/></c>
<c id="te_r2c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=249 w=210 h=42/></c>
<c id="te_r3c0" v="add &lt;repo&gt;[@&lt;tag&gt;]" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=291 w=170 h=57/></c>
<c id="te_r3c1" v="接入完成；已接入且完成 → 無變更；dry-run 本機" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=291 w=250 h=57/></c>
<c id="te_r3c2" v="@&lt;tag&gt; 與鎖定不同（改用 upgrade）；私有且無憑證又未指定 @&lt;tag&gt;（6-3）；dest 不合法／撞名；&lt;ns&gt; 撞名；CI 需改 tracked；指紋不同（6-12）；未完成交易恢復失敗（6-27）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=291 w=420 h=57/></c>
<c id="te_r3c3" v="pull 失敗／逾時；dist 含 symlink；寫入失敗（version.toml 一律未動）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=291 w=260 h=57/></c>
<c id="te_r3c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=291 w=240 h=57/></c>
<c id="te_r3c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=291 w=210 h=57/></c>
<c id="te_r4c0" v="remove &lt;repo&gt;" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=348 w=170 h=42/></c>
<c id="te_r4c1" v="完成（初始檔永不刪、印清單）；未接 → 提示" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=348 w=250 h=42/></c>
<c id="te_r4c2" v="dev 覆寫中（先 undev）；CI 需改 tracked；指紋不同" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=348 w=420 h=42/></c>
<c id="te_r4c3" v="寫入失敗（可恢復狀態）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=348 w=260 h=42/></c>
<c id="te_r4c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=348 w=240 h=42/></c>
<c id="te_r4c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=348 w=210 h=42/></c>
<c id="te_r5c0" v="update [&lt;repo&gt;]" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=390 w=170 h=42/></c>
<c id="te_r5c1" v="已列出（有新版也 0；末行 6-15）" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=390 w=250 h=42/></c>
<c id="te_r5c2" v="未完成交易（6-33）；任一目標查詢失敗（含無憑證 6-3：設 token 或 upgrade &lt;repo&gt;@&lt;tag&gt;；即使另有新版）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=390 w=420 h=42/></c>
<c id="te_r5c3" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=880 y=390 w=260 h=42/></c>
<c id="te_r5c4" v="--exit-code 且有新版" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1140 y=390 w=240 h=42/></c>
<c id="te_r5c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=390 w=210 h=42/></c>
<c id="te_r6c0" v="upgrade [&lt;repo&gt;[@&lt;tag&gt;]]" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=432 w=170 h=73/></c>
<c id="te_r6c1" v="完成；無新版；(1) 補齊待合併後停（6-14）；dry-run 本機" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=432 w=250 h=73/></c>
<c id="te_r6c2" v="無 baseline（先 add）；dev 覆寫中（先 undev）；CI 需改 tracked（6-5）；指紋不同；自身升級後「請 commit 並再跑原指令」（6-2；已改第一行是明列例外）；6-2b" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=432 w=420 h=73/></c>
<c id="te_r6c3" v="pull 失敗；git merge-file I/O 錯誤；寫入失敗（工具層 version.toml 不動）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=432 w=260 h=73/></c>
<c id="te_r6c4" v="合併衝突（留標記、baseline 仍推）；合併結果 TOML／just 解析失敗（留原檔、baseline 不推）；(0) 仍有衝突標記" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1140 y=432 w=240 h=73/></c>
<c id="te_r6c5" v="@&lt;舊版&gt; 無法無損讀（6-10）；6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=432 w=210 h=73/></c>
<c id="te_r7c0" v="dev &lt;repo&gt;／vendor_kit" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=505 w=170 h=57/></c>
<c id="te_r7c1" v="覆寫寫入 version.local.toml" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=505 w=250 h=57/></c>
<c id="te_r7c2" v="工具不在 version.toml；缺 &lt;dir&gt;/dist/init.toml；CI 拒絕；-p／-i 互斥用錯" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=505 w=420 h=57/></c>
<c id="te_r7c3" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=880 y=505 w=260 h=57/></c>
<c id="te_r7c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=505 w=240 h=57/></c>
<c id="te_r7c5" v="-i 舊引擎 P／schema 低於薄殼首行且要重產 tracked 薄殼 → 拒絕" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=505 w=210 h=57/></c>
<c id="te_r8c0" v="undev &lt;repo&gt;／vendor_kit" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=562 w=170 h=42/></c>
<c id="te_r8c1" v="完成；未啟用 → 提示" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=562 w=250 h=42/></c>
<c id="te_r8c2" v="指紋不同" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=562 w=420 h=42/></c>
<c id="te_r8c3" v="重新 materialize 失敗（保留可恢復狀態）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=562 w=260 h=42/></c>
<c id="te_r8c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=562 w=240 h=42/></c>
<c id="te_r8c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=562 w=210 h=42/></c>
<c id="te_r9c0" v="sync [&lt;repo&gt;] [--verify]" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=604 w=170 h=42/></c>
<c id="te_r9c1" v="快路徑（不起容器）；materialize／verify 完成" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=604 w=250 h=42/></c>
<c id="te_r9c2" v="薄殼不符（6-1，不重寫）；未完成接入（6-13）；CI 下 baseline 落後（6-5）；CI 下任何 local 覆寫；未完成交易（6-33）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=604 w=420 h=42/></c>
<c id="te_r9c3" v="pull 失敗／逾時；verify 失敗且重裝失敗" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=604 w=260 h=42/></c>
<c id="te_r9c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=604 w=240 h=42/></c>
<c id="te_r9c5" v="6-18／6-19" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=604 w=210 h=42/></c>
<c id="te_r10c0" v="prune" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=646 w=170 h=42/></c>
<c id="te_r10c1" v="完成（印刪了什麼、保留什麼；活躍 .tmp.* 只列出）；dry-run 零刪除" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=646 w=250 h=42/></c>
<c id="te_r10c2" v="vk-resolve 不合（6-30）；無 tty 需問（6-4）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=646 w=420 h=42/></c>
<c id="te_r10c3" v="任一 docker rm／image rm／network rm／volume rm 失敗（摘要全列）" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=646 w=260 h=42/></c>
<c id="te_r10c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=646 w=240 h=42/></c>
<c id="te_r10c5" v="6-18" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=646 w=210 h=42/></c>
<c id="te_r11c0" v="help／h" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=688 w=170 h=30/></c>
<c id="te_r11c1" v="永遠 0（不觸網、不安裝）" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=688 w=250 h=30/></c>
<c id="te_r11c2" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=460 y=688 w=420 h=30/></c>
<c id="te_r11c3" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=880 y=688 w=260 h=30/></c>
<c id="te_r11c4" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1140 y=688 w=240 h=30/></c>
<c id="te_r11c5" v="—" s="sc=#999999;fs=12;fc=#ffffff"><g x=1380 y=688 w=210 h=30/></c>
<c id="te_r12c0" v="ci/check.sh" s="sc=#999999;fs=12;fc=#ffffff;fst=1"><g x=40 y=718 w=170 h=42/></c>
<c id="te_r12c1" v="⓪～⑤ 全過" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=210 y=718 w=250 h=42/></c>
<c id="te_r12c2" v="⓪ version.local.toml 被 track；① sync 的 1；② verify 印記不符；③ upgrade --dry-run 需改 tracked 檔（印清單）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=460 y=718 w=420 h=42/></c>
<c id="te_r12c3" v="④⑤ 工具／專案測試原碼傳出" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=718 w=260 h=42/></c>
<c id="te_r12c4" v="③ 仍有衝突標記" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1140 y=718 w=240 h=42/></c>
<c id="te_r12c5" v="① 的 3" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=1380 y=718 w=210 h=42/></c>
<c id="k14a" v="多工具彙總（已定，Q27）：不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）→ 做得完的做完 → 最後回最需要處理的碼：失敗 1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=40 y=784 w=500 h=57/></c>
<c id="k14b" v="結束碼 3 邊界（已定，Q23、v2.7-4）：版本／協定／schema 不合，須先升級或退回才能繼續；回 3 時零寫入、無任何例外（救援路徑亦同）；新舊以 P／schema 比較，不用版本字串；floor 檢查先於任何上網；網路／認證／不存在 → 1，不得偽裝成 3；既定回 1（印記不符、薄殼被改、自身升級完成要重跑）維持 1" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=560 y=784 w=520 h=73/></c>
<c id="k14c" v="CI 對應動作（已定）：0 → 過（merge）；1 → 修（照訊息裡的指令：本機 upgrade &lt;repo&gt; -y 後 commit 並 push／add／undev／git checkout 還原薄殼／加 -y／設 token）；2 → 解衝突（編輯檔案去掉 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記 → 重跑 upgrade 直到乾淨）；3 → 換版本（upgrade vendor_kit／git revert／bootstrap.sh 重建）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=1100 y=784 w=490 h=88/></c>
<c id="k14d" v="圖上顏色對應（v2.6-15、v2.7-8）：0 = 綠橢圓；1 需要人動作（印指令：請先 undev／請先 add／請先 git init／請重跑／請 upgrade vendor_kit／請設 token 或指定 @&lt;tag&gt;）= 橙橢圓；2 = 橙；3 = 橙；1 失敗（拉不到、寫入失敗、驗證失敗）= 紅橢圓" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=888 w=500 h=73/></c>
<c id="k14e" v="check.sh 整體結束碼 = 第一個失敗步驟的碼：⓪ local 被 track → 1；① sync 1／3；② verify 1；③ upgrade --dry-run：需改 tracked → 1、仍有衝突標記 → 2；④⑤ 原碼傳出（1／2／3 語意只對 vendor_kit 自身步驟成立）；⓪–⑤ 六步、一關過才下一關" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=560 y=888 w=520 h=57/></c>
<c id="k14f" v="「—」= 該動詞沒有這個結束碼；表內 6-N = interface_spec §6 逐字訊息編號；dry-run 在本機一律 0（CI 為真且需改 tracked 檔 → 1）；EOF／Ctrl-C 中止 apply → 1、不套用、不記 declined；sync --verify（F5 已定）= 每檔 sha256 全驗，結束碼同 sync" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1100 y=888 w=490 h=73/></c>
<c id="p14_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=991 w=200 h=60/></c>
<c id="p14_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=991 w=140 h=64/></c>
<c id="p14_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=999 w=140 h=44/></c>
<c id="p14_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=993 w=190 h=56/></c>
<c id="p14_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=993 w=210 h=56/></c>
<c id="p14_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1001 w=88 h=40/></c>
<c id="p14_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1001 w=170 h=40/></c>
<c id="p14_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=991 w=280 h=60/></c>
<c id="p14_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1059 w=120 h=36/></c>
<c id="p14_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1059 w=150 h=36/></c>
<c id="p14_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=350 y=1059 w=170 h=36/></c>
<c id="p14_lgx_c0" v="綠格：結束碼 0" s="sc=#999999;fs=12;fc=#d5e8d4"><g x=540 y=1059 w=110 h=36/></c>
<c id="p14_lgx_cx" v="橙格：需要人動作（1／2／3）" s="sc=#999999;fs=12;fc=#ffe6cc"><g x=670 y=1059 w=190 h=36/></c>
<c id="p14_lgx_c1" v="紅格：失敗 1" s="sc=#999999;fs=12;fc=#f8cecc"><g x=880 y=1059 w=110 h=36/></c>
<c id="p14_lgx_cell" v="白格：表格內容" s="sc=#999999;fs=12;fc=#ffffff"><g x=1010 y=1059 w=110 h=36/></c>
<c id="p14_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1097 w=200 h=28/></c>
<c id="p14_tk0" v="結束碼 0" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1131 w=150 h=40/></c>
<c id="p14_tv0" v="成功（含 warn）：add 已接入完成、remove 未接、undev 未啟用、upgrade vendor_kit 無新版且薄殼相符、update 已列出（有新版也 0）、dry-run 本機皆 0 + 提示" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1131 w=610 h=40/></c>
<c id="p14_tk1" v="結束碼 1" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1171 w=150 h=55/></c>
<c id="p14_tv1" v="一般失敗或需使用者處理／重跑：工具層動詞回 1 時 version.toml 不動；例外：自身升級已改第一行後回 1、upgrade vendor_kit 重產薄殼後回 1（6-2）；圖上：印指令要人動作 = 橙、拉不到／寫入失敗／驗證失敗 = 紅" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1171 w=610 h=55/></c>
<c id="p14_tk2" v="結束碼 2" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1226 w=150 h=55/></c>
<c id="p14_tv2" v="合併衝突（留 &lt;&lt;&lt;&lt;&lt;&lt;&lt; vendor_kit:baseline 標記、印檔名、baseline 仍推到新版；解完重跑直到乾淨）；合併結果 TOML／just 解析失敗 → 2 留原檔、dest 入 conflicts、baseline 不推；update --exit-code 有新版 → 2" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1226 w=610 h=55/></c>
<c id="p14_tk3" v="結束碼 3（Q23）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1281 w=150 h=55/></c>
<c id="p14_tv3" v="現有薄殼／檔案／引擎的組合需先升級或退回：(a) P &lt; floor 6-18 (b) schema 高於支援 6-19 (c) 降版無法無損讀 6-10 (d) dev -i 舊引擎要重產薄殼 (e) 舊薄殼跑新 major 一般動詞 6-36；零寫入、無任何例外；以 P／schema 比" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1281 w=610 h=55/></c>
<c id="p14_tk4" v="多工具彙總（Q27）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1336 w=150 h=40/></c>
<c id="p14_tv4" v="不帶 repo 的動詞先完整預檢（任一預檢失敗才整體不動）、做得完的做完，最後回最需要處理的碼：1 &gt; 衝突 2 &gt; 有新版 2 &gt; 0；update 同時遇 1 與 2 → 1；訊息全列；舊薄殼對未知碼原樣傳出、不吞" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1336 w=610 h=40/></c>
<c id="p14_tk5" v="check.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1131 w=150 h=55/></c>
<c id="p14_tv5" v=".vendor_kit/ci/check.sh：export CI=1 → ⓪ local 被 track → 1 → ① sync（frozen）→ ② verify → ③ upgrade --dry-run → ④ 工具測試 → ⑤ 專案測試；⓪–⑤ 六步、一關過才下一關；整體結束碼 = 第一個失敗步驟的碼（④⑤ 原碼傳出）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1131 w=610 h=55/></c>
<c id="p14_tk6" v="frozen（CI 為真）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1186 w=150 h=40/></c>
<c id="p14_tv6" v="CI 非空且不為 0／false → 不寫 tracked 檔、不查最新版；需改 tracked 檔 → 1 印清單（與 -y 無關）；6-6～6-8 提醒不紅燈；update 不受限" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1186 w=610 h=40/></c>
<c id="p14_tk7" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1226 w=150 h=55/></c>
<c id="p14_tv7" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1226 w=610 h=55/></c>
<c id="p14_tk8" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1281 w=150 h=71/></c>
<c id="p14_tv8" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1281 w=610 h=71/></c>
</diagram>
<diagram id="v1p15" name="流程 v2：vendor_kit release（1）build 與驗收"><c id="title" v="流程 v2：vendor_kit release（1）── build → release-test → 驗收（#26／#27、§7.4）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=116/></c>
<c id="hdr0" v="維護者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=136 w=220 h=28/></c>
<c id="hdr1" v="GitHub Actions" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=136 w=560 h=28/></c>
<c id="hdr2" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=860 y=136 w=320 h=28/></c>
<c id="hdr3" v="Release 資產" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1200 y=136 w=390 h=28/></c>
<c id="bR" v="release vN（1）：兩平台各自 build → release-test → 驗收 → 兩平台一致檢查 → 全部通過？否 → 候選作廢；是 → 接（2）頁推 image 與資產" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=180 w=1590 h=991/></c>
<c id="bR_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bR"><g x=1546 y=5 w=30 h=20/></c>
<c id="v0" v="推候選（候選 tag／workflow_dispatch 指定 vN）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bR"><g x=20 y=36 w=220 h=80/></c>
<c id="v1" v="workflow 觸發：amd64 job + arm64 job（原生 runner）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=56 w=560 h=40/></c>
<c id="v2" v="build（#26）：兩 runner 各自單平台 buildx build（同一份 Dockerfile；LABEL =1／.protocol／.schema）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=136 w=560 h=42/></c>
<c id="v3a" v="release-test（各平台原生）：env-test" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=199 w=560 h=40/></c>
<c id="v3n" v="release-test 矩陣：rootless docker、Podman；just 1.33.0 + latest；不用 QEMU 當閘門" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bR"><g x=1180 y=198 w=390 h=42/></c>
<c id="v3b" v="release-test：完整主機流程 install → add → upgrade → dev/undev → remove → prune → uninstall" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=260 w=560 h=42/></c>
<c id="v4a" v="驗收（§7.4-1）：floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=322 w=560 h=40/></c>
<c id="v4g" v="已釋出引擎 image r（floor 以來每一版；永不刪）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bR"><g x=840 y=322 w=320 h=40/></c>
<c id="v4r" v="已釋出 bootstrap.sh(r)（Release 資產；永不刪）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bR"><g x=1180 y=322 w=390 h=40/></c>
<c id="v4b" v="fixture 的 version.toml 第一行改成候選 C" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=382 w=560 h=40/></c>
<c id="v4c" v="跑 §7.4-1 序列：sync 1+6-1 → upgrade vendor_kit 1+6-2 → sync 0 → 第二次 upgrade vendor_kit 0" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=442 w=560 h=42/></c>
<c id="v5a" v="驗收（§7.4-4～8）：連升 r_i → r_j → C；floor 直接跳升；降版；&lt; floor synthetic；舊引擎讀新檔 3" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=504 w=560 h=42/></c>
<c id="v5b" v="驗收（§7.4-3、9～13）：升級後 == 全新安裝；fresh clone 無 gen；frozen sync；中斷重跑；TOML 異常" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=566 w=560 h=42/></c>
<c id="v5c" v="驗收（§7.4-16／17）：離線包 amd64／arm64、斷網可用；禁止由候選樹複製 fixture、禁 stub 引擎" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=628 w=560 h=42/></c>
<c id="v6a" v="兩平台一致檢查：工具 dist 逐檔位元組一致" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=706 w=560 h=40/></c>
<c id="v6n" v="已定（decisions/multiarch）：不能靠單一 bake --push 帶測試就宣稱「失敗就不發佈」；分架構各自 build／test，綠了才 push-by-digest，最後由單一 job 合成 index；兩 runner 各自 push 同 tag 會互相覆蓋" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bR"><g x=1180 y=690 w=390 h=73/></c>
<c id="v6b" v="兩平台一致檢查：引擎 image 兩平台 LABEL（protocol／schema）一致" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR"><g x=260 y=783 w=560 h=40/></c>
<c id="v7x" v="否 → 失敗：不推 image、不發 Release、不進正式 tag（候選作廢）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bR"><g x=20 y=843 w=220 h=80/></c>
<c id="v7" v="全部通過？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bR"><g x=260 y=858 w=220 h=50/></c>
<c id="v7z" v="是 ↓ 續「release（2）」頁：push-by-digest → index → bootstrap.sh／tar／.digest → Release" s="text;fs=12;sc=none;fc=none;fst=1" parent="bR"><g x=260 y=943 w=560 h=42/></c>
<c id="ve0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v0" target="v1"></c>
<c id="ve1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v1" target="v2"></c>
<c id="ve2" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v2" target="v3a"></c>
<c id="ve2n" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v3a" target="v3n"></c>
<c id="ve2b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v3a" target="v3b"></c>
<c id="ve3" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v3b" target="v4a"></c>
<c id="ve4" v="拉" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v4a" target="v4g"></c>
<c id="ve4r" v="取" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v4g" target="v4r"></c>
<c id="ve4b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v4a" target="v4b"></c>
<c id="ve4c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v4b" target="v4c"></c>
<c id="ve5" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v4c" target="v5a"></c>
<c id="ve5b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v5a" target="v5b"></c>
<c id="ve5c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v5b" target="v5c"></c>
<c id="ve6" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v5c" target="v6a"></c>
<c id="ve6n" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v6a" target="v6n"></c>
<c id="ve6b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v6a" target="v6b"></c>
<c id="ve7" s="fs=12;exitX=0.196;exitY=1;entryX=0.5;entryY=0" edge="1" source="v6b" target="v7"></c>
<c id="ve8" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="v7" target="v7x"></c>
<c id="ve9" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.196;entryY=0" edge="1" source="v7" target="v7z"><g x=-0.6/></c>
<c id="p15_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1187 w=200 h=60/></c>
<c id="p15_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1187 w=140 h=64/></c>
<c id="p15_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1195 w=140 h=44/></c>
<c id="p15_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1189 w=190 h=56/></c>
<c id="p15_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1189 w=210 h=56/></c>
<c id="p15_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1197 w=88 h=40/></c>
<c id="p15_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1197 w=170 h=40/></c>
<c id="p15_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1187 w=280 h=60/></c>
<c id="p15_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1255 w=120 h=36/></c>
<c id="p15_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1255 w=150 h=36/></c>
<c id="p15_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=350 y=1255 w=170 h=36/></c>
<c id="p15_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=540 y=1255 w=170 h=36/></c>
<c id="p15_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1293 w=200 h=28/></c>
<c id="p15_tk0" v="release" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1327 w=150 h=40/></c>
<c id="p15_tv0" v="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1327 w=610 h=40/></c>
<c id="p15_tk1" v="多架構 image／index digest（#26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1367 w=150 h=71/></c>
<c id="p15_tv1" v="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1367 w=610 h=71/></c>
<c id="p15_tk2" v="release-test" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1438 w=150 h=55/></c>
<c id="p15_tv2" v="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1438 w=610 h=55/></c>
<c id="p15_tk3" v="env-test" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1493 w=150 h=40/></c>
<c id="p15_tv3" v="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1493 w=610 h=40/></c>
<c id="p15_tk4" v="驗收（§7.4）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1533 w=150 h=71/></c>
<c id="p15_tv4" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1533 w=610 h=71/></c>
<c id="p15_tk5" v="兩平台一致檢查" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1604 w=150 h=40/></c>
<c id="p15_tv5" v="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1604 w=610 h=40/></c>
<c id="p15_tk6" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1327 w=150 h=71/></c>
<c id="p15_tv6" v="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&lt;org&gt;/vendor_kit:vN@sha256:&lt;index digest&gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &lt;tar&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1327 w=610 h=71/></c>
<c id="p15_tk7" v="tar／.digest／SHA256SUMS（#27、Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1398 w=150 h=55/></c>
<c id="p15_tv7" v="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&lt;hex64&gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1398 w=610 h=55/></c>
<c id="p15_tk8" v="LABEL" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1453 w=150 h=40/></c>
<c id="p15_tv8" v="引擎 image build 時帶 io.github.&lt;org&gt;.vendor_kit=1、….protocol=&lt;floor_P&gt;-&lt;current_P&gt;、….schema=&lt;N&gt;（啟動器不起容器即可判 floor）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1453 w=610 h=40/></c>
<c id="p15_tk9" v="SemVer" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1493 w=150 h=40/></c>
<c id="p15_tv9" v="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1493 w=610 h=40/></c>
<c id="p15_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1533 w=150 h=71/></c>
<c id="p15_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1533 w=610 h=71/></c>
</diagram>
<diagram id="v1p15c" name="流程 v2：vendor_kit release（2）推 image 與資產"><c id="title" v="流程 v2：vendor_kit release（2）── 推 image → 資產 → Release（#26／#27、Q26）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（#26 多架構、#27 bootstrap.sh 交付、Q26 .digest、v2.7-1、interface_spec §4.7 image 命名／label、§7.4 驗收、§8-12；decisions/multiarch 最終建議）：兩架構原生 runner 分建分測、綠了才 push-by-digest 再由單一 job 合成 index；驗收由已釋出版驅動候選；bootstrap.sh 內嵌完整 ref；各平台 tar + .digest + SHA256SUMS 進 Release；local_bootstrap.sh 只是便利包裝（非契約）；失敗不進正式 tag；已釋出物永不刪。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=116/></c>
<c id="hdr0" v="維護者" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=136 w=220 h=28/></c>
<c id="hdr1" v="GitHub Actions" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=280 y=136 w=560 h=28/></c>
<c id="hdr2" v="GHCR" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=860 y=136 w=320 h=28/></c>
<c id="hdr3" v="Release 資產" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1200 y=136 w=390 h=28/></c>
<c id="bR2" v="release vN（2）：全過才 push-by-digest → 單一 job 合成 index → 產 bootstrap.sh → tar + .digest → 離線包 → SHA256SUMS → 打正式 tag → 發布 Release" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=180 w=1590 h=870/></c>
<c id="bR2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bR2"><g x=1546 y=5 w=30 h=20/></c>
<c id="v8e" v="來自「release（1）」頁：build／release-test／驗收／兩平台一致全部通過" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bR2"><g x=260 y=36 w=560 h=58/></c>
<c id="v8a" v="兩平台各自 push-by-digest（不打 tag；tag vN 不覆蓋）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=115 w=560 h=40/></c>
<c id="v8ag" v="ghcr.io/&lt;org&gt;/vendor_kit@sha256:&lt;amd64 digest&gt;、@sha256:&lt;arm64 digest&gt;" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bR2"><g x=840 y=114 w=320 h=42/></c>
<c id="v8b" v="單一 job：docker buildx imagetools create -t vendor_kit:vN &lt;兩個 digest&gt; → 合成 index" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=176 w=560 h=42/></c>
<c id="v8bg" v="ghcr.io/&lt;org&gt;/vendor_kit:vN@sha256:&lt;index digest&gt;（多架構；公開）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bR2"><g x=840 y=176 w=320 h=42/></c>
<c id="v8c" v="imagetools inspect 斷言：index 含 linux/amd64 + linux/arm64" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=238 w=560 h=40/></c>
<c id="v9" v="產 bootstrap.sh：內嵌完整引擎 ref（tag@index digest）；檔名固定" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=299 w=560 h=40/></c>
<c id="v9r" v="bootstrap.sh（releases/download/vN/；latest 連結指向最新）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bR2"><g x=1180 y=298 w=390 h=42/></c>
<c id="v10a" v="docker save 各平台 image → vendor_kit-vN-amd64.tar、vendor_kit-vN-arm64.tar" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=360 w=560 h=40/></c>
<c id="v10ar" v="vendor_kit-vN-&lt;平台&gt;.tar（各平台一個）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bR2"><g x=1180 y=360 w=390 h=40/></c>
<c id="v10b" v="寫同名 .digest 旁檔（一行 sha256:&lt;hex64&gt; = index digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=420 w=560 h=40/></c>
<c id="v10br" v="vendor_kit-vN-&lt;平台&gt;.tar.digest" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bR2"><g x=1180 y=420 w=390 h=40/></c>
<c id="v10c" v="組離線包 vendor_kit-vN-local.tar.gz" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=531 w=560 h=40/></c>
<c id="v10cr" v="離線包內容" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bR2"><g x=1180 y=480 w=390 h=142/></c>
<c id="v10cr_0" v="bootstrap.sh（契約入口：bootstrap.sh --local &lt;tar&gt;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="v10cr"><g x=8 y=26 w=374 h=26/></c>
<c id="v10cr_1" v="各平台 tar + .tar.digest" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="v10cr"><g x=8 y=58 w=374 h=26/></c>
<c id="v10cr_2" v="local_bootstrap.sh：便利包裝（非契約；偵測架構、挑 tar、exec bootstrap.sh --local）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="v10cr"><g x=8 y=90 w=374 h=42/></c>
<c id="v10d" v="寫 SHA256SUMS（列所有資產）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=642 w=560 h=40/></c>
<c id="v10dr" v="SHA256SUMS" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bR2"><g x=1180 y=642 w=390 h=40/></c>
<c id="v11a" v="打正式 tag vN（指向候選 commit）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=702 w=560 h=40/></c>
<c id="v11b" v="發布 Release vN：附 bootstrap.sh、tar、.digest、離線包、SHA256SUMS；release notes 含 index digest 與不用腳本的替代 docker run 指令" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bR2"><g x=260 y=762 w=560 h=42/></c>
<c id="v11n" v="已釋出 image／Release 資產／fixture 永不刪；下游 Renovate 會看到新 tag@digest" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12" parent="bR2"><g x=1180 y=762 w=390 h=42/></c>
<c id="v12" v="0：Release vN 發布" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bR2"><g x=20 y=824 w=220 h=40/></c>
<c id="ve10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v8e" target="v8a"></c>
<c id="ve10g" v="推" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v8a" target="v8ag"></c>
<c id="ve11" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v8a" target="v8b"></c>
<c id="ve11g" v="建" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v8b" target="v8bg"></c>
<c id="ve11c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v8b" target="v8c"></c>
<c id="ve12" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v8c" target="v9"></c>
<c id="ve12r" v="產" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v9" target="v9r"></c>
<c id="ve13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v9" target="v10a"></c>
<c id="ve13r" v="產" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v10a" target="v10ar"></c>
<c id="ve13b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v10a" target="v10b"></c>
<c id="ve13br" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v10b" target="v10br"></c>
<c id="ve13c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v10b" target="v10c"></c>
<c id="ve13cr" v="組" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v10c" target="v10cr"></c>
<c id="ve13d" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v10c" target="v10d"></c>
<c id="ve13dr" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v10d" target="v10dr"></c>
<c id="ve14" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v10d" target="v11a"></c>
<c id="ve15" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="v11a" target="v11b"></c>
<c id="ve15n" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="v11b" target="v11n"></c>
<c id="ve16" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="v11b" target="v12"><g x=-0.88 pts=560,1024/></c>
<c id="p15c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1066 w=200 h=60/></c>
<c id="p15c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1066 w=140 h=64/></c>
<c id="p15c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1074 w=140 h=44/></c>
<c id="p15c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1068 w=190 h=56/></c>
<c id="p15c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1068 w=210 h=56/></c>
<c id="p15c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1076 w=88 h=40/></c>
<c id="p15c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1076 w=170 h=40/></c>
<c id="p15c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1066 w=280 h=60/></c>
<c id="p15c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1134 w=120 h=36/></c>
<c id="p15c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=180 y=1134 w=170 h=36/></c>
<c id="p15c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=370 y=1134 w=170 h=36/></c>
<c id="p15c_lgx_entry" v="虛線橢圓：來自其他頁" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=560 y=1134 w=200 h=36/></c>
<c id="p15c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1172 w=200 h=28/></c>
<c id="p15c_tk0" v="release" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1206 w=150 h=40/></c>
<c id="p15c_tv0" v="vendor_kit 引擎的一次發行：候選 → 兩平台各自 build → release-test → 驗收 → 推 image → 產資產 → 正式 tag vN；任一關失敗就不成為正式版；已釋出 image／Release 資產／fixture 永不刪" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1206 w=610 h=40/></c>
<c id="p15c_tk1" v="多架構 image／index digest（#26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1246 w=150 h=71/></c>
<c id="p15c_tv1" v="兩個 runner（amd64、arm64 原生）各自單平台 build + release-test，綠了才 push-by-digest，由單一 job 以 docker buildx imagetools create 合成 index（不是同一次 buildx --platform 多平台；兩 runner 各自 push 同 tag 會互相覆蓋）；index 的 sha256 = version.toml 鎖定用的 digest" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1246 w=610 h=71/></c>
<c id="p15c_tk2" v="release-test" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1317 w=150 h=55/></c>
<c id="p15c_tv2" v="amd64 與 arm64 原生 runner（不用 QEMU 當閘門）各跑 env-test + 一條完整主機流程（install → add → upgrade → dev/undev → remove → prune → uninstall）；rootless docker 與 Podman 進矩陣；just 1.33.0 + latest" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1317 w=610 h=55/></c>
<c id="p15c_tk3" v="env-test" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1372 w=150 h=40/></c>
<c id="p15c_tv3" v="release-test 的第一段：在乾淨 runner 驗主機需求（docker ≥ 19.03、just ≥ 1.33.0、POSIX sh、git）與引擎 image LABEL 齊全；過了才跑完整主機流程" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1372 w=610 h=40/></c>
<c id="p15c_tk4" v="驗收（§7.4）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1412 w=150 h=71/></c>
<c id="p15c_tv4" v="floor 以來每個已釋出 bootstrap.sh(r) + 引擎 image r 建 fixture → 候選 C：sync（1 + 6-1）→ upgrade vendor_kit（1 + 6-2）→ sync 0 → 第二次 upgrade vendor_kit 0；連升；floor 跳升；降版；&lt; floor synthetic；fresh clone 無 gen；frozen sync；中斷重跑；升級後 == 全新安裝；離線包 amd64／arm64；禁止由候選樹複製 fixture、禁 stub 引擎" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1412 w=610 h=71/></c>
<c id="p15c_tk5" v="兩平台一致檢查" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1483 w=150 h=40/></c>
<c id="p15c_tv5" v="工具 dist：兩平台逐檔位元組一致（路徑、型別、hash、權限、禁 symlink）；引擎 image：兩平台 LABEL（….protocol、….schema）一致；index inspect 斷言含 linux/amd64 與 linux/arm64" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1483 w=610 h=40/></c>
<c id="p15c_tk6" v="bootstrap.sh" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1206 w=150 h=71/></c>
<c id="p15c_tv6" v="release 附的 POSIX sh 薄層，內嵌所屬引擎的完整 ref（ghcr.io/&lt;org&gt;/vendor_kit:vN@sha256:&lt;index digest&gt;）；檔名固定：releases/download/vN/bootstrap.sh，README 連 releases/latest/download/bootstrap.sh；離線契約入口 = bootstrap.sh --local &lt;tar&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1206 w=610 h=71/></c>
<c id="p15c_tk7" v="tar／.digest／SHA256SUMS（#27、Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1277 w=150 h=55/></c>
<c id="p15c_tv7" v="各平台 docker save 的 tar 旁附同名 .digest 旁檔（一行 sha256:&lt;hex64&gt; = 正式 index digest）；SHA256SUMS 列所有資產；離線包 vendor_kit-vN-local.tar.gz 含 bootstrap.sh、各平台 tar + .digest，另附 local_bootstrap.sh 便利包裝（非契約，v2.7-1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1277 w=610 h=55/></c>
<c id="p15c_tk8" v="LABEL" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1332 w=150 h=40/></c>
<c id="p15c_tv8" v="引擎 image build 時帶 io.github.&lt;org&gt;.vendor_kit=1、….protocol=&lt;floor_P&gt;-&lt;current_P&gt;、….schema=&lt;N&gt;（啟動器不起容器即可判 floor）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1332 w=610 h=40/></c>
<c id="p15c_tk9" v="SemVer" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1372 w=150 h=40/></c>
<c id="p15c_tv9" v="major = 提高 floor 或需要使用者手動步驟；minor = 新功能（含 P+1、新增欄位）；patch = 修正；Renovate preset 建議 major 分開 PR" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1372 w=610 h=40/></c>
<c id="p15c_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1412 w=150 h=71/></c>
<c id="p15c_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1412 w=610 h=71/></c>
</diagram>
<diagram id="v1p16" name="流程 v2：離線包（1）bootstrap.sh --local"><c id="title" v="流程 v2：離線包（1）── bootstrap.sh --local &lt;引擎 tar&gt; → load → install（#27、Q26、§4.8）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &lt;引擎 tar&gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &lt;repo&gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &lt;repo&gt; --local &lt;工具 tar&gt;；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=147/></c>
<c id="hdr0" v="使用者（離線機）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=167 w=230 h=28/></c>
<c id="hdr1" v="bootstrap.sh（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=290 y=167 w=400 h=28/></c>
<c id="hdr2" v="docker daemon" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=710 y=167 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=167 w=320 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1310 y=167 w=280 h=28/></c>
<c id="bO1" v="離線接入（1）只涉及引擎：離線包 →（可選 local_bootstrap.sh 挑 tar）→ bootstrap.sh --local &lt;引擎 tar&gt;（契約入口；不帶 -t）→ 判別值三分支 → 前置檢查 → docker load → .digest ↔ image ID → install → version.local.toml" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=211 w=1590 h=1632/></c>
<c id="bO1_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bO1"><g x=1546 y=5 w=30 h=20/></c>
<c id="o0" v="有網路的機器下載 vendor_kit-vN-local.tar.gz（SHA256SUMS 驗）→ 帶到離線機" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bO1"><g x=-9 y=36 w=288 h=102/></c>
<c id="o1" v="解開：bootstrap.sh、各平台引擎 tar + .tar.digest（另附 local_bootstrap.sh）；不含工具 tar" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=20 y=158 w=230 h=73/></c>
<c id="o1w" v="【便利包裝，非契約】（可選）sh local_bootstrap.sh [-y] 做三步：" s="text;fs=12;sc=none;fc=none;fst=1" parent="bO1"><g x=20 y=251 w=230 h=57/></c>
<c id="o1a" v="docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=20 y=328 w=230 h=57/></c>
<c id="o1b" v="挑該平台的引擎 tar（vendor_kit-vN-&lt;arch&gt;.tar）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=20 y=405 w=230 h=42/></c>
<c id="o1c" v="exec ./bootstrap.sh --local &lt;tar&gt; &quot;$@&quot;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=20 y=467 w=230 h=42/></c>
<c id="o2" v="sh bootstrap.sh --local &lt;引擎 tar&gt; [-y]（契約入口；-t &lt;repo&gt; 走 registry 需網路，離線機不帶）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=20 y=552 w=230 h=57/></c>
<c id="o3" v="--local 值含 / 或以 .tar 結尾？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=540 w=300 h=81/></c>
<c id="o3t" v="否 → 視為 image tag：不 docker load、不讀 .digest；本機須已有該 image（inspect 無 → 1）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=520 y=653 w=150 h=88/></c>
<c id="o3n" v="已定（B1；grilling 2026-09-19 末條、v2.7-2、v2.8-4）三分支：值含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）→ docker load；其餘 → image tag；既存檔且可解讀為 tag → 1 + 6-37 消歧（請寫 ./&lt;v&gt; 或完整 ref）；不另加前綴語法" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bO1"><g x=1290 y=529 w=280 h=104/></c>
<c id="o3bx" v="否 → 1：檔案路徑必須存在" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bO1"><g x=20 y=668 w=230 h=58/></c>
<c id="o3b" v="該路徑的檔案存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=672 w=300 h=50/></c>
<c id="o3cx" v="是 → 1 + 6-37：既是存在的檔案也可解讀為 image tag（請寫 ./&lt;v&gt; 或完整 ref）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bO1"><g x=20 y=761 w=230 h=102/></c>
<c id="o3c" v="值同時可解讀為 image tag？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=772 w=300 h=81/></c>
<c id="o4x" v="否 → 1：同名 .tar.digest 旁檔缺" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bO1"><g x=20 y=894 w=230 h=58/></c>
<c id="o4" v="同名 .tar.digest 存在？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=883 w=300 h=81/></c>
<c id="o5x" v="否 → 1 + 6-16：請先 git init" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bO1"><g x=20 y=984 w=230 h=58/></c>
<c id="o5" v="在 git repo 內？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=988 w=300 h=50/></c>
<c id="o6x" v="否 → 1 + 6-23：請裝 GitHub release 版 just" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12" parent="bO1"><g x=20 y=1062 w=230 h=80/></c>
<c id="o6" v="just ≥ 1.33.0？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO1"><g x=270 y=1077 w=300 h=50/></c>
<c id="o6c" v="docker load &lt; &lt;引擎 tar&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=270 y=1170 w=300 h=40/></c>
<c id="o6d" v="本機 image vendor_kit:vN（只有 tag、無 RepoDigests）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bO1"><g x=690 y=1162 w=170 h=57/></c>
<c id="o7a" v="讀 &lt;tar&gt;.digest → 正式 index digest" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=270 y=1239 w=300 h=40/></c>
<c id="o7b" v="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID（tag 形由此匯入）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=270 y=1299 w=400 h=42/></c>
<c id="o7bd" v="回 image ID（sha256:&lt;hex64&gt;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=690 y=1299 w=170 h=42/></c>
<c id="o8" v="docker run 本機 image install（本機有 → 不 pull）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=270 y=1412 w=400 h=40/></c>
<c id="o8e" v="install：建薄殼四檔、gen/.stamp、baseline/.gitkeep；version.toml 第一行 = 正式 ref@digest（來自 .digest）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bO1"><g x=950 y=1403 w=320 h=57/></c>
<c id="o8f" v="install 寫" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bO1"><g x=1290 y=1361 w=280 h=141/></c>
<c id="o8f_0" v="version.toml 第一行（正式 ref@sha256:&lt;index digest&gt;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="o8f"><g x=8 y=26 w=264 h=42/></c>
<c id="o8f_1" v="薄殼四檔、gen/.stamp、baseline/.gitkeep、根 justfile 一行、.dockerignore 三行" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="o8f"><g x=8 y=74 w=264 h=57/></c>
<c id="o9" v="install 成功後寫 version.local.toml：vendor_kit = &quot;vendor_kit:vN&quot; + vendor_kit_image_id（失敗清除）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1"><g x=270 y=1522 w=400 h=42/></c>
<c id="o9f" v="version.local.toml（不進 git）：本機 tag + image ID" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bO1"><g x=1290 y=1522 w=280 h=42/></c>
<c id="o9z" v="↓ 續「離線包（2）」頁：工具由使用者另備工具 tar，逐一 add &lt;repo&gt; --local &lt;工具 tar&gt;；之後斷網 sync" s="text;fs=12;sc=none;fc=none;fst=1" parent="bO1"><g x=270 y=1584 w=400 h=42/></c>
<c id="oe0" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o0" target="o1"></c>
<c id="oe1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o1" target="o1w"></c>
<c id="oe1a" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o1w" target="o1a"></c>
<c id="oe1b" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o1a" target="o1b"></c>
<c id="oe1c" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o1b" target="o1c"></c>
<c id="oe1w" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o1c" target="o2"></c>
<c id="oe2" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o2" target="o3"></c>
<c id="oe3t" v="否" s="fs=12;exitX=1;exitY=0.5;entryX=0.5;entryY=0" edge="1" source="o3" target="o3t"><g x=-0.74 pts=615,792/></c>
<c id="oe3b" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o3" target="o3b"><g x=-0.6/></c>
<c id="oe3bx" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="o3b" target="o3bx"></c>
<c id="oe3c" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o3b" target="o3c"><g x=-0.6/></c>
<c id="oe3cx" v="是" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="o3c" target="o3cx"></c>
<c id="oe4" v="否" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o3c" target="o4"><g x=-0.6/></c>
<c id="oe5" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="o4" target="o4x"></c>
<c id="oe6" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o4" target="o5"><g x=-0.6/></c>
<c id="oe6x" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="o5" target="o5x"></c>
<c id="oe6b" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o5" target="o6"><g x=-0.6/></c>
<c id="oe6bx" v="否" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="o6" target="o6x"></c>
<c id="oe7" v="是" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o6" target="o6c"><g x=-0.6/></c>
<c id="oe8" v="載" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o6c" target="o6d"></c>
<c id="oe9" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o6c" target="o7a"></c>
<c id="oe9b" s="fs=12;exitX=0.5;exitY=1;entryX=0.375;entryY=0" edge="1" source="o7a" target="o7b"></c>
<c id="oe9d" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o7b" target="o7bd"></c>
<c id="oe10" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o7b" target="o8"></c>
<c id="oe3tj" v="tag 形：直接 inspect" s="fs=12;exitX=1;exitY=0.5;entryX=0.9;entryY=0" edge="1" source="o3t" target="o7b"><g x=-0.85 pts=910,908;910,1500;650,1500/></c>
<c id="oe11" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o8" target="o8e"></c>
<c id="oe12" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o8e" target="o8f"></c>
<c id="oe13" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o8" target="o9"></c>
<c id="oe14" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o9" target="o9f"></c>
<c id="oe15" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o9" target="o9z"></c>
<c id="p16_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1859 w=200 h=60/></c>
<c id="p16_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1859 w=140 h=64/></c>
<c id="p16_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1867 w=140 h=44/></c>
<c id="p16_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1861 w=190 h=56/></c>
<c id="p16_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1861 w=210 h=56/></c>
<c id="p16_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1869 w=88 h=40/></c>
<c id="p16_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1869 w=170 h=40/></c>
<c id="p16_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1859 w=280 h=60/></c>
<c id="p16_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1927 w=120 h=36/></c>
<c id="p16_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1927 w=150 h=36/></c>
<c id="p16_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1927 w=190 h=36/></c>
<c id="p16_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1927 w=170 h=36/></c>
<c id="p16_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1927 w=170 h=36/></c>
<c id="p16_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1965 w=200 h=28/></c>
<c id="p16_tk0" v="離線包（#27、Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1999 w=150 h=55/></c>
<c id="p16_tv0" v="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1999 w=610 h=55/></c>
<c id="p16_tk1" v="bootstrap.sh --local（契約入口）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2054 w=150 h=71/></c>
<c id="p16_tv1" v="離線接入的契約入口 = bootstrap.sh --local &lt;引擎 tar&gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &lt;repo&gt; 仍是 add &lt;repo&gt;[@tag]，走 registry、需網路，離線機不帶 -t；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）；其餘 → image tag；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&lt;v&gt; 或完整 ref」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2054 w=610 h=71/></c>
<c id="p16_tk2" v="工具 tar（來源，v2.8-5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2125 w=150 h=71/></c>
<c id="p16_tv2" v="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &lt;repo&gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&lt;hex64&gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &lt;repo&gt; --local &lt;工具 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2125 w=610 h=71/></c>
<c id="p16_tk3" v="local_bootstrap.sh（便利包裝，非契約）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2196 w=150 h=55/></c>
<c id="p16_tv3" v="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &lt;tar&gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2196 w=610 h=55/></c>
<c id="p16_tk4" v=".digest 旁檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2251 w=150 h=40/></c>
<c id="p16_tv4" v="&lt;name&gt;.tar.digest 一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2251 w=610 h=40/></c>
<c id="p16_tk5" v="image ID／local_image_id" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1999 w=150 h=55/></c>
<c id="p16_tv5" v="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1999 w=610 h=55/></c>
<c id="p16_tk6" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2054 w=150 h=40/></c>
<c id="p16_tv6" v="不進 git；--local 時寫 vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2054 w=610 h=40/></c>
<c id="p16_tk7" v="離線可用（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2094 w=150 h=55/></c>
<c id="p16_tv7" v="啟動器一律先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2094 w=610 h=55/></c>
<c id="p16_tk8" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2149 w=150 h=55/></c>
<c id="p16_tv8" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2149 w=610 h=55/></c>
<c id="p16_tk9" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2204 w=150 h=71/></c>
<c id="p16_tv9" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2204 w=610 h=71/></c>
</diagram>
<diagram id="v1p16c" name="流程 v2：離線包（2）add --local 與斷網 sync"><c id="title" v="流程 v2：離線包（2）── 另備工具 tar → add --local 逐工具 → 斷網 sync（Q26、§4.8、§7.4-17）" s="text;fs=18;fst=1"><g x=40 y=20 w=1000 h=34/></c>
<c id="pend" v="已定（Q26、v2.4-10 19條-11、v2.6-1、v2.7-1／-2、v2.8-4／-5、interface_spec §1.2、§4.8、§7.4-16／17）：契約入口 = bootstrap.sh --local &lt;引擎 tar&gt;，只涉及引擎（local_bootstrap.sh 只是包內便利包裝、非契約）；-t &lt;repo&gt; 走 registry（需網路），離線接工具 = 使用者另備工具 tar（工具 repo 提供）→ add &lt;repo&gt; --local &lt;工具 tar&gt;；--local 值三分支：含 / 或 .tar 結尾 → 檔案（先驗存在，否則 1）、其餘 tag、既存檔且可解讀為 tag → 1 + 6-37；每個 tar 附同名 .digest 旁檔；version.toml 寫正式 ref@digest、metadata／local 記 image ID；啟動器先 docker image inspect、本機有就不 pull；離線 upgrade 不支援。" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=1040 y=12 w=560 h=147/></c>
<c id="hdr0" v="使用者（離線機）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=40 y=167 w=230 h=28/></c>
<c id="hdr1" v="啟動器（主機 sh）" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=290 y=167 w=400 h=28/></c>
<c id="hdr2" v="docker daemon" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=710 y=167 w=240 h=28/></c>
<c id="hdr3" v="引擎容器" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=970 y=167 w=320 h=28/></c>
<c id="hdr4" v="專案目錄" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=1310 y=167 w=280 h=28/></c>
<c id="bO1b" v="離線接工具（v2.8-5）：工具 tar 由工具 repo 提供、使用者另備（不在 vendor_kit 離線包內）→ 每個工具各跑一次 just vendor_kit add &lt;repo&gt; --local &lt;工具 tar&gt;：判別值 → docker load → 讀 .digest → inspect image ID → 引擎 resolve → apply" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=211 w=1590 h=1002/></c>
<c id="bO1b_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bO1b"><g x=1546 y=5 w=30 h=20/></c>
<c id="oo0" v="來自「離線包（1）」頁：bootstrap.sh --local 完成 install（引擎可離線跑；version.local.toml 已寫）" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1" parent="bO1b"><g x=20 y=36 w=230 h=146/></c>
<c id="oo1" v="有網路的機器取得工具 tar + 同名 .tar.digest（由工具 repo 提供；不在 vendor_kit 離線包內）→ 帶到離線機" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=20 y=218 w=230 h=73/></c>
<c id="oo1n" v="已定（v2.8-5）：vendor_kit 離線包只含引擎；-t &lt;repo&gt; 走 registry（需網路）；離線接工具 = 使用者另備工具 tar（工具 repo 的 docker save + .digest），逐工具 add &lt;repo&gt; --local &lt;工具 tar&gt;；離線 upgrade 不支援" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bO1b"><g x=1290 y=202 w=280 h=104/></c>
<c id="o10l" v="↓ 每個工具各跑一次（一次一個）：" s="text;fs=12;sc=none;fc=none;fst=1" parent="bO1b"><g x=20 y=326 w=230 h=26/></c>
<c id="o10" v="just vendor_kit add &lt;repo&gt; --local &lt;工具 tar&gt; [-y]" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=20 y=372 w=230 h=42/></c>
<c id="o10q" v="判別 --local 值（B1 三分支，同「離線包（1）」頁：路徑不存在 → 1；既存檔且可解讀為 tag → 1 + 6-37）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=372 w=400 h=42/></c>
<c id="o10a" v="docker load &lt; &lt;工具 tar&gt;" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=434 w=300 h=40/></c>
<c id="o10d" v="本機 image &lt;repo&gt;-dist:&lt;tag&gt;" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bO1b"><g x=690 y=434 w=240 h=40/></c>
<c id="o10b" v="讀 &lt;工具 tar&gt;.digest → 正式 index digest（旁檔缺 → 1）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=494 w=400 h=40/></c>
<c id="o10c" v="docker image inspect --format &#x27;{{.Id}}&#x27; → image ID" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=554 w=300 h=42/></c>
<c id="o10cd" v="回 image ID（sha256:&lt;hex64&gt;）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=690 y=555 w=240 h=40/></c>
<c id="o10r" v="docker run 引擎 resolve add &lt;repo&gt; --local（帶 index digest + image ID；永不 -t）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=616 w=400 h=42/></c>
<c id="o10re" v="resolve（不寫）：算計畫、指紋；stdout vk-resolve/1" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bO1b"><g x=950 y=616 w=320 h=42/></c>
<c id="o10p" v="docker create／cp 取本機 image 的 dist（不 pull）→ docker run 引擎 apply add" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO1b"><g x=270 y=744 w=400 h=42/></c>
<c id="o10e" v="apply add：flock → 重驗指紋 → 寫入（version.toml [tools] 正式 ref@digest；metadata 記 local_image_id）" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bO1b"><g x=950 y=736 w=320 h=57/></c>
<c id="o10f" v="add 寫" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1;fst=1;container=1" parent="bO1b"><g x=1290 y=678 w=280 h=174/></c>
<c id="o10f_0" v="version.toml [tools] 行（正式 ref@digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="o10f"><g x=8 y=26 w=264 h=42/></c>
<c id="o10f_1" v="baseline/&lt;repo&gt;/.vendor_kit.toml：source + local_image_id" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="o10f"><g x=8 y=74 w=264 h=42/></c>
<c id="o10f_2" v="cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp（第一行 = index digest）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="o10f"><g x=8 y=122 w=264 h=42/></c>
<c id="o11" v="0：該工具離線接入完成；version.toml 與線上接入一模一樣（可 commit、Renovate 可讀）；下一個工具再跑一次 add" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bO1b"><g x=20 y=872 w=230 h=124/></c>
<c id="oe20" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="oo0" target="oo1"></c>
<c id="oe20l" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="oo1" target="o10l"></c>
<c id="oe21" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10l" target="o10"></c>
<c id="oe21q" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10" target="o10q"></c>
<c id="oe22" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10q" target="o10a"><g x=0.00 pts=490,635;440,635/></c>
<c id="oe22d" v="載" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10a" target="o10d"></c>
<c id="oe23" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10a" target="o10b"><g x=0.00 pts=440,695;490,695/></c>
<c id="oe24" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10b" target="o10c"><g x=0.00 pts=490,755;440,755/></c>
<c id="oe24d" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10c" target="o10cd"></c>
<c id="oe25" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10c" target="o10r"><g x=0.00 pts=440,817;490,817/></c>
<c id="oe25e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10r" target="o10re"></c>
<c id="oe26" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="o10r" target="o10p"></c>
<c id="oe26e" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10p" target="o10e"></c>
<c id="oe27" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="o10e" target="o10f"></c>
<c id="oe28" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="o10p" target="o11"><g x=-0.60 pts=490,1145/></c>
<c id="bO2" v="之後（Q26）：斷網下 sync／build 必成功 —— 啟動器先 docker image inspect，本機有就不 pull；離線 upgrade 不支援" s="swimlane;startSize=30;fst=1;fs=12;container=1;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=20 y=1229 w=1590 h=486/></c>
<c id="bO2_v2" v="v2" s="fc=#00b050;sc=none;fco=#ffffff;fs=9;fst=1" parent="bO2"><g x=1546 y=5 w=30 h=20/></c>
<c id="w0" v="斷網：just &lt;ns&gt; build（自動 _sync）／just vendor_kit sync" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bO2"><g x=20 y=36 w=230 h=80/></c>
<c id="w1" v="快路徑：grep 比對 gen/*.stamp 第一行 vs version.toml；全相符 → 不起容器 → 0（sync --verify 或 CI 為真則全驗）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO2"><g x=270 y=55 w=400 h=42/></c>
<c id="w2" v="有差：docker image inspect &lt;ref&gt;（version.toml 的正式 ref）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO2"><g x=270 y=159 w=400 h=42/></c>
<c id="w2r" v="已定（v2.6-1、19條-11）：不用 --pull never（docker 19.03 無此旗標）；先 inspect 本機有就直接 docker run；離線 upgrade 不支援（只涵蓋 install／add --local）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1" parent="bO2"><g x=1290 y=136 w=280 h=88/></c>
<c id="w3x" v="無 → 1 + 6-31：拉不到（--timeout 內結束、不 hang）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12" parent="bO2"><g x=20 y=244 w=230 h=80/></c>
<c id="w3" v="本機有該 image？" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12" parent="bO2"><g x=270 y=244 w=220 h=81/></c>
<c id="w3d" v="本機已有 image（docker load 過的）" s="fc=#e1d5e7;sc=#9673a6;fs=12" parent="bO2"><g x=690 y=264 w=240 h=42/></c>
<c id="w4" v="有：直接 docker run（不 pull）resolve／apply sync" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12" parent="bO2"><g x=270 y=354 w=400 h=40/></c>
<c id="w4e" v="sync verify：image ID == metadata local_image_id（離線對照 index digest）→ materialize／verify cache" s="fc=#dae8fc;sc=#6c8ebf;fs=12" parent="bO2"><g x=950 y=345 w=320 h=57/></c>
<c id="w4f" v="cache/&lt;repo&gt;/、gen/&lt;repo&gt;.stamp、gen/tools.just（只寫不進 git 的）" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1" parent="bO2"><g x=1290 y=352 w=280 h=42/></c>
<c id="w5" v="0：成功、不起 pull（驗收 §7.4-17）" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12" parent="bO2"><g x=20 y=422 w=230 h=58/></c>
<c id="we0" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w0" target="w1"></c>
<c id="we1" s="fs=12;exitX=0.5;exitY=1;entryX=0.5;entryY=0" edge="1" source="w1" target="w2"></c>
<c id="we2" s="fs=12;exitX=0.275;exitY=1;entryX=0.5;entryY=0" edge="1" source="w2" target="w3"></c>
<c id="we3" v="無" s="fs=12;exitX=0;exitY=0.5;entryX=1;entryY=0.5" edge="1" source="w3" target="w3x"></c>
<c id="we4" v="inspect" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w3" target="w3d"></c>
<c id="we5" v="有" s="fs=12;exitX=0.5;exitY=1;entryX=0.275;entryY=0" edge="1" source="w3" target="w4"><g x=-0.6/></c>
<c id="we6" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w4" target="w4e"></c>
<c id="we7" v="寫" s="fs=12;exitX=1;exitY=0.5;entryX=0;entryY=0.5" edge="1" source="w4e" target="w4f"></c>
<c id="we8" s="fs=12;exitX=0.5;exitY=1;entryX=1;entryY=0.5" edge="1" source="w4" target="w5"><g x=-0.79 pts=490,1680/></c>
<c id="p16c_lg0" v="淺灰：情境分組（無狀態意義）" s="swimlane;startSize=34;fst=1;fs=12;container=0;fc=#f5f5f5;swfc=#ffffff;sc=#000000"><g x=40 y=1731 w=200 h=60/></c>
<c id="p16c_lg1" v="黃：判斷" s="rhombus;fc=#FFF4C3;sc=#000000;fs=12"><g x=260 y=1731 w=140 h=64/></c>
<c id="p16c_lg2" v="綠：起點／終點" s="ellipse;fc=#d5e8d4;sc=#000000;fs=12"><g x=420 y=1739 w=140 h=44/></c>
<c id="p16c_lg3" v="紅：失敗終止（拉不到／寫壞）" s="ellipse;fc=#f8cecc;sc=#000000;fs=12"><g x=580 y=1733 w=190 h=56/></c>
<c id="p16c_lg4" v="橙：需要人動作（1／3 印指令；2 解衝突）" s="ellipse;fc=#ffe6cc;sc=#000000;fs=12"><g x=790 y=1733 w=210 h=56/></c>
<c id="p16c_lg5" v="白：步驟" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12"><g x=1020 y=1741 w=88 h=40/></c>
<c id="p16c_lg6" v="虛線框：專案裡的檔案" s="fc=#ffffff;sc=light-dark(#000000,#9577A3);fs=12;dashed=1"><g x=1128 y=1741 w=170 h=40/></c>
<c id="p16c_lgt" v="實線 = 執行順序（指向檔案時 = 寫入／讀取）" s="text;fs=12;sc=none;fc=none"><g x=1318 y=1731 w=280 h=60/></c>
<c id="p16c_lgx_note" v="便條：補充說明" s="shape=note;size=14;fc=#ffffff;sc=#999999;fs=12"><g x=40 y=1799 w=120 h=36/></c>
<c id="p16c_lgx_rule" v="橘框：規則（已定）" s="fc=#ffe6cc;sc=#d79b00;fs=12;fst=1"><g x=180 y=1799 w=150 h=36/></c>
<c id="p16c_lgx_sub" v="藍：引擎子命令（容器內）" s="fc=#dae8fc;sc=#6c8ebf;fs=12"><g x=350 y=1799 w=190 h=36/></c>
<c id="p16c_lgx_img" v="紫：image（引擎與工具）" s="fc=#e1d5e7;sc=#9673a6;fs=12"><g x=560 y=1799 w=170 h=36/></c>
<c id="p16c_lgx_hdr" v="灰底：泳道／表格表頭" s="fc=#e6e6e6;sc=#999999;fs=12;fst=1"><g x=750 y=1799 w=170 h=36/></c>
<c id="p16c_lgx_entry" v="虛線橢圓：來自其他頁" s="ellipse;fc=#ffffff;sc=#000000;fs=12;dashed=1"><g x=940 y=1799 w=200 h=36/></c>
<c id="p16c_th" v="本頁名詞" s="text;fs=13;sc=none;fc=none;fst=1"><g x=40 y=1837 w=200 h=28/></c>
<c id="p16c_tk0" v="離線包（#27、Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1871 w=150 h=55/></c>
<c id="p16c_tv0" v="Release 資產 vendor_kit-vN-local.tar.gz：bootstrap.sh、各平台 docker save 的引擎 tar + 同名 .digest 旁檔，另附 local_bootstrap.sh 便利包裝；只含引擎、不含任何工具 tar；在有網路的機器下載後帶到離線機；只涵蓋 install／add --local，離線 upgrade 不支援" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1871 w=610 h=55/></c>
<c id="p16c_tk1" v="bootstrap.sh --local（契約入口）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1926 w=150 h=71/></c>
<c id="p16c_tv1" v="離線接入的契約入口 = bootstrap.sh --local &lt;引擎 tar&gt;（interface_spec §1.2）：只涉及引擎（docker load → install）；-t &lt;repo&gt; 仍是 add &lt;repo&gt;[@tag]，走 registry、需網路，離線機不帶 -t；--local 值的判別（B1）：含 / 或以 .tar 結尾 → 檔案路徑（先驗存在，否則 1）；其餘 → image tag；兩者皆成立（既存檔且可解讀為 tag）→ 1 + 6-37「請寫 ./&lt;v&gt; 或完整 ref」" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1926 w=610 h=71/></c>
<c id="p16c_tk2" v="工具 tar（來源，v2.8-5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=1997 w=150 h=71/></c>
<c id="p16c_tv2" v="離線接工具要另備工具 tar：由工具 repo 自己提供（docker save 的 &lt;repo&gt;-dist image + 同名 .tar.digest 旁檔，一行 sha256:&lt;hex64&gt; = 該工具的正式 index digest），不在 vendor_kit 離線包內；使用者在有網路的機器取得、帶到離線機，逐工具執行 just vendor_kit add &lt;repo&gt; --local &lt;工具 tar&gt;" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=1997 w=610 h=71/></c>
<c id="p16c_tk3" v="local_bootstrap.sh（便利包裝，非契約）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2068 w=150 h=55/></c>
<c id="p16c_tv3" v="離線包內附的可選腳本：docker version --format &#x27;{{.Server.Arch}}&#x27; 偵測 daemon 架構 → 挑該平台引擎 tar → exec ./bootstrap.sh --local &lt;tar&gt; &quot;$@&quot;；不是契約入口、不另定介面（v2.7-1）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2068 w=610 h=55/></c>
<c id="p16c_tk4" v=".digest 旁檔" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2123 w=150 h=40/></c>
<c id="p16c_tv4" v="&lt;name&gt;.tar.digest 一行 sha256:&lt;hex64&gt; = 該 image 的正式多架構 index digest；同名旁檔須同在（缺 → 1）；version.toml 仍寫正式 ref@digest（與線上接入一模一樣），不寫本機 tag" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2123 w=610 h=40/></c>
<c id="p16c_tk5" v="image ID／local_image_id" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=40 y=2163 w=150 h=55/></c>
<c id="p16c_tv5" v="docker load 後的 image 只有 tag、沒有 RepoDigests；docker image inspect --format &#x27;{{.Id}}&#x27; 取 image ID：引擎覆寫記 version.local.toml vendor_kit_image_id、工具記 metadata local_image_id（image ID ↔ index digest 對照，供離線驗證）" s="fc=#ffffff;sc=#999999;fs=12"><g x=190 y=2163 w=610 h=55/></c>
<c id="p16c_tk6" v="version.local.toml" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1871 w=150 h=40/></c>
<c id="p16c_tv6" v="不進 git；--local 時寫 vendor_kit = &quot;&lt;tag&gt;&quot; + vendor_kit_image_id（install 成功後才寫、失敗清除）；之後啟動器每次 docker image inspect 比對 ID、不 pull" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1871 w=610 h=40/></c>
<c id="p16c_tk7" v="離線可用（Q26）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1911 w=150 h=55/></c>
<c id="p16c_tv7" v="啟動器一律先 docker image inspect &lt;ref&gt;：本機有 → 不 pull（不用 --pull never，docker 19.03 無此旗標）；斷網 + 本機已有 image → sync／build 必須成功；斷網 + 無 image → 1 + 6-31 在 --timeout 內結束、不 hang" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1911 w=610 h=55/></c>
<c id="p16c_tk8" v="sync 快路徑（Q22）／--verify（F5）" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=1966 w=150 h=71/></c>
<c id="p16c_tv8" v="sync（無參數）啟動器只用 grep 比對 gen/.stamp 第一行 == version.toml 引擎 ref、gen/&lt;repo&gt;.stamp 第一行 == 鎖定 digest、tools.just 存在、無 .tmp.*、非 frozen → 全相符不起容器 0；有差才起引擎；sync --verify 或 CI 為真 → 每檔 sha256 全驗（verify 用 local_image_id 對照）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=1966 w=610 h=71/></c>
<c id="p16c_tk9" v="6-N 訊息編號" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2037 w=150 h=55/></c>
<c id="p16c_tv9" v="interface_spec §6 的逐字訊息清單編號（每句含可直接複製的指令）：6-3 無 registry 憑證、6-4 無 tty、6-12 指紋不同、6-15 update 末行、6-27 未恢復、6-30 vk-resolve 不合、6-31 pull 逾時、6-32 prune 問句、6-33 未完成交易、6-37 --local 值歧義…" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2037 w=610 h=55/></c>
<c id="p16c_tk10" v="結束碼 0／1／2／3" s="fc=#ffffff;sc=#999999;fs=12;fst=1"><g x=840 y=2092 w=150 h=71/></c>
<c id="p16c_tv10" v="0 成功（含 warn）；1 一般失敗或需要人動作（工具層動詞回 1 時 version.toml 不動；自身升級後「請再跑原指令」也是 1）；2 合併衝突（留標記、baseline 仍推、解完重跑）或 update --exit-code 有新版；3 版本／協定／schema 不合（零寫入；先升級或退回才能繼續；以 P／schema 比較，不用版本字串）" s="fc=#ffffff;sc=#999999;fs=12"><g x=990 y=2092 w=610 h=71/></c>
</diagram>
</mxfile>

```
