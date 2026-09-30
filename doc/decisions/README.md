# doc/decisions — 現況與去向

這個目錄**不在 skill 結構裡**。skill 只要求四樣東西：根 `GLOSSARY.md`（名詞）、`docs/adr/`（難逆轉的取捨）、`docs/agents/`（三個設定檔）、`AGENTS.md`（工作約定與 Agent skills 段）；spec 與需求走 GitHub issue。這個目錄現在放設計原則、範圍文件與審閱用的工作目錄；對外契約與不變量（審閱頁 01～04）已搬到 `docs/contract/`，研究紀錄搬到 `docs/research/`（理由見 `AGENTS.md`「決議與文件流程」）。本檔是這個目錄的地圖，審閱頁也一併列在這裡。

三段：**保留** = 現在還在用；**已歸檔** = 原本的 `_legacy` 目錄，已搬出 repo、只留在維護者本機（相對 repo 根目錄是 `../reference/_legacy`），只作參考；**待處理** = 等使用者拍板存廢。

## 保留

### 審閱頁（四頁）

四頁都在 `docs/contract/`。名詞不在這裡：名詞表是根 `GLOSSARY.md`（skill 四樣之一）。

| 檔 | 是什麼 | 最終去向 |
|---|---|---|
| [01 目的與承諾](../../docs/contract/01_purpose.md) | 目的與承諾：痛點、VK 做什麼、對導入、出貨與相容性承諾什麼。已定案。 | 留在 `docs/contract/`：對外契約在 repo 內的權威文件。 |
| [02 不變量](../../docs/contract/02_invariants.md) | 十一條不變量：只記性質。機制已在 2026-09-28 併進各自的 ADR（`docs/adr/` 裡各條列出的 ADR），本頁只留回連。審閱中。 | 留在 `docs/contract/`：性質留一份權威文件，ADR 直接連到它。 |
| [03 訊息與錯誤碼總表](../../docs/contract/03_messages.md) | 結束碼的意思，與 VK 印出、要使用者動手處理的訊息與固定編號；沿用 02 的規則時寫「依第 N 條」。審閱中。 | 留在 `docs/contract/`：對外契約在 repo 內的權威文件。 |
| [04 使用者介面](../../docs/contract/04_interface.md) | 全部 VK recipe 與選項。沿用 01、02 的規則時寫「依第 N 條」，結束碼與訊息連到 03，不重述。審閱中。 | 留在 `docs/contract/`：對外契約在 repo 內的權威文件。 |

### 從已移除的 PRD 拆出來的兩份

| 檔 | 是什麼 | 最終去向 |
|---|---|---|
| [設計原則](design_principles.md) | 設計原則 P1–P6 與衝突優先序。在不變量之下、個別決議之上的判準。 | 每條併進相關 ADR 的決定與理由或 `## Considered Options`。 |
| [範圍與路線圖](scope_roadmap.md) | 產品形狀五條 + 路線圖 + 待拍板清單。 | 路線圖進 GitHub milestone + issue；產品形狀已由 01 頁涵蓋；待拍板項目各開一個 `needs-triage` issue。 |

### 工作用的目錄

| 目錄 | 是什麼 | 最終去向 |
|---|---|---|
| `review_log/` | 審閱頁（01–04）的審閱往返：codex brief／output、Claude 子代理審查紀錄。舊輪次的子目錄已歸檔（跟著原本的 `_legacy` 目錄搬到 repo 外的本機參考目錄）。另有 `versions.json`：`mark_changes.py` 記各鍵版本號的檔，進 git，不屬於審閱往返。 | 審閱往返在審閱頁定案後就沒有讀者，見「待處理」；`versions.json` 在 `mark_changes.py` 還在用時留著。 |
| `_backup/` | 每輪改動前的快照（`<路徑攤平>.pre_rNN.md`），`script/mark_changes.py` 靠它產生改動標示。 | 定案後只有 `mark_changes.py` 還需要最近一輪。見「待處理」。 |
| `_marked/` | `mark_changes.py` 的輸出：新增綠底、被取代的舊文字紅底，給維護者審閱用。只有對外文件（根目錄 README.md 與審閱頁 01～04）產標示版；內部文件（本檔、`AGENTS.md`、`script/README.md` 等）不產。已在 `.gitignore`，是產生物。 | 每輪重新產生，不需要保留。 |
| `_legacy`（已搬出） | 原本放已歸檔的檔案；已搬到 repo 外、只留維護者本機的 `../reference/_legacy`，不進 git。見下一段。 | 本機參考用，確認清楚之後刪。 |

## 已歸檔（repo 外的 `../reference/_legacy`）

這些檔已從 repo 移除，只留在維護者本機，下面的路徑都相對那個目錄。它的 `README.md` 已經寫了「引用這裡的事實之前先確認它還成立」與舊詞→新詞對照表。這裡只說分類。共 103 MB。

| 分類 | 內容 | 為什麼不再用 |
|---|---|---|
| 設計研究 | `base_corpus.md`、`base_pitfalls*.md`、`prior_art*.md`、`compat*.md`、`isolation*.md`、`lock.md`、`diff3.md`、`upgrade.md`、`multiarch.md`、`policy.md`、`devmode.md`、`contract.md` 等 | 9/17–9/19 的逐題研究，結論已進審閱頁、根 `GLOSSARY.md` 或待寫 ADR；敘述用的是已廢止的舊名（「三方」、「專案根」、「動詞」）。 |
| 介面規格 | `interface*.md`（含 185 KB 的 `interface_spec.md`）、`proposal_v1/v2.md`、`remaining.md` | spec 改走 GitHub issue，不留本地規格檔。節次編號（`§4.5`）只在檔內有意義。 |
| 定案流水帳 | `grilling.md` | 逐題追問與定案紀錄。Q 編號只在檔內有意義；要引用當初的定案，寫日期加定案內容。 |
| agy／codex 原始輸出 | `agy/`、`log/`、`review/codex_*`、`review_log/`（舊輪次：`codex_r2`–`codex_r9`、`codex_review`、`r12_codex`、`r13_codex`、`r15_codex`、`review_v1`，共 152 檔 59 MB） | 9/17–9/21 的雙軌審查往返，對象是已作廢的圖頁與舊版名詞。 |
| 舊審閱頁 | `review/01-03_名詞與縮寫.md`、`review/04-05_不變量與角色.md`、`review/terms_moved.md`、`review/invariants_roles.md`、`review/verbs.md`、`review/CONTEXT.draft.md`、`review/legend_page.md`、`review/02_terms.md` | 前七份當時被 01／02 兩頁取代（歷史；當時取代後是 01～03，現為 01～04）；`02_terms.md`（名詞與縮寫）的內容已重寫進根 `GLOSSARY.md`，本檔隨即退場。 |
| 後來補歸檔 | `review/_changes_r63.md`（手寫對照表，已被 `script/mark_changes.py` 取代，內文用「導入根」舊名）、`review/_variants/`（承諾關係三種呈現草稿，已擇一定案）、`dist_distribution_notes.md`（主圖討論紀錄，用三方模型舊名詞） | 見括號。 |
| issue 草稿 | `issues/`（`close_*.md`、`d11`–`d13`、`reframe_14.md`）、`issue_deploy_split*.md` | 已貼上 GitHub，本地副本不同步。 |
| 外部參考 | `wf/`（20 個上游 repo 的 GitHub Actions workflow）、`verify/`（ADR 抓取與 issue JSON） | 一次性取樣，要用再抓。 |
| 圖檔審查產物 | `drawio_audit/`（9 個 `.drawio-audit-*` 目錄 + `files.zip`，35 MB） | draw.io 編輯期間的自動快照。（歷史：還在 repo 內時，`.gitignore` 的 `.drawio-audit-*/` 與 `files.zip` 兩條擋著它們，所以從沒進 git。） |

## 待處理（等使用者拍板）

### 1. 兩個 `.drawio` 主檔

**是什麼**：`dist_distribution.drawio`（主圖 12 頁，457 KB）與 `discussion.drawio`（77 頁，3.4 MB）。

**為什麼卡住**：畫的是舊模型（舊名「三方角色」、「專案根」、「動詞」）。審閱頁 01～04 與根 `GLOSSARY.md` 已改用新名詞，圖沒跟上。`AGENTS.md` 寫「架構圖不是插圖，是測試的依據……模組邊界與泳道由 lint 強制」，但那個 lint 還沒寫，所以現在圖與文字沒有任何機制擋住脫鉤。

**選項**：(a) 依新名詞重畫（成本高：77 頁討論圖是產生器輸出，得先改產生器）；(b) 廢掉兩個檔，等實作階段需要時重畫需要的那幾頁；(c) 留在原位當歷史，檔頭標「舊模型，不要引用」，並把 `AGENTS.md` 那條「圖是測試依據」降級為「待重畫後生效」。

### 2. `script/diagram/`

**是什麼**：圖的產生器與審查工具。19 MB、216 個 `.py`。其中 `_backup/`（17 MB，`gen2`–`gen56`、`make_gen*`、各種 `.v*` 後綴）是歷代痕跡，`_misc/`（900 KB，53 個一次性 patch／診斷腳本）多數假設 cwd 有已不存在的 `v2_only.drawio`。

**為什麼卡住**：依賴的圖頁已作廢（跟第 1 項綁在一起）。`verify_r15.py`、`verify_r16.py` 指向 `decisions/review/terms.md`，但這個檔早就不存在（名詞表現在是根 `GLOSSARY.md`，而且不是逐字上圖了），兩支腳本現在跑起來必定失敗。

**選項**：(a) 整個 `script/diagram/` 歸檔（移到 repo 外的本機參考目錄）；(b) 只留通用的四支（`extract_pages.py`、`lint_pages.py`、`shrink_png.py`、`drawio_common.py`）加 `review_v2_README.md`，其餘歸檔。已歸檔的 `diagram-review-v2` workflow 當時的前置步驟就是跑前三支；(c) 全留，只刪 `verify_r15/16.py` 這類明確壞掉的。

`script/mark_changes.py` 不在此列，它是現在每輪都在用的工具，留。

### 3. `doc/decisions/` 這個目錄本身（已定）

這個目錄刻意用來放設計原則和範圍文件，不是過渡產物。對外契約原本也放這裡，現在搬到 `docs/contract/`；它放 repo、不放 issue：issue 不好追蹤改動，也做不了逐頁審與標示版差異。出處：`AGENTS.md`「決議與文件流程」。

### 4. `design_principles.md` 與 `scope_roadmap.md` 的落點

**是什麼**：從已移除的 `doc/PRD.md` 拆出來的兩份。

**為什麼卡住**：兩份都在等「併進相關 ADR」。相關 ADR 已於 2026-09-28 全部落地（`docs/adr/` 0001–0012），ADR 也已改成 skill 的 ADR 格式、不再有 `> Serves:` 回連，所以前置條件都消失了；剩下的只是決定怎麼併。[ADR-0001](../../docs/adr/0001-why-not-existing-tools.md) 的重評門檻現在寫在它的 Consequences，`design_principles.md` 與 `scope_roadmap.md` 仍以「§5」稱呼那份清單。

**選項**：(a) 留在原位；(b) 現在就把設計原則搬成一份 ADR（原則本身就是難逆轉的取捨），`scope_roadmap.md` 的路線圖進 milestone、待拍板項目各開一個 issue；(c) `scope_roadmap.md` 先動（純轉成 issue，沒有依賴），`design_principles.md` 等 ADR。

### 5. `_backup/`

**是什麼**：每輪改動前的快照。`script/mark_changes.py` 讀 `_backup/docs_contract_<頁名>.<後綴>.md`（路徑攤平的命名；搬目錄前的 `doc_decisions_review_<頁名>` 也認）產生改動標示。

**為什麼卡住**：git 已經有完整歷史，這裡是重複的。但 `mark_changes.py` 的工作流程需要「上一輪的檔」而不是「某個 commit 的檔」，直接刪會讓現在正在用的審閱流程斷掉。

**選項**：(a) 只留每個檔最新的一份快照，其餘刪；(b) 全部歸檔到 repo 外，並改 `mark_changes.py` 從 `git show <ref>:<path>` 取舊版；(c) 審閱頁 01～04 都定案後整個刪，那時 `mark_changes.py` 也不再需要。

### 6. `review_log/`

**是什麼**：審閱頁（01–04）的審閱往返。舊輪次的子目錄已搬走。

**為什麼卡住**：裡面有 codex 與 Claude 兩方的完整審查意見，但「哪幾條被採納、為什麼」只散在往返裡，沒有結論檔。直接歸檔會丟掉「這條當初討論過並否決了」這種資訊。

**選項**：(a) 每輪寫一段結論摘要（採納／否決＋一句理由），原始往返歸檔到 repo 外；(b) 全部歸檔到 repo 外，接受「要查就去翻」；(c) 留在原位直到審閱頁定案。

另外：`review_log/` 裡還留著 9/17–9/22 的舊輪次單檔（`codex_policy_*`、`r2_findings.txt`、`review_v2r2`–`review_v2r15_*`、`codex_brief_r16`–`r19`、`claude_r17_terms.md`，其中 `codex_out_r16.md` 一個檔 440 KB）。當時只搬了子目錄，這些單檔沒動；要不要一起歸檔，跟本項一起決定。

### 7. proto 的 ADR-0001、0002（已完成）

**是什麼**：`docs/adr/README.md` 當時的索引表（歷史；索引表已拿掉）原本註明兩份 ADR「在 `../proto/vendor_kit/docs/adr/`，待搬回」。

**結論（2026-09-28）**：不搬回、不引用。兩份綁原型的 Python 實作與已作廢的詞（舊宣告檔名、舊的工具目錄寫法、乙版、`ensure`／`verify` 這兩個已不存在的 recipe、只畫四條 recipe 的泳道），核心決定已改寫進本 repo 的 `docs/adr/`：測試分層進 ADR-0011，引擎與工具 image 分離進 ADR-0006 與 ADR-0007。原本的 ADR-0003（為什麼不用現成工具）因此改編號為 ADR-0001，機制 ADR 從 0002 連號到 0012。

**隨之改掉的**：索引表重建（歷史；索引表後來隨 ADR 改成 skill 格式一起拿掉）、`docs/agents/domain.md` 的「先去 proto 讀」整段刪除、`doc/decisions/scope_roadmap.md` 的「ADR-0001／0002 搬回」改成「不搬回」。

### 8. `docs/agents/domain.md` 的檔案結構區塊（已完成）

`domain.md` 原本有一個 `## 檔案結構` 區塊，用樹狀圖列出 agent 該讀的檔，每次搬檔都會過時。已採選項 (b)：樹狀圖整段移除，只留「動手之前先讀這些」那四個檔。原先記的三處不對也隨之消失：`dist_distribution_notes.md` 那一行連同樹一起沒了；`GLOSSARY.md` 現在不提 `discussion.drawio` 的頁數，`script/diagram/README.md` 的「77 頁」跟檔案實際頁數一致。

編號保留，不重排 1–7。剩下的只有一個沒拍板的餘項：要不要寫一支 lint 檢查文件裡的路徑都存在（原選項 (c)），掛進 `just test`。目前 `AGENTS.md`、`issue-tracker.md`、`triage-labels.md`、`docs/adr/*` 的路徑引用都對得上。
