題目：把 draw.io 畫的架構圖與流程圖放進 markdown 文件，在 GitHub 上看得到，而且圖跟來源不會脫鉤。

我的處境（回答要符合）：
1. 圖的真本是 repo 裡一份多頁的 `.drawio` 檔。每頁有穩定的 `<diagram id>`，頁名可能會改。
2. 我用 draw.io 的 MCP server（`@next-ai-drawio/mcp-server`）編輯圖。它的 `export_diagram` 能把**指定的一頁**匯出成 `.png`、`.svg` 或 `.drawio` 寫到指定路徑。
3. **不用容器**，也不打算在 CI 裡跑 draw.io 匯出。匯出在作者本機做。
4. 文件是 markdown，放在 GitHub repo 裡，要在 GitHub 網頁上直接看得到圖。

請回答下面每一題，**每一條都附出處連結**，並註明資料年份。查不到就說查不到，不要推測。

A. 格式選 PNG 還是 SVG？
   - GitHub 的 markdown 顯示 SVG 有沒有限制（例如會不會擋、字型會不會掉、`<foreignObject>` 能不能顯示）。draw.io 匯出的 SVG 預設有沒有用到 `<foreignObject>`？
   - 深色模式：GitHub 支援用 `<picture>` 加 `prefers-color-scheme` 放兩張圖嗎？實際寫法是什麼？還是有 `#gh-dark-mode-only` 這類寫法？哪一種是 GitHub 官方文件寫的？
   - 大圖在 markdown 裡怎麼控制寬度（`<img width>`）？

B. draw.io 的「可編輯 SVG」（`.drawio.svg`，圖檔裡內嵌原始 XML）
   - 這是什麼、GitHub 能不能直接顯示、VS Code 的 draw.io 擴充能不能直接編輯它。
   - 代價：檔案大小、多頁文件時每張圖是不是都內嵌整份 XML、git diff 變成什麼樣子。
   - 跟「一份 `.drawio` 真本 + 匯出的圖檔」比，哪個比較適合「一份多頁真本」的情況？

C. 圖檔怎麼命名、放哪
   - 業界常見的放法（跟 markdown 同目錄、集中一個 `images/` 或 `diagrams/`）與相對路徑寫法。
   - 用頁 id 還是頁名當檔名的取捨。

D. 怎麼擋「改了圖卻忘了重新匯出」
   - 不在 CI 跑 draw.io 的前提下，有什麼辦法檢查圖檔跟 `.drawio` 真本一致？例如 pre-commit hook、比對雜湊、在圖檔旁存來源頁的雜湊。有沒有現成工具或實際的 repo 這樣做？
   - 圖檔要不要進 git？進 git 的話 PR diff 怎麼看？

E. 有沒有真實的開源專案這樣做（draw.io 真本 + markdown 嵌圖），給 repo 連結，說明它的做法。

不要概念性建議，要具體到寫法、檔名、設定。
