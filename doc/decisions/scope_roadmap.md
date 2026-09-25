# 範圍、產品形狀與路線圖

> 原出處 `doc/PRD.md`，PRD 已移除；每條將來各自併入相關 ADR。
> 本檔提到的「不變量 N」指 [`doc/decisions/review/03_invariants.md`](review/03_invariants.md) 的第 N 條，「Pn」指 [`doc/decisions/design_principles.md`](design_principles.md) 的設計原則。

## 範圍

### 納入

- 工具 `dist/` 的**打包**（`Dockerfile.dist`、純資料 image）與**散播**（registry、tag@digest）。
- **鎖版**：repo 對「用哪些工具、哪個版本、哪個引擎」的唯一宣告，與從宣告決定性重建快取。
- **初始檔管理**：`init.toml` 宣告的檔在 repo 裡建立一次、之後歸使用者、升級時基準版合併、永不刪。
- **本機開發模式**：把某個工具（含 vendor_kit 自身）指向本機目錄或本機 image。
- **repo 的 CI 契約檢查腳本**：repo 的 CI 只呼叫它；它以結束狀態回報「宣告、快取、初始檔是否一致」。

**母體用推導，不列清單（P6）。** 初始檔要支援哪些類型（純文字、二進位、symlink、目錄），看工具實際在 `init.toml` 用了什麼；一個類型進入支援範圍，是因為有工具在用，不是因為它存在。

### 刻意排除

- **工具本身的功能**：`docker build`、compose 產生、部署等由工具的 just 模組提供；vendor_kit 只負責把模組送到 repo 並掛進命名空間。
- 多 registry 雙推、簽章／驗簽（第一版）、範本變數渲染。
- macOS、Windows 原生（WSL2 視同 Linux，在範圍內）。
- repo 的業務邏輯；工具 repo 之間的相容矩陣。

## 產品形狀

- **純資料 image 散播、宣告鎖版、快取重建**（不變量 2、7）：工具 repo 推 image；repo 一份宣告；內容從宣告重建，不進 repo 的 git。
- **薄啟動器 + 容器內引擎**（不變量 5、6）：主機三個工具；規則在引擎；啟動器凍結。
- **初始檔建一次、歸使用者、基準版合併升級**（不變量 1）：基準版進 git 作合併祖先；衝突用 git 熟悉的標記解。
- **命名空間動詞、成對、跟 base**（不變量 8）：`just vendor_kit add/upgrade/dev` 是使用者需要知道的全部。
- **一份 CI 契約腳本**（不變量 3、4）：repo 的 CI 只呼叫 `.vendor_kit/ci/check.sh`；GitHub／GitLab 差異不進引擎。

## 路線圖

### 第一版

- 引擎子命令與九個動詞 + `bootstrap.sh`；結束狀態 0/1/2；`--dry-run`、`-y`、`--porcelain`。
- 初始檔逐檔狀態機（純文字基準版合併；二進位只比對不合併；symlink 第一版禁止）；基準版 + metadata。
- `.vendor_kit/` 佈局、自有 `.gitignore`、根 `justfile` 一行。
- `dev -p <dir>` 與 `dev vendor_kit -i <image>`；驗收 fixture repo 走完整流程；amd64 + arm64 原生 runner。
- Renovate regex preset；`check.sh` 給 repo 的 CI 與工具 repo CI（`--dist`）。
- ADR-0001／0002 搬回本 repo 並補 `> Serves:`；[`doc/decisions/review/03_invariants.md`](review/03_invariants.md) 列的「待寫 ADR」全部落地。

> ⚠ 待拍板（彙整）：宣告檔名；`just` 最低版本；工具 image 單架構；衝突時基準版是否推到新版（避免重跑再衝突）；Renovate 路徑由 PR 作者本機補合併（vs CI bot commit）；多命名空間工具；image 公開／私有；`.gitignore` 類初始檔的處理。

### v2

- `upgrade --adopt <file>`：把 `add` 時已存在、未納管的檔納入合併。
- tracked 的 `.vendor_kit/files/<repo>/`，讓 compose／GitLab CI 這類「快取不進 git 就讀不到」的引用場景可行。
- 簽章／驗簽；多 registry；範本變數渲染——各自先有使用者需求證據（P6）再進範圍。
- vendir 類下載後端：不採用（見 `../adr/0003-why-not-existing-tools.md`）；只在通過該檔 §5 的十項門檻後重評。
