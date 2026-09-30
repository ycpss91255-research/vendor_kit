## 必改

1. **位置：`docs/contract/03_messages.md:59`，訊息 6-28**

   - **問題：** 把「薄殼被使用者修改」和「薄殼只是跟目前引擎模板版本不同」合併描述成「被修改過」，訊息也固定宣稱「偵測到薄殼被修改」。正常的版本脫節會因此被誤報成使用者動過檔案，與 ADR 不一致。
   - **建議：** 讓時機與訊息能區分「內容被修改」和「不是這版引擎的模板」；至少不要把兩者一律稱為「被修改」。
   - **證據：**
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:16` 明列「被手改」與「跟引擎不是同一版」是兩種情況。
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:26` 說第一次比對抓「被改過」，第二次比對抓「跟這一版引擎不是同一份」。
     - `docs/adr/0004-vk-recipe-interface-and-write-boundary.md:23` 使用較廣的「薄殼不符」，沒有把原因限成使用者修改。

2. **位置：`docs/contract/03_messages.md:64`，訊息 6-41**

   - **問題：** 只說 metadata 缺失或損壞，沒有告訴使用者如何處理；「下一步」欄也是 `—`。這直接違反 01 對所有失敗的承諾。
   - **建議：** 補上實際可行的下一步；若確實沒有通用修復指令，也要明說應備份哪些檔、向誰求助或提供哪些診斷資料，不能停在「無法處理」。
   - **證據：**
     - `docs/contract/01_purpose.md:74`：「失敗必印原因與下一步。」
     - `docs/contract/02_invariants.md:41` 只規定不得猜測，沒有免除說明下一步。
     - `docs/contract/03_messages.md:47` 定義「下一步」欄是訊息中的可執行指令，但 6-41 沒有任何處置方式。

3. **位置：`docs/contract/03_messages.md:46、52`，訊息本文規則與 6-3**

   - **問題：** 第 46 行說「意思欄是訊息本文，逐字照印」，但 6-3 的意思欄在反引號模板之後又有「`<指令>` 依觸發的指令而定……」等說明。無法判定這段說明是否也要輸出；若不輸出，就違反「整欄逐字照印」。
   - **建議：** 明定只有反引號內是逐字本文，欄內其餘內容只是替換規則；或把替換規則移到「時機／下一步」欄。訊息契約必須能唯一決定實際輸出。
   - **證據：**
     - `docs/contract/03_messages.md:46` 把整個「意思」欄定義成逐字本文。
     - `docs/contract/03_messages.md:52` 同一格混合訊息模板與非訊息說明。
     - `docs/contract/03_messages.md:58` 的多行訊息則依第 46 行規則，把「第一行／第二行／第三行」放在反引號外；6-3 沒有遵循同一種標示方法。

## 建議

1. **位置：`docs/contract/03_messages.md:33、60、61`**

   - **問題：** 使用裸稱的「recipe」和「VK recipe」，但名詞表把「VK recipe」與「工具 recipe」定義成不同概念。第 33 行「各 recipe」對第一次閱讀者不清楚是否也包含工具 recipe。
   - **建議：** 第一次改成 `<ins>VK recipe</ins>`，後面一致寫「VK recipe」；6-36 的「其他 recipe」也明確寫成「其他 VK recipe」。
   - **證據：**
     - `GLOSSARY.md:56-57` 定義「工具 recipe」。
     - `GLOSSARY.md:171-179` 分別定義「VK recipe」「可寫 recipe」「唯讀 recipe」。

2. **位置：`docs/contract/03_messages.md:22-24、43`**

   - **問題：** `1` 是「做完但要人接手」，`2` 又包含類別名稱「需人處理」。兩個中文描述非常接近，但核心差別其實是「操作是否已完成」，第一次閱讀不容易立即分辨。
   - **建議：** 在第 43 行補一句：`需人處理` 表示操作尚未成功完成，與結束碼 `1` 的「已完成、後續仍需人工」不同。
   - **證據：**
     - `docs/contract/03_messages.md:22` 定義結束碼 `1`。
     - `docs/contract/03_messages.md:23、43` 讓結束碼 `2` 與訊息類別「需人處理」並存。
     - `GLOSSARY.md:194-198` 對「需人處理」與「失敗」的定義仍未說明「是否完成」這個區別。

3. **位置：`docs/contract/03_messages.md:55、57、60`**

   - **問題：** `<vY>`、`<P>`、`<M>`、`<N>`、`<written_by>`、`<P_shell>` 都只說會換成實際值，沒有說值代表什麼；而且 `<vY>` 與其他地方的 `<version>`、`<tag>` 寫法不同。
   - **建議：** 改用自解釋占位符，例如 `<目標引擎版本>`、`<現有檔案版>`；若必須保留欄位名，至少在表前列一份占位符對照。
   - **證據：**
     - `docs/contract/03_messages.md:46` 只解釋占位符會被替換。
     - `GLOSSARY.md:230-237` 定義介面版與檔案版，但沒有定義 P、M、N、vY 等縮寫。
     - `docs/contract/03_messages.md:58、63` 已使用較清楚的 `<version>`。

4. **位置：`docs/contract/03_messages.md:60`，訊息 6-36**

   - **問題：** 版本組合不合時，非救援 recipe 的 `-h`／`--help` 回 `3`，偏離主流 CLI「help 成功輸出並結束」的慣例。ADR 有相容性理由，因此不列必改，但 03 本身完全沒交代這個反直覺例外的理由。
   - **建議：** 在時機欄補一句簡短理由，例如舊薄殼不能安全轉發新引擎的一般 recipe；不要讓讀者以為是疏漏。
   - **證據：**
     - `docs/contract/03_messages.md:33` 一般規則把 recipe help 視為正常 stdout。
     - `docs/contract/03_messages.md:60` 規定部分 help 改回 `3`。
     - `docs/adr/0007-host-thin-layer-and-shell-integrity.md:11、29-30` 才記載救援路徑受限的理由。
     - GNU `diff --help` 是輸出用法後結束；Python `argparse` 的 help 預設寫 stdout，而用法錯誤才以 `2` 結束。[GNU Diffutils](https://www.gnu.org/software/diffutils/manual/diffutils.html)、[Python argparse](https://docs.python.org/3/library/argparse.html)
     - 既定的 `0/1/2` 分法本身有主流依據：`diff` 是相同 `0`、有差異 `1`、故障 `2`；`grep` 也以 `2` 表示錯誤；`git diff --exit-code` 沿用 diff 語意。[GNU Diffutils](https://www.gnu.org/software/diffutils/manual/diffutils.html)、[GNU grep](https://www.gnu.org/s/grep/manual/html_node/Exit-Status.html)、[git diff](https://git-scm.com/docs/git-diff)