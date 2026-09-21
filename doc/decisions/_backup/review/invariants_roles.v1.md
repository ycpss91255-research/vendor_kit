# 審閱頁 01：不變量與角色

來源：`decisions/interface_spec.md` v3.1（文首、§0、§2、§3.5、§4.5、§4.7、§7、§8）；定案確認：`decisions/grilling.md`。本頁只摘錄、不新增決議；每條附來源。對應討論圖頁「契約：不變量與角色」，以本文字為正本。審閱方式：逐條打勾／打叉，叉的寫一句理由。

## 一句話目的

工具 repo 把 `dist/` 打成 GHCR image（`FROM scratch`、純資料）；下游專案用 `bootstrap.sh` 接入，之後用 `just vendor_kit <verb>` 取得工具、把版本鎖在 `.vendor_kit/version.toml`（`<tag>@<digest>` 一行）、初始檔以三方合併升版。vendor_kit 只搬移，不承諾 dist 內容可執行。<sub>來源：spec 文首、§4.7；grilling Q1、Q21</sub>

## 角色與職責

| 角色 | 負責 | 不負責 |
|---|---|---|
| 工具 repo（`<repo>`） | 維護 `dist/`（`files/`、`init.toml`、`just/<ns>.just`）與三行 `Dockerfile.dist`；用 `check.sh --dist` 驗佈局與兩平台一致；自己在乾淨機器驗交付物可執行；image 公開與否自決 | 不碰下游專案的檔；交付物不得依賴 `.vendor_kit/`；binary 可執行性不由 vendor_kit 代驗 |
| vendor_kit：引擎 image | 所有判斷與寫檔（resolve／apply、三方合併、薄殼重產、schema 讀寫）；只透過掛入的 `/repo` 看專案根 | 不讀 `.git`、不碰 index、不 `git init`；不 commit、不開 PR |
| vendor_kit：薄殼（啟動器） | 進 git、由引擎產的五檔＋`version.toml`；只做 grep／`docker run`／寫操作紀錄檔；`sync` 快路徑不起容器 | 不解析 TOML、不 eval；人不改（被改 → 1 列差異不動） |
| 下游專案（維護者） | 用 `bootstrap.sh` 接入；回答詢問或給 `-y`；commit 薄殼與 `version.toml`；本機 `upgrade <repo> -y` 解合併 | 不需裝引擎語言環境；不手寫 `gen/`、`cache/` |
| CI（`.vendor_kit/ci/check.sh`） | `export CI=1` 後 frozen 跑 sync → verify → `upgrade --dry-run` → 工具測試 → 專案測試；回第一個失敗步驟的碼 | 不寫任何 tracked 檔；不查最新版；平台無關（GitHub／GitLab 一樣） |
| Renovate（下游自選） | 用 vendor_kit repo 根目錄 preset；PR 只改 `version.toml` 一行；major 分開 PR | vendor_kit 本身無 bot；初始檔合併不由 bot 做（維護者本機補完再 push） |

<sub>來源：spec §3.1、§4.5、§4.7、§7.1、§7.3；grilling Q5、Q7、Q21、CI 平台定案、deploy 包定案</sub>

## 本頁名詞（其餘見 CONTEXT.md）

- 專案根：含 `.vendor_kit/` 的目錄；不是 git toplevel。
- 薄殼：進 git、由引擎產、人不改的五檔（`entry.just`、`vendor.just`、`log.sh`、`.gitignore`、`ci/check.sh`）；首行自描述 `# vendor_kit-shell/<P> engine=<vX> sha256=…`。
- 啟動器：薄殼內的 POSIX sh recipe 殼，負責起引擎容器；`bootstrap.sh` = 第一次接入時的啟動器。
- 使用者的檔：專案內非 vendor_kit 自產的一切（根 justfile、根 `.dockerignore`、初始檔落點、其他原有檔）。
- 初始檔：工具 `dist/init.toml` 宣告、`add` 時複製或 append 進專案的檔；baseline 副本在 `.vendor_kit/baseline/<repo>/`。
- 進度日誌：可寫動詞的交易紀錄（`.tmp.<verb>.<id>.toml` 或 metadata `[progress]`），成功即刪。
- 操作紀錄檔：`.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`，每次執行一檔，事後追溯用。
- frozen：`CI` 為真時的模式：不寫 tracked 檔、不查最新版。

## 不變量

- **I1 使用者檔四原則**：可以建（明說建了什麼）、要改先問（`-y` 免問）、永不刪、永不覆蓋（不用工具版本取代客製內容）。<sub>來源：grilling 隔離題定案；spec §0</sub>
- **I2 自動化只碰不進 git 的東西**：`sync`（含工具 recipe 自動前置的 `_sync`）只寫 `cache/`、`gen/`（與操作紀錄檔）；發現薄殼不符只回 1 提示，不重寫。<sub>來源：grilling Q10；spec §0、§1.2 sync</sub>
- **I3 never fail silently**：每個失敗都印訊息並附可直接複製的指令；warn 也明列條目；印到 tty 的訊息同句進操作紀錄檔。<sub>來源：spec §0、§6、§4.10；grilling Q6</sub>
- **I4 結束碼語意**：0 成功（含 warn）；1 一般失敗或需人動作（工具層動詞回 1 時 `version.toml` 不動）；2 合併衝突（留標記、baseline 仍推到新版；`update --exit-code` 有新版亦 2）；3 版本／協定／schema 不合，須先升級或退回。多工具動詞做得完的做完，最後回最需處理的碼（1 > 2 > 0）。<sub>來源：grilling Q23、Q27；spec §2</sub>
- **I5 回 3 零寫入**：不寫任何專案檔；新舊一律比 P／schema，不比版本字串；floor 檢查先於任何上網；網路／認證／不存在回 1，不得偽裝成 3。唯一例外：操作紀錄檔的 `launcher_start`／`engine_start` 已寫屬預期。<sub>來源：grilling Q23；spec §0、§2；例外 = v2.13 P12</sub>
- **I6 橙／紅語意**：需人動作的結束（1 或 3 且印指令；衝突 2 亦同）為橙；紅只給失敗（拉不到、寫入失敗、驗證失敗）。<sub>來源：grilling 2026-09-20；v2.10-1。spec 未載，見文末</sub>
- **I7 CI 真值規則**：環境變數 `CI` 非空且不為 `0`／`false`（大小寫不敏感）→ frozen；`check.sh` 自己 `export CI=1`。frozen 下升為失敗的警告明列：薄殼不符、baseline 落後、未完成接入、任何 local 覆寫、需改 tracked 檔；「沒納管／拒絕過」提醒不紅燈；仍拉鎖定版 image、仍寫 `cache/`、`gen/`；`update` 唯讀不受影響。<sub>來源：grilling 16 條必修、Q5、Q15；spec §0</sub>
- **I8 `-y` 只省略詢問**：不授權覆蓋既有未納管檔、不硬加 append 行、不解除 frozen。無 tty／EOF 且無 `-y` → 1 印 6-4；EOF／Ctrl-C = 中止不套用、不記 declined。<sub>來源：grilling 16 條必修、Q13、19 條-6；spec §0</sub>
- **I9 交付物執行期不依賴 `.vendor_kit/`**：工具 recipe 產生的交付物不得依賴 `.vendor_kit/`、`version.toml`、GHCR，需要的檔打包時複製進去；初始檔只能引用穩定入口 `just <ns> …`，不得寫死 `cache/` 內部路徑。<sub>來源：grilling deploy 包定案、Q14；spec §4.7</sub>
- **I10 專案根與巢狀**：專案根 = 含 `.vendor_kit/` 的目錄（monorepo 子專案各自一套）；須在某 git repo 內；禁巢狀（install 時上層或下層已有 `.vendor_kit/` → 1）；動詞只准在專案根執行，否則 1 印 6-9（`sync` 豁免）。<sub>來源：grilling Q20 定案（改）、Q20 修正；spec §0</sub>
- **I11 進度日誌**：每個可寫動詞第一個寫入前必建（含第一次 `install`、`upgrade vendor_kit`），不設例外；可寫動詞開始前遇未完成交易先恢復再繼續；唯讀動詞只偵測不恢復（`sync`／`update` 印 6-33 結束 1，`help` 仍 0）。<sub>來源：grilling 進度日誌條、2026-09-20（v2.11-1、v2.10-6）；spec §0；第一次 install 也建 = v2.13 P5</sub>
- **I12 操作紀錄檔**：每個動詞每次執行（含 `help`、`sync` 快路徑、`--dry-run`）必寫一檔；啟動器在任何其他動作之前 mkdir＋建檔＋寫 `launcher_start`，失敗 → 1＋6-38、零寫入；引擎 `engine_start` 寫不進亦同；無 `--no-log`。<sub>來源：grilling 2026-09-20 新需求、L1–L6 定案；v2.12 L4；spec §0、§4.10</sub>
- **I13 薄殼人不改**：薄殼首行 hash 不符 → 1 列差異不動；重產只由明確動作（`install`／`upgrade vendor_kit`）做。<sub>來源：grilling Q10、Q17；spec §4.5、§8-6</sub>
- **I14 兩層相容承諾**：救援路徑（`install`、`upgrade vendor_kit`、`sync` 不符提示、`help`）對任何 ≥ floor 的薄殼永久可用；舊資料永遠可讀、可遷；舊薄殼跑新 major 一般動詞只保證乾淨回 3；floor 只能經 ADR 提高。<sub>來源：grilling Q16、Q23；spec §3.5、§8-3～5</sub>

## 例外清單（不變量的明文例外）

- 根 justfile：無 → 建四行（`import '.vendor_kit/entry.just'`、空行、`default:`、`\t@just --list`）；有 → 問後加 import 一行；`uninstall` 只刪完全相同的行。<sub>grilling 隔離題 A、16 條必修；spec §4.5</sub>
- 根 `.dockerignore`：`install` 無則建、有則問後 append 四行（`.vendor_kit/cache/`、`.vendor_kit/gen/`、`.vendor_kit/.tmp.*`、`.vendor_kit/log/`）；`uninstall` 問後逐行只刪原文相同行。<sub>grilling Q22 補（三行）；第四行 v2.13 P13；spec §4.5</sub>
- 初始檔換版／三方合併：已納管初始檔經同意（或 `-y`）換新版或三方合併；衝突留標記回 2、baseline 推到新版；`.vendor_kit/config.toml` 對 `upgrade vendor_kit` 比照。<sub>grilling 隔離題 C；v2.12 L3′；spec §0</sub>
- append 型初始檔：問後加入並記錄實際插入的行；升版只對可辨識的上次插入行提修改；零命中或多處 → 保留只 warn，`-y` 不硬加。<sub>grilling Q6、Q12、Q13</sub>
- 新版刪除的初始檔：只 warn 不刪。<sub>grilling 第 1 頁便條回覆</sub>
- `log/`：vendor_kit 自己的檔，不受四原則；`bootstrap.sh`／第一次 `install` 失敗清半成品時 `log/` 保留；`uninstall` 一律保留 `log/`（`.vendor_kit/` 只剩 `log/`）。<sub>v2.12 L1；v2.13 P4、P6；spec §0、§1.2、§4.10</sub>
- 進度日誌與 `.tmp.*`：同上不受四原則；成功即刪；`prune` 不刪活躍者。<sub>spec §0、§4.6</sub>
- 零寫入的操作紀錄檔例外：見 I5。<sub>v2.13 P12</sub>

## 本頁待拍板

無。spec §9.1 剩下的 P1（啟動器讀 config 方式）、P2（外部 repo 反向採用 POSIX log.sh）、P3（事件集合待 codex 審）都不在本頁範圍。
提醒：本頁引用了 v2.13「主對話已結案、使用者可否決」的項目：P4／P6（失敗與 uninstall 保留 `log/`）、P5（第一次 install 也建進度日誌）、P12（零寫入之操作紀錄檔例外）、P13（`.dockerignore` 第四行）。

## 發現的矛盾（spec 與 grilling 有出入；未取捨，請拍板）

| # | 條目 | grilling | spec v3.1 |
|---|---|---|---|
| 1 | I6 橙／紅語意 | 2026-09-20「需人動作的 1 結束一律橙」；v2.10-1「橙 = 1 或 3 且印指令、2 也橙；紅 = 失敗」 | §0／§2 未載此語意（全文無「橙」） |
| 2 | I10 禁巢狀範圍 | Q20 定案（改）「install 時**上層**已有 `.vendor_kit/` → 1」 | §0「上層**或下層**已有 → 1」（review I-47） |
| 3 | I10 執行位置 | Q20 修正「vendor_kit 動詞只准在含 `.vendor_kit/` 的那一層執行」，無例外 | §0「`sync` 豁免此檢查」（F1） |
| 4 | I7／I8 CI 與 `-y` | 隔離題 C「CI **無 `-y`** 需改檔 → 1 印清單」 | §0「需改 tracked 檔 → 1，**與 `-y` 無關**；`-y` 不解除 frozen」（grilling 16 條必修亦如此，grilling 前後兩說） |
| 5 | I5 零寫入 | Q23「回 3 時零寫入」，無例外 | §0／§4.10「操作紀錄檔例外」（v2.13 P12，主對話結案、可否決） |
| 6 | 例外：`.dockerignore` 行數 | Q22 補「三行」 | §4.5 四行（加 `.vendor_kit/log/`；v2.13 P13） |
| 7 | I14 舊薄殼跑新 major | Q16「回 1」→ Q23「改為 3」（grilling 內已自行更正） | §2、§8-5 回 3（§11-1）；列出僅供確認 |
