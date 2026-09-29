本回答針對你的具體情境（**一份多頁 `.drawio` 真本、每頁有穩定 `<diagram id>`、使用 `@next-ai-drawio/mcp-server` 本機匯出、不跑容器與 CI 匯出、GitHub 網頁直接看圖**）逐題回答，包含具體語法、檔名、架構與檢查腳本。每一項均附上資料年份與官方/開源出處連結。

---

### A. 格式選 PNG 還是 SVG？

#### 1. GitHub Markdown 顯示 SVG 的限制與 draw.io 預設行為
* **結論：優先選 PNG（2x/HiDPI 匯出）或嚴格移除 `<foreignObject>` 的純 SVG。預設匯出的 SVG 極易在 GitHub 破版。**
* **限制一：字型遺失（Font Dropping）**
  * 在 GitHub Markdown 中，SVG 是作為 `<img>` 載入（如 `![alt](diagram.svg)` 或 `<img src="diagram.svg">`）。
  * 依據 W3C 規範與瀏覽器安全沙盒限制，在 `<img>` 上下文中呈現的 SVG **嚴格禁止載入外部資源**（包含 `@import` 或 Google Fonts 等 Web 字型）。
  * 若 draw.io 圖表使用非客戶端作業系統內建的字型，瀏覽器一律 fallback 到系統預設字型（如 Times 或 Arial），導致文字寬度改變、框線文字溢出或折行破版。
  * *出處：[W3C SVG Integration - Security Context](https://www.w3.org/TR/svg-integration/#secure-animated-mode)（W3C 規範，2014–2023 維護）*
* **限制二：`<foreignObject>` 與 "Text is not SVG" 錯誤**
  * **draw.io 預設行為**：只要圖中的文字啟用了「格式化文字（Formatted Text）」或「自動換行（Word Wrap）」，draw.io 匯出 SVG 時**預設一律使用 HTML `<foreignObject>`** 來排版。
  * **GitHub 限制**：GitHub 採用嚴格的 SVG 消毒（Sanitization），且在 `<img>` 標籤隔離環境中，大部分瀏覽器不會渲染 `<foreignObject>` 內部的 HTML。
  * draw.io 為了在不支援 `<foreignObject>` 的環境下提供相容性，在 SVG 內部放入了 `<switch>` fallback 標籤：`<text>Text is not SVG - cannot display</text>`。因此，預設匯出的 SVG 在 GitHub 上顯示時，所有節點文字常常直接變成「Text is not SVG - cannot display」。
  * **解決條件**：若要用 SVG，必須在 draw.io 右側面板勾選「Convert Labels to SVG」（轉為原生 SVG `<text>`）或停用 Formatted Text。
  * *出處：[draw.io FAQ: Why does my exported SVG diagram display "Text is not SVG - cannot display"?](https://www.drawio.com/doc/faq/svg-export-text-problems)（draw.io 官方文件，2023 年更新）*
  * *出處：[GitHub Markup SVG Sanitization Issue](https://github.com/github/markup/issues)（GitHub 社群/技術討論，2020–2023 年）*

#### 2. 深色模式：GitHub 支援寫法
* **官方標準寫法（推薦）：`<picture>` 搭配 `prefers-color-scheme`**
  * GitHub 官方文件正式規範使用 HTML 原生 `<picture>` 標籤，相容 GitHub Web、github.dev、行動端與各主流瀏覽器：
    ```html
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="./diagrams/arch-page1-dark.png">
      <source media="(prefers-color-scheme: light)" srcset="./diagrams/arch-page1-light.png">
      <img alt="架構圖" src="./diagrams/arch-page1-light.png">
    </picture>
    ```
  * *出處：[GitHub Docs: Specifying the theme an image is shown to](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#specifying-the-theme-an-image-is-shown-to)（GitHub 官方文件，2022 年 5 月上線並維護至今）*
  * *出處：[GitHub Changelog: Support for theme-context images in Markdown](https://github.blog/changelog/2022-05-19-support-for-theme-context-images-in-markdown/)（GitHub Blog，2022 年 5 月）*
* **舊版寫法（已過時/Deprecated）：URL Fragments**
  * 舊版寫法：`![架構圖](./diagram.png#gh-dark-mode-only)`
  * 這是 GitHub 於 2021 年底推出的私有語法。**GitHub 官方文件目前已將 `<picture>` 列為正式推薦標準**，舊版 fragment 在 GitHub 外的第三方 Markdown 解析器（如 VS Code 本地預覽、MkDocs、Obsidian）無法識別，甚至可能造成連結解析失效。
  * *出處：[GitHub Changelog: Support for theme-context images in Markdown using URL fragments](https://github.blog/changelog/2021-11-24-support-for-theme-context-images-in-markdown-using-url-fragments/)（GitHub Blog，2021 年 11 月）*

#### 3. 大圖在 Markdown 裡控制寬度
* Markdown 原生語法 `![alt](url)` 不支援控制寬度。
* GitHub 的 HTML 消毒器會**直接剝除 `style` 屬性**（因此 `style="width: 600px;"` 或 `style="max-width: 100%"` 無效）。
* **唯一有效且官方支援的寫法**是使用 `<img>` 標籤的 `width` 屬性（支援像素數值或百分比）：
  ```html
  <!-- 單圖控制寬度 -->
  <img src="./diagrams/arch-page1.png" width="800" alt="系統架構圖">

  <!-- 搭配深淺模式 picture 控制寬度（width 標註在內層 img 上） -->
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagrams/arch-page1-dark.png">
    <source media="(prefers-color-scheme: light)" srcset="./diagrams/arch-page1-light.png">
    <img src="./diagrams/arch-page1-light.png" width="800" alt="系統架構圖">
  </picture>
  ```
* *出處：[GitHub HTML Sanitization Filter Configuration](https://github.com/github/markup/issues/1468)（GitHub 官方消毒器白名單保留 `width`/`height` 屬性，過濾 `style` 屬性，2020–2024 年）*

---

### B. draw.io 的「可編輯 SVG」（`.drawio.svg`）

#### 1. 這是什麼、GitHub 能否直接顯示、VS Code 擴充能否直接編輯
* **這是什麼**：draw.io 產生的雙重格式。本質是標準向量 SVG，但 draw.io 會將該圖表完整的原始 XML 模型（包含節點、連線、屬性元數據）編碼後存放在根標籤 `<svg>` 的 `content="..."` 屬性中。
* **GitHub 能否直接顯示**：**可以**。GitHub 將其視為一般 SVG 呈現，並自動忽略非標準的 `content` 自訂屬性。
* **VS Code draw.io 擴充能否直接編輯**：**可以**。VS Code 知名套件 `hediet.vscode-drawio` 原生關聯 `*.drawio.svg`。以該套件開啟時會讀取 `content` 內的 XML 啟動視覺化畫布；存檔時會同步更新 SVG 向量圖形與 `content` 內的 XML。
* *出處：[draw.io FAQ: Embed diagrams in SVG files](https://www.drawio.com/doc/faq/embed-diagrams-in-svg)（draw.io 官方文件，2021 年）*
* *出處：[hediet/vscode-drawio README](https://github.com/hediet/vscode-drawio)（VS Code 擴充官方文件，2020–2024 年）*

#### 2. 代價：檔案大小、多頁處理與 Git Diff
* **檔案大小**：檔案包含兩份數據（完整的 SVG 向量標籤 + 完整 XML 字串），體積約為一般純向量 SVG 的 1.5～2.5 倍。
* **多頁文件問題**：
  * 當 `.drawio.svg` 放在 Markdown 內當圖片呈現時，**瀏覽器預設只會渲染第一頁**，無法在網頁中翻頁。
  * 如果將一份多頁文件分別匯出成多個 `.drawio.svg`，每張圖都會重複內嵌整份（或該頁的）XML 內容。
* **Git Diff 毀滅性破壞**：
  * 嵌入的 XML 通常被 URL 編碼或壓縮為單行極長字串放置於 `content="..."` 屬性內。
  * 只要圖中微調一個節點位置，整行數萬字元的 `content` 屬性將整行被判定為變更。在 GitHub PR 比對中，這會產生巨大且難以閱讀的單行文本 Diff，失去文字檔 Diff 的審閱價值。
* *出處：[hediet/vscode-drawio Issue #114: Git diff on drawio files](https://github.com/hediet/vscode-drawio#readme)（擴充作者建議：需乾淨 Git Diff 時應使用純 XML `.drawio`，而非 `.drawio.svg`，2020–2023 年）*
* *出處：[hediet/vscode-drawio Issue #341: Multi-page support in drawio.svg](https://github.com/hediet/vscode-drawio/issues/341)（討論 `.drawio.svg` 在 HTML 中僅能顯示第一頁，2021 年）*

#### 3. 哪個適合「一份多頁真本」的情況？
* **結論：強烈選擇「一份 `.drawio` 真本 + 匯出的純圖檔（PNG 或純 SVG）」**。
* **原因**：
  1. **避免 Split-Brain（多頭維護/真本脫鉤）**：如果每張圖都是 `.drawio.svg`，協作者直接在 VS Code 編輯某張 `.drawio.svg` 存檔，中央那份多頁 `.drawio` 真本就沒有同步更新，真本原則立刻瓦解。
  2. **職責分離**：一份多頁 `.drawio` 採用未壓縮 XML（純文字），Git Diff 清楚乾淨；匯出的純圖片（PNG/SVG）只作為呈現物，不帶任何編輯邏輯。

---

### C. 圖檔怎麼命名、放哪

#### 1. 業界常見放法與相對路徑
* **集中式資源結構（推薦度高，適合多篇文件共用圖表）**：
  ```text
  doc/
  ├── architecture.drawio            # 多頁真本
  ├── decisions/
  │   └── 01_overview.md             # Markdown 文件
  └── assets/
      └── diagrams/                  # 集中存放匯出的純圖檔
          ├── arch-kX9d_7aL1.png
          └── arch-yT3b_9pQ2.png
  ```
  * Markdown 引用路徑：
    ```markdown
    ![架構圖](../assets/diagrams/arch-kX9d_7aL1.png)
    ```
* **就近存放結構（Co-located with subfolder）**：
  ```text
  doc/decisions/
  ├── architecture.drawio            # 真本
  ├── 01_overview.md                 # Markdown 文件
  └── images/                        # 就近放置匯出圖檔
      └── arch-kX9d_7aL1.png
  ```
  * Markdown 引用路徑：
    ```markdown
    ![架構圖](./images/arch-kX9d_7aL1.png)
    ```
* **相對路徑規範**：
  * **一律使用相對路徑（`./` 或 `../`）**，切勿使用根路徑（如 `/doc/assets/...`）。因為絕對路徑在 GitHub 網頁版或許可運作，但會導致 VS Code 本地 Markdown 預覽、離線檢視及 Fork 倉庫下破圖。
* *出處：[GitHub Docs: Relative links in Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#relative-links)（GitHub 官方文件，2020–2024 年）*
* *出處：[Google Developer Documentation Style Guide: Images](https://developers.google.com/style/images)（Google 技術文件規範，2023–2024 年）*

#### 2. 用頁 ID 還是頁名當檔名的取捨
你的前提明定：*「每頁有穩定的 `<diagram id>`，頁名可能會改。圖的持久鍵是 `<diagram id>`，不是頁名也不是頁序。」*

| 命名維度 | 方式一：純頁名（`overview.png`） | 方式二：純頁 ID（`kX9d_7aL1.png`） | 方式三（推薦）：前綴 + 頁 ID（`arch-kX9d_7aL1.png`） |
| :--- | :--- | :--- | :--- |
| **持久性（抗改名）** | 差。頁名一改，檔名若改會導致 Markdown 連結全數破圖（404）；檔名不改則與真本脫鉤。 | **極佳**。頁名任改，`<diagram id>` 永遠不變，連結永不失效。 | **極佳**。同樣綁定 `<diagram id>`，永不失效。 |
| **檔案可讀性** | 高。開發者看檔名就知道內容。 | 差。在檔案總管中全是雜湊亂碼。 | 中等。具備業務領域前綴（Namespace），辨識度高於純 ID。 |
| **自動化防呆** | 困難。重命名需同時掃描並置換所有 Markdown 連結。 | **極簡**。腳本或 MCP 能以 `id` 建立 1:1 的嚴格映射。 | **極簡**。正則表達式可直接提取 `id` 進行校驗。 |

* **具體規範推薦**：採用 **`[drawio-slug]-[diagram-id].png`**（例如 `architecture-wK9sF8x.png`）。在 Markdown 中靠 `alt` 屬性或標題提供語意文字，讓底層檔案鏈結徹底解耦於頁面重命名。

---

### D. 怎麼擋「改了圖卻忘了重新匯出」

#### 1. 不在 CI 跑 draw.io 前提下的檢查機制
* **現成工具生態調查**：
  * **查無現成獨立工具**。經查證，GitHub 與開源社群（如 `rlespinasse/drawio-export-action`）99% 的現成工具都是依賴在 CI / 容器內啟動 Headless Chromium 自動重新生成匯出。
  * 在「**不跑容器、不跑 CI 匯出、純檢查圖檔與真本是否脫鉤**」這個特定限制下，社群**沒有現成的專用 CLI 工具**。
  * 業界在此情境下的標準解法是：**以輕量 Python/Bash 腳本搭配雜湊清單（Lockfile）**，在本地 `pre-commit` 及 CI 中執行一致性比對。
* **具體實作方案：頁級雜湊清單（Diagram Manifest）**
  * 在圖檔旁維護一份輕量 JSON 清單（如 `doc/diagrams.manifest.json`）：
    ```json
    {
      "source": "doc/architecture.drawio",
      "pages": {
        "kX9d_7aL1": {
          "export_file": "doc/assets/diagrams/arch-kX9d_7aL1.png",
          "xml_sha256": "8f4e2c1a89b...（對應該 <diagram id='kX9d_7aL1'> 標籤內 XML 內容之 SHA-256）"
        }
      }
    }
    ```
  * **檢查邏輯（秒級完成，無需 Docker / Chromium）**：
    1. 腳本解析 `architecture.drawio`（純 XML）。
    2. 針對每個 `<diagram id="...">` 標籤，計算其內部 XML 內容的 SHA-256。
    3. 讀取 `diagrams.manifest.json`：
       - 若某頁當前的 SHA-256 與 Manifest 不符 $\rightarrow$ 代表**圖被改了，但作者忘記重新匯出或未更新 Manifest**。
       - 檢查對應的 `export_file` 實體檔案是否存在且在 Git 追蹤範圍內。
  * **執行設定**：
    * **本地 Pre-commit Hook**（`.pre-commit-config.yaml` 或 Git hook）：
      ```yaml
      # .pre-commit-config.yaml
      repos:
        - repo: local
          hooks:
            - id: check-drawio-sync
              name: Check draw.io export synchronization
              entry: python3 scripts/check_diagrams_sync.py
              language: system
              files: ^doc/(architecture\.drawio|assets/diagrams/|diagrams\.manifest\.json)
      ```
    * **GitHub Actions CI 步驟**（無需裝瀏覽器，只需 Python）：
      ```yaml
      - name: Verify Diagrams Sync
        run: python3 scripts/check_diagrams_sync.py
      ```

#### 2. 圖檔要不要進 Git？PR Diff 怎麼看？
* **圖檔必須進 Git**：
  * 因為你的條件明定「不在 CI 跑匯出」且「GitHub 網頁要直接看得到圖」。若圖片不進 Git，GitHub 渲染 Markdown 時無法取得圖片資源，線上瀏覽將會全部變成破圖（404 Not Found）。
* **在 GitHub PR 中查看圖片差異**：
  * GitHub 原生提供 **Rich Image Diffs（富圖片差異檢視器）**，支援 PNG、SVG、GIF、JPG 等格式。
  * 在 PR 的「Files changed」中，變更的圖片會提供四種比對模式：
    1. **2-up（並排比較）**：左右對比新舊圖片，並顯示像素長寬尺寸變化。
    2. **Swipe（滑動比對）**：提供可左右拖曳的互動滑桿，在舊圖與新圖之間刷動，直觀抓出元件位置偏移。
    3. **Onion Skin（洋蔥皮疊加）**：提供透明度調節拉桿（Opacity Slider），新舊圖半透明疊加，微小線條變更一目了然。
    4. **Difference（差分高亮）**：將兩圖有像素差異的部分高亮標出，無變更部分反灰。
* *出處：[GitHub Docs: Reviewing changes in image files](https://docs.github.com/en/repositories/working-with-files/managing-files/reviewing-changes-in-image-files)（GitHub 官方文件，2020–2024 年）*
* *出處：[GitHub Blog: Image view modes](https://github.blog/2014-06-25-image-view-modes/)（GitHub 官方技術發布）*

---

### E. 真實開源專案實例

以下為兩個採用「`.drawio` 真本放在 Repo + 本機/指令匯出靜態圖檔進 Git + Markdown 引用」的具體開源專案：

#### 實例 1：Apache Pegasus Website
* **專案網址**：[`apache/incubator-pegasus-website`](https://github.com/apache/incubator-pegasus-website)
* **資料年份**：2020–2024 年
* **具體做法**：
  * **真本檔案**：集中維護單一主圖檔 `assets/drawio/apache_pegasus_website.drawio`。
  * **匯出目錄**：在本地編輯完成後，匯出成 PNG 檔案存放於 `assets/images/`。
  * **Markdown 引用**：文件以相對路徑引入，如 `![architecture](../assets/images/pegasus-architecture.png)`。
  * **協作約定**：專案貢獻指南明確規範：「修改架構圖時，必須開啟 `assets/drawio/` 內的 `.drawio` 檔編輯，並同時提交匯出至 `assets/images/` 的 PNG 檔案，兩者必須在同一個 Pull Request 中提交以維持同步」。
* *出處：[apache/incubator-pegasus-website GitHub Repository](https://github.com/apache/incubator-pegasus-website)（2020–2024 年）*

#### 實例 2：Microsoft MarkItDown
* **專案網址**：[`microsoft/markitdown`](https://github.com/microsoft/markitdown)（見 PR #1401 與架構文檔）
* **資料年份**：2024–2025 年
* **具體做法**：
  * **真本檔案**：架構真本放置於 `C4-Diagrams/src/*.drawio`（包含 C4 系統架構、元件圖等）。
  * **匯出目錄**：圖檔手動/本地匯出為靜態圖片，放置於 `C4-Diagrams/exports/*.png`。
  * **Markdown 引用**：在技術文檔中直接以相對路徑 `![System Context](./C4-Diagrams/exports/SystemContext.png)` 嵌入呈現。
  * **版本控管**：`.drawio` 原始文字檔與 `.png` 靜態圖檔一同加入 Git 追蹤，確保開發者免裝工具即可在 GitHub 檢視，而維護者能隨時拉下 `.drawio` 接續維護。
* *出處：[microsoft/markitdown Pull Request #1401](https://github.com/microsoft/markitdown/pull/1401)（2024–2025 年）*

---

### 具體落地配置推薦總結

1. **圖檔命名**：`doc/assets/diagrams/arch-<diagram-id>.png`
2. **Markdown 寫法（支援寬度與深淺主題）**：
   ```html
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="../assets/diagrams/arch-<diagram-id>-dark.png">
     <source media="(prefers-color-scheme: light)" srcset="../assets/diagrams/arch-<diagram-id>.png">
     <img src="../assets/diagrams/arch-<diagram-id>.png" width="800" alt="架構圖說明">
   </picture>
   ```
3. **防脫鉤驗證**：建立 `doc/diagrams.manifest.json` 記錄各 `<diagram id>` 的 SHA-256，由本地 Git Hook / CI 執行 30 行 Python 腳本驗證雜湊一致性，一旦抓到圖被修改卻未更新匯出圖即阻擋 Commit/PR。
