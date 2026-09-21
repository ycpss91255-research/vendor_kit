只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：vendor_kit 如何把「自己的檔」與「使用者的檔」明確切割

## 背景
vendor_kit 讓工具 repo（例如 base）把 dist/ 打包成 OCI image；下游專案用一個版本檔宣告要哪些工具；專案裡一個薄啟動器（just recipe）每次打 just 都先讓快取目錄與版本檔一致。工具帶「初始檔」（例如 compose.yaml、.github/workflows/ci.yml、Dockerfile），第一次接工具時複製到專案指定路徑給使用者、升級時三方合併。原則：vendor_kit 永不刪、永不覆蓋使用者的檔；碰到使用者的東西只有三處：根 justfile 的一行 import、初始檔、.git/info/exclude。使用者希望這三處也盡量切乾淨。主機只有 docker + git + just（just ≥ 1.33）。

## 請回答（每點都要真實案例與可點的連結；沒找到就寫「沒找到」）

### A. 根 justfile 怎麼不碰使用者的
2. 前例：工具「擁有」專案根 justfile／Makefile、使用者的 recipe 放另一個檔的做法。請只補以下幾個（其他已查過）：pre-commit 只擁有 `.pre-commit-config.yaml`；devcontainer 只擁有 `.devcontainer/`；Nix flake / devenv；Bazel `WORKSPACE` + `.bazelrc` + `user.bazelrc`；git config 的 `include.path` / `includeIf`；just 社群有無「根 justfile 由工具產生、使用者放 justfile.local / .justfile.local」的慣例或討論（GitHub issue／discussion）。每個：誰擁有根檔？使用者擴充放哪？升級時根檔怎麼換？
3. 反過來：工具只在使用者檔裡「加一行」的前例（cargo init 改 .gitignore、direnv 的 .envrc、nvm 改 .bashrc、husky 改 package.json 的 prepare script、rustup/pyenv/conda 改 shell rc、poetry/uv 改 .gitignore、pre-commit install 改 .git/hooks、git-lfs 改 .gitattributes）——使用者反感的點是什麼（找 GitHub issue、HN、Reddit 討論）、有沒有工具後來改掉這種做法（例如 husky v5+ 改為 prepare script、conda init 加 --no-modify-path、rustup 的 --no-modify-path）。另外：有沒有工具寫入 `.git/info/exclude` 而非 `.gitignore` 的前例。

輸出：全中文，每點列事實 + 來源 URL（每個前例都要可點的連結）；最後一張表（做法｜前例｜優點｜缺點｜對我們的適用性只列事實不下結論）。請精簡，總長度控制在 200 行內。
