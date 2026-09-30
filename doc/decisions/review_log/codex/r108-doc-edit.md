## 必改

1. **位置：`doc/decisions/review/03_messages.md:43,45,49,54`**
   - **問題：** 6-4、6-10、6-28、6-41 宣稱「未修改任何檔」或「不動任何檔」，但每次執行都必須先寫執行紀錄。6-10 又是版本組合不合，02 已明定唯一寫入例外就是執行紀錄。這些訊息逐字內容會對使用者說錯話。
   - **建議：** 統一改成「除執行紀錄外，未修改任何 repo 檔或其他 VK 檔」，或使用同樣精確、不否認執行紀錄的說法。
   - **證據：** `doc/decisions/review/02_invariants.md:94,99,102`；`doc/adr/0005-run-log-and-event-registry.md:11,46-47`。

2. **位置：`doc/decisions/review/04_interface.md:167-170`（`--dry-run`）**
   - **問題：** 同一組清單先說「不寫 VK 檔」，下一項又說執行紀錄照寫；執行紀錄在名詞表中明確是 VK 檔，兩句直接矛盾。
   - **建議：** 改成「除執行紀錄外，不寫 repo 檔與其他 VK 檔」。
   - **證據：** `CONTEXT.md:100-101,127-128`；`doc/decisions/review/02_invariants.md:99,102`。

3. **位置：`doc/decisions/review/04_interface.md:203-204`（「使用者的檔與 VK 的檔」）**
   - **問題：** 第 203 行說使用者可以改的進 git VK 檔「只有」`config.toml`，下一行立即說使用者也可以手改版本鎖定行。讀者無法判斷「可以改」是在說所有權、受保護範圍，還是實際允許操作。
   - **建議：** 把兩種情況拆開：`config.toml` 是「交由使用者維護、受合併保護」；版本鎖定行是「由 VK 擁有，但允許使用者按正規形手改」。不要用「只有」把兩者混成同一分類。
   - **證據：** `doc/decisions/review/02_invariants.md:34-39`；`CONTEXT.md:92-104,135-139`；`doc/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md`「工具行的正規形」。

4. **位置：`doc/adr/0008-protocol-and-file-schema-versions.md:15,38-44,84,89`**
   - **問題：** ADR 說版本組合不合能在拉 image、連 registry、起容器前判定，方法卻是讀引擎 image 的 LABEL。本機還沒有該 image 時，LABEL 無從讀取；目前的版本鎖定行只記 image 引用，沒有接受的介面版區間。機制不閉合。
   - **建議：** ADR 必須補上離線可取得且可驗證的判定資料及其擁有者；在此之前，不應聲稱「讀 LABEL 就夠」。這是補齊既定承諾的機制，不是縮小 CI 或離線承諾。
   - **證據：** `doc/decisions/review/02_invariants.md:180,190`；`CONTEXT.md:78-85,135-139,229-236`；`doc/decisions/review_log/discussion_queue.md:118-124` 已記錄同一缺口，尚未定案。

5. **位置：`doc/adr/0008-protocol-and-file-schema-versions.md:53-64,81-84`**
   - **問題：** 第 57 行以「忽略並保留未知欄位」推導「舊引擎讀新檔不會失敗」，但第 62 行又規定檔案版較高就拒絕。修訂雖說新欄位要先讓舊引擎讀得過，仍沒說清楚何時增加 `schema`、舊引擎如何接受尚未存在的新版號。現有文字無法證成 02 的同一 X 向後可讀承諾。
   - **建議：** 明寫新增欄位與提升 `schema` 各自的觸發條件，以及如何保證同一 X 的舊引擎不因新版 `schema` 被拒絕。
   - **證據：** `doc/decisions/review/02_invariants.md:182-190`；`CONTEXT.md:235-236`。

6. **位置：`doc/decisions/review/03_messages.md:34` 與 `:20-23`**
   - **問題：** 第 34 行說類別採名詞表的「三種結果」，但名詞表定義的是需人處理、失敗、警告；表內另有「成功」「做完了但要人接手」「版本組合不合」，後兩者沒有名詞定義。02 又把它們列為獨立結果類別。
   - **建議：** 在 `CONTEXT.md` 補齊所有正式結果類別，或改寫第 34 行，明確說「類別欄只使用哪三種訊息分類」，不要稱它們為完整的結果分類。
   - **證據：** `CONTEXT.md:193-203`；`doc/decisions/review/02_invariants.md:92`。

7. **位置：`doc/decisions/review/03_messages.md:48,52-53`；`doc/adr/0007-host-thin-layer-and-shell-integrity.md:23-26,100`**
   - **問題：** just、Docker、Podman 的檢查宣稱在「任何寫入之前」結束；若檢查失敗便不可能先建立執行紀錄，與「執行紀錄不可關閉；只有建不出紀錄才可沒有紀錄」衝突。ADR-0004 允許無副作用前置檢查排在紀錄之前，但沒有授權失敗後直接結束而不留紀錄。
   - **建議：** 明定這些 bootstrap／主機前置失敗是否屬執行紀錄契約。若屬於，改成建立紀錄後再結束；若確實無法記錄，必須在 02 或 ADR 明列例外，不能由各訊息自行暗示。
   - **證據：** `doc/decisions/review/02_invariants.md:99-104`；`doc/adr/0004-vk-recipe-interface-and-write-boundary.md:71-73`；`doc/adr/0005-run-log-and-event-registry.md:46-47`。

## 建議

1. **位置：`doc/decisions/review/04_interface.md:207-231`**
   - **問題：** 「append 型初始檔」是會影響導入、詢問、納管與移除的正式分類，但 `CONTEXT.md` 沒有定義；第一次看到的人也不知道它與一般初始檔的判別方式。
   - **建議：** 在名詞表定義「append 型初始檔」，至少說明它是把工具提供的行加入既有 repo 檔、而非整份建立或合併的初始檔類型。
   - **證據：** `CONTEXT.md:147-166` 只有初始檔、納管、metadata、基準版與合併相關名詞。

2. **位置：`doc/adr/0008-protocol-and-file-schema-versions.md:25-36`**
   - **問題：** 「新增記錄種類」「新增欄位」沒有說是哪個介面的記錄或欄位。若指 TOML 欄位，應由檔案版處理；若指薄殼—引擎協定，才是介面版 P 的觸發條件。
   - **建議：** 分別寫成具體介面，例如「`vk-resolve/<P>` 新增記錄種類／欄位」，避免跟 TOML schema 混淆。
   - **證據：** `CONTEXT.md:229-236` 將介面版與檔案版分成兩種不同用途。

3. **位置：`doc/decisions/review/03_messages.md:42`（訊息 6-3）**
   - **問題：** 單列同時塞入三個 recipe、認證條件、環境變數、docker 認證差異及兩組下一步，第一次閱讀很難確認各分支究竟印什麼。
   - **建議：** 保留同一編號，但把「時機」與「下一步」拆成 `add`、`update/upgrade` 兩個條列，或將共同訊息與依指令替換部分分行。
   - **證據：** `doc/decisions/review/03_messages.md:36-37` 已要求多行訊息明確標示每一行。

4. **位置：`doc/adr/0008-protocol-and-file-schema-versions.md:1-3`**
   - **問題：** 標題和 `Serves` 一句同時引入 P、schema、區間、LABEL、欄位、遷移與零寫入，資訊密度過高；讀者尚未讀 Decision 就得先理解全部機制。
   - **建議：** `Serves` 只保留服務哪條不變量及本 ADR 的核心決議，其餘交給 Decision 小節目錄。
   - **證據：** `doc/decisions/review/02_invariants.md:178-198` 已提供這份 ADR 所服務的完整性質。

5. **位置：`doc/decisions/review/04_interface.md:114-118`（執行位置）**
   - **問題：** 「每次執行作用於一個明確安裝目錄」被解讀成「只能在安裝目錄執行」，但兩者不是同一件事；目前引用的第 2 條不足以單獨證明工作目錄限制。
   - **建議：** 若限制已定案，將句子寫成介面規則本身，不要暗示它是第 2 條的直接同義重述；或補一句它如何確保安裝目錄唯一且明確。
   - **證據：** `doc/decisions/review/02_invariants.md:59-64`。

6. **位置：全部受審檔案的連結與對外頁 HTML／出處規則**
   - **問題：** 未發現實際壞連結、錯錨點、裸路徑充當連結文字、`_Avoid_` 詞殘留，或對外頁的「出處：」行。`doc/decisions/review/README.md:19` 的 ``[頁名](連結#錨點)`` 是行內程式碼範例，不是壞連結。
   - **建議：** 無須修改。現有 `check_review_pages.py` 會誤把行內程式碼中的示例當連結；若將來擴大它的掃描範圍，應先排除行內程式碼。
   - **證據：** `script/check_review_pages.py:23,79-100`；本次 `check_review_pages.py`、`check_context.py`、`check_terms.py` 均通過其既定掃描範圍。