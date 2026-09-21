# 動詞介面表

本頁列 `just vendor_kit <動詞>` 的 11 個動詞、升引擎與 `bootstrap.sh`，只放契約層：語法（照第 0 頁記法）、做什麼、寫哪類檔、結束碼、CI 模式；步驟細節屬於各流程圖，表末「流程」欄只寫流程名。只用第 0、1 頁的詞，只摘錄規格、不新增決議，出處在文末。審閱方式：逐列看是否與你認知一致，不一致的寫一句理由。

## 本頁名詞（第 0、1 頁沒有的頁內特有詞）
- 快路徑：`sync` 不帶參數（含工具 recipe 自動觸發的那次）時，啟動器寫完執行紀錄後、不起引擎容器就判定「沒事做」的條件，要**全部**成立：① `gen/.stamp` 第一行 = 引擎的版本鎖定行；② 每個工具的印記第一行 = 該工具版本鎖定行的 digest（或本機覆寫的 `path:<dir>`）；③ 每個工具的 `cache/<repo>/` 存在；④ `gen/tools.just` 存在；⑤ 沒有任何進度檔；⑥ 非 CI 模式。全成立 → 0（執行紀錄仍寫）；任一不成立 → 起引擎。
- 指紋重驗：兩段式動詞的 apply 容器在寫入前重算專案狀態的指紋，與 resolve 算出的計畫不同就不寫、以 1 結束並要求重跑。
- 離線包：release 附的 `docker save` tar 與同名 `.digest` 旁檔（正式 digest）；`--local` 用它。

## 通則（每個動詞都適用，表內不重複）
1. 執行紀錄：每個動詞每次執行必寫一檔，`bootstrap.sh` 自己那段亦同（寫在 `log/bootstrap/`）。不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；建不了 → 1 零寫入，沒有關掉它的選項。
2. 專案根：只准在專案根執行，否則 → 1 印出該到哪個目錄；`sync` 被工具 recipe 自動觸發的那次自己先切到專案根。
3. 進度檔：可寫動詞（含 dev）在第一個寫入前建進度檔、成功即刪，開始前遇未完成交易先恢復再繼續（`prune` 例外：遇活躍進度檔只列出提示、不恢復、不阻擋，它不碰進 git 的檔）；唯讀動詞遇到只印恢復指令：`sync`、`update` → 1，`help` 印出仍 0。
4. `-y` 與 CI 模式是兩個獨立開關：`-y` 只省略詢問（需詢問但無 tty 又沒 `-y` → 1），不授權覆蓋、不硬加；CI 模式 = 不寫任何進 git 的檔、不查最新版（`update` 除外），需改進 git 的檔 → 1 印清單（與 `-y` 無關），仍拉鎖定版 image、仍寫 `cache/`、`gen/`；下表 CI 模式欄只寫偏離此通則的例外。
5. 結束碼 3（介面版／檔案版不合）一律零寫入（執行紀錄開頭除外）；網路、認證、不存在 → 1，不得偽裝成 3；不帶 `<repo>` 的動詞失敗策略依各動詞（`upgrade` 逐工具做得完的做完；`uninstall` apply 期間任一失敗就中止），最後回最需處理的碼：有任何 1 → 1，否則有 2 → 2，否則 0；每個工具的訊息全部保留列出。
6. `--dry-run`：只預覽會問什麼、會改什麼，不寫任何進 git 的檔、不建進度檔；需要新版內容的動詞（`add`、`upgrade`）仍拉 image 展開，`uninstall`、`remove`、`prune` 不拉；CI 模式下需改進 git 的檔 → 1 印清單。
7. `--help`：所有動詞都接受，印用法後 0；語法欄不重複列。

## 動詞表
「寫哪類檔」簡寫：鎖定行＝版本鎖定行、基準版＝基準版與 metadata、cache＝`cache/`、gen＝`gen/`（印記、`tools.just`）、薄殼＝薄殼五檔與 `gen/.stamp`、`config.toml`、本機覆寫＝`version.local.toml`、進度檔、專案檔＝根 justfile／`.dockerignore`／初始檔（薄殼與 `config.toml` 是 VK 檔，不歸專案檔）；執行紀錄每列都寫、不列；「（皆刪）」＝括號前列出的類別只刪不建；進度檔一律「建、成功後刪」，不在（皆刪）之內。

| 語法 | 一句話 | 寫哪類檔 | 結束碼 | CI 模式 | 流程 |
|---|---|---|---|---|---|
| `install [-y] [--no-justfile]` | 第一次接入：建 `.vendor_kit/`（引擎鎖定行、`config.toml`、薄殼五檔、空 `baseline/`、`gen/.stamp`），根 justfile 無 → 建四行、有 → 問後加一行，根 `.dockerignore` 無 → 建四行、有 → 問後加四行；`--no-justfile` = 跳過根 justfile 那一步、只印手動加那一行的指示；再跑 = 修復（自描述標頭相符才重寫）；`install <repo>` → 1 改用 `add` | 鎖定行、`config.toml`、薄殼、基準版（只建空 `baseline/`，不建 metadata）、專案檔、進度檔 | 0；1 需人處理（非 git repo、巢狀 `.vendor_kit/`、薄殼被改、需詢問無 tty）／失敗（清掉半成品、`log/` 保留）；3 | 同通則 | install(1)(2) |
| `uninstall [-y] [--dry-run]` | 先對全部工具預檢（任一在 dev 中或不可移除 → 整體不動、1）；過了才逐工具照 `remove` 做（各工具的鎖定行在該工具其餘檔刪完後才刪），再只刪 hash 相符的 VK 自產檔與自己加在根 justfile／`.dockerignore` 的行；被改過的保留並列出；初始檔不刪只印清單；`log/` 一律保留 | 鎖定行、基準版、cache、gen、薄殼、`config.toml`、本機覆寫、專案檔（皆刪）；進度檔 | 0；1 需人處理（預檢失敗：dev 中、需詢問無 tty → 整體不動）／失敗（apply 期間任一工具失敗 → 中止、列出已完成與未處理的部分；該工具鎖定行不動、進度檔保留）；3 | 同通則 | uninstall(1)(2) |
| `add <repo>[@<tag>] [--source <image>] [--local <tar>] [-y] [--dry-run] [--timeout <秒>]` | 接入一個工具：解析版本（沒指定 → 最新正式版）、拉展開、指紋重驗，建初始檔（copy 型已存在不納管、`-y` 也不覆蓋；append 型問後加行）、存基準版、重生 `gen/tools.just`，最後寫鎖定行；已接入且沒指定 tag（或 tag 相同）→ 0；已接入且指定的 tag 與鎖定行不同 → 1 改用 `upgrade`；撞名／越出專案／私有無憑證 → 1，全在寫入前檢查 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（撞名、拒絕、沒憑證、需詢問無 tty）／失敗（拉不到或逾時、指紋不同；鎖定行一律未動）；3 | 同通則 | add(1)(2)(3) |
| `remove <repo> [-y] [--dry-run]` | 移除該工具的 `cache/<repo>/`、基準版、印記與 `tools.just` 內的行，最後才刪鎖定行；append 過的行問後只刪原文相同的；初始檔不刪只印清單；未接入 → 0；不帶 `<repo>` → 印用法、1 | 鎖定行、基準版、cache、gen、專案檔（皆刪）；進度檔 | 0；1 需人處理（dev 中、需詢問無 tty）／失敗（指紋不同、寫不進；鎖定行不動、進度檔保留，工具仍鎖定而 `cache/` 可能部分缺）；3 | 同通則 | remove(1)(2) |
| `update [<repo>] [--exit-code]` | 查 registry 最新正式版與鎖定行比對、逐一列出（不帶 = 全部，含引擎）；私有無憑證 → 該工具 1、其他照查；末行固定印「套用：just vendor_kit upgrade」；不拉 image | －（只寫執行紀錄） | 0；1 需人處理（任一工具查不到 → 整體 1）；`--exit-code` 且有新版 → 2；3 | 例外：仍查 registry（唯讀，本來就不寫進 git 的檔） | update |
| `upgrade [<repo>[@<tag>]] [-y] [--dry-run] [--timeout <秒>]` | 升到最新（或指定）版：拉展開、指紋重驗、換 `cache/`，初始檔逐檔問（沒改 → 換；只有你改 → 不動；兩邊改 → 三方合併、衝突留標記，合併結果是 TOML／just 而解析不過 → 留原檔；新增問建、拒絕記下不再問；刪除只 warn），基準版推到新版（衝突仍推；解析不過的檔不推），最後寫鎖定行。動手前先看兩個前置：① metadata 記有衝突且檔內仍有衝突標記，或衝突中的檔案失蹤（也不算已解）→ 立即 2 停、不做任何事（先手動解完再重跑）；② 「鎖定行已新、基準版仍舊」→ 只補基準版到鎖定行的版本然後停止、印提示，不查最新版、不升版；兩者都沒有才查最新（或用指定的 `@<tag>`）。不帶 `<repo>` 先對全部工具完整預檢，引擎有新版 → 本次只升引擎；`@<tag>` 只配單一 `<repo>`，比現版舊 → warn 仍做 | 鎖定行、基準版、cache、gen、專案檔、進度檔 | 0；1 需人處理（沒基準版先 `add`、dev 中、需詢問無 tty）／失敗（拉不到、指紋不同、合併程式出錯）；2 衝突（留標記、基準版仍推；合併結果解析不過的檔 → 留原檔、該檔基準版不推；手動編輯後重跑直到乾淨；既有衝突未解完（含衝突中的檔案失蹤）就重跑也是 2）；3 | 同通則；`--dry-run` 就是契約檢查腳本用的那一步 | upgrade(1)–(6) |
| `upgrade vendor_kit[@<tag>] [-y] [--dry-run]`（升引擎；`upgrade` 不帶 `<repo>` 遇引擎新版時由啟動器自動接手） | 先做兩個前置：① 薄殼被改（自描述標頭不符）→ 1 列差異不動；② 有未完成的升引擎進度檔 → 本次就是恢復，依進度檔記的目標續跑後面步驟。前置過了才定目標（指定 `@<tag>` 不查 registry）→ 建進度檔 → 改引擎鎖定行 → 啟動器改用新引擎重跑 → 重產薄殼五檔與 `gen/.stamp`，`config.toml` 缺則建、有則三方合併 → 刪進度檔 → 1 要求 commit 後再跑原指令；目標 = 現版且薄殼相符 → 0；鎖定行已改但新引擎拉不到、ID 不符或重產失敗 → 1，進度檔保留、印可複製的恢復指令 `just vendor_kit upgrade vendor_kit`（下次任何可寫動詞也會先恢復）；降版須能無損讀現有檔，否則 3 印「請 git revert」 | 鎖定行（引擎那行）、薄殼、`config.toml`、基準版（`config.toml` 副本）、進度檔 | 0 無變更；1 需人處理（重產完成要 commit 再跑、薄殼被改、鎖定行已改但新引擎拉不到）／失敗（鎖定行未變時重產失敗）；3 降版無法無損讀（零寫入） | 沒指定 `@<tag>` → 不查、目標 = 現版 | 升引擎(1)–(3) |
| `dev <repo> -p <dir>`／`dev vendor_kit -i <tag>` | 寫本機覆寫：工具的 `cache/<repo>/` 改成指向 `<dir>/dist` 的 symlink、印記記 `path:<dir>`；引擎記 tag 與 image ID，之後只驗 ID、不拉；單段、不拉 image；建進度檔；工具須已在鎖定行、`<dir>/dist/init.toml` 須存在；`-i` 只能 tag，較舊引擎不得重產薄殼 | 本機覆寫、cache、gen、進度檔 | 0；1 需人處理（不在鎖定行、缺 `init.toml`、CI 模式）；3 | 例外：一律拒絕 → 1 | dev(1)(2) |
| `undev <repo> [--timeout <秒>]`／`undev vendor_kit [--timeout <秒>]` | 撤本機覆寫那一項（撤的是最後一項則刪整檔），依鎖定行重新拉展開 `cache/`（引擎不展開，下次 `sync` 只提示升引擎）；未啟用 → 0 | 本機覆寫、cache、gen、進度檔 | 0；1 失敗（拉不到、寫不進；進度檔保留）；3 | 同通則 | undev(1)(2) |
| `sync [<repo>] [--verify] [--timeout <秒>]` | 快路徑全成立 → 0 不起容器；否則依鎖定行重建 `cache/`、`gen/`：引擎版 ≠ `gen/.stamp` → 1 跑升引擎；本機覆寫的工具跳過；印記 ≠ 鎖定 digest → 重拉；`--verify` 逐檔驗指紋、不符重裝；未完成接入 → 1 跑 `add`；基準版落後 → warn 提示 `upgrade`；工具 recipe 執行前自動觸發 | cache、gen | 0；1 需人處理（薄殼不符、未完成接入、未完成交易）／失敗（拉不到或逾時、寫不進）；3 | 一律逐檔驗指紋；薄殼不符、基準版落後、未完成接入、任何本機覆寫都升為 1；「未納管／拒絕過」只提醒、不紅燈 | sync(1)–(3) |
| `prune [-y] [--dry-run]` | 保留清單 = 鎖定行引用的 image ＋ 本機覆寫中引擎的 tag／image ID 覆寫實際引用的 image（工具的 `path:<dir>` 覆寫沒有 image、不列）；啟動器依 VK 標籤列出其餘容器／image／network／volume、問後逐一刪；引擎清失效暫存與已完成交易的殘留；活躍（未恢復）的進度檔只列出提示、不刪、不恢復、不阻擋；執行紀錄不歸它清 | 進度檔、暫存；docker 資源 | 0；1 需人處理（需詢問無 tty）／失敗（磁碟滿到執行紀錄寫不進）；3 | 同通則 | prune |
| `help`（別名 `h`） | 印命名空間層說明，明寫「已接入的專案跑 sync，不是 install」；不觸網、不安裝、不偵測狀態；遇未完成交易印恢復指令仍 0 | －（只寫執行紀錄） | 0；1 只在執行紀錄寫不進 | 無差異 | — |
| `sh bootstrap.sh [-t <repo>[@<tag>]]… [-y] [--local <image tag／tar>] [--timeout <秒>] [-h]` | 第一次接入的啟動器：檢查 git repo 與 just ≥ 1.33.0，建執行紀錄，拉（本機有就不拉）引擎 image，跑 `install`，再逐個 `-t` 依序跑 `add`，任一非 0 立即中止、列出已完成與未處理，結束碼 = 失敗那一步的碼原樣傳出（`install` 或 `add` 回 3 → 3、回 2 → 2、其餘 → 1）；專案已有 `version.toml` 就用那行的引擎，只有第一次才用內嵌版本；`--local` 的值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag；tar 由 `.digest` 旁檔取正式 digest、tag 只驗本機 ID 記成本機覆寫；再跑 = 修復 | 經 `install`、`add` 寫的全部；`--local` 時本機覆寫（`install` 成功後才寫） | 0；1 需人處理（非 git repo、just 太舊、需詢問無 tty）／失敗（拉不到、`install` 失敗不留半成品、任一 `add` 失敗）；2、3 = `install`／`add` 回的碼原樣傳出 | 同 `install`、`add` | bootstrap(1)(2)；離線包(1)(2) |

## 本頁待拍板

無；六點已定（2026-09-20，codex 一致）：
1. CI 模式定義加「`update` 除外」（第 0 頁、通則 4、update 列）。
2. 驗收 harness 明確設 `CI=0` 跑完整流程；另設 `CI=1` 案例驗唯讀與拒寫。
3. `install`、`uninstall`、`undev`、`prune` 在 CI 模式靠通則；表只寫偏離通則的例外（`dev` 拒絕、`update` 仍查）。
4. `prune` 保留清單 = 鎖定行 ＋ 本機覆寫實際引用的 image（引擎 tag／ID 覆寫有；工具 `path:<dir>` 無）。
5. 引擎內「拉 image 展開」的內部子命令改名 `fetch`，與第 0 頁模組名一致（內部名、不對外）。
6. 第 0 頁 `update` 改「只寫執行紀錄」。

## 出處（定稿時移除）

通則：spec §0、§1.1（`--dry-run`、`--help`、`--timeout` 適用欄）、§1.2 通則；grilling 01 頁四點拍板 2026-09-20／Q23／Q27／19 條-6、新規則 (a)(b)；codex #37–#40、#52、#53。各動詞：spec §1.1 選項總表、§1.2 動詞表、§2 結束碼總表、§2c 動詞×檔案矩陣、§3.4、§3.6 快路徑、§6 訊息文字；install `--no-justfile` = codex #42；uninstall 兩種失敗 = codex #43、spec §1.2 uninstall；add `@<tag>` = codex #44；update CI 例外 = codex #45、6 點定案 ①③；升引擎恢復 = codex #46、spec §3.4（6-2b）；dev 進度檔 = codex #47、新規則 (b)；undev／sync `--timeout` = codex #48／#49、spec §1.1；prune 保留清單 = codex #50、6 點定案 ④；bootstrap `--local` 消歧 = codex #51、spec §1.1 B1；快路徑條件 = codex #55、codex r2 #55（`cache/<repo>/` 存在）、spec §3.6；sync CI 欄 = codex #56、spec §0 CI 模式；「流程」欄改流程名 = codex #35；簡寫歸類 = codex #36／#41。codex r2（`decisions/review/codex_findings_00_02_r2.md`）：`--dry-run` 拉不拉 image = #52、spec §1.1；通則 3 與 prune 列的 prune 例外 = N7／N10、spec §0 進度檔；通則 5 與 uninstall 失敗策略 = N8；「（皆刪）」不含進度檔 = N11；install 寫檔欄基準版 = N12；bootstrap.sh 結束碼原樣傳出 = N13、spec §1.2 bootstrap.sh；升引擎前置順序 = N14、spec §1.2 upgrade (b)；resolve／apply 名詞 = N15（第 0 頁）；快路徑寫完執行紀錄才判 = N16。codex r3（`decisions/review/codex_findings_00_02_r3.md`）：`--local` 判別順序 = R6、spec §1.1 B1；upgrade 補基準版後停止 = R7、spec §1.2 upgrade (1)；既有衝突未解立即 2 停 = R8、spec §1.2 upgrade (0)；通則 1 含 bootstrap.sh = R9、spec §4.10。codex r4（`decisions/review/codex_findings_00_02_r4.md`）：upgrade 前置 ① 含衝突中的檔案失蹤 = S4、spec §1.2 upgrade (0)；「自描述標頭」= S2；copy 型／append 型定義在第 0 頁 = S5。codex r5（`decisions/review/codex_findings_00_02_r5.md`）：upgrade 合併結果解析不過 → 2 留原檔、該檔基準版不推 = T1、spec §2、§4.3。流程名對應主圖頁序見 `review_v2_out/pages.json`（最終以推送後為準）。
