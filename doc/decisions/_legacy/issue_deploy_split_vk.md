## 定案（2026-09-20）

- deploy（現場部署包）**不做進 vendor_kit**：VK 只搬移，不懂應用的執行模型。
- deploy 維持在 base（`dist/deploy/`，base ADR-23）；VK 對部署包的唯一承諾 = 不變量 I9：工具 recipe 產生的交付物在執行期不得依賴 `.vendor_kit/`、`version.toml`、GHCR（base 現行部署包滿足：image 用 tar 帶、compose 已解析）。

## 待議

將來第二個工具 repo 也需要部署包時，可把 deploy 抽成獨立工具 repo（例如 `deploy_kit`，本身是一個 `dist/`，下游 `add deploy_kit` 取得 `just deploy …`），VK 不需改動。但 deploy 綁在 base 的 `setup.conf` → resolved compose → `.env` 覆寫軸線，能否剝離、剝離後怎麼接回，需 base 評估。

已向 base 徵詢：ycpss91255-docker/base#1191。

## 關閉條件

base#1191 有結論並記入本 issue；若決定抽離，另開實作票（在 deploy_kit repo），本票只追蹤 VK 側是否需配合（預期：不需）。
