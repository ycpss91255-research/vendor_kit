# base dist 分發機制調整：討論紀錄

> 日期：2026-09-16
> 範圍：取代 base 目前以 `git subtree` + symlink 分發 dist 的方式。**base 本體（Dockerfile 模板、wrapper、lib 等）不變**，只調整「dist 怎麼送進 downstream repo」。
> 配套圖：`dist_distribution.drawio`（1 vendor_kit 架構圖、2 出貨路徑、3 流程：啟動器、4 流程：版本生命週期、5 流程：安裝工具、6 名詞說明）

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
| vendor_kit | 通用落地引擎 + manifest 規格，打包成 `vendor_kit:vN` image |
| base | 本體不變；release 時 `FROM vendor_kit:vN` 加入 dist、init 模板、manifest，推出 `base-dist:vX` |
| 其他工具（agent_harness …） | 同樣 `FROM vendor_kit`，打包自己的 dist |
| downstream repo | 只記錄使用的版本 + 一個極薄的 launcher（justfile） |

### 檔案所有權（manifest 核心）

| 類別 | 例子 | 行為 | 進 git |
|---|---|---|---|
| tool-owned | wrapper、lib、runtime 腳本 | 每次落地直接覆蓋；不允許手改 | 否（`.base/`） |
| seed-once | Dockerfile、entrypoint、`.setup.conf`、`main.yaml` | init 時建立一次，之後屬於使用者；需變更時輸出 patch 由使用者決定 | 是 |
| opt-in | hooks | 不預設產生 stub，需要時才建立 | 是 |
| 版本記錄 | `.base-ref` | 使用者或 Renovate 修改 | 是 |
| 產生物 | `compose.yaml`、`.env.generated`、印記檔 | 由工具產生 | 否 |

### init

init 仍由 base 提供，只是來源從 subtree 改為 image。init 不是獨立命令，而是 `land` 的內部步驟：每次 land 遇到缺少的 seed-once／opt-in 檔案就建立，已存在則保留（opt-in 需使用者指定才建立）。

## 4. 流程

**執行 `just <verb>`**
1. 讀 `.base-ref`
2. image 不在本地 → `docker pull`
3. `.base/` 印記與 `.base-ref` 不一致、尚未安裝、或印記不可讀 → `docker run --rm`（host UID/GID）執行引擎 `land`；剛落地成功即直接進入第 5 步，不再 verify
4. 印記一致時 → 執行引擎 `verify` 比對 `.base/` 工具檔 hash（不含使用者檔案），被手改則報錯中止
5. 執行 `.base/` 內 wrapper → `docker compose …`

**升級**：改 `.base-ref` → just → 新版 image 落地。升級邏輯在新版 image 內，不會有「舊工具升級自己」的問題。

**回退**：`git revert` `.base-ref` 的變更 → just → 舊版 image 重新落地。不需額外 rollback 紀錄。

## 5. 可追溯性（出 bug 時）

```
downstream commit → .base-ref（版本）→ image label（base commit SHA）→ base 原始碼
```

必要條件：
- image 加 label：base commit SHA、版本、source repo
- `.base/` 內寫印記檔：寫入的版本 + 各檔案 hash
- GHCR 舊版本不刪、tag 不覆蓋（寫成 CI 規則）
- `git bisect` 在 `.base-ref` 上即可定位是哪次升級引入問題

## 6. 可行性注意事項

- container 必須以 host UID/GID 執行，否則落地檔案為 root 擁有
- gitignore 路線下，`docker build` 前必須先落地（launcher 保證順序）；進 image 的 runtime 腳本亦可考慮改為 `COPY --from=base-dist:vX`
- launcher 無法由 dist 分發自己，需極薄、帶契約版本號，過舊時由引擎提示更新
- image 保留、只刪 container；每次重 pull 會變慢、受 rate limit 影響、離線失效
- 離線機器：`docker save` / `docker load` 預載 image
- 需預留**本地開發模式**：來源暫時指向本機 base checkout，開發 base 時不必每次發佈

## 7. 已排除的方向

| 方向 | 排除原因 |
|---|---|
| 以 binary 取代 base 本體 | 誤解範圍；base 本體必須繼續提供 Dockerfile 等內容 |
| 整套工具在 container 內執行並透過 docker.sock 操作 daemon | host 偵測（GPU/X11/DRI/Jetson）靠 mount 拼湊，漏一項即安靜出錯；bind mount 路徑由 daemon 以 host 路徑解析 |
| 自行開發完整 vendoring engine（含獨立 rollback 紀錄等） | 版本由 image 決定、`.base/` 不進 git 後，rollback 與自我升級問題結構上消失 |

## 8. 待決議

| # | 議題 | 目前傾向 |
|---|---|---|
| 1 | `.base-ref` 用 tag、digest，或 `tag@digest` 並寫 | 未定；tag 較易讀，前提是 tag 不可覆蓋。需確認 GHCR 是否有原生 immutable tag 設定 |
| 2 | `.base/` 是否進 git | 傾向不進 git |
| 3 | image 清理策略 | 保留；定期清理未被引用的版本 |
| 4 | image cache 範圍（機器共用 vs 每 repo 隔離） | 未定 |
| 5 | launcher 契約版本與更新方式 | 未定 |
| 6 | 本地開發模式的切換方式 | 未定 |
| 7 | 既有 15 個 repo 的遷移順序 | 建議從 v0.41 直接跳新機制，不先走 v0.42/v0.43 subtree 遷移；試點 urg_node_humble（簡單）+ isaac（複雜） |
| 8 | vendor_kit 既有 issue 的處置 | #7、#13 等 rollback 相關議題可能失效，需逐一重審 |
| 9 | agent_harness 是否納入同一機制 | 其內容（AGENTS.md、skills）必須實體在 repo 且使用者會修改，屬 seed-once 性質，需確認 manifest 能否涵蓋 |
