# drawio 使用規則

用 drawio MCP 讀圖、改圖、匯出時要守的規則。設計與定案記在 #138。

## 現在用的頁面

- 網址記在 workspace 的 `reference/drawio_session.txt`（workspace 根目錄底下，不在 repo 裡），只有一行，格式是 `http://localhost:<port>/?mcp=<session id>`。
- 腳本與 workflow 一律從這個檔讀 port 和 session id，不寫死在任何地方。

## 規則

1. **頁面由主對話持有**：每個 Claude session 只在開始時由主對話呼叫一次 `start_session`，開一個頁面，再把網址寫進 `drawio_session.txt`。workflow 和子代理一律不呼叫 `start_session`。
2. **重複用同一頁**：之後讀圖、改圖、匯出都用這一頁。
3. **頁面不見了**：
   - 分頁被關掉：打開 `http://localhost:<port>/`，會自動接回最近的 session，不用重開。
   - 重新整理後變空白：表示原本的 server 已經不在。檔案沒事，用下面的 HTTP 方式重新載入就好。
4. **session 失效的判斷**：連不上 port，或回應是 `version == 1` 加上預設空白頁（`<diagram id="blank" name="Page-1">`）。這時腳本要報錯停下，不自動開新頁。

## 為什麼要這樣做

- drawio MCP 每呼叫一次 `start_session`，就會開一個新的瀏覽器分頁，而且關不掉。
- 所有 MCP 工具只作用在「這個 Claude session 的 MCP 程序目前綁定的 session」，沒有參數可以切換到別的 session。
- MCP 自己不會渲染，PNG 是瀏覽器分頁裡的 draw.io 畫出來的，所以至少要有一頁開著。

## MCP 套件固定版本

- 套件是 `@next-ai-drawio/mcp-server`，實測版本 0.2.3。
- 要固定版本，不用 `@latest`，以免內部協定改變。

## 讀寫圖：HTTP（腳本可用）

- 讀：`GET http://127.0.0.1:<port>/api/state?sessionId=<id>`，回傳 `{xml, version, ...}`。
- 寫或載入：`POST http://127.0.0.1:<port>/api/state`，JSON body 是 `{"sessionId": "<id>", "xml": "<mxfile…>"}`，回傳 `{success, version}`。分頁會自動抓到新內容並重新載入，實測約 72 秒內出現。

## 匯出 PNG：只能用 MCP 工具

- 匯出沒有 HTTP 端點，只能用 MCP 工具 `export_diagram(path, format, page_id)`，而且要在持有這一頁的同一個 Claude session 裡呼叫。
- 匯出的 PNG 是透明底，要再用腳本改成白底、縮圖。

## 圖檔位置

- 圖分兩個檔（#278）：
  - `doc/diagram/architecture.drawio`：架構圖，畫模組邊界與呼叫關係。
  - `doc/diagram/flow.drawio`：流程圖，畫步驟與分支，資料流、時序也放這裡。
- 頁 id 依檔案加前綴：架構圖用 `arch-`，流程圖用 `flow-`，例如 `arch-components`、`flow-fetch`。
- 頁 id 是頁的持久鍵，定下後不改；頁名與頁序可以改。`c-` 是早期提案用的前綴，已廢，不再使用。
- 新頁照內容放：畫模組怎麼切、誰呼叫誰，放 `architecture.drawio`；畫一件事的步驟、分支、資料怎麼流或先後順序，放 `flow.drawio`。
- 舊模型的其他圖與它們的產生器不進 git（#35），副本在 workspace 的 `reference/diagram_legacy/`。
- 新的圖由 `diagram-edit` workflow 處理（#138）。
