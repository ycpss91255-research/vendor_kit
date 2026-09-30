# r115 審查：doc/decisions/scope_roadmap.md

範圍：r114（commit ebe85e3）的改動。本輪備份 `_backup/doc_decisions_scope_roadmap.pre_r115.md` 不存在，`git diff HEAD` 為空；改看 `git diff ebe85e3~1 ebe85e3`：第 35 行 `6-3`→`M1`，第 36 行刪掉 `（6-21，` 的 `6-21`。兩處換號本身正確：6-3→M1 對上 03 第 53 行；6-21 不在對照表、03 也沒有這條，刪掉不是漏換。檔內已無其他 `6-N`。

## 必改

1. **第 35 行「image 公開／私有」：「回 1 印 M1」結束碼錯**
   - 問題：M1 在 03 是結束碼 `2`（需人處理）。定案第 18 條把 `1`、`2` 對調後，`1` 只表示「做完了但要人接手」。r114 換了編號，但留著舊的 `1`，同一句話現在直接跟 03 矛盾。
   - 建議：改成「回 2 印 [M1](../../docs/contract/03_messages.md#訊息) 提示…」。
   - 證據：docs/contract/03_messages.md:53（M1 結束碼 `2`）、03_messages.md:25-26（結束碼 1／2 的定義）、discussion_queue.md「已定案」第 18 條。

2. **第 34 行「多命名空間工具」：「撞名 → 1 拒絕」結束碼錯**
   - 問題：04 規定撞名以結束碼 `2` 拒絕。`1` 是舊編號，定案第 18 條對調之前的寫法。這不是 r114 改的，但屬於跨檔不一致，要算在本檔上。
   - 建議：改成「撞名 → 2 拒絕（在任何寫入之前）」。
   - 證據：docs/contract/04_interface.md:125、discussion_queue.md「已定案」第 18 條。

## 建議

1. **第 35 行：「M1」是沒有連結的裸編號**
   - 問題：第一次看的人不知道 M1 指什麼、要去哪裡找。
   - 建議：寫成「[訊息 M1](../../docs/contract/03_messages.md#訊息)」，跟 04:175、ADR-0008 的寫法一致。
   - 證據：docs/contract/04_interface.md:175、docs/adr/0008-protocol-and-file-schema-versions.md（「[訊息 M6]」）。

2. **第 18 行：「VK recipe 十一個」數量不對**
   - 問題：04 的指令清單與 GLOSSARY「VK recipe 與用途」只有 10 個（add、remove、update、upgrade、dev、undev、sync、prune、install、uninstall）。
   - 建議：改成「十個」，或不寫數量、改連 04 的[指令](../../docs/contract/04_interface.md#指令)。
   - 證據：docs/contract/04_interface.md:79-100、GLOSSARY.md:206-225。

3. **第 18 行：「結束狀態 0/1/2/3」、「`--dry-run`」**
   - 問題：GLOSSARY 的詞是「結束碼」。另外 `--dry-run` 不在 04：定案第 26 條把非必要選項留到實作時再定，列成第一版範圍會讓人以為已經承諾。
   - 建議：改成「結束碼 0/1/2/3（見 [03](../../docs/contract/03_messages.md#結束碼)）」；`--dry-run` 拿掉，或註明「實作時再定」。
   - 證據：GLOSSARY.md:203、docs/contract/04_interface.md:171-203、discussion_queue.md「已定案」第 26 條。

4. **第 36 行：「零命中或多處只 warn」用了英文 warn**
   - 問題：GLOSSARY 定義的詞是「警告」。
   - 建議：改成「只印警告」。
   - 證據：GLOSSARY.md:200。

## 其他檢查項（沒有問題）

- 定案第 1～29 條：r114 在本檔只換編號，沒有碰 01／02／03／04 的承諾或介面。Q5、Q13、Q15、Q16 本檔沒有提到。
- 02 第 4 條與 ADR-0008 的改寫不在本檔。本檔沒有描述零寫入或救援路徑，所以沒有需要同步的地方。
- 本檔是內部文件，不受「出處：」規則限制；檔內也沒有「出處：」行。
- 連結目標都存在：01_purpose.md、02_invariants.md、design_principles.md、GLOSSARY.md、adr/0001。第 43 行的 ADR-0001 是用程式碼格式寫的路徑，不是超連結；這不是本輪的改動。
