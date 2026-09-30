題目：把 .drawio 架構圖／流程圖自動匯出成圖檔，嵌進 markdown，整條流程可重複執行。

我的處境與硬性限制，回答必須符合：
1. 圖檔來源是單一一份多頁的 .drawio（目前 77 頁），存在 git repo 裡，是唯一真本。
2. 匯出要能在 CI 與本機用同一條指令跑，不能靠人手動開 GUI 點匯出。
3. 主機可用的東西只有 Docker、Git、just 以及 POSIX 基本指令。**不接受「請先在主機安裝第三方 binary」的方案**（包含 drawio desktop、node 全域套件、Python 第三方套件裝在主機上）。跑在容器內可以。
4. 輸出要嵌進 markdown，而且要在 GitHub 網頁上看得到。
5. 同一份輸入重複匯出，結果最好位元組相同（determinism），至少要能驗證內容沒變。

請回答下面每一個問題，各自附出處連結，並註明你查到的是哪一年的資料：

A. 匯出方式有哪些？各自的實際指令是什麼？
   - drawio desktop 的 CLI（`drawio -x` 之類）headless 要怎麼跑？需不要 xvfb？在容器裡 Electron 會遇到什麼問題（沙箱、`--no-sandbox`、`/dev/shm`）？
   - 有哪些現成的 Docker image 專門做 drawio 匯出（例如 rlespinasse/drawio-export、jgraph/drawio 這類）？各自維護狀況、最後更新時間、支援哪些輸出格式。
   - 有沒有不靠 Electron 的純程式庫路線（直接解 .drawio 的 mxGraph XML 自己畫）？實際可用嗎，還是只能處理簡單圖形。

B. 多頁怎麼處理？
   - 一份多頁 .drawio 匯出時，怎麼指定「第 N 頁」或「某個頁名」？
   - 輸出檔名能不能用頁名或頁 id，還是只能 index？頁序變動時檔名會不會跟著錯位？
   - 有沒有「一次匯出全部頁、每頁一檔」的做法。

C. 輸出格式怎麼選？
   - PNG、SVG、PDF 各自在 GitHub markdown 的顯示狀況（SVG 在 GitHub 上會不會被擋、字型會不會掉、外部字型怎麼處理）。
   - drawio 的「可編輯 PNG／可編輯 SVG」（把原始 XML 內嵌回圖檔）是什麼、怎麼產、有什麼好處與代價（檔案大小、diff）。
   - 大圖在 markdown 裡的可讀性處理：縮放、`<img width>`、是否該切頁。

D. determinism
   - 同一份 .drawio 重複匯出，PNG／SVG／PDF 會不會位元組相同？哪些因素會讓它不同（時間戳、字型、版本、亂數 id）？
   - 有沒有已知的做法讓匯出可重現，或退而求其次：怎麼驗證「圖沒變」（比對 XML 而不是比對圖檔？）

E. 嵌進 markdown 的實務
   - 圖檔放哪、相對路徑怎麼寫、GitHub 與本機編輯器（VS Code）都要能顯示。
   - 有沒有工具能「從 .drawio 產生圖檔並自動更新 markdown 裡的引用」。
   - 圖檔要不要進 git？進 git 的話 diff 會很吵，不進 git 的話 GitHub 上看不到 —— 業界常見做法是什麼，各自的取捨。

F. 有沒有人做過完整的 CI 流程可以參考？
   - 實際的 GitHub Actions 設定範例（產圖 → 檢查有沒有忘記重產 → commit 或當成 artifact）。
   - 「忘記重新匯出」怎麼擋（例如 CI 重產一次再比對，不一致就紅燈）。

不要給我概念性的建議，要具體到指令、image 名稱、旗標、檔案路徑。找不到的就說找不到，不要推測。
