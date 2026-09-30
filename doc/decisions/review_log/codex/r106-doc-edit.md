## 必改

1. **位置：`doc/decisions/review/02_invariants.md:55–208` 多數條目**

   - **問題：** 02 仍大量記載具體檔名、指令行為、資料格式、執行順序與實作判準，沒有落實「只寫概念」。例如 `version.toml`、CI 模式、本機覆寫、結束碼分類、執行紀錄、薄殼比對、`X.Y.Z` 欄位演進規則，都已超出不變量的概念層。
   - **建議：** 每條只保留可長期黑箱驗證的性質；檔名、選項、格式、演算法、時序及錯誤碼移到 03、04 或對應 ADR。不要趁移動內容改變承諾範圍。
   - **證據：** `doc/decisions/review/02_invariants.md:3` 自稱「只寫概念，不寫實現方式」；`doc/decisions/review_log/discussion_queue.md:21–22,94–96` 已定案要求逐條重審並移除實際做法。現存例子見 `02_invariants.md:59–70,80–82,92–104,114,126–132,170–172,182–194`。

2. **位置：`doc/decisions/review/02_invariants.md:150–164`，第 8 條**

   - **問題：** 沒有照已定案內容只留下指定的三個概念。現在第三點是「既有 recipe 的語意固定」，但定案第三句是「各命名空間操作方式一致」；後者反而被塞進第二點。標題與「一句話」也繼續加入 recipe 語意固定。
   - **建議：** 第 8 條概念明確拆成三句：每個介面不可取代；一個概念一種寫法；各命名空間操作方式一致。recipe 相容性若仍需承諾，應由第 10 條承接，不要暗中保留成第 8 條第四個概念。
   - **證據：** `doc/decisions/review_log/discussion_queue.md:22` 明定「只留三句概念」及三句的內容；現文見 `doc/decisions/review/02_invariants.md:150–158`。

3. **位置：`doc/decisions/review/02_invariants.md:70`；`doc/decisions/review/04_interface.md:48–54`**

   - **問題：** registry 承諾互相衝突。02 無條件承諾「主機拉得到的 image，VK 就用得了」；04 又說只有 GHCR 在承諾內，其他 registry 出問題不在承諾內。這不是措辭差異，而是承諾範圍不同。
   - **建議：** 維持 Q10 待維護者決定，不要自行選邊；送審前必須取得決議並讓兩頁一致。
   - **證據：** `doc/decisions/review/02_invariants.md:70`；`doc/decisions/review/04_interface.md:48,54`；衝突已登記於 `doc/decisions/review_log/discussion_queue.md:86–90`。

4. **位置：`doc/decisions/review/03_messages.md:42`，訊息 6-3**

   - **問題：** 時機包含 `add`，但唯一可複製的替代路徑是 `upgrade <repo>@<tag>`。在尚未加入工具時，`upgrade` 不是 `add` 的替代操作。
   - **建議：** 等維護者決定是否存在 `add <repo>@<tag>` 或其他既定寫法，再讓訊息依觸發動作提供可執行的下一步；不要自行擴充介面。
   - **證據：** `doc/decisions/review/03_messages.md:42` 同一列同時寫 `add` 與 `upgrade`；此缺口已記於 `doc/decisions/review_log/discussion_queue.md:70–74`。

5. **位置：`doc/decisions/review/03_messages.md:44`，訊息 6-10**

   - **問題：** 同一訊息同時涵蓋工具與引擎降版，正文卻一律稱「目標引擎」。工具降版時，使用者指定的是工具版本，不是目標引擎，訊息會誤報對象。
   - **建議：** 在 Q9 定案前不要把這列視為可送審定稿；應由維護者決定拆訊息或改成對兩種對象都成立的文字。
   - **證據：** `doc/decisions/review/03_messages.md:44`；`doc/adr/0008-protocol-and-file-schema-versions.md:66–70` 讓兩類降版共用該訊息；問題已登記於 `discussion_queue.md:81–84`。

6. **位置：`doc/decisions/review/03_messages.md:3–5,40–49`**

   - **問題：** 對外頁自稱「列出每個結束碼」以及「VK 會印出、要使用者動手處理的訊息」，但只列八條並明說尚未列齊。缺少 Docker 版本不足、薄殼被修改、非互動且未帶 `-y`、metadata 無法還原、執行紀錄建不出來等已承諾的固定情況。
   - **建議：** 標示版送審前補齊已由 02／ADR 定義的訊息；尚未定案的編號或文字不要自行發明，先留在討論佇列。
   - **證據：** 缺項清單見 `doc/decisions/review_log/discussion_queue.md:76–79`；相關承諾見 `02_invariants.md:41,49,102`、`doc/adr/0007-host-thin-layer-and-shell-integrity.md:23–24,37`。

7. **位置：`doc/decisions/review/04_interface.md:58`，「入口」**

   - **問題：** 「VK 對外只有三個入口」被寫成「依 02 第 9 條」，但第 9 條沒有規定入口數量；它規定公開入口可黑箱驗證，以及開發自身與驗收使用同一種引擎指定機制。條號和錨點本身有效，語意引用不成立。
   - **建議：** 不要用第 9 條替「恰好三個」背書；入口清單直接作為介面頁定義，若「只有三個」是難逆轉決議，再連到真正擁有該決定的 ADR。
   - **證據：** `doc/decisions/review/04_interface.md:58–72`；`doc/decisions/review/02_invariants.md:166–176`。

8. **位置：`doc/decisions/review/04_interface.md:151–164`，「共同選項」**

   - **問題：** 說「哪個指令接受哪個選項，實作時再定」，但 03 已要求 `upgrade <repo> -y` 是可直接複製的契約訊息，因此至少 `upgrade` 接受 `-y` 已經被其他對外頁依賴，不能再留給實作時決定。
   - **建議：** 列出已被 03、02 或 ADR 依賴的指令—選項組合；其餘是否延後另說。
   - **證據：** `doc/decisions/review/04_interface.md:153`；`doc/decisions/review/03_messages.md:43`；同一問題已記於 `discussion_queue.md:39–43`。

9. **位置：`doc/decisions/review/04_interface.md:235`**

   - **問題：** 連結文字不是頁面的實際標題；寫成「01 目的與承諾」，實際標題是「01 專案目的與承諾」。
   - **建議：** 改用完整實際頁名；若是在引用規則，依既定格式補成「依 [01 專案目的與承諾](...)……」。
   - **證據：** `doc/decisions/review/04_interface.md:235`；`doc/decisions/review/01_purpose.md:1`；頁名規則見 `discussion_queue.md:24`。

10. **位置：`doc/adr/README.md:54–56`，「待拍板」**

    - **問題：** 清單已過時，仍把 `version.toml`、just 最低版本、多命名空間等已寫入現行對外頁或 Accepted ADR 的事項列為待拍板。內部索引因此同時給出「已接受」與「尚待決定」兩種狀態。
    - **建議：** 逐項對照現行決議移除已定案項；只保留真的尚待維護者決定者，例如 registry 範圍 Q10。若某項仍有另一個未決面向，應精確寫出那個面向。
    - **證據：** `doc/adr/README.md:56`；`CONTEXT.md:211–214` 已定義 `version.toml`；`doc/adr/0007-host-thin-layer-and-shell-integrity.md:21–26` 已接受 just 下限；`doc/adr/0004-vk-recipe-interface-and-write-boundary.md:79` 已接受多命名空間形狀。

11. **位置：`doc/adr/0009-release-assets-and-offline-import.md:58`；`doc/adr/0011-test-layers-and-ci-matrix.md:35–39,67`**

    - **問題：** 0011 的 Decision 已定工具 image 為 amd64＋arm64 多架構，但 0009 與 0011 Alternatives 又說「dist image 單架構 amd64」仍待拍板。Accepted 決議內部互相打架。
    - **建議：** 先確認真正有效的決議狀態；若多架構已定案，刪除待拍板敘述；若仍未定案，0011 不應把多架構寫成 Accepted Decision。
    - **證據：** `doc/adr/0011-test-layers-and-ci-matrix.md:5,35–39,67`；`doc/adr/0009-release-assets-and-offline-import.md:58`。

12. **位置：`doc/adr/0004-vk-recipe-interface-and-write-boundary.md:84`**

    - **問題：** Consequences 仍說使用者要記 recipe 名「加上 `help`」，但同檔修訂已拿掉 `help` recipe。這不是清楚標示的歷史段落，而是仍呈現為現行後果。
    - **建議：** 把 Consequences 改成現行 `-h`／`--help` 與無指令時印用法的結果，或明確將舊句標為歷史且不適用。
    - **證據：** `doc/adr/0004-vk-recipe-interface-and-write-boundary.md:57–65,82–85`；現行介面見 `doc/decisions/review/04_interface.md:126–138`。

13. **位置：`doc/adr/0004-vk-recipe-interface-and-write-boundary.md:89`**

    - **問題：** 說三個「需要寫進 git」情境各有固定訊息編號，但目前 03 只列了基準版落後 6-5、未完成導入 6-13；薄殼不符沒有列入總表。
    - **建議：** 補齊第三個固定訊息，或把 ADR 改成不宣稱已具備三個編號；編號需依既定決議流程定案。
    - **證據：** `doc/adr/0004-vk-recipe-interface-and-write-boundary.md:27–28,33–38,89`；`doc/decisions/review/03_messages.md:40–49`。

14. **位置：多份 ADR 的 Consequences**

    - **問題：** 保留了已完成的「需要同步更新」待辦，讀者會誤以為 02 尚未更新。
    - **建議：** 改為歷史敘述「已同步更新」，或移除；內部文件不得留過時操作指示。
    - **證據：**
      - `doc/adr/0005-run-log-and-event-registry.md:57` 對照 `doc/decisions/review/02_invariants.md:108`
      - `doc/adr/0007-host-thin-layer-and-shell-integrity.md:105` 對照 `02_invariants.md:120,136,198`
      - `doc/adr/0012-deterministic-behavior-and-escaping.md:46` 對照 `02_invariants.md:208`

15. **位置：`doc/adr/0011-test-layers-and-ci-matrix.md:35–39`；`doc/adr/0009-release-assets-and-offline-import.md:19–24`**

    - **問題：** 「工具 image 兩平台位元組一致」與「每平台各一份 image tar、旁檔記多架構 index digest」之間的比較對象不清楚。不同架構的 OCI image tar 通常含不同 manifest/config；「兩平台位元組一致」若指整個 image，不符合 0009 的每平台資產形狀；若只指 `dist/` 內容，現文說得太寬。
    - **建議：** 明確寫成驗證工具 image 內展開的交付資料逐檔位元組一致，或明列真正比較的層級，避免被理解為兩份 image tar 本身相同。
    - **證據：** `doc/adr/0011-test-layers-and-ci-matrix.md:35–39`；`doc/adr/0009-release-assets-and-offline-import.md:19–24`；01 的承諾只要求搬運內容不變，見 `doc/decisions/review/01_purpose.md:25–28,36`。

## 建議

1. **位置：`doc/decisions/review/02_invariants.md:92`**

   - **問題：** 「成功、失敗或需人處理、完成但要人接手、版本組合不合」混用已定義名詞與未定義描述；「完成但要人接手」在 `CONTEXT.md` 沒有條目。
   - **建議：** 若它是正式結果類別，補入名詞表；否則直接寫結束碼 `2` 對應的兩種情況，並把細節留在 03。
   - **證據：** `doc/decisions/review/02_invariants.md:92`；既有結果名詞見 `CONTEXT.md:341–355`。

2. **位置：`doc/decisions/review/03_messages.md:40–49`**

   - **問題：** 表格單列過長，尤其 6-3、6-10、6-23；第一次閱讀時很難同時分辨觸發條件、逐字訊息、占位符和下一步。
   - **建議：** 每個訊息改成獨立小節，或至少把「時機／逐字訊息／下一步」分成多行；保留固定錨點。
   - **證據：** `doc/decisions/review/03_messages.md:42–49`。

3. **位置：`doc/decisions/review/04_interface.md:197–224`**

   - **問題：** 「使用者的檔」「VK 擁有但進 git 的檔」「append 型初始檔」「可收回的行」連續混在同一節，初讀者不容易看出分類與處置的對應關係。
   - **建議：** 用小表格列「對象／擁有者／可否建立／修改前是否詢問／移除時行為」，再把例外放表後。
   - **證據：** `doc/decisions/review/04_interface.md:194–229`；分類來源見 `CONTEXT.md:216–262`。

4. **位置：`doc/decisions/review/04_interface.md:153`**

   - **問題：** 一句同時包含適用範圍、非承諾聲明及延後決定，讀起來繞，而且「實作時再定」容易被理解為實作者可自行改契約。
   - **建議：** 拆成「本節只定義語意」與「接受這些選項的指令清單」兩段；未定部分明寫「尚未定案」，不要寫成實作自由。
   - **證據：** `doc/decisions/review/04_interface.md:151–164`。

5. **位置：所有受審檔案的連結**

   - **問題：** 沒發現裸 URL、空白連結文字或不存在的本機目標；`script/check_review_pages.py` 也通過。但 ADR 索引大量只寫 `ADR-000N` 或反引號路徑，並非可直接點擊，降低查閱效率。
   - **建議：** 不必把每個一般檔名都做成連結；但「建立或服務它的 ADR」及 ADR 索引表中的 ADR 名稱應優先做成有名稱的超連結。
   - **證據：** 例如 `doc/decisions/review/02_invariants.md:53,74,108`、`doc/adr/README.md:41–52`；現有正確格式可參考 `doc/adr/0004-vk-recipe-interface-and-write-boundary.md:3`。

6. **位置：對外頁 `02_invariants.md`、`03_messages.md`、`04_interface.md`**

   - **問題：** 沒有找到「出處：」行，這一項符合已定案規則。
   - **建議：** 維持現狀；ADR 內的「出處」不受「對外頁禁止」規則限制。
   - **證據：** 對外頁搜尋無命中；ADR 中的歷史來源例見 `doc/adr/0007-host-thin-layer-and-shell-integrity.md:72,84`。