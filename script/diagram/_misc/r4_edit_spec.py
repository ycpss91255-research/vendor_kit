import pathlib
p = pathlib.Path("interface_spec.md"); s = p.read_text()
pairs = [
# 標題
("# vendor_kit 介面規格（interface reference）v3.4（2026-09-20；**v3.4 = codex 二審 00–02 頁",
 "# vendor_kit 介面規格（interface reference）v3.5（2026-09-20；**v3.5 = codex 三審 00–02 頁（新發現 R1–R9）全部採納 + grilling「00–02 codex 三審新定案」，改動見 §10 #161–#168**；v3.4 = codex 二審 00–02 頁"),
# 前版
("`interface_spec.pre_r3.md`（v3.3 = codex 二審併入前）。",
 "`interface_spec.pre_r3.md`（v3.3 = codex 二審併入前）、`interface_spec.pre_r4.md`（v3.4 = codex 三審併入前）。"),
# 來源優先序
("來源優先序（高 → 低）：\n000. v3.4 新併入：",
 "來源優先序（高 → 低）：\n0000. v3.5 新併入：`decisions/review/codex_findings_00_02_r3.md`（R1–R9 全部採納）與 `grilling.md`「00–02 codex 三審新定案」（2026-09-20）：`<repo>` 名稱規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點）；工具版本鎖定行在 `[tools]` 表下、正規形在第 0 頁完整定義；`--local` 判別順序（`.tar` 結尾 → 檔案；否則含 `/` 且存在同名檔 → 6-37；否則 tag）；執行紀錄含每次 bootstrap.sh 執行；名詞「工具 recipe」。\n000. v3.4 新併入："),
# 占位符
("占位符（名詞一律照第 0 頁「00 名詞與縮寫」，`<sub>` 出處註記保留來源原文的舊詞）：`<repo>` 下游 repo 名、",
 "占位符（名詞一律照第 0 頁「00 名詞與縮寫」，`<sub>` 出處註記保留來源原文的舊詞）：`<repo>` 下游 repo 名（名稱規則見 §1.2 add：`[a-z0-9_][a-z0-9_-]*`）、"),
# §0 執行紀錄
("| 執行紀錄 | 每個動詞每次執行（含 help、update、sync 快路徑、prune、`--dry-run`）除印 tty 外必寫一檔 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）：",
 "| 執行紀錄 | 每個動詞每次執行（含 help、update、sync 快路徑、prune、`--dry-run`）及每次 `bootstrap.sh` 執行（自身那段在 `log/bootstrap/`）除印 tty 外必寫一檔 `.vendor_kit/log/<verb>/<UTC-ts>-<id8>.jsonl`（§4.10）："),
# §1.1 --local B1
("離線。值的判別（B1）：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立 → 1 + 6-37。",
 "離線。值的判別（B1，**依序、互斥**）：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 + 6-37 消歧；否則 → image tag（含 `/` 但無同名檔的完整 ref 也是 tag 形）。"),
# §1.2 add <repo> 規則
("`<repo>` 必填，須符合 `[A-Za-z0-9_][A-Za-z0-9_.-]*`、不得為 `vendor_kit`（保留）",
 "`<repo>` 必填，須符合 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點：它是 `[tools]` 下未加引號的 TOML 鍵，句點會被讀成 dotted key；OCI repo 名本就小寫）、不得為 `vendor_kit`（保留）；頂層 `schema`／`written_by`／`vendor_kit` 與 `[tools]` 下的工具鍵不同層、不撞名"),
# §3.3 安全字串
("- **安全字串**（`<kind>`、`<name>`、`<repo>`、`yes|no`、整數）：`[A-Za-z0-9_.-]+`。",
 "- **安全字串**（`<kind>`、`<name>`、`<repo>`、`yes|no`、整數）：`[A-Za-z0-9_.-]+`（`<repo>` 另受 §1.2 add 名稱規則 `[a-z0-9_][a-z0-9_-]*` 限制，是其子集）。"),
# §4.1 契約
("| 版本鎖定行契約 | **每一行唯一正規形**（01 頁 I18）：引擎行 `vendor_kit = \"<ref>\"`、`[tools]` 內每工具一行 `<repo> = \"<ref>\"`（`<ref>` = `<image>:<tag>@sha256:<digest>`）——",
 "| 版本鎖定行契約 | **每一行唯一正規形**（本節為正本；00 頁「版本鎖定行」與 01 頁 I18 引用本節）：引擎行在頂層 `vendor_kit = \"<ref>\"`、`[tools]` 表下每工具一行 `<repo> = \"<ref>\"`（`<ref>` = `<image>:<tag>@sha256:<digest>`；`<repo>` 為未加引號的 TOML 鍵，須符合 §1.2 add 的 `[a-z0-9_][a-z0-9_-]*`，故不含句點、不會成 dotted key；頂層 `schema`／`written_by`／`vendor_kit` 與工具鍵不同層、不撞名，保留名只有 `vendor_kit`）——"),
("| `[tools].<repo>` | string | 每工具 | ",
 "| `[tools].<repo>` | string | 每工具 | `<repo>` 照 §1.2 add 名稱規則（小寫、不含句點）；"),
# §6 6-37
("| 6-37 | `--local` 值既是存在的檔案也像 image tag（B1 兩者皆成立） | `--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請寫 ./<v>，要指定 image 請寫完整 ref（<host>/<org>/<name>:<tag>）。`（結束 1、零寫入）| 需人處理 | <sub>[grilling 2026-09-19 末條；v2.7-2]</sub> |",
 "| 6-37 | `--local` 值不以 `.tar` 結尾、含 `/`、且存在同名檔（B1 第二支） | `--local 的值 <v> 既是存在的檔案也可解讀為 image tag。要指定檔案請用以 .tar 結尾的路徑；要指定 image 請先移走或改名同名檔 <v>。`（結束 1、零寫入）| 需人處理 | <sub>[grilling 2026-09-19 末條；v2.7-2；grilling 三審新定案 2026-09-20；codex r3 R6]</sub> |"),
# §9.2 B1
("| B1 | `--local` 值：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；其餘 → image tag；兩者皆成立 → 1 + 6-37 消歧；不加前綴語法 | grilling 2026-09-19 末條；v2.7-2 |",
 "| B1 | `--local` 值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則含 `/` 且存在同名檔 → 1 + 6-37 消歧；否則 → image tag；不加前綴語法 | grilling 2026-09-19 末條；v2.7-2；grilling 三審新定案 2026-09-20（codex r3 R6） |"),
# §10
("| 160 | §11 | 新增 41–43（`--dry-run` 拉 image 範圍、bootstrap.sh 結束碼、多工具失敗策略） | 本次 |\n\n共 160 處（v3 新增 #58–#95；v3.1 新增 #96–#116；v3.2 新增 #117–#130；v3.3 新增 #131–#147；v3.4 新增 #148–#160）。",
 "| 160 | §11 | 新增 41–43（`--dry-run` 拉 image 範圍、bootstrap.sh 結束碼、多工具失敗策略） | 本次 |\n\n| 161 | 標題、導言 | v3.5；前版 `interface_spec.pre_r4.md`；來源優先序加 0000（codex 三審 findings r3 + grilling 三審新定案） | codex r3 全部採納 |\n| 162 | §1.2 add、導言占位符、§3.3 安全字串、§4.1 欄位表 | `<repo>` 名稱規則改 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點；未加引號的 TOML 鍵不得成 dotted key；OCI repo 名本就小寫）；00 頁佔位符同步 | codex r3 R2；grilling 三審新定案 |\n| 163 | §4.1 版本鎖定行契約 | 工具行明定在 `[tools]` 表下、與頂層 `schema`／`written_by`／`vendor_kit` 不同層不撞名，保留名只有 `vendor_kit`；本節為正規形正本，00 頁「版本鎖定行」寫全正規形、01 頁 I18 改為引用第 0 頁（去掉 00 → 01 的後引） | codex r3 R1、R3；grilling 三審新定案 |\n| 164 | §1.1 `--local`（bootstrap.sh）、§6 6-37、§9.2 B1 | 判別改為依序互斥：以 `.tar` 結尾 → 檔案（必須存在）；否則含 `/` 且存在同名檔 → 1 + 6-37；否則 tag；6-37 觸發條件與訊息文字同步（改用 `.tar` 結尾或移走同名檔）；00 頁選項清單、02 頁 bootstrap.sh 列同步 | codex r3 R6；grilling 三審新定案 |\n| 165 | §0 執行紀錄、§4.10（不變） | 「每個動詞每次執行」補「及每次 bootstrap.sh 執行（`log/bootstrap/`）」；00 頁執行紀錄、01 頁 I12、02 頁通則 1 同步 | codex r3 R9；grilling 三審新定案 |\n| 166 | 00 頁 | 新增名詞「工具 recipe」（`dist/just/<ns>.just` 提供、以 `just <ns> …` 執行；執行前自動觸發 sync）；01 頁角色表「binary 可執行性」改「交付物的可執行性」 | codex r3 R4、R5；grilling 三審新定案 |\n| 167 | 02 頁 upgrade 列（規格 §1.2 upgrade (0)(1) 不變） | 補兩個前置：metadata 記有衝突且檔內仍有標記 → 立即 2 停；「鎖定行已新、基準版仍舊」→ 只補基準版到鎖定版然後停止、印提示；結束碼欄加「既有衝突未解重跑也是 2」 | codex r3 R7、R8 |\n| 168 | §11 | 新增 44–45（`<repo>` 句點 vs 未加引號 TOML 鍵；`--local` 含 `/` 與 `.tar` 結尾非互斥） | 本次 |\n\n共 168 處（v3 新增 #58–#95；v3.1 新增 #96–#116；v3.2 新增 #117–#130；v3.3 新增 #131–#147；v3.4 新增 #148–#160；v3.5 新增 #161–#168）。"),
# §11
("| 43 | 多工具失敗策略：§0「做得完的做完」vs §1.2 uninstall「任一工具 remove 回 1 → 中止」 | codex r2 N8 → 依各動詞：upgrade 做得完的做完、uninstall 中止並列出未處理（§0、01 頁 I4） |\n\n共 43 條。",
 "| 43 | 多工具失敗策略：§0「做得完的做完」vs §1.2 uninstall「任一工具 remove 回 1 → 中止」 | codex r2 N8 → 依各動詞：upgrade 做得完的做完、uninstall 中止並列出未處理（§0、01 頁 I4） |\n| 44 | `<repo>` 名稱：§1.2 add 舊規則 `[A-Za-z0-9_][A-Za-z0-9_.-]*` 允許句點與大寫 vs §4.1／I18 要求工具行為未加引號的 TOML 鍵（`foo.bar = …` 會被讀成 dotted key） | grilling 三審新定案 → `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點；§1.2 add、§4.1）；不採 quoted key（正規形只留一種） |\n| 45 | `--local` 判別：B1「含 `/` 或 `.tar` 結尾 → 檔案；兩者皆成立 → 6-37」把 `./engine.tar` 這種最常見寫法判成歧義 | grilling 三審新定案 → 依序互斥：`.tar` 結尾 → 檔案；否則含 `/` 且存在同名檔 → 6-37；否則 tag（§1.1、§6 6-37、§9.2 B1） |\n\n共 45 條。"),
]
for old, new in pairs:
    n = s.count(old)
    assert n == 1, f"expected 1, got {n}: {old[:90]!r}"
    s = s.replace(old, new)
p.write_text(s); print("ok spec", len(pairs))
