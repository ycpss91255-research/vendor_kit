# 題目：vendor_kit 的檔跟使用者的檔怎麼明確切割（三題）

## 背景（已定案）
乙版架構；主機只需 docker+git+just(≥1.33)；`just vendor_kit` 命名空間；動詞 install/uninstall（專案層）、add/remove（工具層）、update/upgrade、dev/undev、sync；**vendor_kit 永不刪、永不覆蓋使用者的檔**；初始檔 add 時複製（已存在只 warn）、upgrade 三方合併（git merge-file --diff3，衝突留標記回 2）、新版刪除的檔只 warn 不刪；baseline 全文存 `.vendor_kit/baseline/<repo>/`。
目前 vendor_kit 會碰使用者東西的只有三處：(1) 根 justfile 一行 `import '.vendor_kit/entry.just'`（install 加、uninstall 相同才刪）(2) 初始檔 (3) `.git/info/exclude` 我們的區塊（不碰 .gitignore）。使用者要求：這三處也盡量切乾淨、規則明確到不會亂。
just 實測事實（agy/just_rules_tested.md）：`justfile` 與 `.justfile` 並存報錯；根 justfile 為 symlink 時 import/mod 相對路徑與 justfile_directory() 以 symlink 所在目錄（repo root）為準；`import?` 缺檔靜默；`mod?` 缺檔呼叫才報錯；`--justfile-name`/`JUST_JUSTFILE_NAME` 可改搜尋檔名；重複 recipe 預設報錯。

## 三題與候選
### A. 根 justfile
A1 現狀：使用者擁有根 justfile，install 加一行 import（沒有 justfile 就建一個只含這行）。
A2 base 式：根 `justfile` = symlink → `.vendor_kit/entry.just`（vendor_kit 擁有、升級整檔換），使用者 recipe 放 `justfile.local`（entry.just 內 `import? 'justfile.local'`）；install 遇到已有 justfile → 拒絕並提示改名為 justfile.local。
A3 混合：沒有 justfile → A2 symlink；已有 → A1 加一行。
A4 完全不碰：install 只印「請在根 justfile 加這一行」，使用者自己加。
評估維度：侵入性、升級時誰換、Windows/WSL2 symlink、fresh clone 行為、與 base 下游現有慣例（base 的 init.sh 已把根 justfile 做成 symlink！同一專案若同時用 base 與 vendor_kit，根 justfile 只能有一個擁有者——這是關鍵衝突，請正面處理：vendor_kit 接管根檔後 base 的 `just docker/base` 要從 `.<repo>/just/…` 經 gen/tools.just mod 進來）。

### B. 版本檔與目錄的命名／位置
(a) 現狀：`.version`、`.version.local`、`.vendor_kit/`、`.<repo>/`（工具快取在根）。
(b) 全收進 `.vendor_kit/`：`.vendor_kit/version.toml`、`.vendor_kit/version.local.toml`、`.vendor_kit/cache/<repo>/`；根目錄只剩 `.vendor_kit/`（+ justfile 一行或 symlink）。
(c) 根檔改名 `.vendor_kit_version`（+ `.vendor_kit_version.local`），快取仍 `.<repo>/`。
評估：一眼識別、Renovate regex 誤傷、啟動器 grep、工具 just 模組 mod 路徑、`.<repo>/` 與 base 現有 `.base/` subtree 目錄撞名（base 下游已有 `.base/` 是 subtree；vendor_kit 的快取若也叫 `.base/` 會撞）。

### C. 初始檔隔離
C1 現狀：複製到工具指定路徑（compose.yaml、.github/workflows/x.yml…）+ baseline 全文 + merge-file。
C2 C1 + dpkg conffile 式 hash 短路（disk==old→靜默換新；disk≠old 且 old==new→保留；兩邊都改→才 merge-file）。
C3 rpm 式：兩邊都改時不動使用者檔，寫 `<file>.vendor_kit.new` 並警告（不留衝突標記）。
C4 薄 include：能 include 的類型（compose `include:`、justfile `import`、GitLab CI `include: local`）初始檔只是一行 include 指向 `.<repo>/files/…`，內容隨 image 升級、不需合併；做不到的（Dockerfile、GitHub Actions caller、.gitignore、.editorconfig）才走 C1/C2。工具作者在 init.toml 標每檔模式。
C5 檔頭標記：初始檔第一行 `# vendor_kit: from <repo> vX — 可自由修改，upgrade 會三方合併`（能加註解的檔型）+ baseline 清單；不改行為只標示。
（C2/C4/C5 可疊加。）

## 要回答
每題選一個（可組合）並說理由；把「vendor_kit 會碰使用者東西的完整清單」重寫成最終版（檔｜動詞｜規則）；指出 agy 哪些說法不能用。
