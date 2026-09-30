## 必改

1. **位置：`doc/decisions/review/02_invariants.md:70`、`doc/decisions/review/04_interface.md:48-55`**

   - **問題：** registry 承諾範圍互相衝突。02 無條件承諾「主機拉得到的 image，VK 就用得了」；04 卻說非 GHCR 即使主機拉得到，出問題也不在承諾內。
   - **建議：** 二選一統一：
     - 若契約真的是 registry-neutral，刪掉 04 的「出問題不在承諾內」。
     - 若只承諾 GHCR，02 必須把承諾縮成 GHCR；但這會改動不變量，不能只在 04 偷縮。
   - **證據：** `doc/decisions/review/02_invariants.md:70`；`doc/decisions/review/04_interface.md:50-55`。

2. **位置：`doc/adr/0010-dev-self-and-acceptance.md:27`、`doc/adr/0009-release-assets-and-offline-import.md:49`**

   - **問題：** fixture 永不刪雖然從舊 02 搬到了 ADR-0009，但 ADR-0010 仍說 fixture 屬於「不變量 2 那批永不刪的資產」。現行第 2 條只要求版本鎖定行指到的東西一直取得到；fixture 不由版本鎖定行指向，不能由第 2 條推出。
   - **建議：** ADR-0010 改成直接引用 ADR-0009 的 2026-09-30 修訂，或另找真正要求 fixture 永久保存的上位承諾；不要再寫成第 2 條的直接結論。
   - **證據：** `doc/decisions/review/02_invariants.md:66`；`doc/adr/0009-release-assets-and-offline-import.md:45-49`；`doc/adr/0010-dev-self-and-acceptance.md:25-27`。

3. **位置：`doc/decisions/review/04_interface.md:63`**

   - **問題：** 「下載 bootstrap.sh」是具名超連結，但目標目前回 HTTP 404，不符合「目標存在」。同頁第 67 行雖誠實說明尚未發布，仍不能讓第 63 行的下載連結成立。
   - **建議：** 發布前改連到存在的 release 頁，或先以非連結文字列出預定網址；資產發布後再換回直接下載連結。
   - **證據：** `doc/decisions/review/04_interface.md:63-67`；實際請求 `https://github.com/ycpss91255-research/vendor_kit/releases/latest/download/bootstrap.sh` 回 404。

4. **位置：`doc/adr/0005-run-log-and-event-registry.md:64`、`doc/adr/0008-protocol-and-file-schema-versions.md:99`、`doc/adr/0012-deterministic-behavior-and-escaping.md:51`**

   - **問題：** 三處直接使用 `P5`，但 `CONTEXT.md` 沒有定義；第一次讀 ADR 的人也不知道它指什麼。實際定義在另一份未連結的設計原則文件。
   - **建議：** 寫成具名連結，例如「[P5：一條規則一個擁有者](../decisions/design_principles.md#p5-一條規則一個擁有者)」。
   - **證據：** `doc/decisions/design_principles.md:30`；上述三個 ADR 行號；`CONTEXT.md` 無 `P5` 條目。

## 建議

1. **位置：`doc/decisions/review/02_invariants.md:92-109`**

   - **問題：** 第 4 條仍保留大量機制：副作用與執行紀錄的先後、進度檔建立時點、多工具預檢、鎖定行最後寫、恢復順序、升引擎例外。這與頁首「只寫概念，不寫實現方式」的界線不一致。雖然沒有具體選項、檔名或訊息編號，但內容仍是執行時序。
   - **建議：** 02 只保留可觀察性質，例如「任何副作用之前必須留下可追溯紀錄」「未完成狀態必須可恢復且可辨識」；精確順序只留在 ADR-0004、0005、0007。
   - **證據：** `doc/decisions/review/02_invariants.md:3,92-109`；`doc/adr/0004-vk-recipe-interface-and-write-boundary.md:69-80`；`doc/adr/0005-run-log-and-event-registry.md:43-47`；`doc/adr/0007-host-thin-layer-and-shell-integrity.md:87-96`。

2. **位置：`doc/decisions/review/02_invariants.md:157-179`**

   - **問題：** 第 8 條已拿掉 U 編號，但並非直觀的「三句概念」：先有命名空間規則，再有三條寫法規則，再有三條語意規則及兩段理由。讀者很難判斷所謂三句究竟是哪三句。
   - **建議：** 明確收斂成三個並列概念：「介面不可取代」「同一概念同一寫法」「既有語意固定」；成對、查／套用、無害等具體規則移到 04 或 ADR-0004。
   - **證據：** `doc/decisions/review/02_invariants.md:157-179`；具體介面已列於 `doc/decisions/review/04_interface.md:119-154`。

3. **位置：`doc/decisions/review/04_interface.md:48-55`**

   - **問題：** 這一節整體寫成「依第 2 條」，但第 2 條只直接支持認證由主機／CI 處理及「主機拉得到就能用」；引擎公開、工具可私有、token 變數、版本列舉失敗處置、只測 GHCR，都不是第 2 條的文字結論。
   - **建議：** 把「依第 2 條」縮到真正受其約束的句子；其餘標成介面契約本身，不要讓讀者以為每項都能在第 2 條找到。
   - **證據：** `doc/decisions/review/02_invariants.md:55-74`；`doc/decisions/review/04_interface.md:46-55`。

4. **位置：`doc/decisions/review/04_interface.md:202-210`**

   - **問題：** `.vendor_kit/config.toml` 被稱作「VK 的設定檔」並「比照初始檔」，但 `CONTEXT.md` 沒有定義這個檔；初始檔的現行定義又限定為工具提供、導入 repo 後交給使用者的 repo 檔。兩者分類關係第一次看不清楚。
   - **建議：** 在 `CONTEXT.md` 補正式名詞，或在 04 明說它「不是初始檔，只沿用初始檔的保護與合併規則」。
   - **證據：** `doc/decisions/review/04_interface.md:202,210`；`CONTEXT.md:216-223,284-302`。

5. **位置：`doc/decisions/review/04_interface.md:158-165`**

   - **問題：** 「`-y`：免問」與「不把 append 型的行硬插進去」需要讀者自行推斷「硬插」指未納管既有檔，而不是所有 append。後面的第 217 行又說已有檔「問過才 append」，容易讓人誤讀成 `-y` 對 append 無效。
   - **建議：** 明寫判準，例如「`-y` 可代替原本允許的詢問，但不能把已存在、尚未納管的檔改成 append 納管」。
   - **證據：** `doc/decisions/review/02_invariants.md:44-49`；`doc/decisions/review/04_interface.md:158-165,214-218`。

6. **位置：`doc/adr/0009-release-assets-and-offline-import.md:28,41,59`、`doc/adr/0010-dev-self-and-acceptance.md:3,19,41-43,57,64`**

   - **問題：** 正文與 Consequences 大量保留舊指令，再要求讀者依後面的修訂「一律讀作」新指令。內容在決議歷史上可追，但現行規則難讀，搜尋也會同時找到有效與無效寫法。
   - **建議：** 歷史段保留舊寫法；現行 Consequences、驗收敘述與檔頭改用現行寫法。至少 ADR-0009:59 應直接寫 `add <repo> -i <image>`，ADR-0010:64 應直接寫 `dev --engine -i`。
   - **證據：** `doc/decisions/review/04_interface.md:83-85,183-191`；上述 ADR 行號。

7. **位置：`doc/decisions/review/03_messages.md:43`**

   - **問題：** 同一列混用正式名詞「警告」與英文 `warn`；第一次讀的人會懷疑這是另一種結果類別。
   - **建議：** 改成「本機只印警告、結束碼 `0`」。
   - **證據：** `doc/decisions/review/03_messages.md:34-35,43`；`CONTEXT.md:349-351`。

8. **位置：題目列出的 ADR 路徑**

   - **問題：** 題目中的 0002、0003、0006、0011、0012 檔名在工作樹不存在；現存的是同編號但不同名稱的檔。若別處仍使用題目中的舊路徑，會是斷鏈。
   - **建議：** 後續審閱清單以現存正式檔名為準。
   - **證據：**
     - `doc/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md`
     - `doc/adr/0003-baseline-merge-and-line-records.md`
     - `doc/adr/0006-tool-image-as-data-only.md`
     - `doc/adr/0011-test-layers-and-ci-matrix.md`
     - `doc/adr/0012-deterministic-behavior-and-escaping.md`

逐條比對舊 02 後，未發現整段承諾完全消失：具體內容均可在 03、04 或相應 ADR 找到；fixture 永不刪是唯一「文字已搬到、但上位依據沒有一起成立」的情形。現有本地 Markdown 連結路徑與已引用錨點均通過；對外頁沒有「出處：」行；`_Avoid_` 自動檢查亦通過。