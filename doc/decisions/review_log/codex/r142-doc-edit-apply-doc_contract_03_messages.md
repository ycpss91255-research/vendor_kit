已修改 [03_messages.csv](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/doc/contract/03_messages.csv)，未 commit、未 push，未執行 git 寫入指令。

備份：`doc_contract_03_messages.pre_r142.3.csv`，修改前 SHA-256 與來源 CSV 相同。

- 已改：VK0022 統一為 `a newer version ... current ..., latest ...`。
- 已改：VK0001 保留 CSV 原本語意，並依訊息格式改成小寫開頭；其他檔交給跨檔一致性。
- 已改：VK0024 改成 `no command specified`。
- 已改：VK0025 改成 `missing required argument: <參數>`。
- 已改：VK0027 改成 `invalid tag format: <tag>; expected vX.Y.Z with no leading zeros in X, Y, or Z`。
- 已改：全檔還原八組原始占位符，包括中文占位符。
- 已改：全部 message 依規則改成小寫開頭；單句訊息移除句尾句點。
- 已改：VK0020 改用 `prompted`：`it was not prompted again or applied`。
- 已改：VK0006～0009、VK0014～0015、VK0028～0029 改用 glossary 英文名詞：`shell`、`schema version`、`lock version line`、`per-file digest`、`fetch`、`install directory`。

驗證結果：

- CSV 結構、9 欄、32 碼順序、BOM、LF、占位符：通過。
- `check_terms.py`：通過。
- `check_context.py`：通過。
- `check_review_pages.py`：通過。
- `git diff --check`：通過。
- `check_messages.py`：尚報 15 項；7 項是並行修改中的檢查器尚未排除 `<…>` 內中文字，8 項屬 `03_messages.md`／`04_interface.md` 的跨檔一致性，均未越界修改。