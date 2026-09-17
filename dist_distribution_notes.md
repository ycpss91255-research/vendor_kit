# base dist 分發機制調整：討論紀錄

> 日期：2026-09-16
> 範圍：取代 base 目前以 `git subtree` + symlink 分發 dist 的方式。**base 本體（Dockerfile 模板、wrapper、lib 等）不變**，只調整「dist 怎麼送進 downstream repo」。
> 配套圖：`dist_distribution.drawio`（1 vendor_kit 架構圖、2 框架定義、3 流程：使用者指令、4 流程：版本生命週期、5 流程：vendor_kit 內部、6 原型對照、7 資料夾架構、8 測試分層與強制閘門、9 使用者介面：just 指令表；名詞表在各頁底部）
> 圖面審查：每輪改完跑 `.claude/workflows/diagram-review.js`（Claude 子代理 + codex 雙軌審查）
> 可執行原型：`../proto/`（vendor_kit / tool / project 三個資料夾，見 §9）

---

## 1. 現況問題（實際掃描 ycpss91255-docker org）

| 問題 | 觀察 |
|---|---|
| 版本漂移 | 14 個 repo 停在 v0.41.0；jetson_sdk_manager v0.39.0；isaac v0.42.0；base 已到 v0.43.0-rc2 |
| 卡在 layout 遷移前 | v0.42 的 `dist/` 重構與 `.setup.conf` 搬遷，只有 isaac 完成 |
| workflow pin 混用 | ros_distro / ros2_distro 的 `main.yaml` 同時有 `@v0.41.0` 與 `@v0.20.0` |
| 複製過量 | urg_node_humble 160 個檔案中 119 個在 `.base/`（約 74%）；isaac 的 `.base/` 含 base 自己的 115 個 test 檔與 37 個 doc 檔 |
| hook stub 雜訊 | 每 repo 14 個 stub，全 org 只有 4 個有實際內容（isaac ×2、realsense_ros1/2 ×1） |
| 分發機制各自發明 | base（subtree）、agent_harness（自有 init/upgrade）、multi_run（`.template_version`） |
| 自我升級缺陷 | agent_harness 註解記錄：base 曾因升級搬走 upgrade.sh，導致下一次升級失敗 |

## 2. 核心約束

- Host 只安裝 **Docker + Git + just**（不可要求 Python 等）
- 允許使用網路（可從 GHCR pull image）

## 3. 決策：以 GHCR image 分發 dist

**一句話：base 發佈時把 dist 打包成 image 推上 GHCR；downstream 執行 image，由它把 dist 寫進 repo，跑完 container 即刪除。**

### 角色分工

| 元件 | 職責 |
|---|---|
| vendor_kit | 通用安裝工具（`install / init / verify / diff`），打包成 `vendor_kit:vN` image；本身以 Python 實作、只在容器內執行。安裝目錄 `.<name>/`，name = `.version` 裡的工具名（由啟動器以 `--name` 傳入） |
| base | 本體不變；release 時 `FROM vendor_kit:vN` 加入 `dist/` 與 `init.toml`，推出 `base-dist:vX` |
| 其他工具（agent_harness …） | 同樣 `FROM vendor_kit`，打包自己的 dist |
| downstream repo | 只記錄使用的版本 + 一個極薄的 launcher（justfile） |

### 出貨規則（只有兩條）

1. **`dist/` 底下全部出貨**，寫進下游的 `.<name>/`（name = 工具名；base 就是 `.base/`）；每次 upgrade 整批覆蓋（原子替換），下游不可改。base 今天的 `upgrade.sh` 第 1 步 `git subtree pull` 就是這個行為，只是範圍從整個 repo 縮到 `dist/`。
2. **`init.toml` 列的檔案**，`init` 時再複製一份到指定路徑；已存在則跳過，之後歸下游所有，upgrade 不碰。

```toml
# init.toml（放在工具 repo 根目錄，跟 dist/ 一起進 image）
[[file]]
src  = "dockerfile/Dockerfile"     # 相對 dist/
dest = "Dockerfile"                # 相對下游 repo 根目錄

[[file]]
src  = "template/hooks/"           # 目錄整個複製
dest = "script/hooks/"
```

| 類別 | 例子 | 行為 | 進 git |
|---|---|---|---|
| `dist/` 全部 | wrapper、lib、runtime、模板、config、smoke 測試 | 每次 upgrade 整批覆蓋 | 否（`.base/`） |
| `init.toml` 列的 | Dockerfile、entrypoint、setup.toml、main.yaml、hooks、.gitignore | init 建立一次，之後屬於使用者；upgrade 時 `diff` 顯示差異、不自動改 | 是 |
| 版本記錄 | `.version` | 由 Renovate 或 `just upgrade` 改；使用者只 merge | 是 |
| 產生物 | `compose.yaml`、`.env`、印記檔 | 由工具產生 | 否 |

hooks 由 init 明確生成（對齊 `init.sh` 現況），不設 opt-in 類別。

**與 base 今天 `upgrade.sh` 的差異（刻意改變）**：今天第 3～5 步會自動改寫使用者的 `Dockerfile`、`script/entrypoint.sh`（`dockerfile_migrate.sh` 的 16 個遷移）、`main.yaml`（`@tag` sed）、`.gitignore`。新架構下工具不改使用者檔：
- `main.yaml` 的 `@tag` → Renovate github-actions manager 更新
- `Dockerfile` 遷移 → `just diff` 顯示，使用者自己改。**前提是 base 遵守 ADR-0006 的 `dist/` 路徑契約不亂搬**；那 16 個遷移的根因幾乎全是 base 內部搬路徑
- `.gitignore` → 列入 `init.toml`，init 建一次
- 若日後仍需自動遷移，加明確的 `just upgrade --migrate`，預設不動（待決議）

### init

`init` 是獨立命令（`just init`），只在專案第一次接上工具時執行一次；`install` 永不建立或修改使用者檔案（使用者刻意刪除的檔案不會復活）。`init` 對已存在的檔案一律跳過，所以新舊 repo 用同一個指令。

### 自動提醒（升級）

- **Renovate**（主要）：`customManagers` 用 regex 追蹤 `.version` 中 `ghcr.io/…:tag@sha256:…`（`datasourceTemplate: docker`；tag 為 `currentValue`、digest 為 `currentDigest`），上游有新版就開 PR；15 個 repo 共用一份 preset。PR 的 CI 跑 install + wrapper smoke test。
- **`just upgrade`**（手動備援）：查 GHCR 最新版 → 改 `.version` → install → diff。細節待議。
- base 端 release 時可加 `repository_dispatch` 推播給 downstream 當即時通知（選配）。

### 前例與定位

方案沒有完整前例；各部分對應：Gradle Wrapper（薄啟動器 + 版本檔 + 自動下載）、Dev Container Features / Homebrew bottles（GHCR 當檔案倉庫、digest 鎖版本）、Copier（初始檔歸使用者 + 升級 diff）、Carvel vendir（宣告式目錄同步的 manifest/lock 設計）、OpenAPI Generator docker CLI（以 image 出貨、bind mount 寫回專案）。

## 4. 流程

**執行 `just <verb>`**
1. 讀 `.version`
2. image 不在本地 → `docker pull`
3. `.<name>/` 印記與 `.version` 不一致、尚未安裝、或印記不可讀 → `docker run --rm`（host UID/GID）執行 `install`；剛安裝成功即直接進入第 5 步，不再 verify
4. 印記一致時 → 執行 `verify` 比對 `.<name>/` 每檔 hash，被手改則報錯中止
5. 執行 `.<name>/` 內 wrapper → `docker compose …`

**升級**：改 `.version` → just → 新版 image 落地。升級邏輯在新版 image 內，不會有「舊工具升級自己」的問題。

**回退**：`git revert` `.version` 的變更 → just → 舊版 image 重新落地。不需額外 rollback 紀錄。

## 5. 可追溯性（出 bug 時）

```
downstream commit → .version（版本）→ image label（base commit SHA）→ base 原始碼
```

必要條件：
- image 加 label：base commit SHA、版本、source repo
- `.base/` 內寫印記檔：寫入的版本 + 各檔案 hash
- GHCR tag 不覆蓋；仍被任何 downstream `.version` 引用的版本不可刪（寫成 CI 規則；未被引用版本的清理策略見 §8 第 3 項）
- `git bisect` 在 `.version` 上即可定位是哪次升級引入問題

## 6. 可行性注意事項

- container 必須以 host UID/GID 執行，否則落地檔案為 root 擁有
- gitignore 路線下，`docker build` 前必須先落地（launcher 保證順序）；進 image 的 runtime 腳本亦可考慮改為 `COPY --from=base-dist:vX`
- launcher 無法由 dist 分發自己，需極薄、帶契約版本號，過舊時由引擎提示更新
- image 保留、只刪 container；每次重 pull 會變慢、受 rate limit 影響、離線失效
- 離線機器：`docker save` / `docker load` 預載 image
- 需預留**本地開發模式**：來源暫時指向本機 base checkout，開發 base 時不必每次發佈
- **rootless Docker / userns-remap / 遠端 daemon**：`-u UID:GID` 不通吃、bind mount 掛不到遠端；要偵測並明寫支援範圍
- **多架構**：Apple Silicon、Jetson 需各自的 vendor_kit image；`.version` 鎖 image **index** digest
- **私有 GHCR**：使用者與 Renovate 各自需要 token
- **替換原子性**：並行 `just`、安裝中斷 → 先寫暫存目錄再換名，並加 lock
- **驗證邊界**：印記可被寫，驗證基準應來自鎖定的 image；比對檔案集合、執行權限、symlink，不只內容 hash
- **`diff` 需三方比對**（舊模板→新模板 vs 使用者檔→新模板），否則使用者修改會淹沒真正的升級需求

## 7. 已排除的方向

| 方向 | 排除原因 |
|---|---|
| 以 binary 取代 base 本體 | 誤解範圍；base 本體必須繼續提供 Dockerfile 等內容 |
| 整套工具在 container 內執行並透過 docker.sock 操作 daemon | host 偵測（GPU/X11/DRI/Jetson）靠 mount 拼湊，漏一項即安靜出錯；bind mount 路徑由 daemon 以 host 路徑解析 |
| 自行開發完整 vendoring engine（含獨立 rollback 紀錄等） | 版本由 image 決定、`.base/` 不進 git 後，rollback 與自我升級問題結構上消失 |

## 8. 待決議

| # | 議題 | 目前傾向 |
|---|---|---|
| 1 | `.version` 記什麼 | **已定**：一個 `.version` 檔（TOML，`[tools]` 下一個工具一行 `name = "ghcr.io/…:tag@sha256:…"`）；digest 鎖內容、tag 供 Renovate 判斷版本系列；name 決定安裝目錄 `.<name>/` |
| 2 | `.<name>/` 是否進 git | **已定**：不進 git |
| 3 | image 清理策略 | 被引用的版本一律保留；未被引用的版本可定期清理（週期未定） |
| 4 | image cache 範圍（機器共用 vs 每 repo 隔離） | 未定 |
| 5 | launcher 契約版本與更新方式 | 傾向 `justfile` 由 vendor_kit 出貨（因為它綁 vendor_kit 子命令介面）；第一次進專案的 bootstrap 方式未定 |
| 6 | 本地開發模式的切換方式 | 未定 |
| 7 | 既有 15 個 repo 的遷移順序 | 建議從 v0.41 直接跳新機制，不先走 v0.42/v0.43 subtree 遷移；試點 urg_node_humble（簡單）+ isaac（複雜） |
| 8 | vendor_kit 既有 issue 的處置 | #7、#13 等 rollback 相關議題可能失效，需逐一重審 |
| 9 | agent_harness 是否納入同一機制 | 其內容（AGENTS.md、skills）屬 init.toml 類；先做只服務 base 的最小版本，再驗證通用性 |
| 10 | 是否保留自動遷移 `just upgrade --migrate` | 預設不動；等 dist 路徑契約穩定後再評估 |
| 11 | `diff` 是否做三方比對（舊模板→新模板 vs 使用者檔→新模板） | §6 建議三方；圖與原型目前是二方，待決 |
| 12 | `verify` 的基準：印記檔 vs 重新從 image 取；是否比對檔案集合、權限、symlink | §6 建議從 image；圖與原型目前只比印記的內容 hash，待決 |
| 13 | 並行安裝的 lock | §6 建議要；圖與原型目前只有暫存目錄＋原子改名，待決 |
| 14 | 模板是否帶入變數（專案名等）渲染 | 目前只複製；圖上標「待定」 |

## 9. 出貨物清單（安裝後 downstream repo 的實際樣貌）

image 只是運送容器，不會出現在 repo；repo 裡看到的是安裝工具從 image 寫出來的檔案。以同時使用 base 與 agent_harness 的專案為例：

```
my_robot_project/
├── .version                ← 進 git   Renovate／just upgrade 改；一行一個工具（tag@digest）
├── justfile                ← 進 git   啟動器；第一次由人放進去，之後幾乎不動
├── Dockerfile              ← 進 git   使用者檔案：第一次安裝時從 base 模板建立，之後歸使用者
├── entrypoint.sh           ← 進 git
├── setup.toml              ← 進 git
├── .github/workflows/main.yaml ← 進 git
├── script/hooks/           ← 進 git   init 建立的 stub
├── AGENTS.md               ← 進 git   使用者檔案：來自 agent_harness 模板
├── .base/                  ← 不進 git  base 的工具檔，每次安裝整批重寫，不可手改
│   ├── wrapper/ lib/ runtime/
│   └── .stamp              ←            印記檔：安裝版本 + 每個檔案的指紋
├── .harness/               ← 不進 git  agent_harness 的工具檔，同上
├── compose.yaml            ← 不進 git  wrapper 執行時產生
└── .env.generated          ← 不進 git
```

`.version` 範例：

```toml
[tools]
base    = "ghcr.io/ycpss91255-docker/base-dist:v0.43.0@sha256:3f2a9c…"
harness = "ghcr.io/ycpss91255-research/agent_harness-dist:v0.5.2@sha256:8b1d…"
```

`git ls-files` 只會看到 `.version`、`justfile`、使用者檔案；`.base/`、`.harness/` 是第一次跑 `just` 才長出來的。

## 10. vendor_kit repo 結構與測試分層（第 7、8 頁；決策日期 2026-09-17）

**決策：單一 container、單一 Python package（7 個模組），但測試分層與隔離全部用「強制閘門」實現，不靠提醒或紀錄。**

### 目錄（tool-first：`test/<工具>/<層級>/`）

```
vendor_kit/
├── src/vendor_kit/        cli.py dist_reader.py repo_fs.py template.py stamp.py diff.py report.py（= 第 1 頁 7 個模組）
├── test/
│   ├── env/check.sh            環境檢查（smoke）：python3 ≥ 3.11、tomllib、vendor_kit 進入點、toml-bridge、WORKDIR
│   ├── lint/{ruff,import-linter}/ + mirror_check.py + blackbox_check.py
│   ├── pytest/unit/            test_<模組>.py ×7（鏡射 src）
│   ├── pytest/integration/     test_install.py test_init.py test_verify.py test_perf_verify.py test_diff.py
│   ├── pytest/system/          docker run 整個 image（CI 主機）
│   ├── pytest/acceptance/      第 3 頁三條泳道：假專案裡真的打 just（CI 主機）
│   ├── fixtures/               假 dist/、init.toml、VERSION、project/（假專案：justfile）、tool_image/（假工具 image 的 Dockerfile）
│   └── (system / acceptance 各有 conftest.py：sys.modules["vendor_kit"] = None)
├── Dockerfile                  runtime 的基底 = toml-bridge image（ghcr.io/ycpss91255-docker/toml-bridge@sha256:0a01f9…，提供 Python 與 TOML 工具）
│                               stage：runtime → env-test → test-base → lint / unit-test / install-test / init-test / verify-test / diff-test；runtime → release → release-test
├── docker-bake.hcl             group validate（env-test + 六個測試 stage）、group release（release + release-test）
└── doc/adr/
```

### 強制閘門（違反就 CI 紅）

| 層 | 閘門 | 實作 |
|---|---|---|
| smoke（環境檢查） | `env-test` stage 跑 `test/env/check.sh`；`test-base FROM env-test`，所以環境不對就沒有任何測試會跑（環境檢查先於一切） | `env-test` stage |
| lint | ruff；黑箱檢查；import-linter 契約（cli → dist_reader\|repo_fs → template\|diff\|stamp\|report；cli/template/diff/stamp/report 不准直接 import pathlib/shutil/os/io）；鏡射檢查（每個 src 模組必有 test_<模組>.py） | `lint` stage |
| unit | conftest 把 open()/Path.read_*/write_*/socket 換成 `pytest.fail` | `unit-test` stage |
| integration | conftest 禁 subprocess/socket；只給 tmp 目錄；只走 `cli.main()`；一個子命令一個 stage、各自只 COPY 自己的檔；`verify` 200 檔 < 0.5s | 四個 `*-test` stage |
| system / acceptance | lint 的 `blackbox_check.py`：測試檔不准 import vendor_kit；conftest 再把 `sys.modules["vendor_kit"]` 設為 None；只准 docker run／just + 檔案系統 | CI 主機（`.github/workflows/ci.yaml`） |
| release | `release` 只 FROM `runtime`（BuildKit 不會執行、也不會打包任何 test stage）；`release-test` FROM release 真的跑一次 install + verify，失敗就不 push | `release`、`release-test` stage |

前例：Docker multi-stage test stage、Google Small/Medium/Large、pytest src layout、import-linter；ROS 2 `system_tests`／REP-2004、Linux KUnit（in-tree）vs kselftest（out-of-tree）。層級名稱依 ISTQB（unit / integration / system / acceptance）；smoke 是類型不是層級：這裡指 env-test，先於所有測試。

原型狀態（2026-09-17）：`docker buildx bake validate` 六個 stage 全綠；`bake release` 含 release-test（install + verify）通過；system 4 個、acceptance 4 個測試在主機 pytest 通過；`proto/project` 的 `just init / build / diff` 走完整流程；ADR-0001「測試分層與強制閘門」已寫（`proto/vendor_kit/doc/adr/`）。

## 11. 使用者介面：just 指令表（第 9 頁）

使用者只會碰 justfile 提供的指令；每個指令執行前都先自動走第 3 頁「日常」的檢查（`_ensure`：印記第一行 ≠ .version → install；相同 → verify；verify 失敗就中止）。

**vendor_kit 提供（每個專案都一樣）**

| 指令 | 什麼時候 | 做什麼 | 背後 |
|---|---|---|---|
| `just init` | 第一次接上工具 | 安裝 `.<name>/`，照 init.toml 建立初始檔（已存在不動） | 容器：install → init |
| `just diff` | 升級之後 | 顯示新版模板 vs 你的初始檔差異，不改檔 | 容器：diff |
| `just upgrade` | 沒有 Renovate 時手動升級 | 改 .version 為最新 → 重裝 → 顯示差異（細節待議，§8 #5） | 查 GHCR → 改 .version → install → diff |
| （自動 `_ensure`） | 每個指令前 | 檢查／安裝／驗證 | 容器：install 或 verify |

verify 不開放給使用者單獨打：它是每個指令前的守門。

**工具 `<name>` 提供（由工具的 dist/ 決定，每個工具可以不同；以「容器工作流」工具為例）**

| 指令 | 做什麼 | 背後 |
|---|---|---|
| `just build` | 建置專案自己的 image | `.<name>/` 的 build 腳本 → docker compose build |
| `just run` | 啟動專案容器 | run 腳本 → docker compose up |
| `just exec` | 進到容器裡下指令 | exec 腳本 → docker compose exec |
| `just stop` | 停掉並移除容器 | stop 腳本 → docker compose down |

為什麼是這四個：一個容器的一生 = 做出來 → 開起來 → 進去用 → 關掉，一個階段一個指令；換工具就換一套。每個工具指令前後可掛使用者自己的 hooks（`script/hooks/pre|post/<指令>.sh`，init 建立的空殼）。
