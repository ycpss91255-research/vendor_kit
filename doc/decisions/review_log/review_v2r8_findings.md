# 第八輪審查 verdict claude=還不行 codex=還不行；must_fix 18，optional 10，rejected 1

## 流程 v2：upgrade ── B. 手動路徑（1′）apply 前置: must_fix 1 / optional 0
- [顏色] b10dx、b10nx: 「否 → 1：dest 不合法」「是 → 1：命名空間撞名」仍為紅色；v2.9-2 規定需人動作用橙，add（1′）同情境已改橙。  (claude+codex)

## 流程 v2：離線包（1）bootstrap.sh --local: must_fix 2 / optional 0
- [顏色] o3bx、o3cx、o4x: 「檔案路徑必須存在」「6-37 值歧義」「.tar.digest 旁檔缺」三個 1 結束橢圓用紅色，bootstrap.sh（1）頁同情境 a8ex／a8tx 用橙（需人動作）；同一情況兩頁顏色不一致。  (claude+codex)
- [內容一致性] o3t → o7b → o8e: tag 形不讀 .digest，但 o8e 說正式 digest 取自既有 version.toml；第一次 install 沒有既有 version.toml，此分支缺少可成立的 digest 來源。  (codex)

## 架構圖 v2: must_fix 1 / optional 0
- [排版] f_user / f_user_f0: 「初始檔（使用者的，進 git；永不刪、永不覆蓋）」容器標題折成兩行，第二行被內框「Dockerfile 等（copy）」（y=30 起）蓋住，字被裁切看不到。  (claude)

## 流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install: must_fix 1 / optional 0
- [排版] ae11b × ae6y: 「無：docker pull」→「docker run install」的線先往下再往左的水平段，與「本機有？」的「有」垂直線交叉。  (claude)

## 流程 v2：install（2）根 justfile 與 .dockerignore: must_fix 1 / optional 1
- [內容一致性] igx、igz: 兩個 0 結束橢圓內含「修復型先刪進度日誌」動作（印指示＋刪日誌一格兩事）；「是」分支有獨立「刪進度日誌」步驟格，否分支卻藏在終點裡。  (claude)
  (opt) [排版] ie13: 「無：建 justfile」→「印 justfile 結果」的線繞到分組最上方（入口橢圓上面）再繞左側下來，折四次；目標就在正下方。  (claude)

## 流程 v2：dev <repo>: must_fix 2 / optional 0
- [顏色] d3a: 「是 → 1：CI 拒絕 dev」為紅色；v2.8-7 規定 CI 拒絕 dev 為橙，dev vendor_kit 頁同情境 v2x 已是橙。  (claude)
- [顏色] d1x、d3c: 路徑不存在或缺 dist/init.toml 是使用者可修正的輸入問題，依本頁圖例及結束碼表應用橙色，不是紅色拉取／寫入失敗。  (codex)

## 契約 v2：啟動器 ↔ 引擎契約④: must_fix 0 / optional 1
  (opt) [可讀性] d2_in: stdout → 「apply|yes？」判斷的線上標「③」，但 ③ 是後面的主機 docker 群組，初看以為判斷屬於 ③。  (claude)

## 流程 v2：bootstrap.sh（2）--local 記錄 → 逐工具 add: must_fix 0 / optional 1
  (opt) [可讀性] a10l: 逐工具 add 只有浮動文字「← 對每個 -t 重複」，沒有「還有下一個 -t？」迴圈菱形；update 頁同型問題本輪已加迴圈。  (claude)

## 流程 v2：sync（1′）引擎 resolve: must_fix 0 / optional 1
  (opt) [可讀性] 對每個工具重複（浮動文字）: 逐工具判斷同樣只有浮動字「← 對每個工具重複」，無迴圈菱形回到 path 覆寫判斷。  (claude)

## 流程 v2：install（1）薄殼: must_fix 0 / optional 1
  (opt) [可讀性] i4en → i4ld: 「薄殼已存在？否 → 第一次=全新建」之後又匯入「第一次 install（薄殼原本不存在）？」再問一次同一件事；且該菱形的「否」標籤壓在「否（修復型）：建進度日誌」框左上角。  (claude)

## 流程 v2：add（2）apply 寫入段: must_fix 0 / optional 1
  (opt) [排版] ce28n、ce28y: 「問要在 X 加這幾行嗎」的「是」「否」兩條線從菱形底邊出，標籤壓在 c20／c20n 框的上緣。  (claude)

## 流程 v2：upgrade ── E(c) upgrade vendor_kit（1）: must_fix 1 / optional 1
- [內容一致性] s12w: 修改 version.toml 第一行之前沒有建立 upgrade 進度日誌；upgrade 是可寫動詞，第一個寫入前必須已有可恢復日誌。  (codex)
  (opt) [排版] se11px、se11vx: 「失敗」垂直線直接落在「是」水平線上（T 接後共用一段進紅橢圓），「是」標籤緊貼失敗線；sync（1）ne5x/ne5y、E(a) se6px/se6vx 同型。  (claude)

## 流程 v2：upgrade ── E. 自身升級 (a)(b): must_fix 0 / optional 1
  (opt) [內容一致性] s2lx: 第一行已改後新引擎「拉不到／image ID 不符 → 1：印原因」，§3.4 規定此情況印 6-2b（引擎已鎖定為 vY 但薄殼尚未重產）。  (claude)

## 流程 v2：prune: must_fix 1 / optional 1
- [排版] q12c、q12d: 每格同時做資源清理及更新日誌 done，是兩個獨立寫入動作；應像交易頁一樣拆成「執行清理」與「更新進度日誌」。  (codex)
  (opt) [內容一致性] q12c、q12d: 「刪失效暫存 → 日誌 done」「刪殘留 .tmp → 日誌 done」各一格兩事（刪＋更新日誌），交易頁 t5 已拆成三格。  (claude)

## 流程 v2：離線包（2）add --local 與斷網 sync: must_fix 1 / optional 1
- [內容一致性] o10q → o10a／o10b: o10q 宣稱支援 tar／tag 三分支，但唯一後續仍固定 docker load 並讀 .digest；缺少 tag 形「不 load、不讀 .digest、只 inspect image ID」的實際分支，違反 v2.9 澄清。  (codex)
  (opt) [排版] o10a、o10c（oe22～oe25）: 逐工具鏈上 docker load／docker image inspect 兩框寬 300、其餘 400，導致每段直線都多一個小折。  (claude)

## 契約 v2：不變量與角色: must_fix 1 / optional 0
- [可讀性] p1_tv17: 名詞表寫「sync／update／help 只印 6-33」，但 help 不受未完成交易影響，與 §0、6-33 矛盾；應刪除 help。  (codex)

## 契約 v2：目錄樹與檔案範例: must_fix 1 / optional 0
- [排版] t_tmp: 同一格同時放交易日誌 .tmp.<verb>.<id>.toml 與啟動器暫存目錄 .tmp.dist.<id>/，是兩種不同檔案／用途，應拆成兩格。  (codex)

## 契約 v2：schema：version.toml／local／metadata／印記／薄殼首行: must_fix 1 / optional 0
- [排版] p2b_vl_r2c0、p2b_mt_r0c0: 表格宣稱「一列一欄位」，但把 schema 與 written_by 合在同一欄位格，應各拆一列。  (codex)

## 流程 v2：sync（2）apply: must_fix 1 / optional 0
- [排版] m3v: 同一格同時做「逐檔 sha256 驗證」及「失敗後重裝並警告」，屬兩個可獨立失敗的動作，應拆成驗證與重裝兩格。  (codex)

## 流程 v2：upgrade ── B. 手動路徑（2′）收尾寫入: must_fix 1 / optional 0
- [內容一致性] b18: 文字宣稱解析失敗後「baseline 已在目標版」，但解析失敗的該檔 baseline 必須保留原版；應明寫「除解析失敗檔外」。  (codex)

## 流程 v2：upgrade ── E(c) upgrade vendor_kit（2）: must_fix 1 / optional 0
- [內容一致性] s13x: 把所有薄殼重產失敗都導向 6-2b；6-2b 只適用第一行已變或第二次又變，「無新版、第一行未變」而重產失敗時不應宣稱引擎已鎖定為新版本。  (codex)

## 流程 v2：update: must_fix 1 / optional 0
- [內容一致性] bU: 摘要只列結束碼 0／1／2，遺漏全域相容性檢查可能回 3；應改為 0／1／2／3，避免與結束碼決策表及 floor 規則矛盾。  (codex)

## rejected
- [流程 v2：bootstrap.sh（1）檢查 → 引擎 image → install] a8i (codex): tag 形只取得 image ID，未說明第一次 install 在既有 version.toml 不存在時正式 ref@index digest 從何而來；無法同時滿足「tag 形不讀 .digest」與必須寫正式 digest。 → 圖上已閉環：本頁「專案已有 version.toml？」→ 否 → 「引擎 ref = 內嵌引擎 ref（第一次接入）」，而本頁名詞表定義引擎 ref = 「ghcr.io/…/vendor_kit:vN@sha256:…」（即含 index digest 的完整 ref），XML 其他頁亦明寫「bootstrap.sh 內嵌完整 ref（tag@index digest）」；install 寫的