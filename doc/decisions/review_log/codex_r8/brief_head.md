# 第八輪獨立審查 brief（codex）

你是獨立審查者。請依下列審查標準，對照附件「決策紀錄」（interface_spec.md）與附件 PNG（共 47 頁，依附加順序對應下列頁次）及 drawio XML，逐頁審查。

## 審查標準（使用者定的）
1. 架構圖只畫模組→最小單元與模組間傳的資料；流程圖另外分頁。
2. 顏色要有明確一致的意義，以各頁底部圖例為準；沒有的顏色不可出現。
3. 字要少，一般人（非工程師）也看得懂；專有名詞要在該頁底部「本頁名詞」表裡。
4. 線段：不穿無關方框、不交叉、不壓字、不裁切、不懸空、不該折的不折。
5. 線上文字 12pt。
6. 內容要跟 notes 的決策一致，且不可出現任何特定工具名（如 base）當實例，一律用 <repo>。
7. 每個方塊只放一件事（一個動作、一個判斷、一個檔案、一個最小單元）；一格裡有兩件事（例如「寫 A 並刪 B」「檢查 X 然後重生 Y」）就是問題，要拆成兩格。

## 本輪改動
第八輪：依第七輪 6 項必修＋5 項選修與 v2.9 澄清（--local tag 形不讀 .digest、前置檢查不分型別；add 私有無憑證分支、dest／撞名→橙；sync 版本變動那次全驗；upgrade B(2) 先解析再原子替換、解析失敗保留原檔；uninstall append 逐行比對；prune 進日誌走 apply；help 低於 floor 回 3；矩陣／目錄樹 install .tmp 欄；排版：離線包 o3t、bootstrap ae8n、dev 起點間距、t5 拆三格、update 迴圈、o10p/o10e 拆、be7 少折、be17 對齊、te14 頂點）。共 47 頁。

## 特別注意
對照 interface_spec.md 逐頁找：(1) 第七輪 6 項必修＋5 項選修是否修掉；(2) 頁間入口出口；(3) 每格一件事（只算真的兩個獨立動作）；(4) legend／名詞表。只回報真正的問題；已接受的設計不要再質疑。若某頁沒有問題請明說。最後給一句總評：這 47 頁能否交給使用者看（允許少量選修）。

## 要你回答的格式
逐頁列出 (A) 排版問題 (B) 顏色不符圖例 (C) 一般人看不懂的點與名詞表遺漏 (D) 與 notes 矛盾之處，每項給元件／線段 id（找不到 id 就寫元件上的文字）與一句說明，並標明是否必修（必須修才可交付）。最後一行明確寫「可以交付」或「還不行」。

## 附件 PNG 的頁次（依附加順序）
1. 契約 v2：不變量與角色
2. 契約 v2：動詞介面表
3. 契約 v2：規則、選項表、不開的動詞
4. 契約 v2：目錄樹與檔案範例
5. 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行
6. 契約 v2：動詞 × 檔案矩陣
7. 契約 v2：工具 repo 契約③
8. 契約 v2：啟動器 ↔ 引擎契約④
9. 契約 v2：CI 契約⑤ 與驗收矩陣
10. 架構圖 v2
11. 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install
12. 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add
13. 流程 v2：install（1）薄殼
14. 流程 v2：install（2）根 justfile 與 .dockerignore
15. 流程 v2：add（1）resolve → docker
16. 流程 v2：add（1′）apply 前置
17. 流程 v2：add（2）apply 寫入段
18. 流程 v2：sync（1）啟動器快路徑
19. 流程 v2：sync（1′）引擎 resolve
20. 流程 v2：sync（2）apply
21. 流程 v2：upgrade ── A. Renovate 路徑
22. 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker
23. 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置
24. 流程 v2：upgrade ── B. 手動路徑（2）逐檔詢問與合併
25. 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入
26. 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退
27. 流程 v2：upgrade ── E. 自身升級 (a)(b)
28. 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）
29. 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）
30. 流程 v2：dev <repo>
31. 流程 v2：dev vendor_kit
32. 流程 v2：undev <repo>
33. 流程 v2：undev vendor_kit
34. 流程 v2：remove（1）resolve → apply 前置
35. 流程 v2：remove（2）寫入段
36. 流程 v2：uninstall（1）resolve → apply 前置
37. 流程 v2：uninstall（2）寫入段
38. 流程 v2：prune
39. 流程 v2：update
40. 狀態機 v2：初始檔五態
41. 狀態機 v2：交易與進度日誌
42. 相容性矩陣 v2
43. 結束碼決策表 v2
44. 流程 v2：vendor_kit release（1）build 與驗收
45. 流程 v2：vendor_kit release（2）推 image 與資產
46. 流程 v2：離線包（1）bootstrap.sh --local
47. 流程 v2：離線包（2）add --local 與斷網 sync

