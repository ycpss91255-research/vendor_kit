## 必改

1. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:8`**  
   **問題：** 「`update` 不寫任何檔」不正確。每次 VK 執行仍須寫執行紀錄；`update` 的「唯讀」只代表不動進 git 的檔與進度檔。  
   **建議：** 改成「`update` 不動進 git 的檔、也不動進度檔」。  
   **證據：** `GLOSSARY.md:178-179` 定義唯讀 recipe；`docs/contract/02_invariants.md:99-102` 要求副作用前留下執行紀錄且紀錄不可關閉；`docs/adr/0005-run-log-and-event-registry.md:22-23` 亦要求 VK recipe 寫執行紀錄。

2. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:17、23`**  
   **問題：** 「CI 紅燈只有五項」及「CI 模式下一定以結束碼 `2` 結束的封閉清單」寫得像是 CI 中所有非成功結果只有這五項且一律回 `2`；但 CI 也可能遇到版本組合不合，依法必須回 `3`，亦可能遇到其他一般失敗。  
   **建議：** 明確限縮成「只有這五項是由 CI 模式本身額外升格為 `2` 的情境」；不要稱為 CI 中全部紅燈的封閉清單。  
   **證據：** `docs/contract/03_messages.md:24-28` 規定版本組合不合回 `3`，多結果取最大值；`docs/contract/03_messages.md:55、57、60` 列出在 CI 也可能發生的結束碼 `3` 情境；`docs/contract/04_interface.md:267-271` 只規定 CI 模式對進 git 寫入及本機覆寫的附加限制。

3. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:23`**  
   **問題：** 五項不是互斥項目。「需要改進 git 的檔」已涵蓋「基準版落後」及「未完成導入」所需的後續處理，因而無法穩定地說是「五項」，也無法逐項寫互斥測試。  
   **建議：** 改成有明確邊界的具體條件，或把前三項表述為「需要改進 git 的檔」的具名子類，不再宣稱五個並列條件。  
   **證據：** `docs/contract/03_messages.md:54` 的基準版落後要求本機執行 `upgrade` 後 commit；`docs/contract/03_messages.md:56` 的未完成導入要求執行 `add`；`docs/contract/04_interface.md:269-270` 把總規則寫成「進 git 的檔一律不寫／遇到非寫不可的情況回 `2`」。

4. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:28`**  
   **問題：** 殘留已從 04 刪除的對外選項 `--dry-run`。目前 04 依定案第 26 條只列必要參數，沒有定義這個選項；GLOSSARY 也沒有定義。0004 卻仍把它當成既存介面，形成跨檔不一致。  
   **建議：** 刪除「`--dry-run` 不建」；若未來決定提供，再由對外介面文件先定義後引用。  
   **證據：** `doc/decisions/review_log/discussion_queue.md:47` 定案 04 只列指令與必要參數；`docs/contract/04_interface.md:76-203` 的完整指令及選項區沒有 `--dry-run`；`GLOSSARY.md:169-204` 的執行與結果名詞也沒有它。

5. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:29`**  
   **問題：** 「不帶工具名、一次處理多個工具」與 04 現行必要參數不一致。04 只列 `upgrade <repo>`，沒有不帶 `<repo>` 的多工具 `upgrade` 或其他對應寫法。0004 因此仍依賴已刪介面。  
   **建議：** 刪除此步，或只描述不依賴已刪指令形狀的內部批次處理規則。不要在 0004 宣告 04 未提供的使用方式。  
   **證據：** `docs/contract/04_interface.md:82-99` 列出的 `add`、`upgrade`、`remove`、`dev`、`undev` 都有明確必要對象；`docs/contract/03_messages.md:26-28` 只規定「一次處理多個工具」時如何彙總結束碼，沒有定義不帶工具名的指令寫法。

6. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:29`**  
   **問題：** 「任一項不過就……以 `2` 結束」違反已定案的結束碼規則。完整預檢可能發現版本組合不合，該結果必須是 `3`；多結果也必須取最大值，不能一律壓成 `2`。  
   **建議：** 改成「依各原因的結束碼彙總並取最大值」；若此句只指特定類型的預檢失敗，須明列範圍。  
   **證據：** `docs/contract/03_messages.md:21-28` 定義 `0`～`3` 並規定多結果取最大值；`docs/contract/02_invariants.md:92-95` 規定版本組合不合是獨立結果且多工具取最需處理者；`doc/decisions/review_log/discussion_queue.md:35` 明確定案沒有特例、取數字最大值。

7. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:33`**  
   **問題：** 「`gen/tools.just` 與 `cache/` 在同一個 apply 內原子替換」沒有成立的機制說明。兩者是不同目錄；「同一個 apply」不等於能把兩個路徑作為一個原子交易替換，後一句「多一層暫存目錄與替換步驟」也不能證明外部永遠看不到一新一舊。這正是本 ADR 第 10 行拒絕的狀態。  
   **建議：** 不要宣稱跨兩個路徑「原子替換」；改寫成實際可保證的可觀察性與恢復條件，或明確指出共同原子切換點。  
   **證據：** `GLOSSARY.md:108-113` 將 `cache/` 與 `gen/` 定義為不同目錄；本檔 `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:10` 自己指出兩次寫入之間中斷會留下不一致。

## 建議

1. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:3`**  
   **問題：** 整段由四個因果鏈串成一個超長句；第一次閱讀很難分辨哪些是背景、決定及理由。「多工具、逐檔合併都會在中途失敗」也寫成必然發生，語意過強。  
   **建議：** 拆成三至四句，並把「都會」改成「都可能」。  
   **證據：** `docs/contract/02_invariants.md:97-106` 討論的是操作「可能」中途失敗及其恢復要求，並非每次必然失敗。

2. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:9、23`**  
   **問題：** 「這個版本你拒絕過」不是 GLOSSARY 定義的名詞，也沒有對應目前 03 的訊息項目；讀者無法知道「拒絕」是拒絕詢問、拒絕合併，還是略過某個新版。  
   **建議：** 換成已有定義的狀態名稱，或刪除這個例子。  
   **證據：** `GLOSSARY.md:134-168` 的版本、來源及合併名詞沒有「拒絕過的版本」；`docs/contract/03_messages.md:50-64` 現有訊息表也沒有此狀態。

3. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:28、33`**  
   **問題：** `.tmp.<verb>.<id>.toml`、`apply` 都是未說明的內部術語。首次閱讀者不知道 `<verb>` 對應 VK recipe 還是引擎內部動作，也不知道 `apply` 是階段、程序或命令。  
   **建議：** 使用既有的「recipe」用語，並用一句話界定 `apply`；若只是暫定實作名稱，移到實作 issue。  
   **證據：** `GLOSSARY.md:169-179` 定義的是 VK recipe、可寫 recipe、唯讀 recipe，沒有 `verb` 或 `apply`；本檔 `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:20` 又說內部機制之後要搬到實作 issue。

4. **位置：`docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19`**  
   **問題：** 「需要寫進 git 的情境各有固定訊息編號」是全稱，但後面只列三種；本檔第 23 行的五項中，本機覆寫與泛稱的「需要改進 git 的檔」沒有在這裡對上固定編號。  
   **建議：** 改成「下列三種已有固定訊息編號」，或補齊實際對應；不要用「各有」暗示完整覆蓋。  
   **證據：** 本檔 `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:19、23`；`docs/contract/03_messages.md:50-64` 的現有編號表。