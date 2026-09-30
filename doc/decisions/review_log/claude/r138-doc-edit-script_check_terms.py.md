# r138 doc-edit 審查：script/check_terms.py

範圍：`diff -u doc/decisions/_backup/script_check_terms.pre_r138.md script/check_terms.py`（備份實際檔名沒有 `.py`），只改了第 112–113 行：`CSV_TEXT_FIELDS` 拿掉 `note`，註解拿掉 invariant／details。

## 必改

1. **位置**：script/test/test_check_terms.py 第 30–45 行 `CsvTest.test_csv_text_fields_scanned`（配合 script/check_terms.py 第 113 行）
   - **問題**：`CSV_TEXT_FIELDS` 已拿掉 `note`，測試還用 `code,status,situation,message,note,details` 的假 CSV，而且斷言 `VK0001:note` 會被掃到。`python3 -m unittest discover -s script/test` 結果是 FAILED (failures=1)，違反 ask「測試跟著改……全部要過」。
   - **建議**：假 CSV 表頭改成 `code,status,level,disposition,situation,message,next_step`（有 BOM）。每個文字欄各放一格含「舊詞」或不含舊詞的值，斷言 `csv_cells` 回傳 `disposition`、`situation`、`message`、`next_step` 四欄（空值不列），`code`／`status`／`level` 不掃。多行格保留在某個文字欄裡，繼續測跨行值。註解可以加一欄非文字欄（例如 `note`），驗證不在清單內的欄不會被掃。
   - **證據**：script/test/test_check_terms.py:37、:42、:45；unittest 輸出 `First extra element 2: 'VK0001:note'`。

## 建議

1. **位置**：script/check_terms.py 第 112 行註解
   - **問題**：「code、status、level 是固定值域」沒錯，但現在表頭只有 7 欄，註解可以直接寫成「其餘三欄」，免得之後增減欄位時漏改。目前內容正確，不必改。
   - **建議**：維持原樣，或改成「其餘欄（code、status、level）」。
   - **證據**：doc/contract/03_messages.csv:1 表頭 `code,status,level,disposition,situation,message,next_step`。

其他核對：
- 已定案（map #78 Decisions so far）：沒有牴觸。
- 對外承諾：沒有動到 01～04。
- 連結：diff 裡沒有新增連結。
- 四支 lint（check_terms、check_context、check_messages、check_typography）都回 0。check_terms 印出「OK: 掃 30 個 .md 檔、1 個 CSV」。
- script/README.md 第 128 行的欄位清單和程式一致。
