# 待討論佇列

維護者還沒正面回覆的問題都記在這裡，依序一條一條討論。規則（維護者 2026-09-30）：

- 維護者沒有正面回覆的，一律當作尚未回覆，不當定案。
- 送給維護者之前，先跟 codex 討論清楚，把雙方結論與證據寫在該條底下。
- 定案後把結果寫進對應文件或 ADR，這裡標「已定案」並寫明日期與落在哪裡。

## 已定案（維護者 2026-09-30 直接指示）

這些是指示，照做，不再問：

1. 非標示版（正式檔、正文副本）裡不寫版本號；版本只在 `_marked/` 的檔名。程式已改（`script/mark_changes.py`，版本號記在 [versions.json](versions.json)）；正式檔裡現有的 `> 版本 vN` 行在下一輪 doc-edit 拿掉。
2. 錯誤碼總表排在介面頁之前：總表成為 03，介面頁成為 04；結束碼的說明從介面頁移到總表。理由：文件只能向前依賴。
3. 介面頁「版本不足時以 `1` 結束」之類的句子，連到總表對應的訊息。
4. 01～04 與根目錄 README 補目錄（table of contents）。
5. 介面頁「入口」：`bootstrap.sh` 排第一（第一步），再來 `just vendor_kit`、`check.sh`。
6. 介面頁「清單裡的名詞」不重新定義，直接連到 `CONTEXT.md` 對應條目，只維護一處。
7. 介面頁「指令的數量與語意」整段拿掉。
8. README 裡使用者不需要的資訊（開發進度等）先記錄，v1.0.0 時重新調整：[issue #73](https://github.com/ycpss91255-research/vendor_kit/issues/73)。
9. 02 重新審一次：不變量只寫概念，不寫 repo 內部的實際情況（指令寫法、選項名稱等）。

## 待討論

### Q1 02 第 8 條的 U1～U6 要不要編號

- 維護者：一般清單不行嗎？之後一直增加怎麼維護？說服我增加 U1～U6。
- 現況：`U1`～`U6` 只在 02 自己引用（第 266～271 行的「實際做法」逐條對應）；ADR 沒有用 `U` 編號引用。設計原則頁（`design_principles.md`）有 P1–P6 的先例，ADR 以 `Serves:` 回連它們。
- 待 codex 討論。

### Q2 介面頁的「共同選項」

- 維護者的回覆只寫了「共同選項」四個字，沒有下文。
- 待確認：是要跟「指令的數量與語意」一樣拿掉，還是另有意見。

### Q3 總表排在介面頁之前的依賴方向

- 總表的「下一步」欄會寫指令（例如 `upgrade --engine`），指令寫法定義在介面頁。總表排前面時，這算不算向後依賴？
- 補充（r103 後）：02 本身也用編號引用總表的訊息（例如第 128～129 行的 6-5、6-13）。總表排在 03 時，02 → 03 一樣是引用後面的頁。r103 在[審閱頁說明](../review/README.md)「寫法規則」加了例外「訊息編號可由 02、03、ADR 回連」，跟「只能向前依賴」衝突，要一起定。
- 待 codex 討論（已送 discuss，round `q20260930`，題 `dep-order`；02 → 總表的引用是後補的，下一輪再送）。

### Q4 介面頁與 README 的「出處」行

- 維護者：02 討論過不保留出處，為什麼這裡又有？skill 要求的？
- 事實：skill 沒有要求。02 在 commit `06397c4`（「出處與機制段移出」）拿掉出處；理由和機制由 ADR 記錄。介面頁與 README 的出處行是之後各輪加的，跟 02 的做法不一致。
- `ADR-0007 §1` 的 `§1` 指 ADR-0007 自己的「### 1. 主機依賴的版本下限」小節；[ADR 規則](../../adr/README.md)只規定必要段落（Context／Decision／Consequences／Alternatives），沒有定義 `§` 寫法。
- 提議：對外頁不留出處行，跟 02 一致。待 codex 討論。

### Q5 本機沒有引擎 image 時，版本組合怎麼判定

- r103 codex 必改指出：[ADR-0008](../../adr/0008-protocol-and-file-schema-versions.md) 說啟動器讀引擎 image 的 LABEL 就能判定版本組合、不必連 registry，但本機還沒有那個 image 時 LABEL 從哪裡來沒說，機制不閉合。
- codex 提的修法（本機沒有 image 時延到拉 image 之後才判定、要連 registry）會削弱 [02](../review/02_invariants.md) 第 322 行「不必連上任何 registry 就判定得出來」，所以沒有套用，ADR-0008 維持原文。
- 待 codex 討論：要補哪個離線可取得的資料來源（例如記在 VK 檔裡的介面版區間），還是修改不變量。

### Q6 r103 總表草稿的兩處內容

- 6-3（沒有 registry 憑證）也會在 `add` 時出現，但訊息的下一步只給 `upgrade <repo>@<tag>`；介面頁沒有 `add <repo>@<tag>`。
- r103 套用必改時，6-39（偵測到 podman）的類別從「需人處理」改成「失敗」（沒有可複製的指令）；6-19 補了下一步 `just vendor_kit upgrade --engine`。
- 待 codex 討論。

## 已回答的事實問題（不需定案）

- 「不變量」不是大陸專用詞：國家教育研究院樂詞網 invariant 收「不變量」「不變式」（[樂詞網](https://terms.naer.edu.tw/detail/3214182/)）。repo 裡對外文件全部用「不變量」；「不變式」只出現在 `_legacy/` 兩處。
- GNU 慣例的長選項寫 `--`：glibc 手冊 Argument Syntax：「Long options consist of `--` followed by a name」；單獨的 `--` 結束選項解析（[glibc 手冊](https://sourceware.org/glibc/manual/latest/html_node/Argument-Syntax.html)）。
- `CONTEXT.md` 放 repo 根目錄：skill `setup-matt-pocock-skills` 的 domain.md 規定單一語境時放 repo 根目錄。
