本前例研究針對啟動器自我升級機制，深入查證 **Batect** 與 **Gradle Wrapper** 的設計，並分析其如何解決「舊版啟動器升級新版工具時，新版需要新參數／掛載」之問題。

---

### 1. Batect：`./batect --upgrade` 的自我替換機制（wrapper script vs. jar）

* **架構分工**：
  * **Wrapper Script（進 git）**：包含專案根目錄下的 shell 腳本 `./batect`（Linux/macOS）與批次檔 `batect.cmd`（Windows），負責環境檢查、下載與啟動 jar（[GitHub batect/batect.dev 原始碼](https://github.com/batect/batect.dev/blob/main/docs/reference/cli.mdx)）。
  * **Jar 核心（不進 git）**：Batect 核心邏輯打包為單一 JAR，不在版控內，而是由 wrapper 自動下載至使用者家目錄的快取空間（如 `~/.batect/cache/<version>/batect-<version>.jar`）（[Charles Korn 部落格專文](https://charleskorn.com/posts/2021/04/05/how-i-collect-telemetry-from-batect-users/)）。
* **自我升級運作流程**：
  * 當使用者執行 `./batect --upgrade` 時，當前運行的舊版 JAR 會向更新伺服器（`updates.batect.dev` API）查詢最新版本號。
  * 舊版 JAR 從伺服器下載最新的 wrapper scripts（`batect` 與 `batect.cmd`），並**直接覆寫專案目錄中現有的 wrapper script 檔案**（[Batect 官方更新說明文件](https://batect.dev)）。

---

### 2. Batect：升級順序（先換 wrapper 還是先換 jar？）

* **先換 wrapper script，下次執行時才換 jar**：
  * `./batect --upgrade` 執行完成時，**只覆寫了本地的 wrapper script**，並未在執行升級當下直接改動或預先替換正在運行的 jar（[Charles Korn 部落格專文](https://charleskorn.com/posts/2021/04/05/how-i-collect-telemetry-from-batect-users/)）。
  * 降落至磁碟的全新 wrapper script 內寫入了新版的版號與校驗碼。
  * **延遲下載 jar**：當使用者下一次調用 `./batect <task>` 時，新版 wrapper script 會讀取內嵌的新版號，檢查本地快取目錄尚未有該版本 jar，才觸發下載新版 JAR，驗證 checksum 後啟動新版執行（[Renovate batect-wrapper 官方模組說明](https://docs.renovatebot.com/modules/manager/batect-wrapper/)）。

---

### 3. Batect：wrapper 與 jar 版本的綁定方式

* **靜態內嵌與強綁定**：
  * Batect 的 wrapper script 內部直接宣告了兩行硬編碼常數：
    ```bash
    VERSION="0.85.0"
    CHECKSUM="<sha256-digest>"
    ```
    檔案註解明示「請勿手動修改此檔，升級時將被覆寫」（[GitHub batect/batect.dev 原始碼](https://github.com/batect/batect.dev/blob/main/docs/reference/cli.mdx)）。
  * Wrapper 與 JAR 是 **1 對 1 強制綁定**：特定版本的 wrapper script 必定且只能啟動該特定版本的 JAR。若要換版本，唯一途徑就是改寫 wrapper script 裡的 `VERSION` 與 `CHECKSUM`（手動改寫、透過 `./batect --upgrade` 改寫，或由 Renovate 自動發 PR 改寫）（[Renovate batect-wrapper 官方模組說明](https://docs.renovatebot.com/modules/manager/batect-wrapper/)）。

---

### 4. Gradle Wrapper：組件產生順序與 `gradle-wrapper.jar` 更新時機

* **由「當前舊版」執行**：
  * 執行 `./gradlew wrapper --gradle-version <new-version>` 時，是由當前正在運行的舊版 Gradle Daemon 執行 `Wrapper` task（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）。
* **檔案產生順序與更新時機**：
  1. **第一次執行（First Run）**：當前版本的 Gradle 只會改寫 `gradle/wrapper/gradle-wrapper.properties`，將屬性 `distributionUrl` 更新為指向新版 Gradle distribution zip（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）。
  2. **`gradle-wrapper.jar` 與腳本未更新**：第一次執行時，本機甚至尚未下載新版 Gradle distribution，當前的 Gradle 無法取得新版 JAR 與腳本，因此官方文件明確指出「`gradle-wrapper.jar` 在第一次執行時會保持未更動（left untouched）」（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）。
  3. **`gradle-wrapper.jar` 真正的更新時機**：只有在新版本 Gradle 被下載並實際啟動後再次執行 wrapper task，新版本的 Gradle 才會從自身 distribution 中解出新版 `gradle-wrapper.jar` 與 `gradlew` 腳本覆寫進專案（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）。

---

### 5. Gradle Wrapper：「double-run（跑兩次）」官方建議與對 vendor_kit 的設計啟發

* **官方明確建議 double-run**：
  * Gradle 官方文件在 *Upgrading the Gradle Wrapper* 章節明文提示：
    > *「Note that running the wrapper task once will update gradle-wrapper.properties only, but leave the Wrapper itself in gradle-wrapper.jar untouched. This is usually fine as new versions of Gradle can be run even with older Wrapper files. If you want **all** the Wrapper files to be completely up-to-date, you will need to run the wrapper task a second time.」*（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）
  * 其提示（Tip）補充：*「Don’t forget to run the wrapper task again to download the Gradle distribution binaries (if needed) and update the gradlew and gradlew.bat files.」*（[Gradle 官方文件：Upgrading the Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper)）。
* **對 vendor_kit 升級流程設計的啟發**：
  * **背景矛盾**：在 vendor_kit 中，工具與啟動器由 `.version` 宣告，啟動器 recipe 放在 `.vendor_kit/`（進 git），升級僅改 `.version`。若舊版啟動器 recipe 去啟動新版 image，新版 image 可能需要新的 Docker 參數或掛載路徑，舊 recipe 會直接失效。
  * **借鑒 Gradle double-run / Batect 兩階段升級模型**：
    1. **階層化隔離（Minimal Bootstrapper vs. Core Launcher）**：
       Batect 的 wrapper 本身極為單純（只負責解析版本、拉取、啟動），將「環境掛載」等複雜參數移到由 image 產生的階段，不要讓進 git 的啟動器包含脆弱的運行參數。
    2. **升級兩階段執行（Two-Phase Update）**：
       當使用者改寫 `.version` 中的 `vendor_kit = "..."` 之後，若執行 `just upgrade` 或執行任何 task：
       * **Phase 1（自我更新）**：啟動器先行比對目前 `.vendor_kit/` 內的 recipe 版本與 `.version` 是否一致；若不一致，**只做一件事**：用最原始的 `docker run` 將新版 image 中的 `.vendor_kit/` recipe 檔案抽出覆寫到專案目錄。
       * **Phase 2（重新調用）**：提示使用者重新執行，或在腳本內部透過 `exec just ...` 以全新的啟動器 recipe 重新進入流程，此時新版啟動器即可使用新版專屬的 Docker 參數與掛載。

---

### 來源清單

1. https://docs.gradle.org/current/userguide/gradle_wrapper.html#sec:upgrading_wrapper
2. https://github.com/batect/batect.dev/blob/main/docs/reference/cli.mdx
3. https://charleskorn.com/posts/2021/04/05/how-i-collect-telemetry-from-batect-users/
4. https://docs.renovatebot.com/modules/manager/batect-wrapper/
5. https://batect.dev
exit=0
