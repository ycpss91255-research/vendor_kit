import pathlib, sys
def edit(path, pairs):
    p = pathlib.Path(path); s = p.read_text()
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, f"{path}: expected 1 occurrence, got {n}: {old[:80]!r}"
        s = s.replace(old, new)
    p.write_text(s); print("ok", path, len(pairs))

# ---------- 00_terms.md ----------
edit("review/00_terms.md", [
# R1 + R2 + R3：版本鎖定行正規形在第 0 頁完整定義，工具行在 [tools] 表下
("| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（引擎那行的鍵是 `vendor_kit`）；進 git；只有這行決定裝哪一版；唯一正規形見第 1 頁 I18 |",
 "| **版本鎖定行** | lock line | `.vendor_kit/version.toml` 內每個工具（與引擎）各一行；進 git；只有這行決定裝哪一版。**唯一正規形**：引擎行在檔案頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`；工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`（`<repo>` 是未加引號的 TOML 鍵，名稱規則見佔位符）。每行：行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。頂層另有 `schema`、`written_by` 兩個欄位，與 `[tools]` 下的工具行不同層、不會撞名 |"),
# R9：執行紀錄含 bootstrap.sh
("| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞每次執行一檔；不進 git；事後追溯用。",
 "| **執行紀錄** | run log | `.vendor_kit/log/<verb>/<時間戳>-<id>.jsonl`；每個動詞及每次 `bootstrap.sh` 執行各一檔（`bootstrap.sh` 自己那段寫在 `log/bootstrap/`）；不進 git；事後追溯用。"),
# R2 + R3：<repo> 名稱規則
("| **佔位符** | placeholder | `<repo>` 下游 repo 名；",
 "| **佔位符** | placeholder | `<repo>` 下游 repo 名，規則 `[a-z0-9_][a-z0-9_-]*`（小寫、不含句點，才能當 `[tools]` 下未加引號的 TOML 鍵；OCI repo 名本就小寫），`vendor_kit` 保留給引擎、不得作工具名；"),
# R5：工具 recipe
("| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |",
 "| **`dist/`** | dist | 下游 repo 的出貨目錄：`files/`（全部展開到 `cache/`）、`init.toml`、`just/<ns>.just`；其他內容不出貨 |\n| **工具 recipe** | tool recipe | 工具的 `dist/just/<ns>.just` 提供、下游使用者以 `just <ns> …` 執行的 just 指令；相對於 VK 自己的動詞 `just vendor_kit …`。每次執行前自動觸發一次 `sync` |"),
# R6（順帶去掉第 0 頁對第 2 頁的前引）
("`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag（判別規則在第 2 頁 `bootstrap.sh` 列）。",
 "`bootstrap.sh` 的 `--local <image tag／tar>` 另可收本機 image tag，值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag。"),
# 出處
("來源：`decisions/review/codex_findings_00_02.md`（00 頁 #1–#16、用詞 #34／#54）、`decisions/review/codex_findings_00_02_r2.md`（#31、#52、N1–N6、N15；進度檔的 prune 例外 = N7）、`decisions/grilling.md`「02 頁 6 點定案」「兩條新規則」「補三條不變量」「專案定名」（2026-09-20）、`decisions/interface_spec.md` v3.4 §0、§1.1、§1.2、§4.1–§4.6。",
 "來源：`decisions/review/codex_findings_00_02.md`（00 頁 #1–#16、用詞 #34／#54）、`decisions/review/codex_findings_00_02_r2.md`（#31、#52、N1–N6、N15；進度檔的 prune 例外 = N7）、`decisions/review/codex_findings_00_02_r3.md`（R1 正規形寫全於本頁、R2／R3 `<repo>` 名稱規則與 `[tools]` 表、R5 工具 recipe、R6 `--local` 判別順序、R9 執行紀錄含 bootstrap.sh）、`decisions/grilling.md`「02 頁 6 點定案」「兩條新規則」「補三條不變量」「專案定名」「00–02 codex 三審新定案」（2026-09-20）、`decisions/interface_spec.md` v3.5 §0、§1.1、§1.2、§4.1–§4.6。"),
])

# ---------- 01_invariants_roles.md ----------
edit("review/01_invariants_roles.md", [
# R4
("交付物不得依賴 `.vendor_kit/`；binary 可執行性不由 VK 代驗 |",
 "交付物不得依賴 `.vendor_kit/`；交付物的可執行性不由 VK 代驗 |"),
# R1／R2／R3：I18 引用第 0 頁
("- **I18 版本鎖定行唯一正規形**：每工具（與引擎）一行 `<repo> = \"<image>:<tag>@sha256:<digest>\"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。",
 "- **I18 版本鎖定行唯一正規形**：形式照第 0 頁「版本鎖定行」：引擎行在頂層 `vendor_kit = \"<image>:<tag>@sha256:<digest>\"`、工具行在 `[tools]` 表下 `<repo> = \"<image>:<tag>@sha256:<digest>\"`——行首無空白、鍵後一個空白、`=`、一個空白、雙引號字串、無尾端註解、LF 結尾；引擎寫出一律此形。`<repo>` 照第 0 頁名稱規則（小寫、不含句點，能作未加引號的 TOML 鍵），與頂層 `schema`／`written_by`／`vendor_kit` 不同層、不撞名。禁 BOM、禁重複鍵、禁 TOML 表旁路寫法（例如 `[tools.<repo>]`、`[vendor_kit]`）；引擎讀到非正規形 → 1 列出差異、不動。"),
# R9
("- **I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只預覽不寫的執行）必寫一檔。",
 "- **I12 執行紀錄**：每個動詞每次執行（含 help、沒起容器的 sync、只預覽不寫的執行）及每次 `bootstrap.sh` 執行（寫在 `log/bootstrap/`）必寫一檔。"),
# 出處
("來源檔：spec = `decisions/interface_spec.md` v3.4；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`；codex = `decisions/review/codex_findings_00_02.md`；codex r2 = `decisions/review/codex_findings_00_02_r2.md`。",
 "來源檔：spec = `decisions/interface_spec.md` v3.5；grilling = `decisions/grilling.md`；v2.x = `decisions/proposal_v2.md`；review = `interface_spec_review.md`；codex = `decisions/review/codex_findings_00_02.md`；codex r2 = `decisions/review/codex_findings_00_02_r2.md`；codex r3 = `decisions/review/codex_findings_00_02_r3.md`。"),
("| 三方角色表 | spec §3.1、§4.5、§4.7、§7.1、§7.2、§7.3；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則與名詞定案（2026-09-20）；`--dist` 與下游 CI 入口分開 = codex #17；衝突要手動編輯再重跑 = codex #18、spec §1.2 upgrade 結束碼 2 |",
 "| 三方角色表 | spec §3.1、§4.5、§4.7、§7.1、§7.2、§7.3；grilling Q5、Q7、Q21、deploy 包定案；三方寫法 = grilling 審閱規則與名詞定案（2026-09-20）；`--dist` 與下游 CI 入口分開 = codex #17；衝突要手動編輯再重跑 = codex #18、spec §1.2 upgrade 結束碼 2；「交付物的可執行性」= codex r3 R4 |"),
("| I12 | grilling 2026-09-20 新需求、L1–L6 定案、新規則 (a)；v2.12 L4；spec §0、§4.10（訊息 6-38）；順序 = codex #8／#26 |",
 "| I12 | grilling 2026-09-20 新需求、L1–L6 定案、新規則 (a)；v2.12 L4；spec §0、§4.10（訊息 6-38）；順序 = codex #8／#26；含 bootstrap.sh = codex r3 R9、spec §4.10 |"),
("| I18 | spec §4.1 版本鎖定行契約；codex #31（r2 判未修）、codex r2 #31 |",
 "| I18 | spec §4.1 版本鎖定行契約；codex #31（r2 判未修）、codex r2 #31；引用第 0 頁、`[tools]` 表與 `<repo>` 名稱規則 = codex r3 R1–R3、grilling「00–02 codex 三審新定案」 |"),
])

# ---------- 02_verbs.md ----------
edit("review/02_verbs.md", [
# R9
("1. 執行紀錄：不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；建不了 → 1 零寫入，沒有關掉它的選項。",
 "1. 執行紀錄：每個動詞每次執行必寫一檔，`bootstrap.sh` 自己那段亦同（寫在 `log/bootstrap/`）。不寫檔、不拉 image、不起容器的前置檢查（是否 git repo、just 版本）可在建紀錄之前；任何寫入、拉取、起引擎之前必已有紀錄；建不了 → 1 零寫入，沒有關掉它的選項。"),
# R7 + R8
("基準版推到新版（衝突仍推），最後寫鎖定行；先補「鎖定行已新、基準版仍舊」；不帶 `<repo>` 先對全部工具完整預檢",
 "基準版推到新版（衝突仍推），最後寫鎖定行。動手前先看兩個前置：① metadata 記有衝突且檔內仍有衝突標記 → 立即 2 停、不做任何事（先手動解完再重跑）；② 「鎖定行已新、基準版仍舊」→ 只補基準版到鎖定行的版本然後停止、印提示，不查最新版、不升版；兩者都沒有才查最新（或用指定的 `@<tag>`）。不帶 `<repo>` 先對全部工具完整預檢"),
("2 衝突（留標記、基準版仍推，手動編輯後重跑直到乾淨）；3 |",
 "2 衝突（留標記、基準版仍推，手動編輯後重跑直到乾淨；既有衝突未解完就重跑也是 2）；3 |"),
# R6
("`--local` 的值：含 `/` 或以 `.tar` 結尾 → 檔案路徑（必須存在），其餘 → image tag，兩者都成立 → 1 要求改寫；",
 "`--local` 的值依序判別：以 `.tar` 結尾 → 檔案路徑（必須存在，否則 1）；否則值含 `/` 且存在同名檔 → 1 要求消歧；否則 → image tag；"),
# 出處
("快路徑寫完執行紀錄才判 = N16。流程名對應主圖頁序見 `review_v2_out/pages.json`（最終以推送後為準）。",
 "快路徑寫完執行紀錄才判 = N16。codex r3（`decisions/review/codex_findings_00_02_r3.md`）：`--local` 判別順序 = R6、spec §1.1 B1；upgrade 補基準版後停止 = R7、spec §1.2 upgrade (1)；既有衝突未解立即 2 停 = R8、spec §1.2 upgrade (0)；通則 1 含 bootstrap.sh = R9、spec §4.10。流程名對應主圖頁序見 `review_v2_out/pages.json`（最終以推送後為準）。"),
])
