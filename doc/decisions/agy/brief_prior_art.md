只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：為 vendor_kit 找「類似專案的對外介面」與「可直接取代的現成工具」

## vendor_kit 在做什麼
- 「工具 repo」（例如一個放 Dockerfile 範本、腳本、just recipe 的 base repo）把自己的 dist/ 目錄打包成 OCI image（FROM scratch 只放檔案）推到 GHCR，amd64+arm64。
- 「下游專案」用一個版本檔 `.version`（TOML：一行一工具 `<repo> = "image:tag@sha256"`，含 vendor_kit 引擎自己的版本）宣告要哪些工具哪個版本。
- 每次在專案打 `just`，薄啟動器（專案裡 .vendor_kit/ 的 just recipe）會確認 `.<repo>/` 目錄與 .version 一致，不一致就用 docker 從 image 把檔案抓下來寫進 `.<repo>/`（不進 git、使用者不可改）。
- 工具帶「初始檔」（init.toml 列出要複製到專案裡的檔案，例如 compose.yaml、CI 設定）；第一次接工具時複製給使用者，之後升級時做三方合併（baseline／使用者現在的檔／新版範本）。
- 本機開發模式：把 `.<repo>/` 改指向本機 checkout 目錄，改工具馬上在專案裡生效。
- 主機只需要 docker + git + just；平台 Linux amd64/arm64（含 Jetson）、WSL2；macOS 不在範圍。
- 使用者希望指令極少（大約：接工具、升級、本機開發，加上對應的解除動作），其他自動化。

## 請回答（每一點都要有真實案例與可點的連結，沒有找到就寫「沒找到」，不要編）

### A. 類似專案的對外介面（至少調查以下，每個工具各一段）
Copier、Cruft（cookiecutter 更新）、projen、Nx generators/migrations、Angular schematics、Yeoman、pre-commit（hooks 由 repo 散播、`pre-commit autoupdate`）、Carvel vendir（vendir.yml + vendir.lock.yml、`vendir sync`）、Carvel imgpkg（目錄推成 OCI image 再拉回）、ORAS（任意檔案推到 OCI registry）、devcontainer Features（OCI artifact + 安裝腳本）、Helm chart 以 OCI 散播、Kustomize remote bases、git subtree／git-subrepo／git-vendor／vendorpull／peru、GitHub 的 actions-template-sync 與 repo-file-sync-action、Gradle Wrapper／Bazelisk／mise（薄啟動器 + 版本檔）、Nix flakes、Dagger modules、Earthly。
每個工具回答：
1. 使用者面對的指令清單（init／add／update／upgrade／remove／diff／本機開發之類，寫原本的指令名）。
2. 版本怎麼鎖（lockfile 格式、tag／digest）、升級怎麼觸發（手動指令、機器人如 Renovate/Dependabot 支援與否）。
3. 升級時使用者已修改過的檔案怎麼處理（覆蓋／三方合併／只顯示 diff／不碰）。
4. 有沒有「解除安裝／移除一個來源」的指令；有沒有「本機路徑覆寫」的開發模式。
5. 主機需要裝什麼（單一二進位？Python？Node？只要 docker？）；支援 Linux arm64 嗎。

### B. 有沒有現成工具可以直接取代 vendor_kit（不用自己寫 repo）
以「只用現成工具」為前提評估這幾組組合，每組列出能做到／做不到的項目與來源：
1. Carvel vendir + imgpkg（vendir 的 image 來源 + lock 檔）。
2. ORAS + 一段 just recipe。
3. Copier（模板 + `copier update` 三方合併）單獨、或 Copier 搭配 1/2。
4. git subtree／git-subrepo 直接 vendoring 工具 repo（目前 base 就是這樣做，問題是 base 迭代與下游綁在一起、base 自己升級要改下游）。
5. devcontainer Features 的 OCI 散播模型。
6. pre-commit 的 repo 散播模型。
特別要查：哪些工具原生支援「從 OCI registry 拉一個純檔案 image 展開到目錄 + lock 檔 + 三方合併使用者檔 + 本機路徑覆寫」全部四項；沒有任一工具全包的話，最接近的是哪個、缺哪一項。

### C. 對「介面命名」的觀察
上述工具中最常見的動詞組合是什麼（例如 add/remove、install/uninstall、update/upgrade、sync、init）；成對的解除動作通常怎麼命名；「只查不套用」通常叫什麼（check／--dry-run／update／outdated）。

輸出格式：全中文；每個工具一段，段尾列來源 URL；最後 B 用一張表（組合｜拉 OCI 檔案｜lock｜三方合併｜本機覆寫｜arm64｜主機需求｜缺什麼）。
