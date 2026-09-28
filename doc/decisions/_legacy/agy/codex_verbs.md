OpenAI Codex v0.153.4
--------
workdir: /home/cyc/Desktop/vendor-kit_ws/src
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: none
reasoning summaries: none
session id: 01a0b43a-44cb-79a2-90ba-439ba52d1ccc
--------
user
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

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
我會核對相關工具的官方命名與行為，再評估這兩組動詞在同一個 justfile 裡是否容易混淆。

web search: 
web search: site.pre-commit.com pre-commit install uninstall install hooks ...
codex
結論：**同意 `install`／`uninstall`，也同意 `sync`；但零參數不足以消除歧義，必須搭配明確的 help 與錯誤訊息。** 內部「拉取並展開」則建議叫 `materialize`，不要只叫 `fetch`。

**（1）`install`／`uninstall`：合理，但 pre-commit 的前例只能支持一部分。**

- `vendor_kit` 命名空間提供了受詞：`just vendor_kit install` 可以理解成「把 vendor_kit 裝進目前專案」。反向 `uninstall` 也自然，比 `init`／`deinit` 更適合「可重跑修復、可拆除」的生命週期。
- [pre-commit install/uninstall](https://pre-commit.com/#pre-commit-install) 確實提供「把整合裝進 repo」的前例；但它安裝的是本機 hooks，你們會改動需提交的專案檔案。**不能讓使用者以為每次 clone 都該 install**：已接入的專案應跑 `sync`。
- apt 聯想確實存在，尤其你們刻意讓 `base update/upgrade` 對齊 apt。使用者推論出 `vendor_kit install base` 很合理；不同命名空間避免了語法撞名，沒有消除語意遷移。
- **不帶參數只是線索，不是解方。** help 應寫「將 vendor_kit 接入目前 Git 專案；重跑修復薄殼」；誤輸入 `install base` 時應明確導向 `add base`。實作須確保能攔截這種誤用。
- 否決 `init` 的理由需要修正：[Cargo 的 `init`](https://dev-doc.rust-lang.org/stable/cargo/commands/cargo-init.html) 本來就可在既有目錄建立 package，並非一定建立新目錄。真正較弱的是它不突出修復語意，且 `deinit` 不如 `uninstall` 直觀。
- `setup`／`teardown` 也可成立，但 `setup` 容易混入每台機器的環境準備，`teardown` 又像暫時性資源清理；此處 `install`／`uninstall` 更具體。
- `uninstall` 的「全部拆掉」必須交代初始檔如何處理：使用者已修改的檔案是否也刪除？命名可以接受，但不能靠這個字暗示能無損還原所有歷史變更。

**（2）`sync`：是這組候選中最好的名字，重點是標明同步依據與範圍。**

- 建議 help：**「依 `.version` 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案。」** 這比 `ensure` 更能說明動作，也涵蓋首次展開、版本切換與損壞後重建。
- 「會寫 lock」是個別工具的行為，並非 `sync` 必然的承諾。[uv](https://docs.astral.sh/uv/concepts/projects/sync/) 將 locking 與 syncing 分開描述，雖然預設會自動鎖定；[vendir](https://carvel.dev/vendir/docs/v0.40.x/sync/) 也支援依鎖定參照同步。因此你們縮小寫入範圍並不違反核心語意。
- 「跟遠端同步＝升級」仍可能被誤讀，但既有 `update`／`upgrade` 已提供清楚分工：查可用版本／變更鎖定版本／依鎖定版本重建本機狀態。**下載鎖定 image 不等於升級。**
- `sync` 不修復接入與 baseline 可以接受，前提是 help 不宣稱「同步整個專案」，警告也不能一面指出 baseline 落後，一面宣告「專案已完全同步」。
- `--frozen` 反而比 `sync` 更需要說明：若一般模式本來就不寫鎖定檔，它額外禁止什麼、哪些警告變成失敗？[uv 的 frozen](https://docs.astral.sh/uv/reference/cli/#uv-sync) 會略過鎖檔是否過期的檢查，不能直接借它表示「更嚴格驗證」。
- fresh clone 的 `sync` 入口必須在 `gen/` 尚不存在時就能執行；否則名稱再好，也會出現「必須先同步才能呼叫同步」的循環。

候選名的主要問題：

- `refresh`：容易被理解成重新查遠端或更新 metadata，與 `update` 靠太近。
- `prepare`：只說時序，沒說要與 `.version` 一致。
- `check`：暗示只讀，與下载、刪換快取、產生模組直接矛盾。
- `restore`：容易聯想到還原舊狀態或撤銷修改，首次建立也較不直觀。
- `materialize`／`hydrate`：適合內部術語，對使用者較生僻；前者尤其適合「把鎖定內容展開成檔案」。
- `up`：在已有 `docker` 的環境裡容易聯想到啟動服務，也可能被當作 upgrade 縮寫。
- 內部 `fetch`：只突出取得資料，隱藏驗證與展開；若函式包辦整段，`materialize` 更準確。

| 動詞 | 你的裁定 | 一句理由 |
|---|---|---|
| `install` | 同意 | 命名空間提供受詞，適合接入與重跑修復，但須導正 `install <repo>` 誤用。 |
| `uninstall` | 同意 | 與 install 成對，須明定使用者修改過的初始檔如何處理。 |
| `sync` | 同意 | 最能表達依 `.version` 使本機產物一致，且與 upgrade 分工清楚。 |
| 內部 `fetch` | 改名為 `materialize` | 同時涵蓋取得、驗證與展開，較符合完整操作。 |
tokens used
22,479
結論：**同意 `install`／`uninstall`，也同意 `sync`；但零參數不足以消除歧義，必須搭配明確的 help 與錯誤訊息。** 內部「拉取並展開」則建議叫 `materialize`，不要只叫 `fetch`。

**（1）`install`／`uninstall`：合理，但 pre-commit 的前例只能支持一部分。**

- `vendor_kit` 命名空間提供了受詞：`just vendor_kit install` 可以理解成「把 vendor_kit 裝進目前專案」。反向 `uninstall` 也自然，比 `init`／`deinit` 更適合「可重跑修復、可拆除」的生命週期。
- [pre-commit install/uninstall](https://pre-commit.com/#pre-commit-install) 確實提供「把整合裝進 repo」的前例；但它安裝的是本機 hooks，你們會改動需提交的專案檔案。**不能讓使用者以為每次 clone 都該 install**：已接入的專案應跑 `sync`。
- apt 聯想確實存在，尤其你們刻意讓 `base update/upgrade` 對齊 apt。使用者推論出 `vendor_kit install base` 很合理；不同命名空間避免了語法撞名，沒有消除語意遷移。
- **不帶參數只是線索，不是解方。** help 應寫「將 vendor_kit 接入目前 Git 專案；重跑修復薄殼」；誤輸入 `install base` 時應明確導向 `add base`。實作須確保能攔截這種誤用。
- 否決 `init` 的理由需要修正：[Cargo 的 `init`](https://dev-doc.rust-lang.org/stable/cargo/commands/cargo-init.html) 本來就可在既有目錄建立 package，並非一定建立新目錄。真正較弱的是它不突出修復語意，且 `deinit` 不如 `uninstall` 直觀。
- `setup`／`teardown` 也可成立，但 `setup` 容易混入每台機器的環境準備，`teardown` 又像暫時性資源清理；此處 `install`／`uninstall` 更具體。
- `uninstall` 的「全部拆掉」必須交代初始檔如何處理：使用者已修改的檔案是否也刪除？命名可以接受，但不能靠這個字暗示能無損還原所有歷史變更。

**（2）`sync`：是這組候選中最好的名字，重點是標明同步依據與範圍。**

- 建議 help：**「依 `.version` 重建本機工具快取與產生的模組；不修改鎖定版本或需提交的檔案。」** 這比 `ensure` 更能說明動作，也涵蓋首次展開、版本切換與損壞後重建。
- 「會寫 lock」是個別工具的行為，並非 `sync` 必然的承諾。[uv](https://docs.astral.sh/uv/concepts/projects/sync/) 將 locking 與 syncing 分開描述，雖然預設會自動鎖定；[vendir](https://carvel.dev/vendir/docs/v0.40.x/sync/) 也支援依鎖定參照同步。因此你們縮小寫入範圍並不違反核心語意。
- 「跟遠端同步＝升級」仍可能被誤讀，但既有 `update`／`upgrade` 已提供清楚分工：查可用版本／變更鎖定版本／依鎖定版本重建本機狀態。**下載鎖定 image 不等於升級。**
- `sync` 不修復接入與 baseline 可以接受，前提是 help 不宣稱「同步整個專案」，警告也不能一面指出 baseline 落後，一面宣告「專案已完全同步」。
- `--frozen` 反而比 `sync` 更需要說明：若一般模式本來就不寫鎖定檔，它額外禁止什麼、哪些警告變成失敗？[uv 的 frozen](https://docs.astral.sh/uv/reference/cli/#uv-sync) 會略過鎖檔是否過期的檢查，不能直接借它表示「更嚴格驗證」。
- fresh clone 的 `sync` 入口必須在 `gen/` 尚不存在時就能執行；否則名稱再好，也會出現「必須先同步才能呼叫同步」的循環。

候選名的主要問題：

- `refresh`：容易被理解成重新查遠端或更新 metadata，與 `update` 靠太近。
- `prepare`：只說時序，沒說要與 `.version` 一致。
- `check`：暗示只讀，與下载、刪換快取、產生模組直接矛盾。
- `restore`：容易聯想到還原舊狀態或撤銷修改，首次建立也較不直觀。
- `materialize`／`hydrate`：適合內部術語，對使用者較生僻；前者尤其適合「把鎖定內容展開成檔案」。
- `up`：在已有 `docker` 的環境裡容易聯想到啟動服務，也可能被當作 upgrade 縮寫。
- 內部 `fetch`：只突出取得資料，隱藏驗證與展開；若函式包辦整段，`materialize` 更準確。

| 動詞 | 你的裁定 | 一句理由 |
|---|---|---|
| `install` | 同意 | 命名空間提供受詞，適合接入與重跑修復，但須導正 `install <repo>` 誤用。 |
| `uninstall` | 同意 | 與 install 成對，須明定使用者修改過的初始檔如何處理。 |
| `sync` | 同意 | 最能表達依 `.version` 使本機產物一致，且與 upgrade 分工清楚。 |
| 內部 `fetch` | 改名為 `materialize` | 同時涵蓋取得、驗證與展開，較符合完整操作。 |
