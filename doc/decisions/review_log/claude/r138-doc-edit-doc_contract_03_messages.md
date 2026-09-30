# r138 審查：doc/contract/03_messages.csv

範圍：`diff -u doc/decisions/_backup/doc_contract_03_messages.pre_r138.csv doc/contract/03_messages.csv`

核對結果：
- 表頭是 `code,status,level,disposition,situation,message,next_step`，每列 7 欄；UTF-8 BOM、LF（CR 0 個）。五支 lint 全過。
- 每列的 code、level、disposition、message、next_step 跟備份逐字相同；只有 situation 有改。
- note／invariant／details 的去處：
  - VK0001、VK0032 的 note：併進 situation
  - VK0002、VK0005 的 details（原本連到 ### 節）：節的內容併進 situation；VK0005 的主機前置檢查另外寫在 03.md「輸出」
  - VK0006 的 note：併進 situation；「不重產」本文已經寫了
  - VK0007 的 note：`<tag>` 那部分併進 situation；「寫入前結束」由 03.md 結束碼 `3` 那列涵蓋
  - VK0008 的 note：由結束碼 `3` 涵蓋
  - VK0009 的 note：「寫入前結束」由結束碼 `3` 涵蓋；-h 那部分 04_interface.md:126 已經寫了
  - VK0010 的 note：併進 situation
  - VK0011、VK0012 的 note：併進 situation，03.md「輸出」也有
  - VK0013 的 note：本文已經寫了
  - VK0024 的 note：只是指向 03.md「輸出」的說明；那條規則還在「輸出」裡
  - invariant 欄：照 ask 刪掉
- 沒有違反 #78 的已定案決定（#96 主機前置檢查不留執行紀錄、#91 結束碼等都一致）。CSV 裡不再有連結，沒有要驗證的錨點。

## 必改

（無）

## 建議

1. **位置**：VK0005、VK0011、VK0012 的 situation 括號「（主機前置檢查：排在建執行紀錄之前，失敗時不建執行紀錄、不動任何 VK 檔）」
   - **問題**：03.md「輸出」已經有同一條共通規則，這裡寫成兩份。ask 要的是「併進 situation 或共通規則」，擇一就好。situation 本來是代碼唯一的意思，把行為規則塞進去，會讓「什麼情況發出」讀起來不清楚。
   - **建議**：三列都縮成「…（主機前置檢查）」，或者把括號整個拿掉，細節只留在 03.md「輸出」。
   - **證據**：03_messages.csv 第 6、12、13 列；03_messages.md「輸出」第 4 點。
2. **位置**：VK0002 的 situation
   - **問題**：這格變成兩句長句，偏離 ask 的「精簡一句」。另外，原本 ### VK0002 寫的「不在原指令字串尾端直接接 -y」已經刪掉；雖然「逐項重組」隱含了這點，但這條原本是明寫的防呆。
   - **建議**：維持現有的語意，可以精簡成「…；<加上 -y 的原指令> 由這次的參數逐項重組並依 POSIX shell 加引號，-y 放在單獨的 -- 之前，沒有 -- 就放最後」。「不在尾端直接接」要不要保留，交給改稿方判斷。
   - **證據**：03_messages.csv 第 3 列；備份 doc_contract_03_messages.pre_r138.md:87。
3. **位置**：VK0007 的 situation「本文的 <tag> 原樣印出」
   - **問題**：跟 VK0001 的「<tag> 原樣印出」寫法不一致。
   - **建議**：統一成「<tag> 原樣印出，由使用者換成…」，拿掉「本文的」。
   - **證據**：03_messages.csv 第 2、8 列。
4. **位置**：script/test/test_check_terms.py:42（不在這一輪的改檔清單內）
   - **問題**：`python3 -m unittest discover -s script/test` 失敗 1 個：test_csv_text_fields_scanned 仍然預期有 `VK0001:note`。ask 要求測試全過，但目前沒過；而且這支測試檔不在改檔清單上。
   - **建議**：把預期改成新的欄位集合（disposition、situation、message、next_step 中非空的那幾格），並把這支檔加進這一輪的改檔清單。
   - **證據**：執行 unittest，FAIL: test_csv_text_fields_scanned，出錯在 test_check_terms.py:42。
