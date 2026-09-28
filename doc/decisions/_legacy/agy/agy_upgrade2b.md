本調查針對 `vendor_kit` 升級與回退流程，調研現行主流工具（Batect、Gradle Wrapper、rustup、uv、Bazelisk、Nix Flakes、Terraform）的架構模式與前例，並提供具體流程建議。

---

# 3. 「啟動器自我升級」前例研究

當「舊版啟動器」負責升級到新版，若新版需要新參數、新設定格式或新通訊協定時，現有工具採用了不同的演進模式：

### (1) Batect：Wrapper 腳本覆寫更新
* **機制**：
  專案根目錄的 `./batect`（或 Windows 下的 `batect.cmd`）是一個被納入 Git 追蹤的 shell 啟動包裝器（wrapper script），內部包含 `VERSION="x.y.z"`。
  當使用者執行 `./batect --upgrade` 時，啟動器會連線至 GitHub Releases 下載最新版的 `./batect` wrapper script 並**直接覆寫本機的 wrapper 腳本**。
* **應對新參數/新格式**：
  若新版本需要新的環境變數、Docker 旗標或 JVM 參數，這些新邏輯會直接包含在被替換下載的新 wrapper 腳本內。下次執行時，新版 wrapper 腳本才會負責下載並啟動對應的新版 Batect 運行檔。
* **來源連結**：
  * [Batect Documentation - Upgrading Batect](https://batect.dev/docs/getting-started/tutorial#upgrading-batect)
  * [GitHub: batect/batect](https://github.com/batect/batect)
  * [Renovate batect-wrapper Manager](https://docs.renovatebot.com/modules/manager/batect-wrapper/)

---

### (2) Gradle Wrapper：兩階段執行（Two-stage execution）
* **機制**：
  升級指令為 `./gradlew wrapper --gradle-version <version>`。官方與社群的最佳實踐均要求**連續執行兩次（run twice）**：
  1. **第一階段（First Run）**：由當前舊版 Gradle 執行 `wrapper` task。這一步只會將新的版本號寫入 `gradle/wrapper/gradle-wrapper.properties`，但此時生成的 `gradle-wrapper.jar` 與 `gradlew` 腳本仍然是由舊版 Gradle 生成的。
  2. **第二階段（Second Run）**：再次執行 `./gradlew wrapper` 時，啟動腳本讀取更新後的屬性檔，自動下載並啟動「新版 Gradle 發行版」。此時由**新版 Gradle** 重新產出並覆寫 `gradle-wrapper.jar` 與 `gradlew` 啟動腳本。
* **應對新參數/新格式**：
  舊版啟動器不需要預先知道新版啟動腳本的所有細節，只需負責把「目標版本」寫入屬性檔；隨後由新版執行引擎接管，重新產出符合新規格的啟動器與二進制 Jar 包。
* **來源連結**：
  * [Gradle User Manual - Upgrading the Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)
  * [Gradle 1.6 Release Notes: Multi-process safe wrapper upgrading](https://docs.gradle.org/1.6/release-notes.html)

---

### (3) `rustup self update` 與 `rustup update` 的關係與順序
* **關係與預設順序**：
  * `rustup update`：預設會**先同步並升級所有已安裝的 Rust toolchains**（`info: syncing channel updates for ...`），在工具鏈升級完成後，再檢查並執行 `rustup` 本身的自我升級（`info: checking for self-updates`）。可透過 `--no-self-update` 或設定 `RUSTUP_AUTO_SELF_UPDATE=disable` 關閉自我升級。
  * `rustup self update`：獨立只升級 `rustup` 管理器本體，不更動 toolchains。
* **新格式/新參數衝突時的處理**：
  * Rust 的發布清單帶有 `manifest-version`（目前主流為 v2）。若未來的清單格式或新組件（如早期新增 `rust-analyzer` 或支援新 target架構）超出舊版 rustup 的解析能力，舊版 rustup 會直接報錯：`error: manifest version '{0}' is not supported`。
  * 因此在架構改版或遇到解析失敗時，官方與社群的標準修復指引是**「先手動執行 `rustup self update`，換上新版啟動器，再執行 `rustup update`」**。
* **來源連結**：
  * [The Rustup Book - Basics](https://rust-lang.github.io/rustup/basics.html)
  * [GitHub rust-lang/rustup: errors.rs (UnsupportedVersion error)](https://github.com/rust-lang/rustup/blob/master/src/errors.rs)
  * [GitHub rust-lang/rustup: rustup_mode.rs](https://github.com/rust-lang/rustup/blob/master/src/cli/rustup_mode.rs)

---

### (4) `uv self update` 與 `uv tool upgrade` 的關係
* **關係**：
  * `uv self update`：專門更新 `uv` 執行檔本體（重新觸發 installer 並更新 PATH）。
  * `uv tool upgrade <tool>`：專門更新透過 `uv tool install` 安裝於使用者隔離虛擬環境（`~/.local/share/uv/tools/`）中的 Python CLI 工具。
  * 兩者完全**解耦（Decoupled）**，執行 `uv tool upgrade` 不會自動檢查或升級 `uv` 本身。
* **應對新參數/新格式**：
  `uv tool` 仰賴每個 tool 目錄內的 environment receipt 來追蹤元資料。如果新版 tool 需要新的隔離機制或依賴解析格式，是由升級後的 `uv` 二進制來處理相容性轉換。
* **來源連結**：
  * [uv CLI Reference - uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)
  * [uv CLI Reference - uv tool upgrade](https://docs.astral.sh/uv/reference/cli/#uv-tool-upgrade)
  * [uv Documentation - Tools Guide](https://docs.astral.sh/uv/guides/tools/)

---

### (5) 順序總結：「先換自己再換工具」vs「先換工具再換自己」

| 策略 | 代表工具 | 優勢 | 潛在問題 | 適用情境 |
| :--- | :--- | :--- | :--- | :--- |
| **先換自己再換工具**<br>*(Manager/Launcher First)* | **Batect** (`--upgrade`)<br>**rustup** (遇到 manifest 升級時) | 確保啟動器具備最新參數、協定解析能力與旗標支援，絕不傳遞舊參數給新工具。 | 若新啟動器有 breaking change，尚未升級工具前啟動器可能先行失效。 | 工具依賴啟動器傳入執行參數、或版本宣告檔格式有結構改變時。 |
| **先換工具再換自己**<br>*(Tool First / 兩階段)* | **Gradle Wrapper** | 啟動腳本由新工具負責「自我生成」，專案內不需要維護獨立的啟動器升級邏輯。 | 舊啟動器若遇到無法解析的新格式會卡死，需分兩次執行（第一階段改宣告、第二階段由新工具替換腳本）。 | 啟動腳本本質上就是工具發行版的一個「附屬產物」時。 |

> **對 vendor_kit 的結論**：
> `vendor_kit` 的啟動器（`.vendor_kit/` 內的 recipe）是由 `vendor_kit` 映像檔產出的。因此應採**「先換自己再換工具」**：在更新 `.version` 後，下次執行 `just` 時，啟動器必須先比對 `vendor_kit` 核心版本，若版本更新，先啟動新版 `vendor_kit` 容器刷新 `.vendor_kit/` 中的啟動器 recipe，再由新版 recipe 接管工具的執行與升級。

---

# 4. 回退：只改版本檔就能回退的前例研究

調研當使用者僅透過 Git 或文字編輯器將版本宣告檔改回舊版時，工具是否能立即生效，或是否需要額外指令：

### (1) Bazelisk：`.bazelversion`
* **回退行為**：**不需要任何額外指令即可生效**。
* **機制**：
  Bazelisk 是 Bazel 的啟動器封裝。每次在終端機輸入 `bazel <command>` 時，Bazelisk 都會在執行期讀取專案目錄下的 `.bazelversion` 檔案。若使用者透過 `git revert` 或編輯器將版本改為舊版（例如 `7.0.0` 改回 `6.4.0`），下次執行 `bazel` 時，Bazelisk 就會直接檢查本機快取是否有該舊版；若無則自動下載舊版並執行。
* **來源連結**：
  * [GitHub: bazelbuild/bazelisk README](https://github.com/bazelbuild/bazelisk)
  * [Bazel Documentation: Installing Bazel using Bazelisk](https://bazel.build/install/bazelisk)

---

### (2) Nix Flakes：`flake.lock`
* **回退行為**：**不需要任何額外指令即可生效**。
* **機制**：
  Nix 是宣告式且內容定址（content-addressed）的套件管理系統。當使用者透過 `git checkout -- flake.lock` 或 `git revert` 將 `flake.lock` 還原為舊提交時，下次執行 `nix build` 或 `nix develop` 時，Nix 會直接解析被鎖定的舊版 commit SHA 與 narHash，並直接從本機 `/nix/store`（或遠端 binary cache）還原出舊版環境。除非使用者顯式輸入 `nix flake update`，否則 Nix 嚴格遵守 `flake.lock`，改回即生效。
* **來源連結**：
  * [Nix Reference Manual - nix flake](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html)
  * [Nix Documentation - Flakes Guide](https://nix.dev/concepts/flakes.html)

---

### (3) Terraform：`.terraform.lock.hcl`
* **能否降級？**：**可以降級，但不能「只改 lock 檔」就直接使用，必須搭配指令重新初始化**。
* **機制與限制**：
  1. **需要額外指令**：Terraform 執行時（如 `terraform plan` / `apply`）不會自動下載或替換已經下載到本機 `.terraform/providers/` 快取目錄中的二進制外掛。因此若透過 Git 把 `.terraform.lock.hcl` 還原到舊版，**必須顯式執行 `terraform init`** 才會重新驗證並下載舊版 provider。
  2. **降級操作規範**：
     * 若在 `.tf` 檔指定了較低版本約束，只跑 `terraform init` 會噴錯（提示 lock file 與設定約束不一致）。
     * 正確降級指令為：**`terraform init -upgrade`**（官方設計中 `-upgrade` 代表「重新評估約束並更新 lock 檔」，當約束調低時即執行降級）。
     * 另外，若要手動為特定平台重新鎖定 provider 雜湊，官方提供了專門指令：`terraform providers lock`。
* **來源連結**：
  * [HashiCorp Terraform - Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)
  * [HashiCorp Terraform CLI - terraform init](https://developer.hashicorp.com/terraform/cli/commands/init)
  * [HashiCorp Terraform CLI - terraform providers lock](https://developer.hashicorp.com/terraform/cli/commands/providers/lock)

---

# 5. 建議的 upgrade 流程

基於上述前例（Bazelisk 的「每次執行即時比對版本檔自動就緒」、Gradle 的「新舊版本過渡與兩階段刷新」、Batect 的「不自動更動使用者檔」原則），為 `vendor_kit` 設計以下四條升級與回退路徑。

各步驟的操作者角色定義：
* **機器人 (Renovate)**：自動發 PR 的機器人。
* **使用者 (User)**：開發者本人。
* **啟動器 (Launcher)**：Host 上的 `just` 與 `.vendor_kit/` 生成的 recipe。
* **容器 (Container)**：Docker 運行的工具 dist 容器或 vendor_kit 容器。

---

### 路徑一：Renovate 自動 PR 路徑
1. **機器人 (Renovate)**：
   偵測到 GHCR 上有新版 tool 或 vendor_kit image，向專案發出 PR，修改 `.version` 檔中對應工具的行（包含最新 digest 與 tag）。
2. **使用者 (User)**：
   在本地 checkout 該 PR 分支（或在 GitHub 合併後於本地 `git pull`）。
3. **使用者 (User)**：
   執行日常指令（例如 `just <name>`）或 `just diff <name>`。
4. **啟動器 (Launcher)**：
   讀取 `.version`，比對本機快取目錄 `.<name>/.installed_version`：
   * 發現版本不一致，呼叫 **容器 (Container)** 從新版 image 提取二進制/dist 檔案，原子更新至本機 `.<name>/`。
   * 將最新範本寫入 `.<name>/template/`（暫存區，不進 git）。
5. **使用者 (User)**：
   執行 `just diff <name>`。
6. **啟動器 (Launcher)**：
   調用三方 diff 工具（比對：`.vendor_kit/baseline/<name>/` 舊基準 vs `.<name>/template/` 新範本 vs 使用者目前設定檔）。
7. **使用者 (User)**：
   檢視 diff，手動將需要採納的範本變更合併到自己的專案設定檔中（維持「工具不自動改使用者檔」原則）。
8. **使用者 (User)**：
   執行 `just accept <name>`。
9. **啟動器 (Launcher)**：
   將 `.<name>/template/` 複製覆寫至 `.vendor_kit/baseline/<name>/`，更新基準副本。
10. **使用者 (User)**：
    執行 `git commit`，提交設定檔變更與 `.vendor_kit/baseline/<name>/`。

---

### 路徑二：`just upgrade <name>` 手動升級路徑
1. **使用者 (User)**：
   執行 `just upgrade <name>`（或可選指定版本 `just upgrade <name> v2.0.0`）。
2. **啟動器 (Launcher)**：
   透過 Docker / 遠端 API 查詢 GHCR 上 `<name>-dist` 的最新 digest 與 tag，將其寫入專案根目錄的 `.version`。
3. **啟動器 (Launcher)**：
   呼叫 **容器 (Container)** 拉取新 image，將二進制檔案解壓至 `.<name>/`，並將新版範本置於暫存區。
4. **使用者 (User)**：
   執行 `just diff <name>` 檢視設定檔與新範本差異。
5. **使用者 (User)**：
   手動調整自己的專案設定檔。
6. **使用者 (User)**：
   執行 `just accept <name>`。
7. **啟動器 (Launcher)**：
   將新範本更新至 `.vendor_kit/baseline/<name>/`。
8. **使用者 (User)**：
   執行 `git commit`，提交 `.version`、`.vendor_kit/baseline/<name>/` 與個人設定檔。

---

### 路徑三：vendor_kit 自身升級路徑（`.version` 中的 `vendor_kit = ...`）
*核心原則：採「先換自己再換工具」，由新版 vendor_kit 容器刷新 host 上的 recipe*
1. **使用者 (User)** 或 **機器人 (Renovate)**：
   更新 `.version` 中的 `vendor_kit = "ghcr.io/...:tag@sha256:..."`。
2. **使用者 (User)**：
   執行任何 `just` 指令（例如日常的 `just test` 或 `just update`）。
3. **啟動器 (Launcher, 舊版 recipe)**：
   在執行任務前觸發 self-check hook，比對 `.version` 中的 `vendor_kit` 版本與 `.vendor_kit/.installed_version`：
   * 發現版本變更，啟動器暫停目前任務，調用 **容器 (Container, 新版 vendor_kit image)**。
4. **容器 (Container, 新版 vendor_kit)**：
   執行自我安裝邏輯，將新版的 launcher recipe、共用腳本覆寫至 `.vendor_kit/`，並寫入新的 `.vendor_kit/.installed_version`。
5. **啟動器 (Launcher)**：
   自動使用新載入的 recipe 繼續完成原本使用者呼叫的任務（或提示使用者重新執行一次指令，類似 Gradle 的過渡）。
6. **使用者 (User)**：
   執行 `git commit`，將更新後的 `.vendor_kit/` 啟動器 recipe 提交進 Git。

---

### 路徑四：回退路徑（Rollback）
*核心原則：效法 Bazelisk 與 Nix，宣告式檔案改回即生效，使用者無須記憶複雜 rollback 指令*
1. **使用者 (User)**：
   透過 Git 還原 `.version`（例如 `git checkout HEAD~1 -- .version` 或 `git revert <commit>`）。
2. **使用者 (User)**：
   執行一般的 `just <name>`（無需執行特殊回退指令）。
3. **啟動器 (Launcher)**：
   在啟動前偵測到本機現存的 `.<name>/` 版本高於（或不等於）`.version` 所指定的舊版 image digest：
   * 啟動器調用 **容器 (Container, 舊版 image)**。
   * 自動以舊版 image 重新覆寫解壓 `.<name>/`，還原回舊版工具環境。
4. **啟動器 (Launcher)**：
   以舊版工具完成使用者指令。
5. **使用者 (User)**（可選）：
   若使用者在升級時已經跑過 `just accept`，使用者只需執行 `git checkout HEAD~1 -- .vendor_kit/baseline/<name>/` 與自己的設定檔，即可將基準與設定檔一併還原。
