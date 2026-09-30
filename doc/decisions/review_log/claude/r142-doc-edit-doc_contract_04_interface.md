# r142 審查：doc/contract/04_interface.md

範圍：這一輪只改了 4 個輸出範例裡的訊息本文（L132、L145、L150、L155、L232）。對照 map #78 的 Decisions so far：沒有違反定案，#114 前綴格式 `vendor_kit: <level>[VKnnnn]:`、#117 level 與結束碼對應（error→2、warn→1）都照舊；01、02 的承諾沒動。五支 lint 都過，但沒有一支比對範例本文和 CSV。

問題集中在一點：依 #122，CSV 是唯一出處，可是範例本文是另外譯的，4 條裡有 3 條跟 03_messages.csv 的 `message` 對不上；VK0022 在 04、03.md、CSV 甚至是三個不同版本。

## 必改

1. **L132 VK0024 本文跟 CSV 不一致**
   - 問題：04 寫 `No command specified.`，03_messages.csv 的 VK0024 `message` 是 `No command was specified.`（03.md L50 跟 04 一樣，CSV 是另一種）
   - 建議：以 CSV 為準（#122）。04 L132 與 03.md L50 改成 `vendor_kit: error[VK0024]: No command was specified.`；如果要保留較短的說法，就改 CSV，三處用同一句
   - 證據：04_interface.md L132；03_messages.csv VK0024 列；03_messages.md L50；#122

2. **L145 VK0025 本文跟 CSV 不一致**
   - 問題：04 寫 `Missing required argument: <repo>.`，CSV 是 `Required argument is missing: <argument>.`。句型不同，代入占位符後也對不上
   - 建議：改成 `vendor_kit: error[VK0025]: Required argument is missing: <repo>.`（或改 CSV，兩邊用同一句）
   - 證據：04_interface.md L145；03_messages.csv VK0025 列

3. **L155 VK0027 本文跟 CSV 不一致**
   - 問題：04 寫 `Invalid tag format: 1.2.0; expected vX.Y.Z with no leading zeros in X, Y, or Z.`，CSV 是 `Invalid tag format: <tag>. Use vX.Y.Z with no leading zeros in X, Y, or Z.`
   - 建議：改成 `vendor_kit: error[VK0027]: Invalid tag format: 1.2.0. Use vX.Y.Z with no leading zeros in X, Y, or Z.`
   - 證據：04_interface.md L155；03_messages.csv VK0027 列

4. **L232 VK0022 本文跟 CSV、03.md 三方都不一致**
   - 問題：
     - 04：`A newer version of base is available: current v1.2.0, latest v1.3.0. Run: …`
     - CSV：`A newer version of <repo> is available: current <current_tag>; new <new_tag>. Run: just vendor_kit upgrade <repo>`
     - 03.md L41：`A new version of B is available: current v1.2.0, new v1.3.0. Run: …`
   - 建議：以 CSV 為準，改成 `vendor_kit: warn[VK0022]: A newer version of base is available: current v1.2.0; new v1.3.0. Run: just vendor_kit upgrade base`，03.md L41 也同步。`next_step` 仍逐字出現在本文裡
   - 證據：04_interface.md L232；03_messages.csv VK0022 列；03_messages.md L41

5. **L231 stdout 範例還是中文，跟 03.md 的英文範例對不上**
   - 問題：04 的 stdout 寫 `base 有新版 v1.3.0（目前為 v1.2.0）。`，03.md L40 同一種查詢結果已改成英文 `B has a new version v1.3.0 (current: v1.2.0).`。同一種輸出在兩頁用兩種語言，而 ask 要求輸出範例（程式碼區塊）一起改英文
   - 建議：改成 `stdout: base has a new version v1.3.0 (current: v1.2.0).`，跟 03.md L40 同一個句型
   - 證據：04_interface.md L231；03_messages.md L40

## 建議

1. **用法行仍是中文，跟英文診斷混在同一個 stderr**
   - 位置：L70 用法區塊；範例 L133、L146、L151、L156 的 `stderr: 用法：just vendor_kit <指令> [參數] [選項]`
   - 問題：維護者要求本文改英文，理由是編碼與相容性。用法行同樣印在 stderr，而且緊接在英文診斷後面，這個理由對它一樣成立。主流 CLI 的用法行都以 `usage:` 開頭：GNU getopt 系工具、git（`usage: git …`）、Python argparse（`usage: prog …`）
   - 建議：問維護者用法與 `-h` 輸出是否也改英文，例如 `usage: just vendor_kit <command> [arguments] [options]`。這一條超出本輪 ask（只講診斷），所以列為建議
   - 證據：04_interface.md L70、L133、L146、L151、L156；03_messages.md L62（「訊息本文為英文」只講診斷）

2. **把範例與 CSV 的比對寫成 lint**
   - 位置：L132、L145、L150、L155、L232 的範例區塊
   - 問題：這一輪 4 條範例有 3 條偏離 CSV，五支 lint 全過，沒有攔下來。這是會反覆出現的問題
   - 建議：在 check_messages.py（或 check_review_pages.py）加一條檢查：掃 03／04 程式碼區塊裡的 `vendor_kit: <level>[VKnnnn]: <text>`，確認 level 跟 CSV 相同，`<text>` 符合 CSV `message` 把 `<…>` 換成任意值後的樣式
   - 證據：五支 lint 的輸出（皆 OK）；上面必改 1～4
