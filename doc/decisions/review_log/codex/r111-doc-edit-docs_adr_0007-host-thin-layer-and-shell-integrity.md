## 必改

1. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:15,22`**

   - **問題：** 宣稱已安裝目錄也能由啟動器檢查 just 版本，但日常入口本身就是 `just vendor_kit …`。若 just 太舊，可能在解析 `vendor.just` 時就失敗，啟動器根本沒有執行機會。03 也把訊息 6-23 的觸發情境限定為 `bootstrap.sh`，與 0007 的「首次導入或已有安裝目錄都一樣」直接不一致。
   - **建議：** 刪除「已有安裝目錄也一樣」及「just 下限都由主機側檢出」的保證，或補出一個不依賴 just、能在日常入口之前執行的機制。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:15,22`
     - `docs/contract/03_messages.md:58`
     - `docs/contract/04_interface.md:69-71`
     - `docs/contract/04_interface.md:93-99`

2. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:16,26`**

   - **問題：** 把「薄殼被手改」與「未被修改、只是跟目前引擎模板不同」合併成同一個結束碼 `2`，但 03 的訊息 6-28 只定義「薄殼被修改」，並要求使用者「手動還原」。舊薄殼配新引擎並不等於被使用者修改，手動還原也不能修復版本不一致。
   - **建議：** 分開兩種狀態及處置；至少不要讓合法的舊薄殼套用 6-28。若版本不一致由 `upgrade --engine` 重產，應明寫它走另一個判定／訊息。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:16,26-27`
     - `docs/contract/03_messages.md:59`
     - `docs/contract/02_invariants.md:130-132`

3. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:28`**

   - **問題：** 第一段升級在已改版本鎖定行後，以 `2` 停下並要求使用者重跑；這是明確的「需人處理」訊息，但 03 的訊息總表沒有對應項目。0007 因而新增了一個沒有固定編號、沒有逐字訊息、沒有可直接複製下一步的對外情境。
   - **建議：** 讓 0007 引用 03 中專門對應兩段式升級的訊息；若 03 尚無該訊息，先補入總表再引用。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:28`
     - `docs/contract/03_messages.md:5`
     - `docs/contract/03_messages.md:43-48`
     - `docs/contract/02_invariants.md:104`

4. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:22`**

   - **問題：** 「下限數字會隨時間提高」沒有說只能跨 X。若在同一個 X 提高 Docker 或 just 下限，原本可用的主機會失去既有用法，違反同一個 X 內不破壞的承諾。這不只關係不變量 5。
   - **建議：** 明定提高主機版本下限屬不相容變動，只能隨 X 變動，並須事前公告及提供手動步驟。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:22`
     - `docs/contract/01_purpose.md:89-90`
     - `docs/contract/02_invariants.md:180-186`

5. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:26`**

   - **問題：** 所述機制無法完整支持「薄殼被改過必須能被發現並停下」。驗證器也是薄殼的一部分：`entry.just`、`vendor.just` 或啟動器片段若被改成不啟動引擎，便不會執行引擎的重算與模板比對。自描述標頭只能發現仍願意走驗證流程的修改，不能保證任何薄殼修改都被發現。
   - **建議：** 明確界定此保證只涵蓋「入口與驗證流程仍被執行」的非對抗性損壞；若不變量仍要求無條件發現，則必須指出薄殼之外的可信驗證入口。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:24,26`
     - `GLOSSARY.md:30-34`
     - `docs/contract/02_invariants.md:126-130`

## 建議

1. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:3`**

   - **問題：** 單段同時交代三個風險、四項決定、升級時序與救援路徑，第一次閱讀很難分辨哪句是背景、哪句是決議。
   - **建議：** 拆成「問題」「主機薄層決議」「升引擎與救援路徑」三段；內容不必改。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:3`

2. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:25`**

   - **問題：** 「內嵌版本只用在第一次導入」容易被讀成第一次導入必定使用內嵌來源，沒有說離線導入的 `bootstrap.sh -i <image>` 會覆蓋它。
   - **建議：** 改成「未指定本機 image 時，內嵌版本只作第一次導入的預設值」。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:25`
     - `docs/contract/01_purpose.md:71`
     - `docs/contract/04_interface.md:200-201`

3. **位置：`docs/adr/0007-host-thin-layer-and-shell-integrity.md:24`**

   - **問題：** 一句列出環境偵測、字串比對、文法驗證、Docker 呼叫、寫紀錄及清理責任，後半又夾入 `sync`、`prune` 的例外，閱讀負擔過高。
   - **建議：** 拆成「啟動器可做的事」與「仍留在啟動器的快路徑」兩點。
   - **證據：** `docs/adr/0007-host-thin-layer-and-shell-integrity.md:24`