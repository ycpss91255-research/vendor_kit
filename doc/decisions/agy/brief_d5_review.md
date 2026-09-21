題目：#5 啟動器出貨與 bootstrap（已由使用者定案，現在要批判性檢視定案有沒有漏洞）

決議 D5：啟動器由 vendor_kit 出貨（.vendor_kit/ 兩層 justfile + bootstrap.sh）
> 討論紀錄：`dist_distribution_notes.md` §8 #5；圖：`dist_distribution.drawio` 第 2、7、9、10 頁；原型：`proto/vendor_kit` `aa07bdc`、`proto/project` `6260da4`。

## 決議（2026-09-17）

啟動器由 **vendor_kit 出貨**，拆成兩層：

| 檔 | 誰擁有 | 進 git | 內容 |
|---|---|---|---|
| `justfile`（根） | 使用者 | 是 | 兩行：註解 + `import ".vendor_kit/vendor.just"`；使用者自己的 recipe 加在後面，工具永不碰 |
| `.vendor_kit/vendor.just` | vendor_kit | 是 | 標準 recipe：`_ensure`（每個指令前自動檢查／安裝）、`init`、`diff`、`upgrade`、`_vk` |
| `.vendor_kit/tools.just` | vendor_kit（衍生） | 是 | 依 `.version` 產生，每個工具一行 `import? "../.<name>/just/tool.just"`；每次 install 後重寫 |
| `.vendor_kit/.stamp` | vendor_kit | 是 | 第一行 = vendor_kit image，之後 = vendor.just 的 sha256；被手改 → 中止 |
| `.version` | Renovate／`just upgrade` | 是 | 多一行 `vendor_kit = "ghcr.io/…:vN@sha256:…"`，啟動器版本獨立鎖定、獨立升級 |

**bootstrap**：release 附 `bootstrap.sh`（POSIX sh）：檢查 docker/git/just → `docker run --rm -u UID:GID -v $PWD:/repo <vendor_kit image> --name vendor_kit --self <image> bootstrap`（寫出上表；已存在的 `justfile`／`.version` 不動）→ 問要不要接一個工具（寫一行到 `.version`、`just init`）→ 刪掉自己。

**工具側**：工具的 `dist/just/tool.just` 提供自己的日常指令（build / run / …），`just init` 後由 `tools.just` 接上。

## 理由

- 主機只有 Docker + git + just，`just` 第一次跑時還沒有任何容器跑過 → 啟動器必須已在 repo 裡（進 git）。
- 使用者一定會往 justfile 加自己的 recipe；vendor_kit 升級常改 docker run 參數 → 混在同一檔每次升級都要人肉合併。拆兩層後工具檔可整個換新、使用者檔永不碰。
- 前例（agy）：Gradle Wrapper、Batect 是「啟動器進 git」型且禁止手改；Bazelisk／mise／uv／Nix／Dagger 都要主機另裝 CLI，不符限制。bootstrap 一行 docker run 的前例：mkdocs-material、Jekyll、Hugo、Terraform、devcontainer CLI。

## 已排除

- A 單一 justfile 由 vendor_kit 出貨、升級時只 diff：每次升級人肉 merge。
- B justfile 專案自理、vendor_kit 只給範本：容器介面一改舊 justfile 就壞且難查。
- vendor.just 不獨立鎖版本、跟著某個工具 image 走：升級 vendor_kit 與升級工具混在一起，追查問題時分不清是誰壞。

## 待辦

- [ ] `just upgrade` 細節（另一題）
- [ ] 正式圖第 2／7／9／10 頁補 `tools.just`、`--self`、`bootstrap-test` stage



補充：upgrade 分析建議 .vendor_kit/ 拆成「程式集合（世代目錄 + 單一固定入口）」與「baseline/（持久）」；just 已定命名空間 vendor_kit（根 justfile 用 mod? vendor_kit）；tools.just 由 .version 衍生、每次 install 重寫（進 git 會髒）。原型：proto/vendor_kit（launcher.py、bootstrap 子命令、release/bootstrap.sh）、proto/project。