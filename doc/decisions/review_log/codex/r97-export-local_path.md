## 必改

- **位置：`doc/decisions/research/agy_drawio_export.md`「B.1 指定第 N 頁」** — 把「`--page-index` 是 0-based」改成 **1-based**；目前 draw.io Desktop CLI 的實際指令是：
  ```bash
  drawio -x -f png -p 1 -o out/v1p0.png discussion.drawio
  drawio -x -f svg -p 1 -o out/v1p0.svg discussion.drawio
  ```
  官方目前也把 `-p/--page-index` 定義為 1-based；`-a/--all-pages` 只適用 PDF/HTML，PNG/SVG 必須逐頁呼叫。[draw.io MCP 所附 CLI 文件](https://github.com/jgraph/drawio-mcp/blob/main/plugins/codex/drawio/skills/drawio/SKILL.md#drawio-cli)

- **位置：`doc/decisions/research/agy_drawio_export.md`「不用容器的路徑」** — 補上首選路徑「既有 Next AI Draw.io MCP＋瀏覽器」，因 repo 的 `127.0.0.1:6002/api/state` 可由 [push_r16.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/push_r16.py:4) 與 upstream 預設 port 6002 確認是 `@next-ai-drawio/mcp-server`，不是官方 `@drawio/mcp`。[Next AI MCP README](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/README.md#available-tools)

- **位置：[review_v2_README.md](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:15)「主對話要先跑的三個指令」** — 文件必須補上 `png_v2/*.png` 的產生步驟；目前第 21 行直接拿不存在的來源目錄餵給 `shrink_png.py`，流程本身不完整。

- **位置：[shrink_png.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/shrink_png.py:1)** — 不要把它描述成 draw.io 匯出器；它只用 Pillow 讀取既有 PNG、縮放、鋪白底並產生 `pngs.json`，沒有解析或渲染 draw.io。

## 建議

- **位置：作者的圖面匯出流程／`discussion.drawio`** — 首選目前已要掛載的 Next AI Draw.io MCP，主機需求是 Node/npm（通常以 `npx` 啟動）及保持開啟的瀏覽器，不需要 draw.io Desktop、容器或 Python renderer：
  ```text
  load_diagram({path:"/home/cyc/Desktop/vendor-kit_ws/src/discussion.drawio"})
  list_pages({})
  export_diagram({
    path:"/home/cyc/Desktop/vendor-kit_ws/src/doc/assets/discussion/v1p0.png",
    format:"png",
    page_id:"v1p0"
  })
  ```
  `export_diagram` 支援 `drawio`、`png`、`svg`，不支援 PDF；PNG/SVG 一次一頁，可用 `page_id`、`page_name` 或 0-based `page_index`，沒有 selector 時只匯出瀏覽器目前 active page，輸出名稱完全由 `path` 決定，因此 77 頁應由 agent 依 `list_pages` 結果逐頁呼叫並以 page id 命名。[工具實作](https://github.com/DayuanJiang/next-ai-draw-io/blob/main/packages/mcp-server/src/index.ts#L911-L1154)

- **位置：MCP 安裝設定** — 固定 `@next-ai-drawio/mcp-server` 至至少 `0.2.1`；PNG/SVG 是 0.1.16 才加入，多頁 selector 是 0.2.1 才加入，若使用未固定的舊版，不能假設上述多頁行為存在。

- **位置：MCP 匯出操作** — PNG/SVG 匯出時必須讓 session 與瀏覽器頁籤保持開啟；指定頁會暫時載入單頁 projection、匯出後還原，因此一次約有 1–2 秒頁籤閃動，但不受頁序變動影響。

- **位置：本機備援流程／`discussion.drawio`** — 若不走 MCP，安裝 draw.io Desktop 後可直接使用 CLI；一般 Linux 桌面 session 不需容器，無圖形 display 的主機才另需 X/Xvfb：
  ```bash
  mkdir -p out
  drawio -x -f png -p 1 -o out/v1p0.png discussion.drawio
  drawio -x -f svg -p 1 -o out/v1p0.svg discussion.drawio
  drawio -x -f pdf -a -o out/discussion.pdf discussion.drawio
  ```
  PNG/SVG 沒有一次全頁選項，應先由 Python 建立 **1-based index → id** 對映，再逐頁執行：
  ```bash
  python3 - discussion.drawio out <<'PY'
  import os, subprocess, sys
  import xml.etree.ElementTree as ET

  source, output = sys.argv[1:]
  os.makedirs(output, exist_ok=True)
  for index, page in enumerate(ET.parse(source).getroot().findall("diagram"), 1):
      page_id = page.attrib["id"]
      subprocess.run([
          "drawio", "-x", "-f", "png", "-p", str(index),
          "-o", os.path.join(output, page_id + ".png"), source,
      ], check=True)
  PY
  ```

- **位置：瀏覽器版 draw.io／File → Export as** — 只裝瀏覽器也能手動輸出 PNG、JPEG、SVG、PDF 等格式，但對 77 頁沒有穩定、可重跑的批次命名流程，因此只適合作為臨時備援。[支援格式](https://www.drawio.com/docs/manual/export/export-diagram/)

- **位置：純 Python 路徑** — 不要把純 Python 當正式匯出方案；現有 [extract_pages.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:31) 只解析未壓縮 XML，而 [_misc/rough_render.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/_misc/rough_render.py:1) 明示只畫粗略方塊、線與部分文字，不能忠實還原 draw.io 排版。

- **位置：建議新增的 `doc/assets/discussion/`** — 建議以 `<diagram id>.png` 保存 77 張非嵌入 XML 的 PNG 並納入 Git，Markdown 使用相對路徑；代價是 binary diff 與 repo 體積增加，好處是 GitHub 和 VS Code Markdown 預覽都直接可見，且 GitHub能顯示並視覺比較 PNG。[GitHub 圖片支援](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files)

- **位置：Markdown 引用圖的位置** — 使用可點擊原圖的相對連結，例如：
  ```markdown
  [![install 流程](../assets/discussion/v1p5.png)](../assets/discussion/v1p5.png)
  ```
  相對路徑同時適用 GitHub 分支檢視與 VS Code；若圖片不進 Git，GitHub 上必然看不到，除非另外建立並維護外部發布服務。[GitHub 相對圖片路徑](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes#relative-links-and-image-paths-in-readme-files)

## 沒問題

- **位置：`discussion.drawio` 的 `<diagram>` 元素** — 現檔 77 頁都有非空且互不重複的穩定 id，例如第一頁 `v1p0`、最後數頁 `d0b`～`d4`；只要重畫時保留 id，就可把 id 當穩定檔名，不必依賴頁名或頁序。

- **位置：[extract_pages.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:31)** — 它以 `<diagram id="…" name="…">` 讀頁，篩選條件也是 page id，並輸出 `<id>.json`、`<id>.md` 及包含順序的 `pages.json`，不是用 index 認頁。

- **位置：[drawio_common.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/drawio_common.py:4)** — 共用解析器同樣回傳 page id、name 與 cells，既有 overflow/overlap 檢查不依賴頁序。

- **位置：[review_v2_README.md](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:51)「extract_pages.py 的判定規則」** — 「一頁等於一個 `<diagram id name>`」及後續產物以 id 對齊 PNG 的設計正確，可直接延續到新匯出流程。

- **位置：Git 歷史 `03d8745` 與 [finish_r15.py](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/finish_r15.py:4)** — 可確認舊路徑是先把頁面推入 port 6002 的 MCP session，再取得 `png_v2/<id>.png`，最後用 Pillow 清掉 stale 檔、鋪白底並產生 manifest；但 PNG 本身從未進 Git，commit 只說成果由 session scratchpad 搬入，因此 Git 歷史無法證明當時每張 PNG 的精確 MCP 呼叫。

- **位置：[script/diagram/README.md](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/README.md:5) 與 [review_v2_README.md](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/review_v2_README.md:18)** — 舊的「MCP/browser 產生 `png_v2` → `shrink_png.py` 產生 `review_v2_png`」路徑現在仍可用，而且新版 MCP 已能明確以 `page_id` 匯出；缺的是把這一步及最低 MCP 版本正式寫進文件。

全程只讀，未修改任何檔案。