# 給 base repo 的 issue 草稿

標題：deploy 部署包是否可抽成獨立工具 repo（經 vendor_kit 派發）？徵詢意見

## 背景
vendor_kit（ycpss91255-research/vendor_kit）正在取代 subtree：工具 repo 把 `dist/` 打成 GHCR image，下游專案用 `just vendor_kit add/upgrade` 搬進來、鎖版本、三方合併初始檔。vendor_kit 的定位是「只搬移」，不懂應用的執行模型；對部署包的唯一承諾是「交付物執行期不得依賴 `.vendor_kit/`、`version.toml`、GHCR」（base 現行部署包滿足：image 用 tar 帶、compose 已解析）。

## 問題
base 的 `dist/deploy/`（ADR-23：`image.tar.xz` + 已解析 `compose.yaml` + `.env`／`.env.local` + `config/` 覆寫 + `deploy.sh`）目前綁在 base 的 `setup.conf` → `.env.generated` → resolved compose 與「進 git = 開發者預設、不進 git = 現場覆寫」軸線上。

如果將來第二個工具 repo 也需要部署包，選項是把 deploy 抽成獨立工具 repo（例如 `deploy_kit`，本身也是一個 `dist/`，下游 `add deploy_kit` 拿到 `just deploy …`），vendor_kit 不需改動。

想請 base 維護者評估：
1. deploy 對 `setup.conf`／compose 產生流程的依賴，能不能剝離成「給我 image + resolved compose + manifest，我產包」的純介面？剝離的代價？
2. 若剝離，base 這邊怎麼接回（base 的 `just deploy` 變成呼叫 `deploy_kit`？）；`deploy.manifest`／`cd-guard.sh` 歸誰？
3. 現階段是否值得動；還是等第二個需求出現再說（vendor_kit 這邊目前定案：維持 deploy 在 base）。

## 目前 vendor_kit 的定案
- 不會把 deploy 做進 vendor_kit。
- 維持 deploy 在 base；抽離與否由 base 決定，vendor_kit 側只保證 I9。

追蹤：vendor_kit issue #<待開>。
