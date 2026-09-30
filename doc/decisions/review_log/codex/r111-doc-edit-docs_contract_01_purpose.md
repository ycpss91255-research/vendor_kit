## 必改

1. **位置：`docs/contract/01_purpose.md:26`**

   - 問題：把「版本鎖定行」寫成每個安裝目錄只有一行，而且這一行同時記錄所有工具與引擎；名詞表定義的版本鎖定行是一個引擎或工具各自的一個 TOML 項目。
   - 建議：改成「每個安裝目錄只有一份版本鎖定行的集合」或直接說「只有一份 `version.toml`，其中各項版本鎖定行……」。
   - 證據：`GLOSSARY.md:93-95,136-137`；`docs/contract/02_invariants.md:57-64`；`docs/adr/0002-vendor-kit-dir-layout-and-lock-line-form.md:20-26`。

2. **位置：`docs/contract/01_purpose.md:29`**

   - 問題：「把某個工具（含 VK 自己）指到本機目錄或本機 image」把來源類型交叉寫成四種可能；定義其實是工具只能指向本機目錄，引擎只能指向本機 image。
   - 建議：改成「把工具指到本機目錄，或把 VK 引擎指到本機 image」。
   - 證據：`GLOSSARY.md:142-146`。

3. **位置：`docs/contract/01_purpose.md:53`**

   - 問題：「原有的內容不動」是絕對承諾，但首次導入可以在取得同意後修改既有 `justfile`、`.dockerignore` 或 append 型初始檔。這裡把「不覆蓋」擴張成了「完全不修改」。
   - 建議：改成「不刪、不覆蓋原有內容；需要加入內容時先取得同意」。
   - 證據：`docs/contract/02_invariants.md:21-28,44-49`；`docs/contract/04_interface.md:220-244`；`docs/adr/0003-baseline-merge-and-line-records.md:23-28`。

4. **位置：`docs/contract/01_purpose.md:60`**

   - 問題：「每一版都是不可變的」容易被理解成 tag 不可變，但 tag 明定可以重新指到另一個 digest；真正不可變、被鎖定的是 digest 對應的內容。
   - 建議：改成「每個已鎖定 digest 對應的內容不可變且永久保留」；不要把「版本」與 tag、digest 混為一談。
   - 證據：`GLOSSARY.md:78-86`；`docs/contract/02_invariants.md:59,66,72`；`docs/adr/0009-release-assets-and-offline-import.md:3,15-20`。

5. **位置：`docs/contract/01_purpose.md:73`**

   - 問題：「可以退回舊版」沒有同一個 X 的限制，讀起來承諾任何跨大版退回都能直接靠還原版本鎖定行完成；不變量只保證同一個 X 內直接退回，跨 X 可能需要手動步驟。
   - 建議：明寫「同一個 X 內可以退回舊版」；跨 X 只承諾依事前公告的遷移步驟處理。
   - 證據：`docs/contract/02_invariants.md:178-194`。

6. **位置：`docs/contract/01_purpose.md:74`**

   - 問題：「失敗必印原因與下一步」比既定規則多承諾了一層。所有非成功結果都要印原因，但只有「需人處理」一定要附可直接複製的指令；部分失敗訊息明定沒有「下一步」欄內容。
   - 建議：改成「不是成功的結果必印原因；需要人處理時另印可直接複製的下一步指令」。
   - 證據：`docs/contract/02_invariants.md:97-104`；`docs/contract/03_messages.md:43-47,61-64`。

7. **位置：`docs/contract/01_purpose.md:86`**

   - 問題：「Z 變動：修 bug 或小調整」允許非錯誤修正的「小調整」，範圍比不變量寬；定案規則是 Z 只能修正行為錯誤，不增加新的對外介面。
   - 建議：改成「Z 變動：只修正行為錯誤，不增加新的對外介面」。
   - 證據：`docs/contract/02_invariants.md:182-186`。

## 建議

1. **位置：`docs/contract/01_purpose.md:21,75`**

   - 問題：「只依賴／只需要 Git、Docker、just」省略了支援平台既有 shell 與基本指令的前提。第一次看的讀者可能把它理解成不會使用任何其他主機命令。
   - 建議：兩處都寫成「除支援平台既有的 shell 與基本指令外，主機只需另外準備 Git、Docker、just」。
   - 證據：`docs/contract/02_invariants.md:110-116`；`docs/contract/04_interface.md:22-40`；`docs/adr/0007-host-thin-layer-and-shell-integrity.md:22-24`。

2. **位置：`docs/contract/01_purpose.md:38`**

   - 問題：使用了名詞表的 _Avoid_ 詞「簽章」。雖然這裡指數位簽署而非 VK 的印記，仍會造成同一詞在契約內有兩種可能含義。
   - 建議：改成「image 的數位簽署與驗證」。
   - 證據：`GLOSSARY.md:115-117`。

3. **位置：`docs/contract/01_purpose.md:70`**

   - 問題：「任何機器」過度寬泛；本頁前面已排除 macOS、Windows 原生，不變量也只要求支援平台結果一致。
   - 建議：改成「在任何支援的機器／平台」。
   - 證據：`docs/contract/01_purpose.md:39`；`docs/contract/02_invariants.md:200-208`。

4. **位置：`docs/contract/01_purpose.md:26,72`**

   - 問題：兩句各塞入多個不同概念，第一次閱讀時不容易辨認「唯一性單位」及「哪些是 repo 檔、哪些是 VK 檔」。
   - 建議：第 26 行拆成「唯一版本來源」與「同一 repo 可有多個安裝目錄」兩句；第 72 行拆成 repo 檔與 VK 檔兩個子項。
   - 證據：`docs/contract/01_purpose.md:26,72`；名詞邊界見 `GLOSSARY.md:97-102,136-146`。