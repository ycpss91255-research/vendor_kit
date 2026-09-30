已建立修改前備份 `script_check_review_pages.pre_r142.2.md`，且雜湊與原始備份一致。未 commit、未 push、未執行 git 寫入。

- 已改：`script/check_review_pages.py` 第 174–175 行，CSV 指令遇到 `and retry.`、句讀、非 ASCII 字元或欄尾即停止。
- 未改：`script/README.md` 與 `script/test/test_check_review_pages.py` 屬於別的檔，交給跨檔一致性。

驗證結果：

- 指定四支檢查腳本全部通過。
- 4 個 regex 邊界案例通過。
- 單檔測試僅舊斷言失敗：仍期待 `just vendor_kit upgrade <repo> -z and retry.`；目前實際結果已是必改要求的 `just vendor_kit upgrade <repo> -z`。