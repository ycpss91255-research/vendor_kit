
## 流程 v2：uninstall（2）寫入段: must_fix 1 / optional 0
- [排版] xe16f: 「是：只刪原文相同的那幾行」往右寫 .dockerignore 的線（xe16f）與「無／否：不動 .dockerignore」往下到「刪進度日誌」的線（xe16w）交叉。

## 流程 v2：dev <repo>: must_fix 1 / optional 0
- [排版] de1: 起點橢圓 d0（x 20–240）與判斷 d1q（x 240 起）緊貼，de1 這條線長度為零、看不到箭頭，讀者看不出流向。

## 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）: must_fix 1 / optional 0
- [內容一致性] s12: 「薄殼 == 上次產物？」（被改 → 1 + 6-28）放在 E(c)(2)，位於 E(c)(1) 的「改 version.toml 第一行」（s12w）之後；interface_spec §1.2 upgrade (b) 把薄殼被改列為「前置」、須在 (1)(2) 之前，否則被改時第一行已寫入、不

## 流程 v2：prune: must_fix 1 / optional 1
- [可讀性] q12e: 「apply prune：flock → 重驗指紋 → 刪失效的 .tmp.dist.*／殘留 .tmp.*」一格三件事；其他頁（remove、undev、uninstall）都把 flock、重驗指紋、寫入拆成三格。
  (opt) [排版] q12e: 一格同時包含拿鎖、重驗指紋、刪 .tmp.dist.*、刪完成交易殘留四個獨立動作，應至少拆成鎖、重驗、清理三格。

## 流程 v2：vendor_kit release（1）build 與驗收: must_fix 1 / optional 0
- [排版] pend: 右上便條文字超出便條框與頁面右緣（「image 命名」「綠了」被裁切）。

## 流程 v2：vendor_kit release（2）推 image 與資產: must_fix 1 / optional 0
- [排版] pend: 右上便條同樣文字溢出框外、右緣被裁切。

## 相容性矩陣 v2: must_fix 0 / optional 1
  (opt) [內容一致性] tb_r3c3: (b) 表降版列結束碼寫「0（無損）／3」，但同列動作是「正常重產薄殼」；spec §1.2 upgrade (b) 降版同 P／schema 時「依上列 0／1」（重產薄殼 → 1 + 6-2），(a) 表 P > c

## 流程 v2：upgrade ── A. Renovate 路徑: must_fix 0 / optional 1
  (opt) [可讀性] a6c: 「commit、push」一格兩個動作。

## 流程 v2：upgrade ── 逐檔判斷、衝突重入、回退: must_fix 0 / optional 1
  (opt) [排版] cx_e0: 起點橢圓 cx0 與判斷 cx1 中心高度差 9px，水平線出現不必要的小折；cx_e1 亦有 5px 折。

## 流程 v2：add（1）resolve → docker: must_fix 0 / optional 1
  (opt) [排版] cfe: 「add 前」→「add 後」兩框中心高度差 9px，橫線出現不必要的小折。

## 流程 v2：remove（1）resolve → apply 前置: must_fix 0 / optional 1
  (opt) [排版] me9c: 「否」線以 entryX=0.708 接到 --dry-run 菱形的斜邊而非頂點，線末端出現小折；同型問題見 uninstall（1）xe5f、remove（2）me11h／me12m、prune qe11／qe20、

## 契約 v2：規則、選項表、不開的動詞: must_fix 0 / optional 1
  (opt) [內容一致性] p1C_no: 把 --porcelain 寫成「未定案」，但本頁同時宣告「無待拍板」，且 interface_spec §9.1 明定待定項為 0。

## 流程 v2：bootstrap.sh（1）: must_fix 2 / optional 0
- [內容一致性] a8q: 只依「含 / 或以 .tar 結尾」直接分流，沒有實作 B1 的「值同時是既存檔案且可解讀為 image tag → 1 + 6-37」消歧分支。
- [內容一致性] a8q → a8l: 檔案路徑分支沒有先判斷檔案存在，圖上直接進 docker load，與「路徑必須存在，否則 1」不一致。

## 流程 v2：install（2）根 justfile 與 .dockerignore: must_fix 0 / optional 2
  (opt) [可讀性] i7: 寫成「建 justfile（兩行）」但右側逐字內容實際是四行，會直接誤導讀者。
  (opt) [內容一致性] i7f: 逐字框以四個空白／&nbsp; 顯示 recipe 縮排而非 <pre> 中的真 tab，不符合規格要求的逐字四行內容。

## 流程 v2：add（2）: must_fix 1 / optional 1
- [排版] c16 至 c20: 標示「逐檔」但沒有回到下一個 [[file]] 的迴圈或「全部檔案完成？」匯合，圖面表示處理一個初始檔後便直接寫 baseline。
  (opt) [排版] c20q: 兩條出口沒有「是／否」線上文字，在交會密集處只能靠目標框猜測分支。

## 流程 v2：sync（1′）: must_fix 0 / optional 1
  (opt) [顏色] ncx: CI 因 local 覆寫而拒絕屬「需要人處理」情境，依圖例與第 43 頁決策表應為橙色，目前用紅色失敗終點。

## 流程 v2：dev vendor_kit: must_fix 1 / optional 1
- [內容一致性] v2c: 把 docker image inspect <tag> 畫成引擎容器內的藍色步驟；規格明定引擎容器不呼叫 docker，image ID 必須由主機啟動器取得後交給引擎。
  (opt) [顏色] v2x: CI 拒絕 dev 與第 30 頁相同，應是橙色需要人動作，目前為紅色。

## 流程 v2：remove（2）: must_fix 0 / optional 1
  (opt) [排版] m9m: 三條出口到零命中、唯一命中、多處命中都沒有線上分支文字，讀者無法由線段本身確認哪條代表哪個結果。

## 流程 v2：uninstall（2）: must_fix 2 / optional 0
- [內容一致性] x4、x5a～x5d: 流程沒有刪除 baseline/.gitkeep 與 baseline/.vendor_kit.toml 的步驟；它們不是逐工具 remove 的 <repo> metadata，保留後 .vendor_kit/ 不可能成為空目錄。
- [內容一致性] x5q／x5t: 圖宣稱目錄空時可 rmdir，但按本頁已畫出的刪除集合，兩個 baseline 根檔仍會存在，出口與前序動作不相容。

## 流程 v2：update: must_fix 0 / optional 1
  (opt) [內容一致性] u7 → u8a: 無憑證而查詢失敗後仍流向「取 SemVer 最大正式版」，但此分支沒有 registry 結果可解析；應直接記錄該目標失敗並進下一目標／彙總。

## 狀態機 v2：交易與進度日誌: must_fix 1 / optional 1
- [內容一致性] bT1、t4f、r3: 頁面宣稱涵蓋所有可寫動詞且恢復清單含 install，但日誌位置只列 add／upgrade 與 remove／uninstall／undev／prune，沒有 install 的日誌位置或「第一次 install 另走回滾、不使用日誌」的例外說明。
  (opt) [可讀性] p12_tv3: 名詞表把 install 列為會從進度日誌恢復的動詞，與主圖缺少 install 日誌互相衝突，非工程讀者無法判斷實際契約。

## 流程 v2：離線包（1）: must_fix 1 / optional 1
- [內容一致性] o3: 與第 11 頁相同，只畫路徑／tag 的基本分類，沒有「既是既存檔案又可解讀為 tag」的 6-37 判斷出口。
  (opt) [排版] o1w: 一格同時包含偵測 daemon 架構、選擇平台 tar、exec bootstrap.sh 三個獨立動作；即使是便利包裝也違反一格一件事。

## 流程 v2：離線包（2）: must_fix 2 / optional 1
- [內容一致性] o10l、o10a: 圖宣稱 bootstrap.sh 會「對每個 -t <repo>」找到並載入對應工具 tar，但介面只有單一 --local <tar>，也沒有 <repo> → 工具 tar 的映射或搜尋規則。
- [內容一致性] o10: 畫成 bootstrap.sh 自動呼叫 add <repo> --local <工具 tar>；規格的 bootstrap -t 只呼叫 add <repo>[@tag]，離線工具應由使用者另行提供工具 tar 並執行 add --local，跨頁入口／出口無法成立。
  (opt) [可讀性] oo0 至 o10l: 沒有說明工具 tar 從何而來；第 46 頁列出的 vendor_kit-vN-local.tar.gz 只明確包含引擎平台 tar，一般讀者會誤以為引擎離線包同時包含所有工具。

TOTAL must_fix 16; by category {'排版': 5, '內容一致性': 10, '可讀性': 1}; rejected 5; pages with findings 23/47