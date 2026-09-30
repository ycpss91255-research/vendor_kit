已完成，未執行 commit、push 或任何 git 寫入指令。

驗證結果：

- `check_terms.py`：OK
- `check_context.py`：OK
- `check_review_pages.py`：OK
- `check_messages.py`：OK
- `check_typography.py`：OK
- 單元測試：151 tests，全部通過
- `git diff --check`：通過
- 備份內容驗證：通過

備份：`doc/decisions/_backup/doc_adr_0013-no-ci-mode-strict-checks-in-test.pre_r143.md`

改動：

- `doc/adr/0013-no-ci-mode-strict-checks-in-test.md` 檔頭：加入 accepted 狀態與服務的不變量連結。
- `doc/adr/0013-no-ci-mode-strict-checks-in-test.md` 決議段落：記錄取消 CI 模式、忽略 `CI` 環境變數及嚴格檢查只綁定 `test`。
- `doc/adr/0013-no-ci-mode-strict-checks-in-test.md` Considered Options：記錄三個方案與採用理由。
- `doc/adr/0013-no-ci-mode-strict-checks-in-test.md` Consequences：明定 VK0014、VK0032、本機覆寫、Renovate 分工及取代 ADR-0004 的範圍。