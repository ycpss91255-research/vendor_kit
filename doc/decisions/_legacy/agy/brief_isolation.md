只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：vendor_kit 如何把「自己的檔」與「使用者的檔」明確切割

## 背景
vendor_kit 讓工具 repo（例如 base）把 dist/ 打包成 OCI image；下游專案用一個版本檔宣告要哪些工具；專案裡一個薄啟動器（just recipe）每次打 just 都先讓快取目錄與版本檔一致。工具帶「初始檔」（例如 compose.yaml、.github/workflows/ci.yml、Dockerfile），第一次接工具時複製到專案指定路徑給使用者、升級時三方合併。原則：vendor_kit 永不刪、永不覆蓋使用者的檔；碰到使用者的東西只有三處：根 justfile 的一行 import、初始檔、.git/info/exclude。使用者希望這三處也盡量切乾淨。主機只有 docker + git + just（just ≥ 1.33）。

## 請回答（每點都要真實案例與可點的連結；沒找到就寫「沒找到」）

### A. 根 justfile 怎麼不碰使用者的
1. just 的檔案尋找規則：搜尋哪些檔名（`justfile`、`.justfile`、`Justfile`…）、大小寫、同時存在多個時的優先順序、往上層目錄找的規則；`JUST_JUSTFILE` 環境變數與 `--justfile` 旗標；`set fallback`；`import` / `import?` / `mod` / `mod?` 的語意與相對路徑解析；`[group]` 屬性；`set positional-arguments`；`just --list` 對 import 進來的 recipe 怎麼顯示。請引用 just 官方手冊（just.systems/man）對應章節。
2. 前例：工具「擁有」專案根 justfile／Makefile、使用者的 recipe 放另一個檔的做法。例如 ycpss91255-docker/base 的 init.sh 把 dist/script/justfile symlink 成下游根 justfile、使用者的東西放 script/local/justfile.local（ADR-00000010/00000011）；其他生態：Makefile 的 `-include local.mk`、`include` 慣例；Taskfile 的 `includes`；Earthly `IMPORT`；mise 的 `mise.toml` + `mise.local.toml`；pre-commit 只擁有 `.pre-commit-config.yaml`；devcontainer 只擁有 `.devcontainer/`。每個：誰擁有根檔？使用者擴充放哪？升級時根檔怎麼換？
3. 反過來：工具只在使用者檔裡「加一行」的前例（cargo init 改 .gitignore、direnv 的 .envrc、nvm 改 .bashrc、husky 改 package.json）——使用者反感的點是什麼、有沒有工具後來改掉這種做法。

### B. 版本檔與工具目錄的命名／位置慣例
4. 工具自己的狀態檔放專案根還是專屬目錄：`.terraform/` + `.terraform.lock.hcl`、`.copier-answers.yml`、`.cruft.json`、`.projen/` + `.projenrc`、`.devcontainer/`、`.mise.toml`／`mise.toml`、`.pre-commit-config.yaml`、`.tool-versions`、`.nvmrc`、`Chart.lock`、`vendir.lock.yml`、`flake.lock`、`.gitmodules`、`.base/`（base subtree）。歸納：什麼情況用「點目錄集中放」、什麼情況「根目錄單檔」；檔名帶工具名（`.copier-answers`）還是通用名（`.version`）的利弊；Renovate custom regex manager 對檔名有沒有限制。
5. 具體評估三個候選：(a) 現狀 `.version` + `.version.local` + `.vendor_kit/` + `.<repo>/`；(b) 全部收進 `.vendor_kit/`（`.vendor_kit/version.toml`、`.vendor_kit/cache/<repo>/`）；(c) 根檔改名 `.vendor_kit_version`。各自對「一眼看出是 vendor_kit 的」「Renovate regex」「啟動器 grep」「工具 just 模組路徑長度」的影響。

### C. 初始檔怎麼明確隔離
6. 前例：生成／範本工具怎麼標示「這個檔是工具給的」：projen 的檔頭註解 + 唯讀 + `.projen/files.json` 清單；Copier 的 `_skip_if_exists`／answers；Cruft 的 `.cruft.json` skip；Yeoman 的 conflict 詢問；Rails generators；`.gitattributes` 的 `linguist-generated`／`merge=` driver；EditorConfig／`# managed by` 標頭（Ansible `ansible_managed`、Puppet、chezmoi）；Helm 的 `helm.sh/resource-policy: keep`。每個：怎麼區分「工具給的、使用者可改」與「工具給的、使用者別改」；升級時怎麼處理。
7. 三方合併的前例怎麼記「上次給你的版本」（baseline）：Copier 在 answers 記 commit 後重生舊版；git 的 merge-base；Debian conffile 的 md5sums（dpkg 的 conffile prompt：使用者改過 + 新版也改 → 詢問；只新版改 → 直接換；只使用者改 → 保留）；rpm 的 `.rpmnew`／`.rpmsave`；chezmoi 的 state。dpkg 的規則對我們是否直接可用？
8. 「初始檔放到工具專屬子目錄、專案根只留 symlink 或 include」的做法有沒有前例（例如 base 用 symlink 指進 .base/；compose 的 `include:`；GitHub Actions 的 reusable workflow 只留一個薄 yml）——哪些檔案類型做得到（compose、CI yml、Dockerfile、justfile、pre-commit config），哪些做不到（必須在固定路徑且不能 include）。

輸出：全中文，每點列事實 + 來源 URL；最後 A、B、C 各一張表（做法｜前例｜優點｜缺點｜對我們的適用性只列事實不下結論）。
