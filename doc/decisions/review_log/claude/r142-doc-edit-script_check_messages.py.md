# r142 審查：script/check_messages.py

對照 #78 的定案（#117、#114、#122 等）：exit_code 對應 warn→1、error→2、fatal→3 跟 #117 第 1、2 點一致；前綴 `vendor_kit: <level>[VKnnnn]:` 沒改（#114）；CSV 仍是唯一出處（#122）。code、level、處置、next_step 的語意沒改。01、02 沒有違反。`python3 script/check_messages.py` 過，`python3 -m unittest discover -s script/test` 144 個測試全過。

## 必改

1. **位置**：doc/contract/03_messages.md 第 41、42、50 行；doc/contract/04_interface.md 第 132、145、155、232 行（check_messages.py 沒擋）
   **問題**：輸出範例的英文本文跟 CSV 的 `message` 對不上，但 03 第 85 行寫 `message`「逐字照印」，兩個對外頁因此互相矛盾：
   - 03:41 `A new version of B is available: current v1.2.0, new v1.3.0.`，CSV VK0022 是 `A newer version of <repo> is available: current <current_tag>; new <new_tag>.`
   - 03:42 `Could not list versions … the host Docker credentials)`（句尾沒有句號），CSV VK0001 是 `Cannot list versions … the host's Docker credentials).`
   - 03:50、04:132 `No command specified.`，CSV VK0024 是 `No command was specified.`
   - 04:145 `Missing required argument: <repo>.`，CSV VK0025 是 `Required argument is missing: <argument>.`
   - 04:155 `Invalid tag format: 1.2.0; expected vX.Y.Z …`，CSV VK0027 是 `Invalid tag format: <tag>. Use vX.Y.Z …`
   - 04:232 `A newer version of base is available: current v1.2.0, latest v1.3.0.`，CSV VK0022 是 `current <current_tag>; new <new_tag>`
   **建議**：以 CSV 為準改掉這些範例（或反過來改 CSV，但兩邊要逐字一致）。同一種錯這次出現 6 處，照規矩要寫進 lint：check_messages.py 新增規則 9，掃 README、doc/contract/*.md、GLOSSARY.md 裡 `vendor_kit: <level>[VKnnnn]: <本文>` 形式的行，檢查 `<level>` 等於該列的 `level`，`<本文>` 符合該列 `message` 的第一行（`<…>` 當萬用字元比對）。
   **證據**：doc/contract/03_messages.md:41,42,50,85；doc/contract/04_interface.md:132,145,155,232；doc/contract/03_messages.csv VK0001、VK0022、VK0024、VK0025、VK0027

2. **位置**：script/check_messages.py 第 20 行（docstring）
   **問題**：這裡寫「CSV 的 message、next_step 裡的 `just vendor_kit …`」由 check_review_pages.py 檢查，但這一輪 check_review_pages 的掃描欄改成了 situation、message、next_step。內部文件不准留過時的資訊。
   **建議**：改成「指令寫法（CSV 的 situation、message、next_step 裡的 `just vendor_kit …`）由 check_review_pages.py 檢查。」
   **證據**：script/check_review_pages.py:13,176；script/README.md:103

3. **位置**：doc/adr/0004-vk-recipe-interface-and-write-boundary.md 第 29 行（check_messages.py 規則 8 會掃 ADR）
   **問題**：這裡兩處寫 `vendor_kit: error[VKnnnn]: <中文本文>`，跟這一輪 check_messages.py 第 183 行「message 不准含中文字元」和 GLOSSARY.md:196 的 `<英文本文>` 衝突。
   **建議**：兩處都改成 `<英文本文>`，或改成 `<message>`。
   **證據**：doc/adr/0004-vk-recipe-interface-and-write-boundary.md:29；GLOSSARY.md:196；script/check_messages.py:183

## 建議

1. **位置**：script/check_messages.py 第 62 行 `CHINESE`
   **問題**：範圍只涵蓋 CJK 統一漢字（基本區、擴充 A、相容區）。全形標點（，。：「」（），U+3000–303F、U+FF00–FFEF）、注音、擴充 B 之後的字（U+20000 以上），以及 `≥` 這類非 ASCII 符號都擋不到。維護者要英文的理由是避免編碼與相容問題，這些字元一樣有這個問題；中文說明裡常用的 `≥`（VK0005、VK0012）也可能被抄進 message。
   **建議**：改成 message 只准 ASCII（`re.compile(r"[^\x00-\x7f]")`），錯誤訊息寫「message 只准 ASCII；中文說明放 description」。目前 CSV 的 message 已全是 ASCII，不會多出錯誤。同步改 docstring 規則 4、script/README.md:98 和測試。
   **證據**：script/check_messages.py:62,183；doc/contract/03_messages.csv VK0005、VK0012 的 description

2. **位置**：script/check_messages.py 第 11–12 行與第 183 行
   **問題**：docstring 把「message 不准含中文字元」歸在規則 4「active 列」底下，但程式碼放在 active 區塊外面（status 打錯字的列也會檢查）。行為沒有錯，是描述跟實作的位置對不上。
   **建議**：docstring 把這條移成獨立一句：「message 不准含中文字元（不分 status）。」或者把檢查搬進 active 區塊。
   **證據**：script/check_messages.py:11-12,174-184

3. **位置**：script/check_messages.py 第 35–37 行 `FIELDS`
   **問題**：script/check_typography.py:40-42 另外寫死了一份相同的 `CSV_FIELDS`。之後表頭再改時，兩份會悄悄脫鉤。
   **建議**：check_typography 改成 `from check_messages import FIELDS`（或者兩支共用一個常數模組），只留一個出處。
   **證據**：script/check_messages.py:35-37；script/check_typography.py:40-42

4. **位置**：script/check_messages.py 第 175–178 行
   **問題**：level 不合法時完全不檢查 exit_code，修好 level 之後才會冒出第二個錯誤，要跑兩次才能修完。
   **建議**：level 不合法時，如果 exit_code 不在 {1,2,3} 也一起報。
   **證據**：script/check_messages.py:175-178
