你是命令列介面設計的審查員，請批判性檢視下面兩個命名決定，找出會讓使用者誤解、與生態系慣例衝突、或與同一 justfile 內其他命名空間衝突的地方；不同意就提出替代名並說明理由；同意也要說明為什麼比替代名好。以繁體中文作答，先給結論再給理由，控制在 60 行內。

## 背景
vendor_kit：工具 repo 把 dist/ 打包成 OCI image 推 GHCR；下游專案用 `.version`（TOML，鎖 image tag@digest，含引擎自己的版本）宣告要哪些工具；專案裡薄啟動器（`.vendor_kit/`，just recipe）每次打 just 都先讓 `.<repo>/`（不進 git 的快取，從 image 展開）與 `gen/`（產生的 just 模組）跟 `.version` 一致，然後才跑使用者要的 recipe。工具帶初始檔（第一次複製給使用者、升級時三方合併）。命名空間 `just vendor_kit <verb>`；同一個專案的 justfile 裡使用者也會打 `just base update/upgrade`（base 是對齊 apt：update 只查、upgrade 套用）、`just docker build`。使用者要指令極少。

已定的動詞：
- 工具層：`add <repo>` ↔ `remove <repo>`（接工具／移除工具）
- 升級：`update`（只查）／`upgrade`（套用，含三方合併）
- 本機開發：`dev <repo> -p <dir>` ↔ `undev <repo>`
- `bootstrap.sh`：release 附的一次性腳本，只做「下載並 docker pull 鎖定版引擎」然後呼叫下面的專案層動詞。

## 待審的兩個命名
(1) 專案層「把 vendor_kit 裝進這個專案」（第一次：建 .version、.vendor_kit/ 薄殼、根 justfile 一行 import；再跑一次 = 修復薄殼，冪等；要求已是 git repo，否則報錯不做 git init）↔ 全部拆掉。
   建議：`install` ↔ `uninstall`（前例 pre-commit install/uninstall：把 hook 裝進這個 repo／拆掉）。
   被否決的：`init` ↔ `deinit`（git submodule 前例；init 在 cargo/npm 是建新專案）、`init` ↔ `uninstall`（不成對）。
   副作用：引擎內部「拉 image 展開到 .<repo>/」原本叫 install，要改名（建議 `fetch`），使用者看不到。
   疑慮請評估：apt 的 install 是「裝一個套件」，使用者會不會以為 `just vendor_kit install base` 是接工具（其實是 add）？`install` 不帶參數是否夠清楚？

(2) 每次打 just 自動跑的前置動作「讓 .<repo>/ 與 gen/ 跟 .version 一致；只碰不進 git 的東西；印記不同就重新展開 image、sha256 驗證失敗就重裝；發現『從未完成接入』或『baseline 落後 .version』只報錯／警告不自己補」。使用者幾乎不會手打，但 fresh clone 後工具 recipe 出現前要跑一次，CI 也會叫它（frozen 模式）。
   原名 `ensure`（使用者覺得不是常見字）。建議改 `sync`（前例 vendir sync、peru sync、uv sync、git submodule update：宣告檔 → 讓現況一致）。
   疑慮請評估：`sync` 在 uv/vendir 會寫 lock 檔，我們的 sync 永不寫要進 git 的檔，會不會誤導？`sync` 會不會被以為是「跟遠端同步 = 升級」？替代名（`refresh`、`prepare`、`check`、`restore`、`materialize`、`hydrate`、`up`）各有什麼問題？

請最後給一張表：動詞｜你的裁定（同意／改名為 X）｜一句理由。
