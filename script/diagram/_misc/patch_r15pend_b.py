import re
B = {
 "v1p5": [
  "a8t：兩條出邊 ae8tx（→ 1 + 6-37）、ae8tn（→ 續頁 A）缺是／否標籤，目標格文字也不以是／否開頭，看不出哪條是哪個分支",
  "a3：bootstrap.sh 前半缺主機側巢狀檢查（上層或下層已有 .vendor_kit/ → 1 + 6-35）；install（1）頁 i2r 說巢狀只能由啟動器在主機側查，但整條 bootstrap 流程沒有任何一格做這項檢查（缺分支）",
 ],
 "v1p5ccc": [
  "a10x／a10rq0：「apply 回 0？」「resolve 回 0？」的否都只接橙終點 a12r（2／3）；apply 回 1（寫入失敗）、resolve 回 1（6-3、dest 撞名）沒有分支到紅終點 a12（a12 雖列「寫入失敗」但沒有線進來）",
 ],
 "v1p5cc": [
  "i7：「無：建 justfile（四行）」是寫入格，缺「失敗」出邊到共通匯流 ix（同頁 i11／igy／igm／idl 都有）",
  "ign：「無：建 .dockerignore（四行）」是寫入格，缺「失敗」出邊到共通匯流 ix",
  "ie20z：新建 .dockerignore（ign）後直接接 idl 刪進度檔，沒經 igm 把新增的行記到 baseline/.vendor_kit.toml；uninstall（2）只刪「紀錄相同的行」，沒紀錄就永遠刪不掉",
  "ix：紅終點只寫「明列已完成／未完成」，沒分「第一次安裝 → 依進度檔移除已寫的檔、不留半成品」（install（1″）i4wq、bootstrap（1′）a9c、spec §1.2 都有分）",
  "ie13／ie20z：兩條流程線都繞到 x=1610 走失敗匯流的同一條垂直線，並與 fb_i11（y=801）、fb_igm（y=1423）的水平段反向重疊，分不清流程／失敗與來源",
 ],
 "v1p5c": [
  "bI：色帶順序「執行紀錄 → 偵測既有進度檔 → 引擎 ref → … → flock」與圖不符：圖裡 ipq「既有進度檔？」排在 docker run／flock 之後、在引擎內；add（1）與 sync（1）頁則是啟動器在起容器前偵測，順序與誰做跨頁不一致",
 ],
 "v1p5cm": [
  "ie4gy：「config.toml 存在？」的「是」標籤放在線尾（565,902→565,1104→640,1104）貼著出口橢圓左上緣，離菱形太遠又貼到別的框；菱形左邊出口本身無標籤",
 ],
 "v1p5b": [
  "cpr／cpq：藍格「先恢復」（引擎做）與 cpq 偵測畫在 c1「docker run <引擎> resolve add」之前，此時沒有容器可執行；v2.17-1 明定偵測→恢復放在 docker run 引擎之後、啟動器不做恢復",
  "ce1tx：「值是存在的 .tar？」→ 紅「1 + 6-24」的「否」標籤擠在 20px 的縫（菱形左緣 x=280、橢圓右緣 x=260），字壓在橢圓邊線上",
 ],
 "v1p6": [
  "npq／npx：6-33 偵測畫在啟動器段、grep／docker run 之前；spec §1.2 sync 與 v2.17-1 明寫 6-33 偵測在引擎 resolve sync 內，啟動器只把「無 .tmp.*」當快路徑條件（啟動器不解析 TOML、讀不到 metadata [progress]）",
  "n1p：「否：inspect；本機無才 docker pull <引擎 ref>」一格兩事；同頁 n1v 與 install（1）頁都拆成菱形＋「無：docker pull」，應比照拆成判斷＋步驟",
 ],
 "v1p6cc": [
  "mb：跨頁出口橢圓「否：續 sync（2）頁（apply|yes）」（y 1905–1985）壓在圖例列上（y≥1947），橢圓下半與文字被圖例蓋住",
 ],
 "v1p6c": [
  "m0m：「處理 mount 記錄：驗 <dir>/dist/init.toml；記 -v …」同格含檢查與記錄兩件事，且 spec §3.3 mount「缺 → 1」沒有失敗出口與終點",
 ],
 "v1p6cw": [
  "me4vn：「否：跳過逐檔驗」標籤壓在 mq 菱形左上邊線上，字被邊線劃過",
 ],
 "v1p7c": [
  "bpr／bpq：偵測進度檔（bpq，啟動器泳道）與先恢復（bpr）畫在 b1「docker run 引擎 resolve upgrade」之前，違反 v2.17-1（恢復由引擎做、在 docker run 之後）；install（1）頁已改為 docker run→flock→偵測，本頁未同步",
 ],
 "v1p7cc": [
  "be20qn：「否」標籤畫在 b13a 方框內左上角，像是 b13a 的文字",
 ],
 "v1p7cccc": [
  "p7cq_tv4：名詞表寫 6-14「結束 2，需人處理」，spec §6 6-14 類別為「—（提醒，不改結束碼）」，同頁便條 b18r 也寫「僅是提醒、不改結束碼」，頁內自相矛盾",
  "fb_b16b／b16x：刪進度檔失敗流進 b16x「1：寫入失敗…進度檔保留」，但此時寫入已全部完成；add（2）c23x 依 v2.17-3 已補「若僅刪進度檔失敗，寫入已完成且進度檔留待下次刪」，本頁終點文字未同步",
 ],
 "v1p7b": [
  "ce_1y 等：左側九條短邊（菱形→藍格）的「是」標籤全都擠在藍格右上 v2 小標上，貼字（v2.17-9 不擠短線）",
  "ce_9n：q9 的「否」標籤被自己的折線劃過",
 ],
 "v1p7bd": [
  "d2wx：共通匯流終點寫「進度檔保留」，但本頁是 sync 的 apply，sync 不建進度檔（spec §2c 只偵測）；sync（2′）頁 m7x 寫的是「cache 可能部分更新，下次 sync 再取」",
  "fb_d2c2／fb_d2c3：失敗線與 d3、d3s 虛線框底邊重合，右側匯流直線與兩框右邊重合，看起來檔案框有實線邊、失敗線從檔案框出來",
 ],
 "v1p7bc": [
  "spr／spq：偵測進度檔（spq）與先恢復（spr）畫在 s1「docker run 舊引擎 resolve upgrade」之前、且在啟動器泳道做恢復，違反 v2.17-1（恢復由引擎做、在 docker run 之後）",
  "se3：「是」標籤壓在 s2so 藍格第一個字上，兩個「是」疊在一起",
  "se6lo：「否」標籤畫在 s2lo 菱形內部、壓到菱形文字「(vendor_kit=)？」",
  "se2n：「否」標籤貼在 s2q 菱形下邊線上，且線從底頂點偏左出、多一個小折",
 ],
 "v1p7bca": [
  "s2c2：缺 --dry-run 分支：spec §1.1 --dry-run 適用 upgrade（含不帶 repo）、§3.2 apply 順序為 argv 一致 → dry-run 分支（唯讀，本機 0）→ 建進度檔；本頁 argv 一致後直接 s2d 建進度檔、s2e 改第一行，--dry-run 時仍會寫檔",
  "se5／fb_s2e：s2e→s2h 的成功線（y=708，x 440–702）與 s2e 的失敗匯流線（y=708，x 1006–1610）同高、左右各一段，縮圖像一條橫貫的線，分不清成功／失敗；建議 fb_s2e 水平段下移 12–16px 或改由方框右側出線",
 ],
 "v1p7bcx": [
  "s12j：「建進度檔（已有 → 沿用）」一格兩事（判斷＋動作）；E(c)(2) 頁同邏輯已拆成 s12jq 判斷＋s12jn 建檔，本頁把判斷藏在括號裡，恢復路徑（來自 E(c)(1) s12jr）看不出走哪條",
  "se12wh／fb_s12j：s12j 往下接啟動器 grep 框的線（y=317，x 440–702）與 s12j 的失敗匯流線（y=317，x 1006–1610）同高、左右各一段，縮圖像一條橫貫整頁的線，分不清成功／失敗",
  "se12hax：「逾時」標籤壓框：s12ha 右邊（x=990）到紅終點 s12hax 左邊（x=1020）只有 30px，標籤貼到橢圓邊線；比照 E(a′)／E(c)(1) 把紅終點右移到 x≥1030",
 ],
 "v1p7bccc": [
  "s12jn：缺 CI 模式閘門：E(c)(1) 的 CI 分支（s12fz 目標 = 現 ref）進本頁後，薄殼不符 → s12jn 建進度檔 → s13 重產進 git 的薄殼五檔，與 spec §0「CI 模式不寫任何進 git 的檔；需改 → 1 印清單」矛盾（B(1′) 頁 b12 有此閘，本頁沒有）",
  "s12jy／s12jn：菱形 s12jy 右頂點（x=860）與藍框 s12jn 左邊（x=860）貼死無間隙，縮圖像一個元件",
  "se15ns：s12jn→s13 的直線（x=930，y 634→829）穿過 se15wf（y=702）與 fb_s12jw（y=744）兩處交叉；fb_s12jw 又與 se15s、se15jy 的水平段同高，三段共線看不出來源",
 ],
 "v1p7bcce": [
  "s13gy：「三方合併到暫存」缺失敗出邊到 s13qx 匯流；spec §1.2 upgrade 明定 git merge-file 的 I/O／執行錯誤 → 1（非 2），本頁只畫解析失敗與衝突兩種",
  "se17adn：「否：不替換；記 declined」標籤落在 x≈327–458、y≈542，而該邊垂直段在 x=420，線從「記 de|clined」字中間穿過",
  "se17gpx：「是：留原檔、不推基準版（記 conflicts）」標籤（y≈416）壓在該邊的水平段（y=416，x 400–610）上，垂直段從標籤左端起筆",
  "se17pnn：B 段「否：不建（記 declined）」標籤（y≈1305）壓在該邊水平段（y=1305，x 400–610）上",
  "fb_s13gw／fb_s13gb／fb_s13gnb：三條失敗匯流線的水平段分別與 se17adn（y=728）、se17gpx（y=796）、se17pnn（y=1460）同高共線，各成一條橫貫左右的線，讀不出左段是「否／解析失敗」、右段是「失敗」",
 ],
 "v1p8": [
  "dpe_n：菱形 dpq 到 d1q 的邊只有 20px（y 465→485），「否」標籤落在 (420,475)，而恢復框回流線 dpe_r 的水平段正好在 y=475（x 420–730）從標籤上穿過",
 ],
 "v1p8c": [
  "u3：u2「有 path 覆寫？」= 否 → u3「0：未啟用」由引擎 resolve 直接終止，啟動器三叉（u4q0 → u4q1 → u5a）沒有 apply|no → 0 的出路（同 remove（1）頁便條所列 m3）",
  "ue8ax：「逾時」標籤壓框：u6a 右邊（x=980）到紅終點 u6ax 左邊（x=1010）只有 30px，標籤貼到橢圓邊線",
 ],
 "v1p8cx": [
  "ue11／fb_u6ced：「是：留著」迴線的水平段（y=524，x 525–640）與 u6ced 的失敗匯流線（y=524，x 996–1610）同高共線，縮圖像一條橫貫的線；另五條失敗線（y=584／704／772／832）都只在對應檔案框底邊下方 10px、貼著框底走",
 ],
 "v1p8cc": [
  "w3：w2q「有 vendor_kit 行？」= 否 → w3「0：未啟用」由引擎 resolve 直接終止，啟動器三叉（w1q0 → w1q1 → w1b）沒有 apply|no → 0 的出路（同 remove（1）頁便條所列 m3）",
  "w2s2：「產生指紋（含 version.local.toml hash）→ stdout vk-resolve/1」一格兩事；undev <repo>（1）u4c／u4d、remove（1）m6d／m6d2、uninstall（1）x2e／x2e2 都拆成兩格，應比照拆成「產生指紋」＋「stdout vk-resolve/1：指紋、apply|yes」",
 ],
 "v1p8bccc": [
  "me12n：「否：不刪（記孤兒 append 行）」標籤被 me11hn（「無」分支的垂直線）穿過，「append 行」字被線切開",
 ],
}
src = open("disc_v1_b.py", encoding="utf-8").read()
lines = src.split("\n")
added = {}; legend_added = []
for key, items in B.items():
    idx = [i for i, l in enumerate(lines) if re.match(rf'addpage\("{key}", ', l)]
    assert len(idx) == 1, key
    ai = idx[0]
    var = re.search(r', (\w+)\)\s*$', lines[ai]).group(1)
    if lines[ai - 1].startswith(f"pendq({var}, "):
        m = re.match(r'(pendq\(\w+, ")(.*)("\)\s*)$', lines[ai - 1])
        assert m, key
        lines[ai - 1] = m.group(1) + m.group(2) + "".join("\\n• " + t for t in items) + m.group(3)
    else:
        # foot() call: find its start line (last line starting with f"foot({var}, " before ai) and drop "pend" from exclusion set
        fi = max(i for i in range(ai) if lines[i].startswith(f"foot({var}, "))
        done = False
        for j in range(fi, ai):
            new = re.sub(r'(ALL - \{[^}]*?)(, "pend"|"pend", )([^}]*\})', lambda m: m.group(1) + m.group(3), lines[j])
            if new != lines[j]:
                lines[j] = new; done = True; legend_added.append(key)
        assert done, key
        lines.insert(ai, f'pendq({var}, "待處理問題' + "".join("\\n• " + t for t in items) + '")')
    added[key] = len(items)
open("disc_v1_b.py", "w", encoding="utf-8").write("\n".join(lines))
print(added, sum(added.values())); print("legend pend added:", legend_added)
