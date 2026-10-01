# script/repo — repo 結構檢查

檢查 repo 本身的結構是否照規則擺放。

## check_script_layout.py

[check_script_layout.py](check_script_layout.py) 檢查 `script/` 的目錄規則：

1. `script/` 頂層只准有 `README.md` 與子目錄，腳本不准直接放頂層。
2. 每個子目錄是一個類別，名稱只用小寫英數與連字號。
3. 每個類別底下要有 `README.md`。
4. 類別底下的子目錄只准有 `test/`。

只看 `git ls-files -co --exclude-standard` 列出的檔（追蹤中，以及未追蹤但沒被忽略的檔）。CI 的 `docs-lint` 會跑這支。

跑法（在 repo 根目錄）：

```sh
python3 script/repo/check_script_layout.py
```

全部符合時印 `OK`；有問題就逐筆印出 `檔:原因` 並以 1 結束。

## 測試

測試在 [test/test_check_script_layout.py](test/test_check_script_layout.py)，跑法：

```sh
python3 -m unittest discover -s script/repo/test
```
