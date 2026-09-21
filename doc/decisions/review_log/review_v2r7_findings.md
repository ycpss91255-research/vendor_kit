
## 流程 v2：離線包（1）bootstrap.sh --local: must_fix 2 / optional 0
- [排版] o3t: 「否 → 視為 image tag」方框（x 520–670）與「該路徑的檔案存在？」菱形（x 270–570）重疊 50px，菱形右頂點壓在方框文字「docker load、不讀」上。
- [內容一致性] oe3tj: 「tag 形：直接 inspect」這條線從 o3t 直接跳到 docker image inspect，繞過了「在 git repo 內？」與「just ≥ 1.33.0？」兩個前置檢查；spec §1.2 bootstrap.sh 的前置檢查不分 --local 值型別。

## 流程 v2：bootstrap.sh（1）: must_fix 2 / optional 0
- [內容一致性] a8i → a8d: tag 形分支（a8q 否）也流進「讀同名 .digest 旁檔（旁檔缺 → 1）」，tag 沒有旁檔會必定失敗；與離線包（1）頁 o3t「tag 形不讀 .digest」互相矛盾。
- [排版] ae8n: a8q 的「否」線先水平到 x=525 再下折，(525,641) 落在「否：docker image inspect <引擎 ref>」方框（x 520–720, y 618–666）內，線穿無關方框且「否」標籤壓在該框左邊框上。

## 流程 v2：dev <repo>: must_fix 1 / optional 0
- [排版] d0 / d1q: 第六輪要求起點與菱形留間距，本輪起點橢圓（x 20–240）與「<dir>/dist/init.toml 存在？」菱形（x 220 起）反而重疊 20px，菱形左頂點與 de1 箭頭都畫進橢圓裡。

## 契約 v2：動詞 × 檔案矩陣: must_fix 1 / optional 0
- [內容一致性] p2c_my_r0c6: 表 B install 列的 .tmp.* 欄寫「—」，但 v2.8-2 與本輪 install(1)／交易狀態機頁都畫修復型 install 會建 .tmp.install.<id>.toml。

## 契約 v2：目錄樹與檔案範例: must_fix 0 / optional 1
  (opt) [內容一致性] t_tmp: .tmp.<verb>.<id>.toml 的寫入者只列 remove／uninstall／undev／prune，漏了修復型 install（名詞表 p2_tv15 同）。

## 流程 v2：update: must_fix 0 / optional 1
  (opt) [可讀性] 與現版比較 → 記「現版 → 最新」: 標示「對每個目標查 registry」但沒有「還有下一個目標？」迴圈回到分流菱形，圖面看起來只查一個目標就彙總；同型問題 add(2) 上輪已要求加迴圈。

## 流程 v2：離線包（2）add --local 與斷網 sync: must_fix 0 / optional 1
  (opt) [可讀性] o10p: 「docker create／cp 取本機 image 的 dist → docker run 引擎 apply add」一格兩個獨立動作；o10e「apply add：flock → 重驗指紋 → 寫入」一格三件事。

## 流程 v2：upgrade ── B. 手動路徑（1）resolve → docker: must_fix 0 / optional 1
  (opt) [排版] be7: 「(1) 有待合併？」的「是」線右出後往下、再往左、再往下、再往右進入「是：目標版 = B」方框，折了三次；目標在右下方，不該折。

## 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置: must_fix 0 / optional 1
  (opt) [排版] be17: 「CI 為真且需改 tracked 檔？」到「--dry-run？」兩菱形中心 x 差 50px，垂直「否」線出現不必要的小折。

## 流程 v2：sync（1′）引擎 resolve: must_fix 0 / optional 1
  (opt) [排版] te14: 「最後合併版本 = version.toml？」的「是」線以 entryX=0.8 接到 gen/tools.just 菱形的斜邊而非頂點，末端多一個小折。

## 流程 v2：add（1）: must_fix 1 / optional 0
- [內容一致性] c2b: 線上解析版本的流程沒有畫出「私有 image、未指定 @<tag> 且無 registry 憑證 → 1 + 6-3」分支，直接接到取得 image ref，與 §1.2 add 不符。

## 流程 v2：add（1′）: must_fix 1 / optional 0
- [顏色] c12x、c12bx: dest 不合法與命名空間撞名都是需要使用者修正的結束碼 1，卻使用紅色失敗終點；依本頁圖例及結束碼決策表應使用橙色。

## 流程 v2：sync（1′）: must_fix 1 / optional 0
- [內容一致性] t2q: 逐檔 SHA-256 驗證只列 sync --verify 或 CI，漏掉 §3.6 規定的「快路徑有差且由版本變動造成的那次」也須全驗。

## 流程 v2：sync（2）: must_fix 1 / optional 0
- [內容一致性] m3（至後續寫入段）: 承接 sync（1′）時沒有補上「版本變動時逐檔驗證」步驟，可能在該次直接 materialize／寫入後結束。

## 流程 v2：upgrade B（2）: must_fix 1 / optional 0
- [內容一致性] b14w: 此格先把合併結果原子替換到目標檔、下一頁才解析 TOML／just；§4.3 要求合併結果先重新解析、解析失敗時保留原檔，順序顛倒。

## 流程 v2：upgrade B（2′）: must_fix 2 / optional 0
- [排版] b15c → b15a: 解析失敗分支寫明該檔 baseline 不推，卻又接回「baseline 推到 N」的共同步驟，線路使例外失效。
- [內容一致性] b15q、b15c: 解析檢查位於前頁已替換目標檔之後；應移到替換前，失敗時留下原檔、記入 conflicts，且該檔 baseline 不推。

## 流程 v2：uninstall（2）: must_fix 1 / optional 0
- [內容一致性] x9b: 以「是否含我們加的三行」作單一全有／全無判斷；§4.3 append 規則要求逐一只刪仍與紀錄原文相同的行，部分缺失或被改時其餘相同的行不能全部略過。

## 流程 v2：prune: must_fix 2 / optional 0
- [排版] qe20: q12 另有一條線直接通往 q13，繞過 q12a～q12d，形成兩條互相矛盾的 apply 路徑。
- [內容一致性] q12a～q12d: apply prune 未畫出建立、更新及最後刪除 .tmp.prune.<id>.toml，與 §4.6 及「交易與進度日誌」頁「prune 自己的交易仍使用進度日誌」矛盾。

## 狀態機 v2：交易與進度日誌: must_fix 1 / optional 0
- [排版] t5: 同一格包含「寫暫存檔 → 原子替換 → 更新日誌 done」三個可獨立失敗的動作，違反每格只放一件事，應拆成三格。

## 結束碼決策表 v2: must_fix 1 / optional 0
- [內容一致性] te_r11c1、te_r11c5: help 被寫成「永遠 0」且結束碼 3 欄為空；§2、§8 與相容性矩陣都規定 P 低於 floor 時任何動詞（含救援路徑）須回 3 + 6-18 且零寫入。

## 流程 v2：離線包（1）: must_fix 2 / optional 0
- [排版] oe3tj: image-tag 分支由 o3t 直接接到 o7b，繞過 o5、o6 的 Git repository 與 just 版本檢查；這兩項是 bootstrap 的共同前置條件，不只 tar 分支需要。
- [內容一致性] o3t～o7b: 同一條繞線使 --local <image tag> 在未通過 6-16／6-23 前就進入 inspect/install 路徑，與 §1.2 bootstrap 前置檢查矛盾。

TOTAL must_fix 20; rejected 1; pages with findings 21/47