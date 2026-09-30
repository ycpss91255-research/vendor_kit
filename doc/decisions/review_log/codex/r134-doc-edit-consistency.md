- 已改：`doc/contract/04_interface.md` 第 189、221 行，將 VK0022、VK0021 改稱「`warn` 診斷」。
- 已改：`doc/contract/03_messages.md` 第 20、64、76 行，分開警告與做完但要人接手，並補齊不用使用者代換的單一指令判準。
- 已改：`doc/contract/03_messages.md` 第 22 行，將「檔案」改為首次標記的「VK 檔」，後次出現移除 `<ins>`。
- 已改：`doc/contract/03_messages.csv` VK0009 的 `note`，將「本頁不定」改為「契約不定」。
- 未改：`doc/contract/README.md` 不在硬性規則允許修改的四個檔案內；目前第 21 行仍是過時範例。
- 未改：`GLOSSARY.md`；備份時內容已符合要求，未覆寫並行修改。

四個指定檢查腳本全部 OK；CSV 的 BOM、LF、檔尾換行亦符合規則。已建立 `pre_r134` 備份，未執行任何 git 寫入、commit 或 push。