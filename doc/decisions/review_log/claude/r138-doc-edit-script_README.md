# r138 doc-edit 審查：script/README.md

## 必改

1. **位置**：script/README.md:61（「### 審閱頁旁的 CSV（`03_messages`）」的「CSV 的逐碼差異」段）
   - **問題**：這一輪 mark_changes.py 新增了表頭改動的標示（開頭列出新舊表頭、刪掉的欄標「（本欄刪除）」、新增的欄標「（本欄新增）」、刪掉的欄在各碼照樣列出舊值並標紅），README 沒同步。ask 明寫「mark_changes.py 的 CSV 標示照新欄位，script/README.md 同步」；這一輪正好刪掉 note／invariant／details 三欄，維護者看標示版時會看到 README 沒寫的段落。
   - **建議**：在該段補一句：「表頭改了（例如刪掉欄）時，逐碼差異開頭先標出新舊表頭，並逐欄註記紅底『（本欄刪除）』或綠底『（本欄新增）』；刪掉的欄照新表頭之後接在各碼後面，列出舊值並標紅，所以只刪欄的代碼也算有改動。」
   - **證據**：script/mark_changes.py:31（docstring 新增一行）、mark_changes.py 的 diff_csv 新增 COLUMN_REMOVED／COLUMN_ADDED 與 `fields = new_fields + removed`；script/README.md:61 未提。

## 建議

1. **位置**：script/README.md:96（「CSV 的 `message`、`next_step` 裡的 `just vendor_kit …` 指令寫法由 `check_review_pages.py` 檢查」）
   - **問題**：README 改成只列 `message`、`next_step`，但 check_review_pages.py 沒跟著改，仍是 `CSV_COMMAND_FIELDS = ("message", "next_step", "note")`，docstring 也寫「message、next_step、note 欄」。CSV 已沒有 note 欄，實際行為一致，但工具與文件的說法不一樣，下次有人照工具原始碼改 README 會改回去。
   - **建議**：同一輪把 check_review_pages.py:13 與 :176 的 `note` 拿掉，讓工具與 README 一致。
   - **證據**：script/check_review_pages.py:13、script/check_review_pages.py:176；script/README.md:96。

## 其他核對結果（無問題）

- 已定案（map #78 Decisions so far）：diff 只動工具說明，跟各條定案不衝突。
- 對外承諾：沒有動 01／02／03／04 的內容。
- 做完沒：表頭（README:87）、retired 列規則（:89）、刪 invariant／details 兩條、引用規則改成代碼一律連 CSV（:94）、check_terms 文字欄（:128）、check_typography 文字欄與固定值域（:148）、開頭拿掉「03 頁的長說明節」（:79），都與 check_messages.py:10–17、:159–225、check_terms.py:113、check_typography.py:37–38 一致。README 其他地方不再提 note／invariant／details（`--note` 是 pack_review 的參數，無關）。
- 連結：diff 沒有新增或改動連結。
