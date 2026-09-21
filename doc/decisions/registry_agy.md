本篇針對 `vendor_kit`（將 `dist/` 打包成 `< 50 MB` 的 `FROM scratch` 純資料多架構 image，下游以 `docker pull` 取得）的使用情境，詳細整理各容器 Registry 的規格上限、計費機制、替代方案與跨 Registry digest 遷移注意事項。

---

### (1) GitHub Container Registry (`ghcr.io`) 限制與規範

#### 1. 公開 Image 的儲存與頻寬
* **費用與配額**：**完全免費且無嚴格容量/流量封頂**。GitHub 官方政策規定所有公開 Packages（包含公開 Container Image）不收取儲存與頻寬費用。
* **GitHub Actions 整合**：由 GitHub-hosted Runner 或 Self-hosted Runner 下載公開 image 亦不產生任何額度扣抵。

#### 2. 私有 Image 的儲存與 Data Transfer 額度及超額計費
* **目前狀態（重要特例）**：截至 2026 年，GitHub 官方文件明定：**「Container Registry（`ghcr.io`）的映像檔儲存與頻寬目前為免費（currently free）」**。GitHub 承諾在未來正式實施計費前，將提供至少 **1 個月的提前通知**。
* **標準 GitHub Packages 額度（若未來恢復/比照 Packages 標準）**：
  | 方案 (Plan) | 包含儲存容量 (Storage) | 每月包含傳輸量 (Data Transfer Out) |
  | :--- | :--- | :--- |
  | **GitHub Free** | 500 MB | 1 GB |
  | **GitHub Pro** | 2 GB | 10 GB |
  | **GitHub Team** | 2 GB | 10 GB |
  | **GitHub Enterprise Cloud** | 50 GB | 100 GB |
  *(註：儲存空間為 GitHub Packages 與 GitHub Actions Artifacts 共用計費)*
* **超額費用（牌價）**：
  * **超額儲存費**：約 **$0.25 USD / GB / 月**（按每小時用量折算，約 $0.008 USD/GB/天）。
  * **超額傳出流量（Data Transfer Out）**：**$0.50 USD / GB**（僅計自 GitHub 外部下載；透過 GitHub Actions 內使用 `GITHUB_TOKEN` 下載者免費）。
  * **傳入流量（Data Transfer In）**：一律免費。

#### 3. 單一 Layer／Manifest 大小上限
* **單一 Layer 大小上限**：**10 GB**（官方明確規定）。
* **單次上傳超時（Upload Timeout）**：**10 分鐘**。
* **Manifest 大小上限**：官方文件**未明訂 Manifest 獨立大小上限**（坊間常提的 4 MB 上限為微軟 Azure Container Registry ACR 之限制，非 GHCR）。實務上多架構 index manifest JSON 通常僅數 KB 至數十 KB，純資料 image 不會觸碰邊界。

#### 4. 匿名 Pull 的 Rate Limit
* **有無像 Docker Hub 的限制？**：**沒有**類似 Docker Hub 的「100 pulls/6h」硬性匿名 pull 次數限制。公開 image 允許匿名 pull。
* **保護機制**：雖然無公開計數器，但底層有 GitHub 全域防濫用與抗 DDoS 限流（Abuse Detection）；若同一來源短時間極高併發請求，會收到 HTTP 429。

#### 5. 已認證 Pull 的 API Rate Limit
* **OCI Distribution 原生操作（`docker pull`）**：沒有公開的每小時 pulls 次數上限。
* **GitHub REST API（若以腳本呼叫 Package 管理 API）**：
  * **個人 PAT（Classic / Fine-grained）**：**5,000 次 / 小時**。
  * **GitHub Enterprise Cloud**：最高 **15,000 次 / 小時**。
  * **GitHub Actions 內的 `GITHUB_TOKEN`**：**1,000 次 / 小時 / Repo**。
  * **未認證 REST API**：**60 次 / 小時**。

#### 6. Tag 數量上限
* **上限**：官方**未明定單一 Package 的 Tag 數量上限**（無 Hard Limit）。
* **實務建議**：大量建置建議搭配保留原則（Retention Policy）或 REST API 定期刪除舊 tag，避免清單過大導致 OCI `tags/list` 翻頁查詢變慢。

> **官方文件參考**：
> - [GitHub Packages 計費說明](https://docs.github.com/en/billing/managing-billing-for-github-packages/about-billing-for-github-packages)
> - [GitHub Container Registry 官方使用與限制指南](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
> - [GitHub REST API 速率限制](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)

---

### (2) GitLab Container Registry（`registry.gitlab.com` 與 Self-Managed）

#### 1. GitLab.com 免費方案（Free）儲存與 Transfer 額度
* **儲存空間（Storage）**：
  * GitLab.com Free 提供每個 Namespace / Project **10 GiB 免費儲存**。
  * **重要現況**：根據 GitLab 官方文件，此 10 GiB 封頂配額**目前僅計算 Git Repository 與 LFS**。**Container Registry、Package Registry 與 CI Artifacts 目前尚未計入 10 GiB 封頂限制中**。
* **傳輸量（Data Transfer / Egress）**：
  * GitLab 曾在 2022 年底宣布對 Free 方案實施每月 10 GB 的 Data Transfer 限制，但因社群強烈反對，該政策**已被無限期擱置（Suspended / Paused）**。目前 GitLab.com **沒有**針對 Container Registry 強制實施 metered transfer 扣抵，UI 亦未對 transfer 提供計費用量報告。

#### 2. 超額行為
* 若 Git + LFS 超過 10 GiB，專案會被鎖定為 **Read-only 狀態**（無法 `git push`、開 MR 或上傳新 LFS）。
* 針對 Container Registry，GitLab 建議在專案設定啟用 **Cleanup Policies** 自動標記與刪除過期 tag，由系統背景跑 Garbage Collection 釋放儲存。

#### 3. 匿名 Pull 是否允許
* **允許**。必須同時符合兩個條件：
  1. 專案 Visibility 設為 **Public**。
  2. 專案的 `Settings > General > Visibility, project features, permissions` 中，將 **Container Registry** 的存取權設為 **Everyone With Access**。
* 若為 Private 專案，則必須使用 Deploy Token、Personal Access Token 或 CI Job Token 登入。

#### 4. Rate Limit
* **GitLab.com SaaS 速率限制**：
  * **未認證請求**：通常為 **500 次 / 分鐘 / IP**。
  * **失敗認證封鎖（Failed Authentication Ban）**：若 1 分鐘內出現 **300 次認證失敗**（包含 Git 與 `/jwt/auth` 容器認證），該來源 IP 會被封鎖（HTTP 403）**15 分鐘**。
  * **已認證請求**：依使用者方案提供約 **2,000 次 / 分鐘** 的 Burst/Sustained 額度。

#### 5. GitLab Self-Managed（自架）有無上限
* **無平台內建上限**：GitLab Self-Managed（無論社群 CE 或企業 EE）的 Container Registry **沒有任何內建的授權容量或傳輸硬上限**。
* **物理邊界**：儲存上限取決於後端掛載的儲存空間（Local Disk、NFS、AWS S3、MinIO 等）及硬體頻寬。
* **速率限制**：管理者可在 `gitlab.rb` 的 `registry['rate_limiter']` 自行開啟、設定或關閉速率閥值。

> **官方文件參考**：
> - [GitLab Usage Quotas 與儲存計算範圍](https://docs.gitlab.com/ee/user/usage_quotas.html)
> - [GitLab Container Registry 使用文件](https://docs.gitlab.com/ee/user/packages/container_registry/)
> - [GitLab.com 專屬速率限制](https://docs.gitlab.com/ee/user/gitlab_com/index.html#gitlabcom-specific-rate-limits)

---

### (3) 其他免費／低成本替代方案

| 平台／工具 | 免費／低成本額度 (標註方案與日期) | Rate Limit (Pull 限制) | 支援多架構 Index | 支援 `FROM scratch` | 特點與適用性 |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Docker Hub** | - **Personal (Free)**：僅 **1 個免費 Private Repo**；Public Repo 無限。<br>- 儲存無明確硬限制。 | - **未認證（匿名）**：**100 pulls / 6 小時 / IP**<br>- **Personal（已認證）**：**200 pulls / 6 小時 / 帳號**<br>- 付費版（Pro/Team）：無此限制。 | **是** | **是** | 知名度最高，但免費用戶之 100/200 次限額極易在 CI/CD 中觸發 429。 |
| **Quay.io** *(Red Hat)* | - **Public Repo**：**完全免費**，儲存與頻寬無限。<br>- **Private Repo**：無免費版，採固定方案（Developer 方案 $15 USD/月 5 個私有 repo，不按流量計費）。 | 公開存取**無硬性 pull 次數限制**（受限於防 DDoS 與濫用防護）。 | **是** | **是** | 公開 image 極佳的替代站點，內建 Clair 弱點掃描。 |
| **AWS ECR Public** | - **儲存**：每月 **50 GB 永久免費**（Always-free），超額 $0.10/GB-月。<br>- **傳輸（Egress）**：<br>  - 匿名下載：**500 GB / 月** 免費。<br>  - AWS 帳號登入：**5 TB / 月** 免費。<br>  - 傳入 AWS Compute：完全免費。 | 公開 Repo 無嚴格次數限制，以流量（500 GB / 5 TB）為限。 | **是** | **是** | 穩定性極高，對於每月 < 50 GB 的公開資料 image 幾乎可常態 0 元。 |
| **Cloudflare R2 + OCI** | - **R2 免費額度**：每月 **10 GB 儲存**、1,000 萬次讀取操作（Class B）。<br>- **Egress**：**0 元（完全無傳出流量費）**。 | 取決於前置 Worker 或自架 Distribution 規格，Cloudflare 本身無 Egress 瓶頸。 | **是** | **是** | **架構方式**：<br>1. 自架 `registry:2`，Storage Driver 設為 S3 指向 R2。<br>2. 採用 Serverless Worker OCI Registry（如社群開源 `cf-workers-oci-registry`）。對於頻繁拉取的小型純資料 image 成本極低。 |
| **CNCF `registry:2`** *(Distribution)* | - **開源免費自架**。 | 無限制（由自行部署之伺服器與網路決定）。 | **是** | **是** | 官方參考實作，極簡輕量，可直接掛載 S3/R2/本地磁碟。 |
| **Harbor** *(CNCF Graduated)* | - **開源免費自架**。 | 無限制（支援自定義 Quota 與 Retention）。 | **是** | **是** | 具備企業級 RBAC、Trivy 弱點掃描、Cosign 簽章驗證、多 Registry 雙向複製鏡像，功能最完整。 |
| **Zot** *(CNCF Sandbox/Incubating)* | - **開源免費自架**。 | 無限制。 | **是** | **是** | 100% OCI-native，單一 Go binary 啟動，極度輕量、啟動極快、原生支援 OCI Artifacts。 |

#### 為什麼全部都支援「多架構 Index」與「`FROM scratch` 純資料 Image」？
1. **多架構 Index**：以上所有 Registry 均完全相容 **Docker Manifest List v2.2**（`application/vnd.docker.distribution.manifest.list.v2+json`）或 **OCI Image Index Specification**（`application/vnd.oci.image.index.v1+json`）。
2. **`FROM scratch`**：在 OCI 規範中，Registry 只是內容定址儲存庫（Content-Addressable Storage, CAS），它將映像檔的 Layers 與 Config 視為不透明的 Blob（未經檢查的 tar 串流與 JSON）。Registry 不會去驗證檔案系統內是否有 Linux 核心、init 或 glibc。因此，任何符合 OCI 規範的 Registry 都天然支援 `FROM scratch`。

> **官方文件參考**：
> - [Docker Hub 下載速率限制官方文件](https://docs.docker.com/docker-hub/download-rate-limit/)
> - [Docker 訂閱與私有 Repo 說明](https://docs.docker.com/subscription/details/)
> - [AWS ECR 定價官方文件](https://aws.amazon.com/ecr/pricing/)
> - [AWS ECR 配額與限制說明](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html)
> - [Quay.io 方案與定價](https://quay.io/plans/)
> - [Cloudflare R2 定價官方文件](https://developers.cloudflare.com/r2/pricing/)

---

### (4) 從 GHCR 換到 GitLab Registry 或自架時，版本鎖定 `<host>/<org>/<name>:<tag>@sha256:<index digest>` 的差異與 Digest 一致性

#### 1. Digest 的計算本質
Container Image 的 Digest 是其 **Manifest JSON 原始位元組串（Raw bytes）的 SHA-256 雜湊值**（即 `sha256(raw_json_bytes)`）。
只要 Manifest JSON 的位元組內容（包含 JSON key 排序、空白字元、換行）未被竄改或重新序列化，該 Digest 就是全球唯一且跨 Registry 不變的。

#### 2. 同一 Image 複製後，Index Digest 是否相同？
這取決於您使用的複製工具機制：

* **使用 `crane copy` 或 `skopeo copy --all`：**
  * **結果：Index Digest 100% 相同，跨 Registry 完全一致**。
  * **原理**：`crane`（Google `go-containerregistry`）與 `skopeo`（Red Hat）是專門為 Registry 間同步設計的工具。它們採用 **Raw Byte-for-Byte Copy** 機制，直接讀取來源端的原始 Index Manifest JSON 與各架構子 Manifest，並原封不動地 `PUT` 至目標 Registry，不解包、不重組 JSON。因此雜湊值絕不改變。
* **使用 `docker buildx imagetools create`：**
  * **結果：單一來源通常相同，但存在重新生成變更的風險**。
  * **原理**：
    * 若僅複製單一來源且來源已是 Index（例如 `docker buildx imagetools create -t <dest> <source>`），Docker 官方規範會執行「Carbon Copy」，盡量保持原始內容。
    * **但要注意**：若在指令中附帶了 `--annotation`、合併多個架構來源、或不同版本的 Buildx/BuildKit 在記憶體內解析後重新生成序列化 JSON（如更換欄位順序或空格），**Index Digest 就會改變**（即便底層各架構 Layer Blob 的 Digest 沒變）。
  * **結論建議**：若要確保跨 Registry 的 Index Digest 絕對一致，**強烈建議使用 `crane copy <src> <dst>` 或 `skopeo copy --all docker://<src> docker://<dst>`**，避免使用 `docker buildx imagetools`。

#### 3. 下游工具以 `<host>/<org>/<name>:<tag>@sha256:<index digest>` 鎖版本的影響
若下游專案採用標準格式鎖定版本：
1. **主機與命名空間路徑必須改寫**：
   * 必須由 `ghcr.io/<org>/<name>` 改為 `registry.gitlab.com/<group>/<name>` 或 `<self-hosted-domain>/<name>`。
2. **Digest 雜湊值無須變更**：
   * 只要遷移時使用 `crane copy` 保留了 Raw Manifest，後方的 `@sha256:<index_digest>` 字串**完全不需要重新計算或變更**，下游可以直接沿用原有雜湊值進行防篡改驗證。
3. **Multi-arch 下的 Client 運作行為**：
   * 當 Docker Client 執行 `docker pull <host>/<name>:<tag>@sha256:<index digest>` 時，Client 會向 Registry 請求該 Index Manifest，再依據當前機器的 CPU 架構（如 `linux/amd64` 或 `linux/arm64`）解析出對應平台的 Sub-manifest，最後下載對應的資料層。
   * 此標準行為在 GHCR、GitLab Registry、Harbor、Zot 或 Distribution 之間完全相容，下游無需修改任何拉取邏輯。
