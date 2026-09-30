## 必改

1. **位置：`docs/adr/0005-run-log-and-event-registry.md:16–17`**

   **問題：** 第 16 行把事件名定為「對外契約的一部分」，但第 17 行要求其他 ADR 引用本 ADR 與 image 裡的真本；本 ADR 沒列事件名，真正清單又只存在引擎 image。這使對外契約的實際內容不在對外契約文件中，無法走契約頁的審閱與版本差異流程。

   **建議：** 二選一寫清楚：

   - 若事件名確實是對外契約，把事件名與相容規則放進 `docs/contract/`，`log-events.txt` 只作可執行的鏡射。
   - 若它只是 VK 內部讀取端的協定，將「對外契約」改成「內部封閉協定」，並說明不承諾第三方直接解析執行紀錄。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:16–17`
   - `AGENTS.md:9–10`：對外契約與 ADR 分工
   - `AGENTS.md:17`：對外契約放在 `docs/contract/`
   - `GLOSSARY.md:243–244`：契約是 VK 對使用者的承諾

2. **位置：`docs/adr/0005-run-log-and-event-registry.md:20–21`**

   **問題：** 第 20 行說「啟動器與引擎寫紀錄前先對表」，其先行文又說真本只有一份、位於引擎 image；第 21 行隨即說啟動器開始寫紀錄時讀不到真本，只能查 `log.sh` 的內嵌子集。兩句字面互相衝突：啟動器並沒有在寫入前對「真本」查表。

   **建議：** 分開寫成「引擎對真本查表；啟動器對內嵌子集查表；release CI 驗證內嵌子集是當版真本的子集」。不要統稱兩者都「先對表」。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:3`：真本只有一份，在引擎 image
   - `docs/adr/0005-run-log-and-event-registry.md:20`
   - `docs/adr/0005-run-log-and-event-registry.md:21`

3. **位置：`docs/adr/0005-run-log-and-event-registry.md:3`**

   **問題：** 「機器可讀的輸出只有 JSONL 執行紀錄與……`vk-resolve/<P>` 文法」說得過滿。結束碼本身也是明定給呼叫端與 CI 判讀的機器介面；目前句子字面把它排除在外。

   **建議：** 收窄為「機器可讀的結構化內容」或「機器可讀的結構化 payload」，並明列結束碼仍是獨立的機器介面。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:3`
   - `docs/contract/03_messages.md:17–29`：結束碼供呼叫者與 CI 判斷
   - `docs/contract/04_interface.md:263`：CI 檢查腳本以 `0`～`3` 回報結果

## 建議

1. **位置：`docs/adr/0005-run-log-and-event-registry.md:3`**

   **問題：** 「後續檢查要看得出上一次執行做到哪裡」把執行紀錄與進度檔的責任混在一起。名詞表把執行紀錄定為事後追溯，把進度檔定為未完成狀態；ADR-0004 也由進度檔負責偵測及恢復未完成執行。

   **建議：** 分成兩句：執行紀錄供追溯與機器讀取結果；進度檔負責辨識及恢復未完成狀態。若後續檢查確實需要讀執行紀錄，應具體指出讀哪種結果，不要籠統寫「做到哪裡」。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:3`
   - `GLOSSARY.md:128–132`
   - `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:28,32–33`
   - `docs/contract/04_interface.md:218`

2. **位置：`docs/adr/0005-run-log-and-event-registry.md:7`**

   **問題：** 拒絕 `--porcelain` 的理由寫成「同一件事要改兩處」，但現行設計本來就同時產生人讀訊息與執行紀錄。真正差異應是是否承諾「同一次呼叫從 stdout 取得穩定結構化結果」，而非單純是否有兩份輸出。

   **建議：** 改用契約成本說明取捨，例如：`--porcelain` 會新增同步回傳格式、欄位相容性及 stdout 穩定性的承諾；執行紀錄已提供持久、可追溯的結構化結果，因此不再開第二個結構化介面。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:7`
   - `docs/contract/03_messages.md:31–39`：現有 stdout、stderr 與執行紀錄並存

3. **位置：`docs/adr/0005-run-log-and-event-registry.md:3,18,20–21`**

   **問題：** 第一次閱讀時，`vk-resolve/<P>`、事件註冊表、真本、內嵌清單與 `FATAL` 都沒有就地解釋；其中事件註冊表還是本 ADR 的核心概念。讀者必須自行推斷「真本」與「內嵌子集」如何互相約束。

   **建議：** 在決定段先用一句話定義註冊表及兩份表示的關係；將 `FATAL` 改為已使用的「實作錯誤並以失敗結束」，或明確定義它是內部嚴重度，而不是新的結果類別。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:3,18,20–21`
   - `GLOSSARY.md:194–201`：既有結果名詞只有需人處理、失敗、警告

4. **位置：`docs/adr/0005-run-log-and-event-registry.md:23`**

   **問題：** 一句同時塞入正常時序、唯一例外、三個檢查、失敗副作用、輸出串流、結束碼及交叉引用，過長且主從關係不易辨認。

   **建議：** 拆成三句：一般時序；前置檢查例外；例外失敗時的結果。內容本身與同輪文件一致，不需改決議。

   **證據：**

   - `docs/adr/0005-run-log-and-event-registry.md:23`
   - `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:26–27`
   - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15`
   - `docs/contract/03_messages.md:58,62–63`

連結部分未發現問題：0005 的五個連結都有名稱，目標路徑存在，錨點與引用對象相符。未使用 GLOSSARY 的 `_Avoid_` 詞。對外頁未發現「出處：」行。第 29 條離線導入與 01、04 一致；0005 沒有引入與第 26、28 條衝突的介面選項。