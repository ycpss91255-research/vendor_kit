# 前例研究 brief：vendor_kit 的 upgrade 流程設計（自我升級與工具升級）

本報告針對套件/工具管理器中「啟動器自我升級（Launcher Self-Update）」、「目標工具升級（Toolchain/Tools Upgrade）」的執行順序與常見架構陷阱進行真實案例調查，分析 rustup、uv、Bazelisk、Gradle Wrapper 等工具的現有設計與 GitHub issue 前例，作為 `vendor_kit` 的升級流程設計參考。

---

### 1. rustup 的自我升級與工具升級機制

1. **`rustup update` 與 `rustup self update` 的連動關係**：
   * 在預設行為下，執行 `rustup update`（更新所有已安裝的 Rust toolchains）時，rustup **會先自動檢查並升級 rustup 本身二進制**，再繼續更新編譯器與工具鏈（[官方文件：Keeping rustup up to date](https://rust-lang.github.io/rustup/concepts/updating.html#keeping-rustup-up-to-date)）。
   * 若只需要手動升級 rustup 二進制本身，可單獨執行 `rustup self update`（[官方文件：Keeping rustup up to date](https://rust-lang.github.io/rustup/concepts/updating.html#keeping-rustup-up-to-date)）。
2. **單次抑制參數 `--no-self-update`**：
   * 在 CI/CD、離線環境或受限環境下，可加上 `--no-self-update` 旗標（例如 `rustup update --no-self-update`），強制作業跳過自我升級階段，僅更新 Rust toolchain（[官方文件：Keeping rustup up to date](https://rust-lang.github.io/rustup/concepts/updating.html#keeping-rustup-up-to-date)）。
3. **全域自我更新行為設定（`auto-self-update`）**：
   * rustup 提供全域設定指令 `rustup set auto-self-update <mode>`，可選值包括：
     * `enable`（預設）：`rustup update` 自動升級 rustup。
     * `disable`：關閉自動自我更新。
     * `check-only`：每次執行僅檢查並輸出新版本提示訊息，但不會自動下載安裝（[官方文件：Keeping rustup up to date](https://rust-lang.github.io/rustup/concepts/updating.html#keeping-rustup-up-to-date)）。

---

### 2. uv 的升級分離設計與檢查機制

1. **`uv self update` 的職責與限制**：
   * `uv self update` 專用於更新 `uv` 執行檔本身，但**僅限於透過官方 Standalone Installer（curl / irm 腳本）安裝的二進制**（[官方文件：uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)）。
   * 若 `uv` 是透過 Homebrew、pip、pipx、Scoop 等系統套件管理器安裝，`uv self update` 會直接停用並提示使用者使用原套件管理器升級，避免覆寫套件管理系統追蹤的檔案（[官方文件：uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)；[官方文件：uv Installer Configuration](https://docs.astral.sh/uv/configuration/installer/)）。
2. **與 `uv python upgrade` / `uv lock --upgrade` 分開的理由**：
   * **架構分層（Layer Separation）**：
     * `uv self update`：屬於外層「Meta-tool / CLI Launcher」本身（安裝於使用者全域 `~/.local/bin`）。
     * `uv python install / pin`：屬於「執行時期解譯器環境（Runtime Interpreters）」。
     * `uv lock --upgrade`：屬於「專案應用層依賴圖（Project Dependencies）」。
   * **建置一致性與最小驚訝原則（Determinism & Reproducibility）**：升級專案依賴鎖定檔（`uv.lock`）或切換 Python 版本時，不應隱式變更 CLI 啟動器版本。若升級 lockfile 順便升級了 `uv`，新版 `uv` 引入的新解析演算法或 lockfile 格式可能導致團隊其他成員或 CI 建置失敗。
   * **權限與部署邊界**：lockfile 屬於 git 儲存庫內檔案，而 CLI 是系統級/使用者級二進制，更新觸發時機與權限管理邊界不同。
3. **日常指令是否會自動檢查新版**：
   * **不會**。uv 在日常指令（例如 `uv run`、`uv lock`、`uv pip install` 等）中**沒有任何背景自動檢查新版或發送更新通知的機制**，所有更新檢查必須由使用者明確執行 `uv self update` 或外部依賴機器人觸發（[官方文件：uv self update](https://docs.astral.sh/uv/reference/cli/#uv-self-update)）。

---

### 3. 常見坑一：舊 Launcher 不認識新格式版本檔（Forward Compatibility Failure）

當專案升級了設定檔版本，但主機上的 Launcher 尚未升級時，舊 Launcher 常因無法向下相容新語法而潰退：

1. **Bazelisk 與 `.bazelversion` 前例**：
   * **GitHub Issue #117**：使用者在 `.bazelversion` 內加入註解（`# comment`），原本 Go 版 Bazelisk 只讀取第一行尚可運作，但舊版或不同實作（如 `bazelisk.py`）未預期多行或註解內容，直接解析失敗崩潰（[GitHub Issue: bazelbuild/bazelisk#117](https://github.com/bazelbuild/bazelisk/issues/117)）。此外，若在 `.bazelversion` 使用了新版 launcher 才支援的分支或 fork 格式語法，舊版會把整行當作無效版本字串向 GCS 抓取二進制，引發 404 錯誤。
2. **rustup 與 `rust-toolchain.toml` 前例**：
   * **GitHub Issue #1823**：早期的 `rust-toolchain` 只是一行純版本字串。當 rustup 引入 TOML 格式（支援 `[toolchain]`、`components`、`targets`）後，若在尚未升級的舊版 rustup（<1.23）環境下執行，舊版無法解析 TOML，會直接將第一行 `[toolchain]` 視為工具鏈名稱，回報致命錯誤：`error: invalid toolchain name '[toolchain]'`（[GitHub Issue: rust-lang/rustup#1823](https://github.com/rust-lang/rustup/issues/1823)）。
3. **對 `vendor_kit` 的啟示**：
   * `.version` 若採用 TOML 格式，**舊版 launcher 在解析 TOML 時必須對未知 key 保留前向相容性（Ignore Unknown Keys）**，不可直接 panic。
   * 建議在 `.version` 頂層加上明確的格式版本號（如 `format_version = 1`）。若舊 launcher 發現 `format_version` 高於自身支援版本，應輸出友善提示（「請先升級 vendor_kit 啟動器」）並中止，而非噴出語法錯誤。

---

### 4. 常見坑二：Bootstrapping 順序問題（Two-stage Bootstrap）

1. **Gradle Wrapper 的「升級必須執行兩次」前例**：
   * **官方文件明確規範**：升級 Gradle Wrapper 時，執行 `./gradlew wrapper --gradle-version <new-version>` **必須連續執行兩次**（[官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)；[GitHub Issue: gradle/gradle#8431](https://github.com/gradle/gradle/issues/8431)）。
   * **原因（二階段 Bootstrapping 陷阱）**：
     * **第一次執行**：由**舊版 Gradle** 執行 wrapper 任務。它只負責下載新版 Gradle distribution 並將新版 URL 寫入 `gradle-wrapper.properties`，但此時留在 repo 內的 `gradle-wrapper.jar` 與 `gradlew` 腳本**仍然是舊版的**。
     * **第二次執行**：wrapper 讀取 properties 下載並啟動了**新版 Gradle**，新版 Gradle 再重新執行 wrapper 任務，才能產出與新版完全相容的 `gradle-wrapper.jar`。
2. **對 `vendor_kit` 的啟示**：
   * `vendor_kit` 的進入點是使用者的 `justfile`，透過 `import .vendor_kit/launcher.just` 載入啟動器 recipe。
   * 如果使用者執行 `just upgrade`：
     * **先升級工具 vs 先升級 launcher**：若新工具需要新的 launcher recipe（例如新的 Docker volume 掛載、新的環境變數傳遞），舊 launcher 在當前 `just` 行程中無法提供這些功能。
     * **進程生命週期**：`just` 在解析時已經將 `.vendor_kit/launcher.just` 讀入記憶體；若在同一指令執行途中改寫 `.vendor_kit/`，可能導致未定義行為或下次執行才生效。
   * **建議流程**：升級必須是「分離兩步」或「明確兩階段」：
     1. **檢查階段**：比對 remote image digest，計算 `.version` diff。
     2. **寫入階段**：僅改寫 `.version`（遵循 vendor_kit「只改 version、不自動執行黑魔法」原則）。
     3. **下次啟動**：在下一次執行 `just` 時，啟動器自舉腳本先檢驗自身版本（`vendor_kit = "..."`），若自身版本改變，先拉取新 launcher image 覆寫 `.vendor_kit/`，再重啟執行後續工具下載。

---

### 5. 常見坑三：Windows 上無法覆寫執行中的 exe（File Locking）

1. **問題根本原因**：
   * Windows 核心（NTFS 與 PE loader）對處於執行狀態的二進制檔案（`.exe`、`.dll`）預設持有唯讀鎖與共用限制，禁止直接寫入覆寫（Truncate/Write）或刪除，會直接回報系統錯誤：`ERROR_ACCESS_DENIED`（os error 5）或 `ERROR_SHARING_VIOLATION`（os error 32）（[GitHub Issue: rust-lang/rustup#2441](https://github.com/rust-lang/rustup/issues/2441)）。
2. **前例：rustup 在 Windows 的自更新痛點**：
   * 在 Windows 上執行 `rustup self update` 時，只要背景有 IDE（VS Code）、language server（`rust-analyzer`、`rls`）或終端機正在使用 rustup 代理的 `rustc.exe`/`cargo.exe`，更新行程就會拋出 `Access is denied` 失敗（[GitHub Issue: rust-lang/rustup#2441](https://github.com/rust-lang/rustup/issues/2441)；[GitHub Issue: rust-lang/rustup#1869](https://github.com/rust-lang/rustup/issues/1869)）。
3. **業界解法（`self-replace` crate 機制）**：
   * Windows PE loader 開啟執行檔時帶有 `FILE_SHARE_DELETE` 權限，因此 Windows **允許重命名（Move/Rename）執行中的檔案**，但不允許覆寫或直接刪除。
   * Rust 社群通用的 `self-replace` crate 實作了三步置換法（[GitHub Source: mitsuhiko/self-replace/src/windows.rs](https://github.com/mitsuhiko/self-replace/blob/main/src/windows.rs)）：
     1. **Move/Rename**：將當前正在執行的 `tool.exe` 重命名為臨時檔（如 `tool.exe.old`）。
     2. **Write New**：將新下載的二進制檔寫入原本的 `tool.exe` 路徑。
     3. **Cleanup**：排程在進程退出或下次啟動時刪除 `.old` 殘留檔案。
4. **對 `vendor_kit` 的啟示**：
   * `vendor_kit` 雖然主要在 Docker 容器內解開 `dist/`，主機依賴 `git` + `just` + `docker`。
   * 但若專案未來在 Windows 主機上執行，將 container 內的二進制檔直接 extract 到本地掛載目錄（如 `.<name>/`）時：
     * 若背景有 Windows 處理序（例如 IDE、終端機或背景執行的 container volume 掛載）佔用了 `.<name>/tool.exe`，`docker cp` 或本地 script 將無法覆寫該檔案。
     * **因應對策**：工具抽取與更新應採用「先解壓至臨時目錄 `.<name>-new/`，再原子重命名（Rename/Swap）」或「提示使用者停止執行中容器/進程」，避免原地（In-place）覆寫造成權限錯誤。

---

## 來源清單

* https://rust-lang.github.io/rustup/concepts/updating.html#keeping-rustup-up-to-date
* https://docs.astral.sh/uv/configuration/installer/
* https://docs.astral.sh/uv/reference/cli/#uv-self-update
* https://github.com/bazelbuild/bazelisk/issues/117
* https://github.com/rust-lang/rustup/issues/1823
* https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper
* https://github.com/gradle/gradle/issues/8431
* https://github.com/rust-lang/rustup/issues/2441
* https://github.com/rust-lang/rustup/issues/1869
* https://github.com/mitsuhiko/self-replace/blob/main/src/windows.rs
exit=0
