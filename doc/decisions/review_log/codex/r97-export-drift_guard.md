## 必改

- [`script/diagram/lint_pages.py:491`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:491)：目前即使有 `warn` 仍固定以 0 結束，只產生 `lint.md/json`，必須改成「違規即非零退出、診斷送 stdout/stderr、報告檔可選」才能掛進 `just test`。

- [`script/diagram/lint_pages.py:40`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:40)：`FLOW_PAGE_RE`、`PAGE0_IDS`、`REVIEW_PAGE_IDS`、頁序及 v1/v2 命名全部綁定舊 77 頁模型；新圖不能直接沿用這套頁面分類。

- [`script/diagram/lint_pages.py:41`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:41)：`KEYWORDS`、`BASE_ALLOW`、事件名、指定訊息碼、流程深度、顏色、頁高、字級等規則都硬編碼舊模型，不應成為新契約 lint 的來源。

- [`script/diagram/lint_pages.py:232`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:232)：現有檢查共包含 `dangling`、`decision`、`endcolor`、`xref`、`term-diff`、`base`、`color`、`termcov`、`onething`，以及 `event-name`、`resolve-3way`、`precheck-recover`、`end-color-text`、`xref-forward`、`write-line`、`write-fail-edge`、`hidden-edge`、`term-count`、`term-dup-page0`、`page-height`、`edge-font`、`merge-fanout`；其中只有斷線、判斷分支、頁面引用、隱形邊等一般圖結構檢查可選擇保留，其餘是舊模型的內容或版式審稿規則。

- [`script/diagram/extract_pages.py:31`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:31)：抽取器用 regex 假設 `<diagram>` 內容是未壓縮 XML，draw.io 原始碼目前仍支援並預設使用壓縮內容，因此 MCP／桌面版重新存檔後可能抽出零節點卻不失敗；必須改成真正的 XML 解析及壓縮頁解碼，或明確拒絕壓縮格式。[draw.io 的壓縮設定與解碼實作](https://github.com/jgraph/drawio/blob/dev/src/main/webapp/js/diagramly/Editor.js#L273-L281)

- [`script/diagram/extract_pages.py:170`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:170)：目前會建立及寫入指定輸出目錄、沒有 schema 驗證、沒有檢查頁數為零，也不清除舊 JSON；應拆成可 import 的純抽取函式與薄 CLI，測試時使用暫存目錄並對解析失敗、重複頁 ID／名稱、空圖非零退出。

- [`CONTEXT.md:86`](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:86)：「圖上出現的 recipe 名要在 `CONTEXT.md` 有定義」可行但不能掃所有英文單字；只應辨識明確語法 `just vendor_kit <recipe>` 或標記為 recipe 的格，再和 `add/remove/update/upgrade/dev/undev/sync/prune/install/uninstall/help` 精確比對，否則一般文字中的 `update`、`install` 會大量誤報。

- [`CONTEXT.md:115`](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:115)：「不得出現 `_Avoid_` 詞」是四個候選中最便宜且最能擋術語漂移的檢查；應從所有 `_Avoid_:` 行機械抽取、只掃可見文字並採字詞邊界／最長詞優先，對 `.version`、`<name>` 等字面值精確比對，避免 `專案` 命中其他合法複合詞。

- [`doc/decisions/review/02_invariants.md`「4. 永不靜默失敗」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:135)：「訊息碼要有出處」可做，但來源必須是 `02_invariants.md` 加 `doc/adr/0001–0012` 的精確 `\b6-\d+[a-z]?\b` 聯集；它能攔截虛構／過期代碼，不能證明該代碼放在正確分支，且範圍寫法、範例及否定敘述應排除或另設顯式登錄標記。

- [`discussion.drawio` 頁籤名稱](/home/cyc/Desktop/vendor-kit_ws/src/discussion.drawio)：頁名對目標清單是低誤報且能防漏頁、重複頁及意外改名的強檢查，但目標清單必須是新流程明確維護的 manifest；不能從舊 77 頁或檔案當下頁名反推，否則只是自我比對。

- [`doc/decisions/research/agy_drawio_export.md`「D. Determinism」](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/research/agy_drawio_export.md:163)：不要用 raw XML byte hash 驗證「圖沒變」；存檔可能改 `<mxfile>` 的時間／agent 等 metadata、序列化順序、壓縮表示，編輯器也可能改 `mxGraphModel` 的 `dx/dy`、座標或連線點，造成與契約無關或僅細微排版的 diff。

- [`doc/decisions/research/agy_drawio_export.md:173`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/research/agy_drawio_export.md:173)：也不要以重匯 PNG 的 byte equality 當門禁；本機 Electron／Chromium、字型、抗鋸齒及編碼器差異會造成噪音，而且 PNG 相等只能證明渲染相等，不能供契約 lint 查文字與關係。

## 建議

- [`script/diagram/extract_pages.py:49`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:49)：最小方案是直接從解壓後的頁面模型抽取「頁 ID／名稱、可見文字、邊 source/target、形狀角色」，契約 lint 不需要座標、色碼、頁高、字級或 Markdown 摘要。

- [`script/diagram/lint_pages.py:253`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:253)：保留通用圖形健全性檢查時，建議只留 `dangling`、`decision`、`xref`、`hidden-edge`，並與契約一致性檢查分組；它們能擋壞圖，但本身不能防圖與契約脫鉤。

- [`script/diagram/lint_pages.py:444`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/lint_pages.py:444)：`term-diff` 可改成「圖中文字對 `CONTEXT.md` 正式詞與 Avoid 詞」的單向檢查；不要再維護圖內第 0 頁名詞表，否則形成第二個真本。

- [`CONTEXT.md:359`](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:359)：最小可行契約 lint 建議只設四個 fail 規則：頁 manifest 完全相等、明確 recipe 引用存在、精確訊息碼存在、Avoid 詞不得出現；不要在第一版加入流程語意推論。

- [`doc/decisions/review/02_invariants.md:152`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:152)：若日後要檢查泳道或步驟順序，應先在圖中加入穩定的機器標記（例如 `data-contract="invariant-4"` 或固定 cell metadata），再驗證必要節點／邊；靠中文句子模糊搜尋無法可靠證明時序。

- [`discussion.drawio` 根元素](/home/cyc/Desktop/vendor-kit_ws/src/discussion.drawio)：若需要頁級「語意簽章」，應解壓每頁後 canonicalize XML，排除文件 metadata 與純 viewport 屬性、排序屬性但保留文字、cell ID、parent、source/target、style、geometry；這適合判斷來源頁是否變動，不等於驗證 PNG 已正確匯出。

- [`doc/decisions/research/agy_drawio_export.md:172`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/research/agy_drawio_export.md:172)：若要驗證匯出圖未過期，建議讓 manifest 記錄每張圖所對應的 canonical page hash，lint 核對 source hash；只有需要檢查渲染回歸時才做固定環境的 pixel/perceptual diff。

- [`doc/adr/0011-test-layers-and-ci-matrix.md`](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0011-test-layers-and-ci-matrix.md:49)：兩支腳本應整理成單一無互動入口，例如 `python3 -m script.diagram.lint discussion.drawio --manifest …`，由它自行建暫存資料並以退出碼回報，`just test` 不應依賴預先生成的抽取目錄。

## 沒問題

- [`script/diagram/extract_pages.py:128`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:128)：現有做法已能從節點與邊文字抽出跨頁引用，概念上可直接支援頁名清單及引用存在性檢查。

- [`script/diagram/extract_pages.py:130`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:130)：保留 source、target、label 與 hidden 狀態足以做斷線、判斷分支及隱形邊檢查，不需要圖檔匯出器。

- [`CONTEXT.md:3`](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:3)：`CONTEXT.md` 已明確是專有名詞來源，recipe 與 `_Avoid_` 均可直接由現行真本抽取，不必另外建立詞彙登錄表。

- [`doc/decisions/review/02_invariants.md:174`](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:174)：圖面 lint 屬作者流程，不受「使用者主機只需 Docker／Git／just」限制，因此使用 repo 既有 Python 工具鏈掛進測試沒有契約衝突。

- [`script/diagram/extract_pages.py:2`](/home/cyc/Desktop/vendor-kit_ws/src/script/diagram/extract_pages.py:2)：抽取器只讀 `.drawio`、不回寫來源檔的方向正確；需要改的是解析可靠性與測試介面，不是引入容器或改變作者工作流。