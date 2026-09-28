# 容器 registry 上限與替代品 —— 事實查證摘要

- 來源：`decisions/registry_agy.md`（agy 2026-09-19 產出）+ Claude 以 WebFetch 抽查官方文件（2026-09-19）。
- 抽查結果欄：**✔** 官方頁面逐字確認；**△** 部分確認／有出入；**✘** 找不到官方依據或與官方不符；**—** 未抽查。

## (1) GHCR（ghcr.io）

| 項目 | 數字／規則 | 方案 | 來源 | 抽查結果 |
|---|---|---|---|---|
| 公開 package 儲存／頻寬 | 免費（"GitHub Packages usage is free for public packages"） | 全部 | [About billing for GitHub Packages](https://docs.github.com/en/billing/managing-billing-for-github-packages/about-billing-for-github-packages) | ✔ |
| Container registry（含私有）儲存／頻寬 | **目前免費**（"currently free"），政策變更前至少提前 1 個月通知 | 全部 | 同上 | ✔ |
| Packages 標準額度（目前不套用於 ghcr.io，僅供未來參考） | Free 500 MB／1 GB·月；Pro 2 GB／10 GB·月；Team 2 GB／10 GB·月；Enterprise Cloud 50 GB／100 GB·月 | 各方案 | 同上 | ✔ |
| 超額單價 | agy：儲存 $0.25/GB·月、傳出 $0.50/GB | — | 同上 | △ 該頁**未列單價**，只說「用 pricing calculator 估算」；數字為 agy 從他處帶入，未證實 |
| Actions 內下載 | 用 GitHub Actions 下載 package 不計入 hosting repo 的 transfer 用量 | 全部 | 同上 | ✔ |
| 單一 layer 大小上限 | 10 GB | 全部 | [Working with the Container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) | ✔ |
| 上傳逾時 | 10 分鐘 | 全部 | 同上 | ✔ |
| Manifest 大小上限 | 官方未明訂（agy 說 4 MB 是 Azure ACR 的限制） | — | 同上 | ✔（確認官方頁無此數字） |
| 匿名 pull 公開 image | 允許（"You can also access public container images anonymously"） | 全部 | 同上 | ✔ |
| 匿名 pull rate limit | 官方**無公布**類似 Docker Hub 100/6h 的數字；agy 稱有全域防濫用 429 | — | 同上 | △ 官方頁確認「沒寫任何 pull rate limit」；「防濫用 429」為 agy 推論，無來源 |
| 已認證 docker pull rate limit | 官方無公布 | — | 同上 | ✔（確認未寫） |
| REST API（package 管理 API，非 docker pull）速率 | 未認證 60/h；PAT 5,000/h；`GITHUB_TOKEN` 1,000/h/repo；Enterprise Cloud 15,000/h | — | [Rate limits for the REST API](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) | ✔ |
| Tag 數量上限 | 官方未明訂 | — | Container registry 頁 | ✔（確認未寫） |

## (2) GitLab Container Registry

| 項目 | 數字／規則 | 方案 | 來源 | 抽查結果 |
|---|---|---|---|---|
| 儲存上限 | **每專案 10 GiB**（gitlab.com Free namespace） | Free | [Storage usage quotas](https://docs.gitlab.com/ee/user/storage_usage_quotas/) | ✔（agy 寫「Namespace / Project」，官方是 per project） |
| 10 GiB 計算範圍 | 只算 Git repository + LFS；**container registry、package registry、artifacts 不計入** | Free | 同上 | ✔ |
| 超額行為 | 專案變 read-only，無法 push | Free | 同上 | ✔ |
| Transfer（egress）限制 | agy：2022 年底宣布 Free 10 GB/月後「無限期擱置」；目前無計量扣抵 | Free | agy 引 usage_quotas.html（**已失效，301→302 至登入頁**） | △ 官方 storage 頁**未提任何 transfer 限制**；[Reduce container registry data transfer](https://docs.gitlab.com/user/packages/container_registry/reduce_container_registry_data_transfer/) 只說「Transfer usage is not available within the GitLab UI」；「擱置」說法無官方 URL 佐證 |
| 匿名 pull | 允許：專案 Public 且 registry visibility = Everyone With Access（API: `enabled`） | 全部 | [GitLab container registry](https://docs.gitlab.com/user/packages/container_registry/) | ✔ |
| 未認證 rate limit | 500 req/min/IP | gitlab.com | [GitLab.com rate limits](https://docs.gitlab.com/user/gitlab_com/rate_limits/) | ✔ |
| 已認證 API rate limit | 目前 2,000 req/min/user；**即將改為分級：Free 100／Premium 1,250／Ultimate 2,000 每分鐘**（第三方文章稱 2026-10-19 生效，未經官方頁確認日期） | 各方案 | 同上 | △ agy 未提分級變更 |
| 失敗認證封鎖 | 1 分鐘 300 次失敗（Git + `/jwt/auth` 合計）→ 封 15 分鐘（HTTP 403） | gitlab.com | 同上 | ✔ |
| Registry 專屬 pull rate limit | 官方無另列 | — | 同上 | ✔（確認未寫） |
| 專案改名限制 | 有 container repo 的專案 ≤ 1,000 個 container repository 才能改名 | 全部 | container registry 頁 | ✔（agy 未提） |
| Self-managed | 無內建授權容量／傳輸上限；`registry['rate_limiter']` 可自設 | CE/EE | agy 引 [administration/packages/container_registry](https://docs.gitlab.com/administration/packages/container_registry/) | — 未抽查（合理：上限由後端儲存決定） |

## (3) 其他替代

| 項目 | 數字／規則 | 方案 | 來源 | 抽查結果 |
|---|---|---|---|---|
| Docker Hub 匿名 pull | 100 pulls / 6 h / IPv4 或 IPv6 /64 | 未認證 | [Docker Hub usage](https://docs.docker.com/docker-hub/usage/)、[pulls](https://docs.docker.com/docker-hub/usage/pulls/) | ✔ |
| Docker Hub Personal pull | docs：**200 / 6 h**；[docker.com/pricing](https://www.docker.com/pricing/) 卻寫 **100 pulls/hr**（兩頁不一致，以 docs 為準但要標明） | Personal | 同上 | △ |
| Docker Hub Pro/Team/Business pull | Unlimited（fair use） | 付費 | 同上 | ✔ |
| Docker Hub 多架構計算 | multi-arch image **每個架構各算一次 pull**；version check 不計 | 全部 | pulls 頁 | ✔（agy 未提，對 CI 影響重要） |
| Docker Hub 免費私有 repo | 1 個 | Personal | usage 頁、pricing 頁 | ✔ |
| Docker Hub abuse limit | 另有每 IP「數千 req/min」級別的防濫用 429，所有方案皆適用 | 全部 | usage 頁 | ✔（agy 未提） |
| Quay.io | agy：公開免費無限；Developer $15/月 5 私有 repo | — | quay.io/plans | ✘ 抽查時頁面回錯誤，無法確認 |
| AWS ECR Public 儲存 | 50 GB/月 always-free | — | [ECR pricing](https://aws.amazon.com/ecr/pricing/) | ✔ |
| AWS ECR Public 傳出 | 匿名 500 GB/月；登入 AWS 帳號 5 TB/月；到任何 AWS region 的 compute 免費無限 | — | 同上 | ✔（agy 寫「超額 $0.10/GB-月」該頁未列，未證實） |
| Cloudflare R2 免費 | 10 GB-月儲存；Class A 100 萬／月；Class B 1,000 萬／月；egress 免費（僅 Standard storage） | Free | [R2 pricing](https://developers.cloudflare.com/r2/pricing/) | ✔ |
| registry:2 / Harbor / Zot | 自架無上限 | — | agy 無 URL | — 常識級，未抽查 |
| 多架構 index 與 `FROM scratch` 支援 | 所有 OCI 相容 registry 皆支援（registry 只存 blob，不檢查 rootfs） | — | OCI image-spec / distribution-spec | — 推論正確，未逐一抽查 |

## (4) 跨 registry 換站與 digest 鎖版本

| 項目 | 數字／規則 | 來源 | 抽查結果 |
|---|---|---|---|
| Digest 定義 | manifest/index **原始位元組**的 sha256；位元組不變則 digest 跨 registry 不變 | OCI distribution-spec / image-spec（agy 未附 URL） | — 與規範一致 |
| `crane copy` | 官方描述："Efficiently copy a remote image from src to dst **while retaining the digest value**" | [crane copy doc](https://github.com/google/go-containerregistry/blob/main/cmd/crane/doc/crane_copy.md) | ✔；注意若加 `--platform` 會只複製單一平台（index digest 就不同），不帶 `--platform` 才整個 index 原樣複製 |
| `skopeo copy --all` | 原樣複製整個 index | agy 無 URL | — 未抽查 |
| `docker buildx imagetools create` | 單一來源通常 digest 不變；加 `--annotation`、合併多來源或重新序列化時 index digest 會變 | agy 無 URL | — 未抽查；建議改用 crane/skopeo 避免風險 |
| 鎖版本字串 | 只換 `<host>/<org>/<name>`，`@sha256:<index digest>` 不必變 | 推論 | ✔ 邏輯正確 |

## 對 vendor_kit 的影響（事實推論）

1. **留在 GHCR 目前零成本**：公開 image 明文免費；私有 ghcr.io 儲存／頻寬「currently free」但 GitHub 保留 1 個月通知後開始計費的權利。若有私有工具 image，需在設計上假設未來會套用 Packages 額度（Free 500 MB／1 GB·月）——純資料 image < 50 MB 儲存不成問題，但 1 GB·月 transfer 會在數十次外部 pull 後用完；GitHub Actions 內用 `GITHUB_TOKEN` 下載不計。
2. **GHCR 匿名 pull 沒有公布的計數上限**：官方頁明確沒寫任何 pull rate limit，所以「CI 每次 pull 會被 100/6h 打到」的顧慮**只適用於 Docker Hub**，不適用於 GHCR。但也沒有 SLA 保證，agy 說的「防濫用 429」無來源。
3. **若換 Docker Hub**：多架構 image 每個架構各算一次 pull；匿名 100/6h 對共用 IP 的 CI（GitHub-hosted runner）極易觸發。不建議。
4. **若換 GitLab.com Free**：container registry 不計入 10 GiB，儲存上無壓力；匿名 pull 可開；但 transfer 額度**官方頁面找不到明確數字**，且用量在 UI 不可見，屬未知風險；另 authenticated API 即將降為 Free 100 req/min（會影響用 API 清理 tag 的腳本，不影響 docker pull）。
5. **若自架（registry:2 / Zot / Harbor 掛 R2）**：R2 egress 免費、10 GB 免費儲存足夠純資料 image，但要自負可用性。
6. **Digest 鎖版本可跨 registry 沿用**：以 `crane copy`（不帶 `--platform`）或 `skopeo copy --all` 搬遷，`@sha256:<index digest>` 不變，下游只需改 host 前綴；用 `docker buildx imagetools create` 搬遷有 digest 改變的風險。vendor_kit 的鎖版本格式不需為換站重新設計，但需要一個「host 可替換」的設定點。

## agy 可疑或無來源的說法

- GHCR 超額單價「$0.25/GB·月、$0.50/GB」：官方 billing 頁未列數字，未證實。
- GHCR「底層有全域防濫用 429」：無來源，官方頁無此描述。
- GitLab「2022 年宣布 Free 10 GB transfer 後無限期擱置」：無官方 URL；agy 引的 `usage_quotas.html` 已失效。官方目前只說 transfer 用量 UI 不可見，未給 Free 數字。
- GitLab「已認證 2,000 req/min」：目前正確，但漏掉即將生效的分級（Free 100/min）。
- GitLab storage「每個 Namespace / Project 10 GiB」：官方是 **per project**。
- Docker Hub Personal 200/6h：docs 如此，但 docker.com/pricing 寫 100 pulls/hr，Docker 兩頁互相矛盾。
- Quay.io 方案／價格：官方頁抽查失敗，未證實。
- AWS ECR Public 儲存超額 $0.10/GB-月：pricing 頁未列（該頁只列免費額度），未證實。
- `skopeo copy --all` 與 `buildx imagetools` 行為：無 URL，未抽查。
- Cloudflare「cf-workers-oci-registry」：社群專案名稱未驗證。
