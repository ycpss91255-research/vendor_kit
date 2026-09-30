# r121 doc-edit 審查：doc/contract/04_interface.md（Claude）

範圍：`diff -u doc/decisions/_backup/doc_contract_04_interface.pre_r121.md doc/contract/04_interface.md`

核對結果：
- 已定案：沒有違反。第 23 條（主機前置檢查失敗不留執行紀錄）與註第 40 行「VK 不留執行紀錄」一致。
- 對外承諾：Docker／just 最低版本、結束碼 `2`、「任何寫入之前」都保留；已有安裝目錄那句照 ask 指定的字改寫，意思和原文等價（原文「不承諾 VK 的訊息與結束碼」→「看到的是 just 自己的錯誤訊息與結束碼」）。
- 做完沒：第 3 行開頭句照 ask 改了；主機需求改成四欄表，工具外部連結、just 下載頁連結、結束碼與訊息總表連結都保留；原本「版本不足時：」清單已刪掉；just 那兩種情況放在表下方的註，ask 允許這樣做。
- 連結：新增或改動的連結 `03_messages.md#結束碼`、`03_messages.md#訊息`，用腳本算過 slug，03 的實際錨點裡有 `結束碼`、`訊息`，都存在。`check_review_pages.py`、`check_terms.py` 都 OK。

## 必改

（無）

## 建議

1. 位置：04_interface.md 第 40 行（註：已有安裝目錄）。
   問題：「just 太舊時，讀 justfile 就會出錯」沒說為什麼會出錯，讀者看不出為什麼 VK 沒機會先檢查版本。維護者正好問到這句（原文「just 解析 justfile 時就先拒絕…」）是什麼意思，表示光看這句看不懂。
   建議：補上原因，例如「justfile 用了 just 1.33.0 才支援的寫法，just 太舊時讀 justfile 就會出錯，輪不到 VK 執行，也就沒機會檢查版本；這時看到的是 just 自己的錯誤訊息與結束碼，VK 不留執行紀錄」。這是說明，不是新承諾。
   證據：doc/adr/0007-host-thin-layer-and-shell-integrity.md 第 24 行（`[group]` 放在 `mod` 上要 1.33；已有安裝目錄時由 just 解析 justfile 時自己報錯）。

2. 位置：04_interface.md 第 35 行，just 列的「版本不足時」欄。
   問題：這一格只寫「見下方的註」，只看表格的人看不到 just 版本不足時的結果；Docker 那列則把結果直接寫在格子裡，兩列寫法不一樣。
   建議：格子裡寫兩句短的，例如「首次導入：`bootstrap.sh` 以結束碼 `2` 結束；已有安裝目錄：由 just 自己報錯，見下方的註」。
   證據：04_interface.md 第 33、35 行。
