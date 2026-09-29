## 必改

- `agy_drawio_export.md:1、229–242、309–315` — 把「主機只有 Docker／Git／just」錯套到作者畫圖流程，並以容器作最終選型；這與已定案前提衝突，整套 Docker 實作與結論都應移除，不作後續方案依據。

- `agy_drawio_export.md:28` — 引用錯誤：它寫 `drawio-desktop issue #137`，但 #137 不是所述的 headless/Xvfb 依據；真正直接記錄無 display 會失敗、用 `xvfb-run` 可成功的是 [issue #146](https://github.com/jgraph/drawio-desktop/issues/146)。建議更正來源。

- `agy_drawio_export.md:10–11` — 「Linux 一律需要 Xvfb」說得過廣；準確說法是：在沒有可用 X11 display 的 Linux 環境，drawio-desktop 的 Electron GUI 程序需要 X server，Xvfb 是常用解法。本機桌面已有 display 時不需要另開 Xvfb。[上游 issue #146](https://github.com/jgraph/drawio-desktop/issues/146) 與 [headless image 說明](https://github.com/rlespinasse/docker-drawio-desktop-headless)支持這個限縮後的說法。

- `agy_drawio_export.md:13–16` — 「容器內必須加 `--no-sandbox`、`--shm-size=1g/2g`、`--disable-gpu`」站不住。上游 headless image 的 runner 確實固定加 `--no-sandbox --disable-gpu`，但沒有證據支持所有 Docker 環境都「必須」如此；`/dev/shm` 64 MB 必然讓 77 頁檔崩潰也沒有實測或 drawio 上游依據。建議改成「特定封裝採用的相容性設定」，不要寫成 drawio CLI 的普遍要求。

- `agy_drawio_export.md:17–27` — 範例中的 `-p 0` 已不符合目前 CLI。drawio-desktop 自 v27.0.2 起 `--page-index` 改為 **1-based**，`0` 會明確報錯；目前上游 `args.js` 也把輸入減一後使用。[官方 CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)。建議鎖定版本並按該版 help 寫指令；以目前版應用 `-p 1` 代表第一頁。

- `agy_drawio_export.md:32–40` — 「社群與官方主要 image」表混淆用途：
  - `rlespinasse/drawio-export`、`rlespinasse/drawio-desktop-headless` 是活躍的社群 image，名稱正確。
  - `jgraph/drawio` 名稱正確且仍維護，但它是官方 Web app image；說它不是 desktop CLI image是對的。不過官方同 repo 另有 `jgraph/export-server`，所以「不支援 CLI 匯出」不應延伸成「官方容器完全沒有匯出能力」。[官方 docker-drawio](https://github.com/jgraph/docker-drawio)
  - `accetto/ubuntu-vnc-xfce-drawio-g3` 存在且近期仍有 image，但現況大小約 378 MB，不是文中聲稱的「超過 2 GB」。[Docker Hub](https://hub.docker.com/r/accetto/ubuntu-vnc-xfce-drawio-g3/)

- `agy_drawio_export.md:35–38` — 版本資料過時／錯配。查證時 `rlespinasse/drawio-export` 最新 release 是 `v4.60.0`，內含 `drawio-exporter 1.6.0`；headless image 是另一條 `v1.x` release 線，目前為 `v1.72.0`，不是「隨上者同步維護」。建議分別記錄 wrapper、exporter、desktop 三個版本，不能只寫模糊的 `v4.x/latest`。

- `agy_drawio_export.md:42–53` — `rlespinasse/drawio-export` 範例的 `--format`、`--folder` 介面未由它引用的 README 證實；目前上游 README 只保證直接掛載 `/data` 後執行 exporter，沒有這段命令。建議以實際固定版本的 `--help` 為準，不要替未驗證旗標背書。[上游 README](https://github.com/rlespinasse/drawio-export)

- `agy_drawio_export.md:58–64` — 「純程式庫路線實際不可用」「只能處理簡單幾何」「甚至直接崩潰」是沒有具體專案版本、測試案例或直接一手來源支撐的總括判斷。建議標成「查不到依據」，不要當成已證明的技術結論。

- `agy_drawio_export.md:70–74` — 「`--page-index` 是 0-based」現在是錯的；目前為 1-based。原生 CLI 目前確實沒有 `--page-name` 或 `--page-id`，這一半可保留。[官方 CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)

- `agy_drawio_export.md:76–78` — 「頁序變動會使檔名內容錯位」不是 drawio 的特殊 bug，而是採用 index 作穩定檔名時必然發生的映射問題。建議改成條件句：「若外部檔名以頁序為鍵，插頁或重排便會使後續名稱與內容重新映射」。

- `agy_drawio_export.md:87` — `id`、`name`「永遠是明文」用詞過度。一般 `.drawio` 的 `<diagram>` 外層屬性確實是明文，即使頁面 payload 壓縮亦然；但「永遠」未有格式規格保證。建議寫成目前格式與本 repo 檔案可觀察到的性質。

- `agy_drawio_export.md:88–103` — Python 範例有三個實質問題：
  - `-p str(idx)` 從 0 開始，與目前 1-based CLI 不符。
  - 只以清理後頁名命名，重名或清理後碰撞會覆寫檔案，不能「徹底根絕」錯位。
  - 頁名可修改，並非穩定識別；本 repo 既有工具已以 page ID 作檔名。
  
  建議以 page ID 作輸出鍵，頁名只作展示 metadata。

- `agy_drawio_export.md:106–117` — `-a/--all-pages` 目前只對 PDF 與 HTML 生效，這點正確；但「77 次需 3–5 分鐘」「`pdftoppm` 只需 1–2 秒」沒有硬體、版本、圖檔與量測資料，屬查不到依據。PDF 再點陣化亦可能改變裁切、透明背景、字型與解析度，不能直接稱為等價替代。

- `agy_drawio_export.md:127–134` — SVG 風險被誇大：
  - draw.io 官方只說某些 viewer 不支援 `foreignObject`；官方文件明載 Edge 支援，沒有支持「大部分瀏覽器、部分 Chrome 會直接隱藏文字」。
  - 目前 CLI 的 `--embed-svg-fonts` 預設為 true，不能一概說 SVG 必然依賴檢視者本機字型。
  - 「PNG 是最優解」「GitHub 100% 完美支援」是選型判斷，不是可查證事實。
  
  建議只保留具體相容性條件。[draw.io SVG 文件](https://www.drawio.com/docs/manual/export/embed-svg/)與[官方 CLI 旗標](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)。

- `agy_drawio_export.md:137–144` — 可編輯圖片的機制描述部分錯誤：
  - PNG 官方明確記載 XML 放在 `zTXt` section；文件沒有支持「`tEXt` 或 `zTXt`，鍵值必為 `mxfile`」這個完整說法。
  - SVG 官方支持 XML 位於根元素 `content` attribute；「或開頭註解」查不到依據。
  - `-e/--embed-diagram` 存在，適用 PNG、SVG、PDF。
  
  建議依官方已證實形式改寫。[PNG embedded XML](https://www.drawio.com/docs/manual/export/xml-in-png/)、[SVG embed](https://www.drawio.com/docs/manual/export/embed-svg/)。

- `agy_drawio_export.md:141` — 「拖入後原地編輯」不精確；官方說法是能重新匯入並繼續編輯，不代表修改後會自動覆寫原圖片。建議改成「可由 draw.io 重新開啟／匯入為可編輯圖」。

- `agy_drawio_export.md:143–144` — 「每張單頁圖必然嵌入整份 77 頁 XML，因此改一頁會令 77 張全變」沒有由所引文件證實；GUI 還提供只嵌 current page 或 all pages 的選項。這項代價取決於實際 export path 和 `All Pages` 設定，應以選定 CLI 版本做實檔檢查後再下結論。[官方 PNG 文件](https://www.drawio.com/docs/manual/export/xml-in-png/)

- `agy_drawio_export.md:165–170` — determinism 段過度斷言：
  - PDF 規格不要求每份 PDF 必須含當下時間與隨機 ID，因此「永遠不同」是錯的。
  - SVG 的 `clipPath` ID 偶爾擾動、固定 image digest 下 PNG byte hash 必然一致，都沒有 drawio 實測或上游保證。
  
  建議全部改成待針對固定 drawio 版本、字型與輸入做重複匯出測試的假設。

- `agy_drawio_export.md:172–185` — 所謂「XML 語意簽章」實際只是對 `<diagram>` 序列化內容做 SHA-256：
  - 未做 canonicalization，不是語意等價比較；XML 屬性順序、壓縮形式或無渲染影響的 metadata 都可能改 hash。
  - 它只能判斷來源頁 payload 是否變動，不能驗證 PNG 是否由該 XML、指定 exporter 與字型正確產生。
  - 以頁名作 manifest key 還有改名與碰撞問題。
  
  建議稱為「每頁來源內容雜湊／增量匯出鍵」，key 用 page ID；若目標是防止圖檔過期，manifest 還必須納入 exporter 版本、參數、字型環境及產物關聯。

- `agy_drawio_export.md:210–214` — 「沒有安全的自動改寫 Markdown 開源工具」「業界做法是……」無法由提供來源證實，應列為查不到依據；而依頁名命名也不是穩定合約，改名與碰撞仍會破壞引用。建議使用 page ID 或顯式 mapping。

- `agy_drawio_export.md:222` — 「77 張通常只有數 MB、對 Git 負擔極小」沒有針對本檔實測，查不到依據；`oxipng` 也不是背景列出的既有工具鏈。建議先以實際 77 頁輸出量測。

- `agy_drawio_export.md:231–265` — `justfile` 範例不能執行：
  - 第 253 行 `f"...{diag.get("name")}..."` 引號造成 Python `SyntaxError`。
  - `-p str(idx)` 使用錯誤的 0-based index。
  - 現行 headless image 對非 root 執行還要求可寫的 `HOME`，並說明自 desktop v24.4.6 起需 `/etc/passwd` 對應；範例只有 `-u`，缺少兩者。[headless image 說明](https://github.com/rlespinasse/docker-drawio-desktop-headless)
  - image 本身已提供 X server wrapper，容器內再直接寫 `xvfb-run /opt/drawio/drawio` 不是其文件化介面。
  
  建議整段刪除；即使只當歷史範例也不能稱為可執行實作。

- `agy_drawio_export.md:269–305` — CI 宣稱「保證圖本永遠一致」過頭。workflow 的 `paths` 未涵蓋 exporter 腳本、字型或依賴版本；若輸出目錄存在未追蹤的新檔，`git diff` 也不顯示其內容。建議僅稱為「在指定觸發條件下檢查工作樹是否變髒」。

## 建議

- `agy_drawio_export.md:7–11` — `drawio -x` 確實是官方 desktop CLI export 模式；Linux 無 display 時需 X server 也站得住。但 `--headless=new` 不是 drawio 文件化旗標這件事，應直接寫成「drawio 沒有文件化的純無視窗 renderer」，不要混用 Chromium headless 旗標概念。[官方 CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)

- `agy_drawio_export.md:37` — `rlespinasse/drawio-export` 確實支援遞迴與 partial export，且格式表列 `jpg/pdf/png/svg/xml/adoc/md`；但「社群首選推薦」無客觀依據。建議刪掉排名語氣。[上游 README](https://github.com/rlespinasse/drawio-export)

- `agy_drawio_export.md:76–104` — 從 `<diagram id name>` 建立 `(index, id, name)` mapping 是可行方向，而且符合既有 Python 工具鏈；建議後續只把 index 當呼叫 CLI 的瞬時參數，持久檔名與 manifest 以 page ID 為準。

- `agy_drawio_export.md:123–125` — GitHub Markdown 不會把 PDF 當 inline image 顯示的方向合理，但「只會變成下載連結」取決於實際 Markdown 寫法；建議改成「PDF 不能透過 image syntax 作一般 inline image」。

- `agy_drawio_export.md:147–159` — 可點擊原圖與 `<img width>` 的 Markdown 寫法合理；`1012px` 是 GitHub UI 實作細節，查不到穩定契約，建議刪除精確數字。

- `agy_drawio_export.md:191–208` — 相對路徑是合適做法；「保證 GitHub 與 VS Code 雙向相容」仍應降為一般相容做法，不宜承諾所有 preview 設定。

- `agy_drawio_export.md:216–223` — 圖片納入 Git 後可在 GitHub 顯示及使用圖片 diff，這點站得住；是否納入 Git 是 repo policy，不應再以舊限制推導為唯一選擇。[GitHub 圖片 diff 文件](https://docs.github.com/en/repositories/working-with-files/using-files/rendering-and-diffing-images)

## 沒問題

- `agy_drawio_export.md:5–8` — `drawio-desktop` 是 Electron 桌面應用，`-x/--export` 是正式 CLI 旗標。[官方專案](https://github.com/jgraph/drawio-desktop)與[CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)

- `agy_drawio_export.md:32–40` — 三個 image 名稱 `rlespinasse/drawio-export`、`rlespinasse/drawio-desktop-headless`、`jgraph/drawio` 都真實存在且仍有維護活動；`accetto/ubuntu-vnc-xfce-drawio-g3` 也存在。

- `agy_drawio_export.md:39` — `jgraph/drawio` 是 Tomcat Web app，不是 drawio-desktop CLI 封裝，判斷正確。[官方 image README](https://github.com/jgraph/docker-drawio)

- `agy_drawio_export.md:71–74` — 原生 CLI 沒有 `--page-name`、`--page-id` 旗標，判斷正確；只有 `--page-index` 與 PDF 的 `--page-range`。注意 index 基準必須按前述改為目前的 1-based。

- `agy_drawio_export.md:80–86` — `.drawio` 多頁檔由 `<mxfile>` 下多個 `<diagram id="…" name="…">` 表示，站得住，也與本 repo 的 `discussion.drawio` 及 `extract_pages.py` 實際結構一致。

- `agy_drawio_export.md:106–108` — 原生 `-a/--all-pages` 目前只適用 PDF 與 HTML，不適用 PNG／SVG，站得住。[官方 CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)

- `agy_drawio_export.md:133、140` — `-s/--scale` 與 `-e/--embed-diagram` 旗標真實存在；`-e` 明列支援 PNG、SVG、PDF。[官方 CLI 原始碼](https://github.com/jgraph/drawio-desktop/blob/dev/src/main/args.js)

- `agy_drawio_export.md:136–141` — 「可編輯 PNG／SVG」的核心概念正確：圖片除了渲染結果，還攜帶可重新匯入 draw.io 的 diagram XML。代價是檔案較大、metadata 可能被圖片處理平台剝除；PNG 仍是 raster，放大會模糊，SVG 則保留向量顯示。[PNG embedded XML](https://www.drawio.com/docs/manual/export/xml-in-png/)、[官方格式比較](https://www.drawio.com/docs/manual/export/export-diagram/)

- `agy_drawio_export.md:138` — PNG 使用 `zTXt` 儲存 XML 有官方明文依據。[官方 PNG 文件](https://www.drawio.com/docs/manual/export/xml-in-png/)

- `agy_drawio_export.md:139` — SVG 的 diagram XML 位於根元素 `content` attribute 有官方明文依據；僅「或開頭註解」那一半應刪除。[官方 SVG 文件](https://www.drawio.com/docs/manual/export/embed-svg/)

- `agy_drawio_export.md:169` — 跨 OS、Chromium、字型與 rasterizer 版本可能產生不同像素／位元組，是合理且技術上成立的風險描述；只是不能反推固定 image digest 就必然 byte-identical。

- `agy_drawio_export.md:173–184` — 以每頁 XML payload hash 做增量匯出，在正確命名為「內容雜湊」且使用 page ID 後，是可行的快取策略；它不等於產物同步驗證或 XML 語意比較。

工作樹未修改。