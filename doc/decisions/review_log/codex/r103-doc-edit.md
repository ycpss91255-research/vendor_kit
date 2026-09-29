## 必改

1. **位置：** [02_invariants.md:148](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:148)（第 4 條）  
   **問題：**「`3` 是唯一零寫入的碼」不成立。低版本 just、Podman 都以 `1` 在任何寫入前結束；執行紀錄建不出來也以 `1` 且不動任何檔。  
   **建議：** 改成「`3` 一律保證零寫入」，不要宣稱其他結束碼不可能零寫入；或明確把唯一性限定在版本組合不合的情況。  
   **出處：** [02_invariants.md:164](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:164)、[ADR-0007 §1:23-26](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:23)、[04_messages.md:19-21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:19)。

2. **位置：** [04_messages.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:18)（6-19）、[04_messages.md:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:21)（6-39）  
   **問題：** 兩列都分類為「需人處理」，但「下一步」是 `—`，也沒有可直接複製的指令。這違反 02 對「需人處理」的明文要求；03 又更廣泛地宣稱結束碼 `1` 一定印下一步。6-19 的「使用支援此檔案版的引擎」也不是可執行指示。  
   **建議：** 補上符合既定介面的確切下一步；若客觀上不存在可複製指令，則須同步修正類別或上位規則，不能維持目前互相矛盾的三種說法。  
   **出處：** [02_invariants.md:166](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:166)、[03_interface.md:183](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:183)。

3. **位置：** [04_messages.md:13-21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:13)（總表）、[ADR-0008 §7:68](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:68)  
   **問題：** 04 自稱列出 VK 會印出且要使用者處理的訊息，但 ADR-0008 的降版拒絕引用 `6-10`，總表沒有這個編號。該處也只是裸文字 `6-10`，不是有名字的超連結。  
   **建議：** 依已定案的編號規則把 6-10 納入總表，並把 ADR 引用改成具名連結；若 6-10 已作廢，則 ADR 必須明確修訂，不能留下懸空錯誤碼。  
   **出處：** [04_messages.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:5)、[review/README.md:20](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:20)、ADR-0008 §7。

4. **位置：** [03_interface.md:23-28](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:23)（主機需求）  
   **問題：**「版本不足時印出安裝指令」涵蓋 Docker 與 just，但引用的 ADR-0007 只對低版本 just 明訂下載與安裝指令；Docker 只定義版本下限與寫入前停止。出處支撐不了這句的範圍。  
   **建議：** 把安裝指令規則限定為 just，或補上 Docker 也必須如此處理的權威決議。  
   **出處：** [ADR-0007 §1:23-26](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:23)。

5. **位置：** [review/README.md:17](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:17)（寫法規則）  
   **問題：** 規定每頁不得引用後面頁，但 02 已按決議 A 引用 04 的固定訊息編號。既定文件結構與寫法規則直接衝突。  
   **建議：** 明訂 04 訊息編號可由 02、03、ADR 回連；若本意只是防止名詞先用後定義，就把限制縮到名詞。  
   **出處：** [02_invariants.md:109](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:109)、[02_invariants.md:128](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:128)、[04_messages.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:5)。

6. **位置：** [review/README.md:7-12](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:7)（「這個目錄放什麼」）  
   **問題：** 閱讀順序只列 01～03，漏掉 04；同檔後面卻寫「目前 01～04」。第一次閱讀者不會從目錄進到錯誤碼總表。  
   **建議：** 加入具名連結「04 訊息與錯誤碼總表」及一句用途。  
   **出處：** [review/README.md:26](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:26)、[AGENTS.md:16](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:16)。

7. **位置：** [AGENTS.md:14](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:14)（決議與文件流程）  
   **問題：** 對外契約只列 01～03，漏掉 04，與同檔第 16 行「審閱頁 01～04」矛盾，也可能讓 agent 誤以為 04 可以搬進 issue。  
   **建議：** 把 `04_messages.md` 加入對外契約列舉。  
   **出處：** [AGENTS.md:16](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:16)、[04_messages.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:5)。

8. **位置：** [decisions/README.md:9-17](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:9)（「審閱頁（三頁）」）  
   **問題：** 標題仍稱三頁，表格也只列 01～03，與目前 01～04 的現況不符。這是內部文件中的過時資訊。  
   **建議：** 改成四頁並新增 04 的表格列。  
   **出處：** [AGENTS.md:16](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:16)、[review/README.md:26](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:26)。

9. **位置：** [decisions/README.md:45](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/README.md:45)（舊審閱頁）  
   **問題：** 寫「現在審閱頁是 01～03」。這不是歷史敘述，而是已過時的現況陳述。  
   **建議：** 改成「當時取代後是 01～03；現為 01～04」，保留歷史時間點。  
   **出處：** [AGENTS.md:21](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:21)、[review/README.md:26](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:26)。

10. **位置：** [ADR-0008:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:15)、[ADR-0008:40-42](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:40)、[ADR-0008:81](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:81)  
    **問題：** ADR 同時要求版本組合判定早於拉 image、不得連 registry，卻說啟動器靠讀「引擎 image 的 LABEL」判定。若 image 尚未在本機，文件沒有說明 LABEL 從何取得，機制不閉合。  
    **建議：** 明寫可離線取得的 LABEL／區間資料存放位置與更新時機，或限定該說法只適用於本機已有 image 的情況；不能同時留下三個無條件陳述。  
    **出處：** [02_invariants.md:322](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:322)、ADR-0008 §3。

## 建議

1. **位置：** [04_messages.md:18](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:18)（6-19）  
   **問題：** `<file>`、`<N>`、`<M>`、`<written_by>` 只統稱為占位符；第一次閱讀者無法立即判斷 N、M 各是哪個版本。  
   **建議：** 在表前或「時機」欄補一份占位符對照。  
   **出處：** [ADR-0008 §4、§6](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:46)。

2. **位置：** [04_messages.md:20](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:20)（6-36）  
   **問題：**「X 較新的引擎」語序不自然；`<P_shell>` 與 `<vY>` 又混用介面版和疑似 release 版，兩者如何比較不清楚。  
   **建議：** 將時機改成 ADR 已使用的「舊薄殼跑新 major」，並解釋兩個占位符；若 `<vY>` 不是 release 版，換成不會誤解的名稱。  
   **出處：** [ADR-0007 §7:63](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:63)、[ADR-0008 §1](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:19)。

3. **位置：** [04_messages.md:13-21](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_messages.md:13)（整張表）  
   **問題：** 表格橫向過寬，6-3、6-23 尤其難以逐欄對齊；手機和窄視窗幾乎無法閱讀。  
   **建議：** 保留已定案欄位，但考慮每個編號一個小節或定義清單；至少把長訊息正文移到表下。  
   **出處：** [review/README.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:3) 明定讀者包含第一次來看的人。

4. **位置：** [ADR-0004:45](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:45)  
   **問題：** `.tmp.<verb>.<id>.toml` 使用未定義的 `verb`；「動詞」又是 CONTEXT 明列的 Avoid 詞。  
   **建議：** 若檔名格式尚可調整，改成 `<recipe>`；若格式已固定，註明 `<verb>` 是歷史欄位名及其與 recipe 的關係。  
   **出處：** [CONTEXT.md:311-315](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:311)。

5. **位置：** [ADR-0004:21、57-70](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:21)、[ADR-0007:44-45、68-91](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:44)  
   **問題：** 原決議與 Consequences 仍出現已廢止的 `help`、`upgrade vendor_kit`，必須先讀後面的修訂才知道不再適用。雖然已標為歷史原文，順讀仍容易誤用。  
   **建議：** 在舊句旁加明顯的「已由下方修訂取代」短註與錨點；不要只靠讀者自行回套修訂。  
   **出處：** ADR-0004 的 2026-09-30 修訂、ADR-0007 的 2026-09-29／30 修訂、02 第 8 條 U2／U5。

6. **位置：** [03_interface.md:84-87](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/03_interface.md:84)  
   **問題：**「常用三個、進階七個」與上方清單視覺上出現的五行、十行不一致；實際上是按 recipe 名去重，但沒有說。  
   **建議：** 寫成「三個 recipe 名／七個 recipe 名；同一 recipe 的不同對象或參數寫法不另計」。  
   **出處：** [02_invariants.md:235-237](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:235)。

7. **位置：** [ADR-0004:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0004-vk-recipe-interface-and-write-boundary.md:3)、[ADR-0007:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:3)  
   **問題：** `Serves` 各是一個塞入多個機制、排除事項與三個回連的長句，服務對象不易掃讀。  
   **建議：** 拆成「服務哪些不變量」與「本 ADR 記錄哪些機制」兩句。  
   **出處：** [AGENTS.md:23-24](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:23) 只要求回連與文件分工，沒有要求單句。

8. **位置：** [AGENTS.md:30](/home/cyc/Desktop/vendor-kit_ws/src/AGENTS.md:30)  
   **問題：** 一個項目同時處理 main 合併、遠端 ruleset、本機 hook、CI 分工、job 名稱和 paths Pending，資訊過密。  
   **建議：** 拆成「合併規則」「防護」「CI 分工」「必過 workflow 不設 paths」四個子項。  
   **出處：** 易讀性。

9. **位置：** [review/README.md:27-40](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:27)  
   **問題：** 第 2、3 步各自包含 round 取號、驗證、備份、版本取號、輸出與刪舊版等多層規則，新接手者難以確認實際順序。  
   **建議：** 拆成 round 取號 → 跑 workflow → 跑 mark_changes → 核對三份檔 → 送審的子步驟。  
   **出處：** [review/README.md:24](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/README.md:24) 稱其為新接手 agent 應直接照做的流程。

連結檢查結果：除 ADR-0008 的裸 `6-10` 引用外，受審檔案中的 Markdown 超連結都有具名文字；所有本機目標路徑與錨點均存在。外部網址未做網路可用性驗證。除 ADR-0004 的 `<verb>` 外，找到的 Avoid 詞都位於明確標成歷史／舊名的敘述中，不另列問題。