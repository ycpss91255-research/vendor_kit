# script — 腳本總覽

`script/` 依類型分子目錄，每個類別一個子目錄。類別目錄底下放這一類的腳本、一份 `README.md`（說明這一類每支腳本的用途與跑法），以及可選的 `test/`（這一類腳本的測試）。

## 目前的類別

| 類別 | 內容 | 說明 |
|---|---|---|
| `doc/` | 文件工具：五支 `check_*.py` 自檢、改動標示 `mark_changes.py`、送審打包 `pack_review.py` | [文件工具說明](doc/README.md) |
| `repo/` | repo 結構檢查：`check_script_layout.py` | [repo 結構檢查說明](repo/README.md) |

## 新增腳本

新腳本放進對應的類別；沒有合適的類別就新開一個，同時寫好該類別的 `README.md`。規則：

- `script/` 頂層只准有本檔與類別子目錄，腳本不放頂層。
- 類別目錄名只用小寫英數與連字號。
- 每個類別都要有 `README.md`。
- 類別底下的子目錄只准有 `test/`。

這幾條由 [check_script_layout.py](repo/check_script_layout.py) 強制，CI 的 docs-lint job 會跑。

VK 程式碼的測試照舊放根目錄 `test/`，不放在 `script/`。
