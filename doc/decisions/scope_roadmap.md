# 產品形狀與路線圖

> 每條將來各自併入相關 ADR。範圍已併入 [`review/01_purpose.md`](review/01_purpose.md)。
> 本檔提到的「不變量 N」指 [`doc/decisions/review/02_invariants.md`](review/02_invariants.md) 的第 N 條，「Pn」指 [`doc/decisions/design_principles.md`](design_principles.md) 的設計原則。

## 產品形狀

- **純資料 image 散播、宣告鎖版、快取重建**（不變量 2、7）：工具 repo 推 image；repo 一份宣告；內容從宣告重建，不進 repo 的 git。
- **薄啟動器 + 容器內引擎**（不變量 5、6）：主機三個工具；規則在引擎；啟動器凍結。
- **初始檔建一次、歸使用者、基準版合併升級**（不變量 1）：基準版進 git 作合併祖先；衝突用 git 熟悉的標記解。
- **命名空間下的 recipe、成對、語意固定**（不變量 8）：`just vendor_kit add`、`upgrade`、`dev` 是使用者需要知道的全部。
- **一份 CI 契約腳本**（不變量 3、4）：repo 的 CI 只呼叫 `.vendor_kit/ci/check.sh`；GitHub／GitLab 差異不進引擎。

## 路線圖

### 第一版

- VK recipe 十一個 + `bootstrap.sh`；結束狀態 0/1/2/3；`--dry-run`、`-y`。
- 初始檔逐檔狀態機（純文字基準版合併；二進位只比對不合併；symlink 第一版禁止）；基準版 + metadata。
- `.vendor_kit/` 佈局、自有 `.gitignore`、根 `justfile` 一行。
- `dev <repo> -p <dir>` 與 `dev --engine -i <image>`；驗收 fixture repo 走完整流程；amd64 + arm64 原生 runner。
- Renovate regex preset；`check.sh` 給 repo 的 CI 與工具 repo CI（`--dist`）。
- 決議紀錄：proto 的 ADR-0001／0002 不搬回（內容綁原型實作與已作廢的詞，核心決定已改寫成 `doc/adr/` 的 0002–0012）；[`doc/decisions/review/02_invariants.md`](review/02_invariants.md) 列的「待寫 ADR」已全部落地。

以下是待拍板清單與現況對照。正式內容以 [`review/01_purpose.md`](review/01_purpose.md)、[`review/02_invariants.md`](review/02_invariants.md) 與根 [`CONTEXT.md`](../../CONTEXT.md)（名詞）為準。

| 項目 | 狀態 | 結論 |
|---|---|---|
| 宣告檔名 | 已定案 | 叫 `version.toml`，與 `version.local.toml`、`cache/<repo>/`、自有 `.gitignore` 一起收進 `.vendor_kit/`（原 `.version` 之名作廢）。 |
| `just` 最低版本 | 已定案 | `just >= 1.33.0`（`[group]` 放 `mod` 上需 1.33），一律 GitHub release 下載版，CI 矩陣 1.33.0 + latest，比 1.33 新的功能由 lint 擋。 |
| 工具 image 單架構 | 已定案 | 改為**多架構** amd64+arm64、同一次 buildx、COPY-only，CI 驗兩平台位元組一致；引擎 image 同（只驗兩平台 LABEL 一致）。 |
| 衝突時基準版是否推到新版 | 已定案 | 推：留 `<<<<<<< vendor_kit:baseline` 標記、印檔名、基準版仍推到新版；唯一例外是合併結果為 TOML／just 而解析不過 —— 留原檔、該檔基準版不推、記入 metadata `conflicts`。 |
| Renovate 的初始檔合併由誰做 | 已定案 | VK 無 bot、不 commit、不開 PR；PR 只改一行版本鎖定行，初始檔合併由人在 PR 分支本機 `upgrade <repo> -y` → commit → push，CI 全部再跑一次才 merge。 |
| 多命名空間工具 | 已定案 | 一個工具可出多個 `<ns>`：`dist/just/<ns>.just` 每檔一個頂層命名空間、數量工具自決、`<repo>.just` 必須存在；`gen/tools.just` 每個 `<ns>` 一行 `mod?`（一工具可多行）；`add` 時 `<ns>` 與其他已接工具、根 `justfile` 既有 recipe／module、保留名 `vendor_kit` 撞名 → 1 拒絕。 |
| image 公開／私有 | 已定案 | 引擎 image 公開（不可逆要提醒），工具 image 由各工具 repo 自決；認證是主機／CI 各自的事，VK 只承諾「主機 docker 拉得到就能用」。未給憑證時不支援需認證的版本列舉，回 1 印 6-3 提示設 `VENDOR_KIT_REGISTRY_TOKEN`（或 `_TOKEN_FILE`）或直接指定 `@<tag>`。 |
| `.gitignore` 類初始檔的處理 | 已定案 | 用 append 型：根 `.gitignore`／`.dockerignore`／`.editorconfig` 這類必須 `strategy = "append"`，用 copy 指向它們 → `check.sh --dist` 報錯；無檔則建、已有則問後 append，刪也只刪原文相同的行（6-21，CRLF/LF 等價，零命中或多處只 warn）。VK 自己不碰使用者的 `.gitignore`：`.vendor_kit/.gitignore` 是 VK 擁有的薄殼檔，VK 自己寫的 repo 檔只有根 `justfile` 一行與根 `.dockerignore` 四行。 |

### v2

- `upgrade --adopt <file>`：把 `add` 時已存在、未納管的檔納入合併。
- 進 git 的 `.vendor_kit/files/<repo>/`，讓 compose／GitLab CI 這類「快取不進 git 就讀不到」的引用場景可行。
- 數位簽章／驗簽；多 registry；範本變數渲染——各自先有使用者需求證據（P6）再進範圍。
- vendir 類下載後端：不採用（見 `../adr/0001-why-not-existing-tools.md`）；只在通過該檔 §5 的十項門檻後重評。
