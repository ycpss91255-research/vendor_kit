# 審圖任務（請用繁體中文回覆）

你是第二位審查者。請審查一份 draw.io 圖檔是否達到下列要求，並列出具體問題。你只需要審，不要改檔案。

## 背景

- 我們有一個 bash 工具集 `base`（ycpss91255-docker/base），提供 Docker 開發環境的 wrapper（build/run/exec/stop）、Dockerfile 模板、compose 產生器等。
- 目前 base 是用 `git subtree` + symlink 複製整棵樹到 15 個下游專案，造成版本漂移、複製過量、升級腳本「自己升級自己」失敗等問題。
- 決策：改用 **GHCR image 分發**。`vendor_kit` 是一個新的、通用的「安裝工具」，本身打包成 image；base（和其他工具）的發佈 image 以 vendor_kit image 為基底，再疊上自己的 dist、模板、檔案清單（manifest）。
- 下游專案只保留：一個極薄的 `justfile`（啟動器）、一行 `.base-ref`（要用的版本）、以及第一次安裝時建立的使用者檔案（Dockerfile、.setup.conf 等）。執行 `just` 時，啟動器起一個 container 跑 vendor_kit，把工具檔案寫進 `.base/`（不進 git）並寫「印記檔」（版本 + 每檔 hash）。
- 檔案分三類：工具擁有（每次覆蓋）、第一次建立（之後屬使用者）、可選（需要才建）。
- 完整決策紀錄在 `dist_distribution_notes.md`（同目錄）。

## 使用者對圖的明確要求（這是驗收標準）

1. **架構圖 ≠ 流程圖**。架構圖只畫「模組 → 子模組 → 最小單元」以及「模組之間傳輸的資料」（線上文字必須是資料，不是動作／步驟）。流程圖是架構圖底下各模組各自的流程，另外分頁畫。
2. 第 1 頁必須是 **vendor_kit 本身的架構圖**（它內部有哪些模組、最小單元、模組間的資料），不是「vendor_kit 怎麼出貨」。出貨關係另放第 2 頁。
3. **顏色要有明確、一致的意義**，不能隨便用。圖例（每頁底部）定義：容器標題色 = 模組狀態（紅新建／綠現有／黃外部系統）；葉節點色 = 單元性質（白新建／灰現有／紫 image 或 container）；流程頁的分組容器用淺灰（無狀態意義）。
4. **字要少**，一般人（非工程師）也看得懂；框內 ≤ 6 字、線上 ≤ 8 字為目標。專有名詞集中在第 6 頁「名詞說明」。
5. **線段要真的連到元件上**，不能有線穿過別的框、線與線交叉、文字被線壓到。
6. 格式對齊參考檔 `~/robot_architectures.drawio` 的慣例：swimlane 容器（標題列、白底、可摺疊）、子元件巢狀在容器內、葉節點 88×40、線 strokeWidth=2、標籤 10px。

## 檔案

- 圖檔：`/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution.drawio`（6 頁，未壓縮 XML，可直接讀）
- 每頁 PNG：本目錄 `p1.png`～`p5.png`（第 1 頁 vendor_kit 架構圖、第 2 頁出貨路徑、第 3 頁流程：啟動器、第 4 頁流程：版本生命週期、第 5 頁流程：安裝工具）
- 決策紀錄：`/home/cyc/Desktop/vendor-kit_ws/src/dist_distribution_notes.md`
- 格式參考：`/home/cyc/robot_architectures.drawio`

## 請回答

A. 逐頁判定：這一頁是「架構圖」還是「流程圖」？符不符合第 1、2 點？若第 1 頁仍像流程圖，指出是哪些線或哪些框造成的。
B. 顏色：有沒有任何顏色用得不符合圖例定義？列出元件 id 或名稱。
C. 文字：哪些框或線的文字過長、或一般人看不懂？給出建議的替代寫法。
D. 線段：從 XML 檢查每條 edge 的 source/target 是否都存在、exit/entry 是否合理；從 PNG 看有沒有穿框、交叉、壓字。逐條列出有問題的 edge id。
E. 內容正確性：圖上的模組／資料與 notes 的決策有無矛盾或遺漏（例如 notes 的第 3、4、5 節）。
F. 最後給一個總結：這份圖「可以交付」或「還不行」，以及還不行的前三個原因。

請直接輸出審查結果，不要複述背景。
