# doc/decisions — 現況與去向

這個目錄**不在 skill 結構裡**。skill 只要求四樣東西：根 `CONTEXT.md`（名詞）、`doc/adr/`（難逆轉的取捨）、`doc/agents/`（三個設定檔）、`AGENTS.md`（工作約定與 Agent skills 段）；spec 與需求走 GitHub issue。這裡的每一份檔都是過渡產物，各自有一條退場路線。本檔就是那張地圖。

三段：**保留** = 現在還在用；**已歸檔** = 原本的 `_legacy/`，已移出 git、只留在維護者本機（相對 repo 根目錄是 `../reference/_legacy`），只作參考；**待處理** = 等使用者拍板存廢。舊內容在 git 歷史與 tag `archive/pr-59`。

## 保留

### 審閱中的兩頁

名詞不在這裡：名詞表是根 `CONTEXT.md`（skill 四樣之一）。

| 檔 | 是什麼 | 最終去向 |
|---|---|---|
| [`review/01_purpose.md`](review/01_purpose.md) | 專案目的與承諾：痛點、VK 做什麼、對三種角色各承諾什麼。已定案。 | 承諾條目拆進 ADR 或 issue；範圍與路線圖進 milestone。拆完退場。 |
| [`review/02_invariants.md`](review/02_invariants.md) | 十一條不變量：只記性質。機制已在 2026-09-28 併進各自的 ADR（`doc/adr/` 0002–0012），本頁只留回連。審閱中。 | 性質留一份權威文件（ADR 的 `> Serves:` 要指得到它）。 |

### 從已移除的 PRD 拆出來的兩份

| 檔 | 是什麼 | 最終去向 |
|---|---|---|
| [`design_principles.md`](design_principles.md) | 設計原則 P1–P6 與衝突優先序。在不變量之下、個別決議之上的判準。 | 每條併進相關 ADR 的 `## Decision`／`## Alternatives`；`doc/adr/README.md` 的 `> Serves:` 規則現在指向本檔，併完要一起改。 |
| [`scope_roadmap.md`](scope_roadmap.md) | 產品形狀五條 + 路線圖 + 待拍板清單。 | 路線圖進 GitHub milestone + issue；產品形狀已由 01 頁涵蓋；待拍板項目各開一個 `needs-decision` issue。 |

### 工作用的目錄

| 目錄 | 是什麼 | 最終去向 |
|---|---|---|
| `review_log/`（已移出 git） | 審閱頁的審閱往返：codex brief／output、Claude 子代理審查紀錄。本機保留、已 gitignore。 | 本機參考用，不進 git。見「待處理」第 6 項。 |
| `_backup/`（已移出 git） | 每輪改動前的快照（`<路徑攤平>.pre_rNN.md`），`script/doc/mark_changes.py` 靠它產生改動標示。本機保留、已 gitignore。 | 本機用，不進 git。見「待處理」第 5 項。 |
| `review/_marked/` | `mark_changes.py` 的輸出：新增綠底、被取代的舊文字紅底，給使用者逐頁審閱用。已在 `.gitignore`，是產生物。 | 每輪重新產生，不需要保留。 |
| `_legacy/`（已移出 git） | 原本放已歸檔的檔案；只留維護者本機的 `../reference/_legacy`。見下一段。 | 本機參考用，確認清楚之後刪。 |

## 已歸檔（repo 外的 `../reference/_legacy`）

這些檔已從 git 移除，只留在維護者本機，下面的路徑都相對那個目錄。它的 `README.md` 已經寫了「引用這裡的事實之前先確認它還成立」與舊詞→新詞對照表。這裡只說分類。共 103 MB。

| 分類 | 內容 | 為什麼不再用 |
|---|---|---|
| 設計研究 | `base_corpus.md`、`base_pitfalls*.md`、`prior_art*.md`、`compat*.md`、`isolation*.md`、`lock.md`、`diff3.md`、`upgrade.md`、`multiarch.md`、`policy.md`、`devmode.md`、`contract.md` 等 | 9/17–9/19 的逐題研究，結論已進審閱頁、根 `CONTEXT.md` 或待寫 ADR；敘述用的是已廢止的舊名（「三方」、「專案根」、「動詞」）。 |
| 介面規格 | `interface*.md`（含 185 KB 的 `interface_spec.md`）、`proposal_v1/v2.md`、`remaining.md` | spec 改走 GitHub issue，不留本地規格檔。節次編號（`§4.5`）只在檔內有意義。 |
| 定案流水帳 | `grilling.md` | 逐題追問與定案紀錄。Q 編號只在檔內有意義；要引用當初的定案，寫日期加定案內容。 |
| agy／codex 原始輸出 | `agy/`、`log/`、`review/codex_*`、`review_log/`（舊輪次：`codex_r2`–`codex_r9`、`codex_review`、`r12_codex`、`r13_codex`、`r15_codex`、`review_v1`，共 152 檔 59 MB） | 9/17–9/21 的雙軌審查往返，對象是已作廢的圖頁與舊版名詞。 |
| 舊審閱頁 | `review/01-03_名詞與縮寫.md`、`review/04-05_不變量與角色.md`、`review/terms_moved.md`、`review/invariants_roles.md`、`review/verbs.md`、`review/CONTEXT.draft.md`、`review/legend_page.md`、`review/02_terms.md` | 前七份被現在的 01／02 兩頁取代；`02_terms.md`（名詞與縮寫）的內容已重寫進根 `CONTEXT.md`，本檔隨即退場。 |
| 本輪剛歸檔 | `review/_changes_r63.md`（手寫對照表，已被 `script/doc/mark_changes.py` 取代，內文用「導入根」舊名）、`review/_variants/`（承諾關係三種呈現草稿，已擇一定案）、`dist_distribution_notes.md`（主圖討論紀錄，用三方模型舊名詞） | 見括號。 |
| issue 草稿 | `issues/`（`close_*.md`、`d11`–`d13`、`reframe_14.md`）、`issue_deploy_split*.md` | 已貼上 GitHub，本地副本不同步。 |
| 外部參考 | `wf/`（20 個上游 repo 的 GitHub Actions workflow）、`verify/`（ADR 抓取與 issue JSON） | 一次性取樣，要用再抓。 |
| 圖檔審查產物 | `drawio_audit/`（9 個 `.drawio-audit-*` 目錄 + `files.zip`，35 MB） | draw.io 編輯期間的自動快照。**注意：`.gitignore` 的 `.drawio-audit-*/` 與 `files.zip` 兩條在新位置仍然生效，所以它們沒進 git，只留在工作區。** |

## 待處理（等使用者拍板）

### 1. 兩個 `.drawio` 主檔 —— 已完成

**是什麼**：`dist_distribution.drawio`（主圖 12 頁）與 `discussion.drawio`（77 頁），畫的是舊模型。

**結論（#35，#164 執行）**：舊圖不進 git，副本留在 workspace 的 `reference/diagram_legacy/`；舊內容也在 git 歷史。只有最新的一份（原 `research/diagram_proposals/proposal_claude_v3.drawio`）進 git，放在 `doc/diagram/architecture.drawio`，以舊模型畫成，之後依新名詞重畫（#138）。`research/diagram_proposals/` 的其他 proposal 一併移出，`research/` 因此移除。

### 2. `script/diagram/` —— 已完成

**是什麼**：圖的產生器與審查工具。

**結論（#35，#164 執行）**：舊圖的產生器（`gen57.py`、`gen_disc.py`、`disc_v1_*.py`）跟舊圖放在一起，移出 git，副本在 workspace 的 `reference/diagram_legacy/script_diagram/`。可重用的工具（`check_overflow.py`、`check_overlap.py`、`lint_pages.py`、`extract_pages.py`、`shrink_png.py`、`drawio_common.py`）與 `README.md`、`STYLE.md` 留著，等 #138 重做時處理。

`script/doc/mark_changes.py` 不在此列，它是現在每輪都在用的工具，留。

### 3. `doc/decisions/` 這個目錄本身

**是什麼**：本目錄。不在 skill 結構裡。

**為什麼卡住**：名詞已經進了根 `CONTEXT.md`，剩下 01／02 兩頁要分流（承諾→ADR 或 issue、不變量→見下面選項、範圍與路線圖→issue／milestone），分流完這個目錄就該消失。但分流的落點還沒定：不變量的「性質」現在沒有對應的 skill 位置——ADR 記機制，`> Serves:` 要指向不變量，那不變量本身放哪？

**選項**：(a) 不變量升格成一份 ADR（0004「十一條不變量」），`doc/decisions/` 整個消失；(b) 不變量併進根 `CONTEXT.md` 的一個章節，跟名詞同一份；(c) 保留 `doc/decisions/` 但只放這兩頁，當作 skill 結構之外刻意保留的第五樣，並在 `AGENTS.md` 講明為什麼。

### 4. `design_principles.md` 與 `scope_roadmap.md` 的落點

**是什麼**：從已移除的 `doc/PRD.md` 拆出來的兩份。

**為什麼卡住**：兩份都在等「併進相關 ADR」。相關 ADR 已於 2026-09-28 全部落地（`doc/adr/` 0001–0012），所以這個前置條件消失了；但 `doc/adr/README.md` 的必要段落規則規定每份 ADR 的 `> Serves:` 要能指向這兩份——併掉它們就得同時改那條規則。

**選項**：(a) 留在原位，等改 `> Serves:` 規則時一併處理；(b) 現在就把設計原則搬成一份 ADR（原則本身就是難逆轉的取捨），`scope_roadmap.md` 的路線圖進 milestone、待拍板項目各開一個 issue；(c) `scope_roadmap.md` 先動（純轉成 issue，沒有依賴），`design_principles.md` 等 ADR。

### 5. `_backup/` —— 已完成

**是什麼**：每輪改動前的快照（路徑攤平的命名）。

**結論（#142）**：移出 git，本機保留、已 gitignore；舊內容在 git 歷史與 tag `archive/pr-59`。`script/doc/mark_changes.py` 照舊讀本機的 `_backup/`。（歷史：原本的選項是只留最新快照、改用 `git show` 取舊版，或審閱頁定案後整個刪。）

### 6. `review_log/` —— 已完成

**是什麼**：審閱頁的審閱往返。

**結論（#142）**：移出 git，本機保留、已 gitignore；舊內容在 git 歷史與 tag `archive/pr-59`。（歷史：原本的選項是每輪寫結論摘要、全部歸檔，或留在原位直到兩頁分流完成。）

### 7. proto 的 ADR-0001、0002 —— 已完成

**是什麼**：`doc/adr/README.md` 索引表原本註明兩份 ADR「在 `../proto/vendor_kit/doc/adr/`，待搬回」。

**結論（2026-09-28）**：不搬回、不引用。兩份綁原型的 Python 實作與已作廢的詞（舊宣告檔名、舊的工具目錄寫法、乙版、`ensure`／`verify` 這兩個已不存在的 recipe、只畫四條 recipe 的泳道），核心決定已改寫進本 repo 的 `doc/adr/`：測試分層進 ADR-0011，引擎與工具 image 分離進 ADR-0006 與 ADR-0007。原本的 ADR-0003（為什麼不用現成工具）因此改編號為 ADR-0001，機制 ADR 從 0002 連號到 0012。

**隨之改掉的**：索引表重建（只有本 repo 的 0001–0012，沒有 proto 的列）、`doc/agents/domain.md` 的「先去 proto 讀」整段刪除、`doc/decisions/scope_roadmap.md` 的「ADR-0001／0002 搬回」改成「不搬回」。

### 8. `doc/agents/domain.md` 的檔案結構區塊 —— 已完成

`domain.md` 原本有一個 `## 檔案結構` 區塊，用樹狀圖列出 agent 該讀的檔，每次搬檔都會過時。已採選項 (b)：樹狀圖整段移除，只留「動手之前先讀這些」那四個檔。原先記的三處不對也隨之消失——`dist_distribution_notes.md` 那一行連同樹一起沒了；`CONTEXT.md` 現在不提 `discussion.drawio` 的頁數，`script/diagram/README.md` 的「77 頁」那行已隨舊圖移出 git 刪除（#164）。

編號保留，不重排 1–7。剩下的只有一個沒拍板的餘項：要不要寫一支 lint 檢查文件裡的路徑都存在（原選項 (c)），掛進 `just test`。目前 `AGENTS.md`、`issue-tracker.md`、`triage-labels.md`、`doc/adr/*` 的路徑引用都對得上。
