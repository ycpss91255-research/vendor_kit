已完成，只修改 [doc/contract/README.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/README.md)，未 commit、push 或執行 git 寫入指令。

備份：`doc/decisions/_backup/doc_contract_README.pre_r144.md`

- `doc/contract/README.md:3`：將 VK、契約首次出現改為 GLOSSARY 分群連結。
- `doc/contract/README.md:9-12`：將使用者、結束碼、VK recipe 的 `<ins>` 改為分群連結。
- `doc/contract/README.md:19-20`：將名詞底線規則改為「正文首次出現連到所屬分群」，並記錄排除範圍、HTML 與錨點規則。

驗證全部通過：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- unittest：157 tests，OK
- README 專用腳本斷言：無 `<ins>/<u>`、5 個原底線名詞各有唯一正確連結、目標檔案存在。