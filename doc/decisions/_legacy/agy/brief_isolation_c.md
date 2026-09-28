只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：vendor_kit 如何把「自己的檔」與「使用者的檔」明確切割

## 背景
vendor_kit 讓工具 repo（例如 base）把 dist/ 打包成 OCI image；下游專案用一個版本檔宣告要哪些工具；專案裡一個薄啟動器（just recipe）每次打 just 都先讓快取目錄與版本檔一致。工具帶「初始檔」（例如 compose.yaml、.github/workflows/ci.yml、Dockerfile），第一次接工具時複製到專案指定路徑給使用者、升級時三方合併。原則：vendor_kit 永不刪、永不覆蓋使用者的檔；碰到使用者的東西只有三處：根 justfile 的一行 import、初始檔、.git/info/exclude。使用者希望這三處也盡量切乾淨。主機只有 docker + git + just（just ≥ 1.33）。

## 請回答（每點都要真實案例與可點的連結；沒找到就寫「沒找到」）

### C. 初始檔怎麼明確隔離
6. 前例：生成／範本工具怎麼標示「這個檔是工具給的」：projen 的檔頭註解 + 唯讀 + `.projen/files.json` 清單；Copier 的 `_skip_if_exists`／answers；Cruft 的 `.cruft.json` skip；Yeoman 的 conflict 詢問；Rails generators；`.gitattributes` 的 `linguist-generated`／`merge=` driver；EditorConfig／`# managed by` 標頭（Ansible `ansible_managed`、Puppet、chezmoi）；Helm 的 `helm.sh/resource-policy: keep`。每個：怎麼區分「工具給的、使用者可改」與「工具給的、使用者別改」；升級時怎麼處理。
7. 三方合併的前例怎麼記「上次給你的版本」（baseline）：Copier 在 answers 記 commit 後重生舊版；git 的 merge-base；Debian conffile 的 md5sums（dpkg 的 conffile prompt：使用者改過 + 新版也改 → 詢問；只新版改 → 直接換；只使用者改 → 保留）；rpm 的 `.rpmnew`／`.rpmsave`；chezmoi 的 state。dpkg 的規則對我們是否直接可用？列事實。
8. 「初始檔放到工具專屬子目錄、專案根只留 symlink 或 include」的做法有沒有前例（例如 base 用 symlink 指進 .base/；compose 的 `include:`；GitHub Actions 的 reusable workflow 只留一個薄 yml）——哪些檔案類型做得到（compose、CI yml、Dockerfile、justfile、pre-commit config），哪些做不到（必須在固定路徑且不能 include）。

輸出：全中文，每點列事實 + 來源 URL（每個前例都要可點的連結）；最後一張表（做法｜前例｜優點｜缺點｜對我們的適用性只列事實不下結論）。請精簡，總長度控制在 200 行內。
