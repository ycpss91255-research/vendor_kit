> **這份已作廢，不得當現況方案。** Gemini（agy）查來的原文，未經查證就寫下的部分很多。
> r97-export 雙軌查證的結論：整份文件架在「主機不裝第三方 binary、用容器匯出」這個**錯誤前提**上
> （那是 VK 對它的使用者的承諾，不是我們畫圖的限制）；`-p/--page-index` 說成 0-based（實際 1-based，
> 傳 0 會 exit 1）；三段示範迴圈照抄一頁都匯不出來；justfile 範例有 SyntaxError 與 just 插值寫錯；
> 引錯兩個 issue、三個出處連結 404。兩軌一致的判斷是**整份文件沒有一段被跑過**。
> 它也漏掉本機唯一實際可用的那條路：已掛好的 drawio MCP。
> 逐條查證見 `../review_log/codex/r97-export-claims.md` 與 `../review_log/r97_雙軌結論.md`。

這份回答針對你的硬性限制（主機僅有 Docker / Git / just / POSIX 工具、不裝第三方 binary、單一 77 頁 `.drawio`、GitHub 網頁可視、CI/本機同一條指令、重現性），逐題提供具體指令、Docker image、參數與出處資料年份。

---

### A. 匯出方式有哪些？各自的實際指令是什麼？

#### 1. drawio desktop CLI（Headless 跑法與容器踩坑）
官方 `drawio-desktop` 本質是基於 Electron / Chromium 的桌面應用程式，目前**未提供**純文字終端模式（`--headless=new`）。在無桌面（Linux CI / 容器）環境執行必須具備虛擬 X 伺服器與 Chromium 專用參數。

- **需要 Xvfb 嗎？**
  **需要**。Linux 下 Electron 啟動時必須連上 X11 Display，否則直接拋出 `Cannot open display` 錯誤退出。標準做法是透過 `xvfb-run -a`（`-a` 自動挑選未佔用的 display 埠號，避免多工衝突）。
- **容器內 Electron 常見三大問題與解法：**
  1. **Chromium Sandbox 崩潰**：Docker 預設 seccomp 限制了 user namespaces，會觸發 `The SUID sandbox helper binary was not found or is not configured properly`。在容器內跑必須在 `drawio` 指令加上 `--no-sandbox`。
  2. **`/dev/shm` 記憶體耗盡（SIGBUS / Crash）**：Docker 預設 `/dev/shm` 只有 64MB。Chromium 處理圖形渲染與處理 77 頁大檔時極易耗盡，導致 renderer process 被 killed。
     - **解法**：`docker run` 必須帶 `--shm-size=1g` 或 `--shm-size=2g`。若容器環境無法調 shm，可傳入 Chromium 參數 `--disable-dev-shm-usage`（會改寫 `/tmp`，但效能較慢）。
  3. **GPU 硬體加速報錯**：無顯卡環境會狂噴 GPU 錯誤訊息，需帶 `--disable-gpu`。
- **容器內實際執行指令（以官方安裝套件為例）：**
  ```bash
  xvfb-run -a /opt/drawio/drawio \
    -x -f png \
    --no-sandbox \
    --disable-gpu \
    --disable-dev-shm-usage \
    -p 0 \
    -o /data/page-0.png \
    /data/architecture.drawio
  ```
  *(出處：[jgraph/drawio-desktop issue #137](https://github.com/jgraph/drawio-desktop/issues/137) 與 [Chromium Docker Running Guidelines](https://github.com/puppeteer/puppeteer/blob/main/docs/troubleshooting.md#running-puppeteer-in-docker)，資料年份：2023–2024)*

---

#### 2. 現成專門做 drawio 匯出的 Docker image
社群與官方目前的主要映像檔狀況如下：

| Docker Image | 維護狀況與最後更新 | 支援輸出格式 | 說明與適用性 |
| :--- | :--- | :--- | :--- |
| **`rlespinasse/drawio-export`** | **主要維護中**<br>（2026 年最新 tag `v4.x` / `latest`，核心元件 `drawio-exporter` 釋出 `v1.6.0`） | `png`, `jpg`, `pdf`, `svg`, `xml`, `adoc`, `md` | **社群首選推薦**。基於 Debian + Xvfb + drawio-desktop + 自研 Rust 匯出封裝，專為 CI 設計，內建自動分頁輸出與 `--on-changes` 增量匯出。 |
| **`rlespinasse/drawio-desktop-headless`** | **維護中**<br>（隨上者同步維護） | 同 drawio 原生 | 僅打包 Xvfb 與 draw.io binary 的純乾淨基底映像檔，適合自己寫 shell 腳本精準調度。 |
| **`jgraph/drawio`** | **官方維護中**<br>（持續更新） | **不支援 CLI 匯出** | **不可用**。這是 diagrams.net 的 **Web App 伺服器**（Tomcat/Jetty），提供瀏覽器網頁版操作，映像檔內無任何 CLI 匯出指令。 |
| **`accetto/ubuntu-vnc-xfce-drawio-g3`** | **維護中**<br>（2024–2025 更新） | 同 drawio 原生 | 帶完整 XFCE 桌面與 noVNC Web GUI 的笨重映像檔（超過 2GB），不適合作為純 CI/CLI 匯出工具。 |

- **`rlespinasse/drawio-export` 實際指令：**
  ```bash
  docker run --rm \
    --shm-size=1g \
    -u $(id -u):$(id -g) \
    -v "$(pwd):/data" \
    rlespinasse/drawio-export:latest \
    --format png \
    --folder /data/doc/assets \
    /data/architecture.drawio
  ```
  *(出處：[rlespinasse/drawio-export GitHub](https://github.com/rlespinasse/drawio-export)、[Docker Hub rlespinasse/drawio-export](https://hub.docker.com/r/rlespinasse/drawio-export)，資料年份：2024–2026)*

---

#### 3. 不靠 Electron 的純程式庫路線（直接解 mxGraph XML 自行繪製）
- **結論：實際「不可用」，僅能處理簡單幾何圖形。**
- **原因：**
  Draw.io 架構並非單純的向量標籤，其繪圖完全依賴前端瀏覽器的 DOM、Canvas 與 mxGraph JS 排版運算：
  1. **文字排版**：Draw.io 的文字預設使用 HTML-formatted text，外銷時是 SVG 的 `<foreignObject>`，其自動折行、字級計算依賴瀏覽器渲染引擎的 `measureText()`。純 Python/Rust/Go 解析器無法計算實際字寬。
  2. **複雜元件與 Stencils**：AWS / GCP / Kubernetes 圖示、自訂形狀（Stencil XML 代碼）、圓角連線的貝茲曲線算路（Orthogonal routing）等，皆由 Draw.io 前端 JS 核心在記憶體動態運算座標。
  3. 目前開源社群（如 `drawio-renderer`、`mxgraph-python` 等探索性專案）僅能還原簡單的矩形、橢圓與固定座標連線，面對 77 頁架構圖中的複合群組、豐富文字與連線路由時，輸出會嚴重變形、甚至直接崩潰。
  *(出處：[jgraph/drawio GitHub Discussions - Server side rendering without browser](https://github.com/jgraph/drawio/discussions)，資料年份：2022–2024)*

---

### B. 多頁怎麼處理？

#### 1. 指定「第 N 頁」或「某個頁名」
- **官方 `drawio` CLI**：
  - **僅支援 index**：參數為 `-p, --page-index <number>`（**0-based 索引**，`0` 代表第 1 頁，`1` 代表第 2 頁）。
  - **不支援 `--page-name` 或 `--page-id`**：官方原生 CLI **沒有**提供頁名或 ID 的查詢與篩選參數。
  *(出處：[jgraph/drawio-desktop CLI Help Documentation](https://github.com/jgraph/drawio-desktop)，資料年份：2023–2024)*

#### 2. 輸出檔名能用頁名／頁 id 嗎？頁序變動時檔名會不會錯位？
- **若使用 index（如 `drawio-1.png`）：**
  **頁序變動會立刻發生「檔名內容大錯位」**。當架構圖在中間插入新的一頁，第 3 頁之後的所有編號往後推，造成 Markdown 引用與圖片內容完全張冠李戴，且 Git 歷史會產生全部圖片被覆寫的假 diff。
- **能用頁名或頁 ID 嗎？如何做到？**
  `.drawio` 本身是 XML 格式，其根標籤 `<mxfile>` 下每一頁都是獨立的 `<diagram>` 節點：
  ```xml
  <mxfile ...>
    <diagram id="aBc123XyZ" name="架構總覽">...</diagram>
    <diagram id="dEf456WvU" name="認證流程">...</diagram>
  </mxfile>
  ```
  **重要特性**：即使 Draw.io 存檔時啟用了 Deflate 壓縮，`<diagram>` 標籤本身的 `id` 與 `name` 屬性也**永遠是明文**！
  因此，穩定的做法是在容器內用一段簡單的 POSIX 指令或 Python（標準庫 `xml.etree.ElementTree`）提取出 `(index, name, id)`，再呼叫 `drawio -p <index> -o <name>.png`：
  ```bash
  # 示範在容器內以 Python 提取頁面並依「頁名」或「ID」精確匯出：
  python3 -c "
  import xml.etree.ElementTree as ET, subprocess, re

  tree = ET.parse('architecture.drawio')
  for idx, diag in enumerate(tree.getroot().findall('.//diagram')):
      name = re.sub(r'[^\w\-]', '_', diag.get('name', f'page_{idx}'))
      page_id = diag.get('id')
      out_path = f'doc/assets/{name}.png'
      cmd = ['xvfb-run', '-a', '/opt/drawio/drawio', '-x', '-f', 'png', '-p', str(idx), '-o', out_path, 'architecture.drawio', '--no-sandbox']
      subprocess.run(cmd)
  "
  ```
  以頁名或 Page ID 命名，頁籤順序怎麼挪動都不會讓檔名錯位。
  *(出處：[diagrams.net file format specification](https://www.drawio.com/doc/faq/uncompressed-xml)，資料年份：2023–2024)*

#### 3. 「一次匯出全部頁、每頁一檔」的做法
1. **原生 CLI 行為**：`drawio -x -a`（`--all-pages`）**僅支援 PDF 格式**，不支援 PNG / SVG。
2. **`rlespinasse/drawio-export` 做法**：其封裝的 `drawio-exporter` 會在內部解析 XML 頁數，並用迴圈逐頁呼叫 `drawio -p $i`，匯出成 `architecture-1.png`, `architecture-2.png`。
3. **高效替代解（77 頁耗時考量）**：
   逐頁叫用 `drawio` 需重開 77 次 Electron，在容器內可能長達 3~5 分鐘。若追求速度，可使用「單次匯出全頁 PDF，再以 `pdftoppm` 切圖」的雙重步驟：
   ```bash
   # 1. 跑一次 Electron 產出 77 頁裁切好的向量 PDF
   xvfb-run -a /opt/drawio/drawio -x -f pdf -a --crop -o /tmp/all.pdf architecture.drawio --no-sandbox
   # 2. 用 poppler-utils pdftoppm 秒級轉為高品質 PNG（耗時僅 1~2 秒）
   pdftoppm -png -r 150 /tmp/all.pdf /data/doc/assets/page
   ```
   *(出處：[jgraph/drawio-desktop issue #137 - CLI: Export all pages](https://github.com/jgraph/drawio-desktop/issues/137)，資料年份：2023–2024)*

---

### C. 輸出格式怎麼選？

#### 1. PNG vs SVG vs PDF 在 GitHub Markdown 的顯示狀況
- **PDF**：
  - **不可行**。GitHub Markdown 的 `![]()` 語法**無法內嵌渲染 PDF**，在網頁上只會變成一個下載連結。
- **SVG**：
  - **高風險，常破版**。GitHub 雖然允許 `![alt](diagram.svg)`，但有嚴格限制：
    1. **GitHub Camo 與 HTML Sanitizer**：會過濾所有 `<script>`、inline 事件與外部字型載入（如 Google Fonts 的 `@import`）。
    2. **`<foreignObject>` 不相容**：Draw.io 的文字框若勾選「Formatted Text」或「Word Wrap」，輸出 SVG 會使用 `<foreignObject>`。大部分瀏覽器（包含 Safari 與部分 Chrome 版本）在 `<img>` 標籤載入含有 `<foreignObject>` 的 SVG 時會**直接隱藏文字**或發出警告。
    3. **字型脫落**：SVG 文字屬於客戶端渲染，若檢視者的本機沒安裝該字型，會自動 fallback 到系統預設字型（如 Times New Roman），造成文字長度失真爆出方框外。
- **PNG**：
  - **最優解**。GitHub 100% 完美支援；字型在容器匯出階段就已經點陣化（Rasterized），所有瀏覽者看到的文字位置完全一致。
  - **清晰度補償**：為了防止高解析度（Retina）螢幕模糊，匯出時應加上 `-s 2`（2x 縮放比例）。
  *(出處：[drawio FAQ: SVG with HTML labels issues](https://www.drawio.com/doc/faq/export-to-svg)，資料年份：2023–2024)*

#### 2. 可編輯 PNG / SVG（Embed Diagram XML）是什麼？怎麼產？代價為何？
- **原理**：Draw.io 能將原始繪圖 XML 隱寫進圖片中：
  - PNG：塞在 PNG 的 `tEXt` 或 `zTXt` chunk（鍵值為 `mxfile`）。
  - SVG：塞在 `<svg>` 根標籤的 `content` 屬性或開頭註解中。
- **指令旗標**：`drawio -x -e`（`--embed-diagram`）。
- **好處**：使用者將 PNG / SVG 檔案直接拖入 Draw.io 網頁或桌面版，就能「原地編輯」該圖。
- **代價（針對你的場景強烈建議「關閉」）**：
  1. **檔案大小虛胖**：77 頁若每張圖都塞一份 XML，會把全檔案圖層重複複製 77 次。
  2. **破壞 Git Diff 與快取**：如果只改了第 1 頁，77 張圖片的 `tEXt` chunk 卻因為包含最新 XML 全體變更，導致 77 張圖全部產生 binary diff。
  *(出處：[drawio documentation: Editable SVG & PNG](https://www.drawio.com/doc/faq/embed-diagram-file)，資料年份：2023–2024)*

#### 3. 大圖在 Markdown 裡的可讀性處理
- **寬度限制**：GitHub Markdown 閱讀欄位最大寬度約 `1012px`，大架構圖會被 CSS `max-width: 100%` 自動壓扁，導致文字難以辨識。
- **實務標準寫法（可點擊放大）**：
  將圖檔包裹一層連結，點擊直接打開 raw 原始大圖：
  ```markdown
  [![系統架構圖](./assets/architecture-overview.png)](./assets/architecture-overview.png)
  ```
- **指定排版尺寸**：
  若匯出使用 `-s 2`（2 倍圖），可用 HTML 標籤限制其在網頁上的外觀尺寸，保有視網膜清晰度：
  ```markdown
  <img src="./assets/architecture-overview.png" width="800" alt="系統架構圖" />
  ```
- **切頁原則**：目前 77 頁已經是切頁狀態，切忌合成一張大圖，各文件應只引用相關的頁面圖檔。

---

### D. Determinism（確定性與驗證圖未變）

#### 1. 同一份 .drawio 重複匯出，位元組會相同嗎？
- **PDF**：**永遠不同**。PDF 規格會在檔案標頭與尾部寫入當下的時間戳記（`/CreationDate`, `/ModDate`）以及隨機生成的 `/ID [<hash> <hash>]`。
- **SVG**：在相同軟體版本下大致相同，但若包含動態生成的 `clipPath` ID 或 Draw.io 內部版本戳記，可能偶爾產生 ID 序號擾動。
- **PNG**：
  - **跨主機 / 跨系統**：通常**不同**。不同 OS 的 Chromium版本、FreeType / Fontconfig 抗鋸齒細微運算差異、libpng / zlib 壓縮演算法版本差異，都會導致位元組或邊緣像素哈希不同。
  - **在固定 Docker 容器內**：若**未**開啟 `-e`（不嵌 XML）且在完全相同的 Docker Image Digest 下重跑，PNG 具備高確定性（Pixel Hash 與 Byte Hash 一致）。

#### 2. 如何使匯出可重現？或退而求其次：怎麼驗證「圖沒變」？
- **實務方案：不要比對圖檔 binary，改比對「各頁 XML 語意簽章」**。
  77 頁的 `.drawio` 是單一文字檔，如果某次 PR 只修改了文字文件，根本不需要浪費 CI 時間重跑 77 頁匯出。
  - 步驟：
    1. 解析 `.drawio`，取出每個 `<diagram>` 節點的內容。
    2. 計算每個 Page 的 SHA256 哈希值，存入快取索引（例如 `.drawio-manifest.json`）：
       ```json
       {
         "架構總覽": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
         "認證流程": "cca17730e25287f3b5ddf79ff0513e9a4f48ff114d29e79435b62b189ff700d1"
       }
       ```
    3. 匯出腳本比對 XML 哈希值：**只對哈希有變動的頁面發動 `drawio` 匯出**。若無變動則跳過，確保未修改的圖片位元組維持不動，避免無效的 Git commit。
  *(出處：[Reproducible Builds: PNG Normalization & Timestamps](https://reproducible-builds.org/docs/deterministic-build-systems/)、[diagrams.net uncompressed XML format](https://www.drawio.com/doc/faq/uncompressed-xml)，資料年份：2023–2024)*

---

### E. 嵌進 Markdown 的實務

#### 1. 圖檔存放與相對路徑（GitHub 與 VS Code 雙向相容）
- **目錄建議**：
  ```text
  repo-root/
  ├── doc/
  │   ├── adr/
  │   │   └── 0001-architecture.md
  │   └── assets/
  │       └── diagrams/
  │           └── architecture.drawio      # 唯一真本
  │           └── arch-overview.png        # 匯出圖檔
  ```
- **相對路徑寫法**：
  在 `doc/adr/0001-architecture.md` 中：
  ```markdown
  ![架構總覽](../assets/diagrams/arch-overview.png)
  ```
  - **相容性保證**：標準相對路徑（`../` 或 `./`）能同時在 GitHub 網頁版、VS Code 內建 Markdown 預覽、本機靜態預覽中正確解析。**切勿**使用 `/doc/...`（以 repo 根目錄為基準的根路徑），因為本機 VS Code 預覽會無法定位根目錄而破圖。

#### 2. 自動更新 Markdown 裡引用的工具？
- **現狀**：有如 `mkdocs-drawio-exporter`（在 MkDocs 建置時解析 `![Page](file.drawio#0)` 並替換），但這是給靜態網站產生器用的。
- **針對 GitHub 網頁原生瀏覽**：
  **沒有安全的「自動改寫 Markdown 內文」開源工具**。業界做法是**維持穩定命名的檔案合約（Naming Contract）**：
  依頁名命名（如 `doc/assets/diagrams/arch-<page_name>.png`），工程師在 Markdown 中手動寫好相對應的檔名一次；後續只要 Draw.io 修改該頁，自動建置只會覆寫該 PNG，Markdown 內容完全不用改動。

#### 3. 圖檔要不要進 Git？
- **業界取捨分析**：
  - **不進 Git**：Git repo 體積小、無 binary diff。但代價是 **GitHub 網頁檢視必定破圖**（直接違反你的限制 4），除非所有人都透過另外架設的 GitHub Pages 讀文件。
  - **進 Git（強烈推薦）**：
    1. **符合唯一訴求**：直接在 GitHub PR、檔案瀏覽器看到架構圖。
    2. **GitHub 原生支援「圖片 Rich Diff」**：在 PR 審查時，GitHub 提供 2-up、Swipe（滑動比對）與 Onion Skin（洋蔥皮疊加）三種視覺比對模式，對架構變更審查非常友善。
    3. **體積控制方式**：77 張 PNG 不使用 `-e`，並在匯出後透過 `oxipng` 壓縮，全部加起來通常在數 MB 內，對現代 Git 效能負擔極小。
  *(出處：[GitHub Docs: Rendering and diffing images](https://docs.github.com/en/repositories/working-with-files/using-files/rendering-and-diffing-images)，資料年份：2023–2024)*

---

### F. CI 流程與防漏防呆完整實作

滿足你的限制 3（主機僅有 Docker、Git、just 與 POSIX 工具）：

#### 1. `justfile` 設定（本機與 CI 共用同一條指令）
在專案根目錄的 `justfile` 定義：

```just
# 匯出所有 drawio 頁面為獨立 PNG（依頁名命名）
export-diagrams:
    docker run --rm \
      --shm-size=1g \
      -u $(id -u):$(id -g) \
      -v "$(justfile_directory()):/workspace" \
      -w /workspace \
      rlespinasse/drawio-desktop-headless:latest \
      bash -c '
        python3 -c "
        import xml.etree.ElementTree as ET, subprocess, re, os
        drawio_file = \"doc/assets/diagrams/architecture.drawio\"
        out_dir = \"doc/assets/diagrams/generated\"
        os.makedirs(out_dir, exist_ok=True)
        tree = ET.parse(drawio_file)
        for idx, diag in enumerate(tree.getroot().findall(\".//diagram\")):
            name = re.sub(r\"[^\w\-]\", \"_\", diag.get(\"name\", f\"page_{idx}\"))
            out_file = f\"{out_dir}/{name}.png\"
            print(f\"Exporting page {idx} ({diag.get(\"name\")}) -> {out_file}\")
            subprocess.run([
                \"xvfb-run\", \"-a\", \"/opt/drawio/drawio\",
                \"-x\", \"-f\", \"png\",
                \"-s\", \"2\",
                \"-p\", str(idx),
                \"-o\", out_file,
                drawio_file,
                \"--no-sandbox\", \"--disable-gpu\", \"--disable-dev-shm-usage\"
            ], check=True)
        "
      '
```

---

#### 2. GitHub Actions 工作流程（`.github/workflows/verify-diagrams.yml`）
用於擋下「工程師修改了 `.drawio` 卻忘記在本地重新匯出」的情況：

```yaml
name: Verify Architecture Diagrams

on:
  pull_request:
    paths:
      - 'doc/assets/diagrams/**'
      - '.github/workflows/verify-diagrams.yml'
      - 'justfile'

jobs:
  check-diagrams-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install just
        uses: extractions/setup-just@v2

      - name: Re-export diagrams
        run: just export-diagrams

      - name: Check for uncommitted diagram changes
        run: |
          if [ -n "$(git status --porcelain doc/assets/diagrams/generated)" ]; then
            echo "::error::偵測到架構圖已過期！請在本地執行 'just export-diagrams' 並 commit 變更後再推上來。"
            git status --short doc/assets/diagrams/generated
            git diff doc/assets/diagrams/generated
            exit 1
          fi
          echo "架構圖同步檢查通過！"
```
*(出處：[GitHub Actions Documentation: Best Practices for Pre-commit / Generated Assets Validation](https://docs.github.com/en/actions)，資料年份：2023–2024)*

---

### 最終選型總結清單

1. **執行體系**：使用 `rlespinasse/drawio-desktop-headless` 容器跑 Python 腳本（免在主機裝任何 binary）。
2. **多頁與命名策略**：從 XML 提取明文 `<diagram name="...">` 屬性，用頁面名稱輸出成獨立檔案，徹底根絕頁序挪移造成的引用大錯位。
3. **格式規格**：採用 **PNG (`-s 2`)**，不勾選嵌入 XML（不加 `-e`），排除 GitHub SVG `<foreignObject>` 破圖風險。
4. **Git 管理**：圖檔正式納入 Git 版控，GitHub 網頁即時可讀並支援視覺化審查。
5. **防呆門禁**：本地與 CI 統一由 `just export-diagrams` 驅動，CI 靠 `git status --porcelain` 防守，保證圖本永遠一致。
