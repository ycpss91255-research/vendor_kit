# 第九輪審查（只有 Claude；codex token 不足）verdict=還不行；must_fix 23，optional 0（未經第三方驗證）
- [內容一致性] 契約 v2：規則、選項表、不開的動詞 / p1C_opt_r7c0: 選項表「--local <image tag 或 tar>」仍把 add 與 bootstrap.sh 一起列為可收 tag 或 tar；v2.10 已定 add --local 只收存在的 tar，應拆成兩列或在適用欄明確區分。
- [排版] 架構圖 v2 / pull_eng / pull_dist / q_reg: 線端接到整個 p4H／p4E 容器而非負責該資料的最小模組；引擎 image／工具 image 應接啟動器模組，registry 查詢應由 registry 模組發出。
- [排版] 架構圖 v2 / m_lg: 「薄殼與根檔管理」列了根 .dockerignore 職責，卻沒有相應的最小單元，模組內容不完整。
- [內容一致性] 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install / p5_tv2: --local 名詞說明稱 tag 形的正式 digest 取自既有 version.toml／metadata；第一次接入沒有這些資料，v2.10 已定應取 bootstrap.sh 內嵌引擎 ref 的 digest。
- [排版] 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add / a10q / ae22y / a11: 每次 add 後直接問「還有下一個 -t？」並繼續迴圈，直到全部跑完才問「任一 add 失敗？」，沒有「本次 add 失敗立即中止」的分支。
- [內容一致性] 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add / a10q / ae22y / a11: 上述迴圈流程與頁面宣告的「一個失敗即中止」不一致。
- [內容一致性] 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add / p5d_tv2: 把第一次 bootstrap tag 形的 digest 說成取自既有檔案，應改為內嵌引擎 ref 的 digest。
- [內容一致性] 流程 v2：install（1）薄殼 / p5c_tv2: 重複過時的 --local 說明：第一次 bootstrap tag 形應使用內嵌引擎 ref 的 digest，而非既有 version.toml／metadata。
- [內容一致性] 流程 v2：install（2）根 justfile 與 .dockerignore / p5cc_tv2: 同樣重複過時的第一次 bootstrap tag digest 來源（應為內嵌引擎 ref 的 digest）。
- [內容一致性] 流程 v2：add（1）resolve → docker / p5b_tv5: --local 名詞說明仍保留「其餘值視為本機 image tag」分支；本頁是 add，v2.10 已定只接受存在的 .tar。
- [內容一致性] 流程 v2：add（1′）apply 前置 / p5bp_tv5: 名詞表同樣把 add 的 --local 說成可收 tag，與 v2.10 矛盾。
- [內容一致性] 流程 v2：add（2）apply 寫入段 / p5bc_tv5: 名詞表同樣保留 add --local 的 tag 分支，與 v2.10 矛盾。
- [排版] 流程 v2：upgrade ── E. 自身升級 (a)(b) / s2lv → s2r: image ID 相符的「否」分支缺線；s2r「docker run 新引擎 upgrade vendor_kit」沒有正常入口，成功路徑懸空。
- [內容一致性] 流程 v2：upgrade ── E. 自身升級 (a)(b) / s2lv → s2r: 因缺少上述連線，local 覆寫 ID 相符時無法進入新引擎接手，流程內容不完整。
- [排版] 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） / s11v → s11r: local image ID 沒有不符時的正常分支缺線；直接執行 upgrade vendor_kit 的成功入口懸空。
- [顏色] 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） / s12hz: 它是「改完第一行後交給新引擎再跑」的跨頁／續跑入口，卻使用代表成功終點的綠色；應使用跨頁入口樣式。
- [內容一致性] 流程 v2：upgrade ── E(c) upgrade vendor_kit（1） / s12t / s12tn / s12vz: 把「指定 @tag」和「frozen」合成同一個「不查 registry、第一行未變」分支；明確指定的 @tag 若不同於目前 ref 仍須以指定目標判斷並可能改第一行，現在會被當成無新版路徑。
- [顏色] 流程 v2：dev vendor_kit / v9: 「請執行 upgrade vendor_kit」是明確需人動作，卻使用綠色成功終點；依本輪規則應為橙色。
- [可讀性] 流程 v2：uninstall（2）寫入段 / x5d: 「刪 gen/ 與 baseline/ 內剩下自產檔」一格包含兩個可獨立失敗、對不同目錄生效的刪除動作，應拆格。
- [排版] 狀態機 v2：交易與進度日誌 / r3 / r3x: 從「本動詞可寫？」的否分支只畫出 sync／update 回 1，沒有 help 的獨立出口。
- [內容一致性] 狀態機 v2：交易與進度日誌 / r3 / r3x: v2.10 已定 help 偵測到未完成交易要印 6-33 但仍回 0；本頁從「任何動詞」進入後沒有這條路徑，與第 1、43 頁的規則不一致。
- [可讀性] 流程 v2：離線包（2）add --local 與斷網 sync / o10e3: 同一格同時寫 version.toml 與 metadata，屬兩個獨立檔案寫入，應拆成兩格。
- [可讀性] 流程 v2：離線包（2）add --local 與斷網 sync / w4e: 同一格同時包含 image ID 驗證、materialize 與 cache verify，三者可各自失敗，應至少拆成「驗證 ID」與「重建／驗證 cache」兩格。

## optional