本研究針對 **vendor_kit** 框架之升級與回退流程，深入調研業界成熟工具與生態系的真實設計前例。依據「只要改版本檔（`git revert`）即可回退」與「需額外狀態/指令回退」兩大陣營進行成因解析，並歸納對 vendor_kit 的架構啟示。

---

### 1. 只要版本檔改回去（Git Revert）即可回退的前例分析

此類工具的核心特點在於：版本控制系統（Git）內的宣告檔即為系統行為的唯一真理來源（Single Source of Truth），回退動作完全等同於版本檔案的復原。

1. **Bazelisk（`.bazelversion`）**
   * **機制**：Bazelisk 作為 Bazel 的薄啟動器（Launcher / Wrapper），在執行時會遞迴向上搜尋目錄樹中的 `.bazelversion` 檔案。
   * **快取與重現**：Bazelisk 會自動解析該版本，並快取在使用者主目錄下的獨立目錄中（Linux/macOS 預設為 `~/.cache/bazelisk/bin/<fork>/bazel-<version>-<os>-<arch>`）。
   * **回退行為**：當開發者以 `git revert` 將 `.bazelversion` 改回舊版號時，下次執行 `bazel ...`（實際上是 Bazelisk）會讀取舊版號。若本機快取已有該二進位檔，則直接執行舊版；若無則自動下載，整個過程完全無需額外命令或重設全域狀態（來源：[Bazelisk 官方儲存庫文件](https://github.com/bazelbuild/bazelisk)）。

2. **Nix Flakes（`flake.lock`）**
   * **機制**：在 Nix Flakes 體系中，`flake.lock` 記錄了所有依賴 input 的精確鎖定資訊（包含 upstream git commit SHA、URL 以及內容雜湊 `narHash`）。
   * **快取與重現**：Nix 採用內容定址儲存（Content-Addressed Storage），所有產物存放在不可變的 `/nix/store/<hash>-<name>` 路徑中。
   * **回退行為**：當執行 `git revert flake.lock` 時，Nix 的求值器（Evaluator）立即指回舊的依賴雜湊。若本地 store 內仍保留有該 store path，評估與構建直接命中，達成 0 秒回退；若已被垃圾回收，Nix 也能依據 lock 檔中不可變的 commit/narHash 重新拉取並重現構建，完全不產生任何破壞性副作用（來源：[Nix 官方手冊 - Flakes 概念](https://nix.dev/concepts/flakes)）。

3. **Terraform Provider 依賴鎖定（`.terraform.lock.hcl`）**
   * **機制**：紀錄 Root Module 所使用的各 Provider 之鎖定版本以及跨平台校驗雜湊（`h1:` 或 `zh:`）。
   * **快取與重現**：Terraform 在執行 `terraform init` 時，會比對鎖定檔並將相應的 Provider 外掛下載至本機快取（如 `.terraform/providers/` 或全域 `plugin_cache_dir`）。
   * **回退行為**：若升級 Provider 後遇到重大瑕疵，只要透過 `git revert` 復原 `.terraform.lock.hcl`（並還原 `versions.tf` 的版本約束）並重新執行 `terraform init`，Terraform 即會重新掛載舊版 Provider 外掛。注意：此處純粹適用於 Provider 外掛二進位檔本身的切換，前提是尚未執行變更遠端資源或升級 State Schema（來源：[Terraform 官方文件 - Dependency Lock File](https://developer.hashicorp.com/terraform/language/files/dependency-lock)）。

4. **Gradle Wrapper（`gradle-wrapper.properties`）**
   * **機制**：專案透過 `gradle/wrapper/gradle-wrapper.properties` 中的 `distributionUrl` 宣告 Gradle 的發行版下載位址與版本（通常為 `-bin.zip`），並可選填 `distributionSha256Sum` 校驗雜湊。
   * **快取與重現**：Gradle Wrapper（`./gradlew`）啟動時，會根據 `distributionBase`（預設為 `GRADLE_USER_HOME`，即 `~/.gradle`）與 `distributionPath`（預設為 `wrapper/dists`），將解壓縮後的發行套件存放於按 URL Hash 隔離的獨立子目錄（例如 `~/.gradle/wrapper/dists/gradle-<version>-bin/<hash>/`）。
   * **回退行為**：一旦透過 `git revert` 將 `distributionUrl` 復原為舊版本，下次執行 `./gradlew` 時腳本立即解析舊 URL，並直接引導至既有的舊版本解壓快取目錄，達成無縫且無副作用的回退（來源：[Gradle 官方文件 - The Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)）。

---

### 2. 純 Git Revert 之所以可行的根本機制（Why they work）

上述工具能做到「`git revert` 即完成回退」，本質上遵循了純函數式與無副作用的軟體架構原則：

1. **宣告內容的絕對不可變性（Content Immutability）**：
   版本宣告所參照的實體（Release Tag、Git SHA、narHash、Distribution URL）具有唯讀與不可變特性，不會隨時間產生語意漂移。
2. **依版本/雜湊鍵值隔離的快取槽位（Version-keyed Cache Isolation）**：
   快取結構均為 `cache_root/<version_or_hash>/`。在執行升級時，系統採用「**新增槽位**（Additive Cache）」而非原地覆蓋（In-place Overwrite）。因此，升級前使用的舊版本 binary / distribution 依然完好無損地留存於本機磁碟中。
3. **啟動器的動態惰性解析（Lazy Resolution in Wrapper）**：
   專案不依賴全域 PATH 中的單一執行檔，而是透過薄啟動器（Bazelisk、gradlew 等）在每次執行當下動態讀取專案內的宣告檔，即時計算該派發哪一個版本的實體。
4. **零全域/主機外溢狀態（No Host-local Mutable State）**：
   工具的安裝與啟動完全被限制在專案目錄或特定使用者快取區內，不在全域登錄檔（Registry）或主機全域設定檔留存可變狀態，因此不會產生因版本切換而造成的全域狀態撕裂。
   （架構原則來源綜合參見：[Bazelisk 架構設計](https://github.com/bazelbuild/bazelisk)、[Nix 設計哲學](https://nix.dev/concepts/flakes) 與 [Gradle Wrapper 架構](https://docs.gradle.org/current/userguide/gradle_wrapper.html)）

---

### 3. 需要額外 Rollback 紀錄或指令的前例及其成因分析

相對於前述的純宣告式回退，許多系統無法單靠 `git revert` 完成回退，必須引入專門的 rollback 指令、狀態快照或人工清理程序。以下是常見的前例與成因：

1. **Rustup 的 `toolchain` 切換與本機目錄覆寫（`rustup override`）**
   * **成因**：狀態外溢至主機本機（Host-local state）。當開發者使用 `rustup override set <toolchain>` 為特定目錄綁定工具鏈時，該設定並不是寫入專案的 Git 追蹤檔案中，而是直接記錄在使用者家目錄的 `~/.rustup/settings.toml` 的 `[overrides]` 區塊內。
   * **為何需要額外指令**：因為改動完全獨立於 Git 之外，`git revert` 對此毫無作用；開發者必須明確執行 `rustup override unset` 或手動執行 `rustup default <toolchain>` 才能還原（來源：[The Rustup Book - Overrides](https://rust-lang.github.io/rustup/overrides.html)）。

2. **`mise`（前身為 rtx）本地狀態與 Shims 管理**
   * **成因**：多層環境維護與儲存積累。`mise` 將工具安裝於 `~/.local/share/mise/installs/`，並依賴 `~/.local/share/mise/shims` 進行指令攔截與派發，本機狀態則存於 `~/.local/state/mise/`。
   * **為何需要額外指令**：
     * 若在升級後退回版本，已安裝的高版本二進位檔案不會自動從硬碟移除，必須由使用者或排程明確呼叫 `mise prune`（清理非最新追蹤版本）或 `mise cache prune`（清理快取）。
     * 若工具的內部執行檔結構改變或 shim 快取不同步，必須執行 `mise reshim` 重建 shim 符號連結（來源：[Mise 官方文件 - Prune CLI](https://mise.jdx.dev/cli/prune.html) 與 [Mise 目錄架構說明](https://mise.jdx.dev/directories.html)）。

3. **Docker 映像檔垃圾回收（Image Garbage Collection / Pruning）**
   * **成因**：被動累積的不可變唯讀層。Docker Daemon 為了效能考量，以保守策略維護本機映像檔快取，不會主動刪除任何未被容器引用的映像檔。
   * **為何需要額外指令**：當專案由映像檔 A 升級至映像檔 B、隨後又 `git revert` 回退至 A 時，Docker Daemon 不會自動清除 B。若採用 mutable tag，舊映像檔會變成 Dangling（`<none>:<none>`）；若採用 digest pinning，映像檔 B 會作為「未被使用（Unused）」的完整映像檔長期滯留於磁碟。必須手動執行 `docker image prune` 或 `docker image prune -a` 才能回收空間（來源：[Docker 官方文件 - Prune unused Docker objects](https://docs.docker.com/engine/manage-resources/pruning/) 與 [Docker CLI - image prune](https://docs.docker.com/reference/cli/docker/image/prune/)）。

4. **Helm Rollback（`helm rollback`）**
   * **成因**：遠端運作狀態（Runtime State）與 Git 宣告脫鉤。Helm 負責管理 Kubernetes 叢集中的動態資源，其實際 Release 歷史以 Secret（或 ConfigMap）持久化於叢集之中，版本編號呈單向遞增（Append-only Revision）。
   * **為何需要額外指令**：若僅在 Git 倉庫中 revert 本地的 `values.yaml` 或 Chart，Kubernetes 叢集對此完全無感，工作負載仍維持在升級後的狀態。必須執行 `helm rollback <RELEASE> [REVISION]`，由 Helm 讀取叢集內的 Release Secret，計算叢集現況與目標 Revision 的 Manifest 差異，執行 pre/post-rollback lifecycle hooks，並對 Kubernetes API 派發資源更新（來源：[Helm 官方文件 - helm rollback](https://helm.sh/docs/helm/helm_rollback/) 與 [Helm 儲存後端機制說明](https://helm.sh/docs/topics/advanced/#storage-backends)）。

5. **Terraform State 版本不可降級（State Forward-only Constraint）**
   * **成因**：資料綱要的單向升級（Schema Irreversibility）。Terraform State 是記錄基礎設施真實狀態的單一資料結構。當新版 Terraform Core 或新版 Provider 對 State 進行了 `apply` 或更新，State 檔案內的綱要格式版本（`serial` 與 schema version）會被永久推進。
   * **為何需要額外指令/手段**：HashiCorp 官方的「v1.0 Compatibility Promises」明確指出：相容性保證僅適用於升級（Upgrades），**不保證支援降級（Downgrades are not guaranteed）**。若舊版 Terraform 讀取到由新版寫入的 State 檔，會引發解析錯誤而拒絕執行。此時單靠 `git revert` 程式碼完全無濟於事，必須從遠端儲存庫還原升級前的 State Snapshot 備份（來源：[HashiCorp 官方文件 - Terraform v1.0 Compatibility Promises](https://developer.hashicorp.com/terraform/language/v1-compatibility-promises)）。

---

### 4. 兩類回退模式之本質對比與架構權衡

| 評估維度 | 純版本檔回退模式（如 Bazelisk, Nix, Gradle） | 需額外狀態/指令回退模式（如 Helm, Terraform State, Mise） |
| :--- | :--- | :--- |
| **狀態所在地** | 專案 Git 倉庫內部（In-repo version file） | 外部全域設定、主機儲存、遠端資料庫/叢集 |
| **回退觸發成本** | 零學習成本：標準 `git revert` + 下次執行即生效 | 需特定 CLI 操作（`helm rollback`, `prune`, `restore`） |
| **冪等性與副作用** | 純讀取/純抽換（Pure & Idempotent），無全域副作用 | 存在狀態遷移（Migration）、Hook 執行、資料破壞風險 |
| **磁碟與資源影響** | 多版本快取並存，可能隨時間膨脹但隔離安全 | 舊版本未回收（Docker layers, Mise installs），或需專屬 GC |
| **資料向下相容性** | 不涉及持久資料綱要，僅抽換無狀態執行檔 | 涉及持久化綱要（Schema）的演進，單向寫入難以向下相容 |

**架構權衡結論**：
若工具本質屬於「**無狀態的開發者 CLI 或建置執行器**」，「純 Git Revert 即可回退」是極佳的設計範式；但若涉及「**遠端持續運行的實體狀態**」或「**資料綱要不可逆遷移**」，則不可避免地必須設計專門的 rollback 指令與狀態備份機制（來源：[Terraform 相容性保證規範](https://developer.hashicorp.com/terraform/language/v1-compatibility-promises) 與 [Bazelisk 架構設計](https://github.com/bazelbuild/bazelisk)）。

---

### 5. 對 vendor_kit 回退流程設計的具體啟示與架構建議

結合 vendor_kit 的環境特徵（Docker + git + just、`.version` 鎖定 digest、`.<name>/` 為自動抽出的未追蹤目錄、工具不自動改使用者檔案），回退流程應採納以下具體設計：

1. **全面貫徹「純 Git Revert 即完成回退」的架構目標**
   * `.version` 採用 `ghcr.io/<org>/<name>:<tag>@sha256:<digest>`，具備絕對不可變性（Content-addressed Immutability）。
   * 當使用者執行 `git revert` 修改 `.version` 後，啟動器（launcher recipe）在下次 `just` 執行時，檢測到現行 `.<name>/` 的已安裝 digest 與 `.version` 記錄不符，即刻以宣告的舊 digest 重新抽出 `dist/`。

2. **嚴格遵循「工具不自動改使用者檔案」原則，防範 Terraform State 陷阱**
   * vendor_kit 規定工具「只顯示 diff，不自動改檔案」，這在架構上天然避開了資料綱要不可降級的痛點。只要工具不主動對專案檔案進行不可逆的升級轉換，回退就永遠只需處理 `dist/` 二進位檔的置換。

3. **設計基於 Digest 的本機快取以實現秒級回退（借鑑 Bazelisk 與 Gradle）**
   * 現狀為「每次 `just` 依 `.version` 安裝」，若回退時重新執行 `docker run` 抽出 `dist/`，會有額外的容器啟動與 I/O 成本。
   * **建議**：可將解抽出的檔案存放在以 digest 命名的內部快取中（如 `.<name>/.cache/<digest>/`），並透過原子符號連結（symlink）或覆寫指向當前版本。一旦發生 `git revert`，啟動器可在 1 秒內切換至舊版本，無需重跑 Docker 抽取程序。

4. **主動提供 Docker 垃圾回收（Image GC）機制（借鑑 Docker Prune 與 Mise Prune）**
   * 升級後再回退，主機上的 Docker Daemon 會累積未使用的升級版本映像檔。
   * **建議**：啟動器不應在日常 `just` 流程中自動執行慢速且具全域干擾性的 `docker image prune`，但應在 `vendor_kit` 中提供輔助 recipe（例如 `just vendor-kit-clean`），或在升級/回退完成時提示磁碟佔用狀況，給予使用者明確的清理途徑。

5. **堅決不將工具狀態寫入主機全域環境（避免 Rustup / Mise 的 Local State 弊病）**
   * 切勿在 `~/.vendor_kit` 或全域環境變數中維護工具綁定關係。確保專案的所有工具依賴完全被封閉在 Git 追蹤的 `.version` 與專案 local 的 `.<name>/` 之中，以保證跨機器、跨 CI/CD 節點與歷史 commit 簽出時的 100% 行為一致性。

---

### 來源清單

* https://github.com/bazelbuild/bazelisk
* https://nix.dev/concepts/flakes
* https://developer.hashicorp.com/terraform/language/files/dependency-lock
* https://docs.gradle.org/current/userguide/gradle_wrapper.html
* https://rust-lang.github.io/rustup/overrides.html
* https://mise.jdx.dev/cli/prune.html
* https://mise.jdx.dev/directories.html
* https://docs.docker.com/engine/manage-resources/pruning/
* https://docs.docker.com/reference/cli/docker/image/prune/
* https://helm.sh/docs/helm/helm_rollback/
* https://helm.sh/docs/topics/advanced/#storage-backends
* https://developer.hashicorp.com/terraform/language/v1-compatibility-promises
exit=0
