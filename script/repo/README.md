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

## check_local_paths.py

[check_local_paths.py](check_local_paths.py) 掃 `git ls-files` 列出的文字檔，擋本機絕對路徑（對其他人沒用，也會洩漏使用者名稱）。規則直接載入 `.claude/hooks/comment_tag_guard.py` 的 `LOCAL_PATHS`，不另抄一份。符號連結與二進位檔（含 NUL 位元組或不是 UTF-8）跳過。

白名單 `ALLOW` 寫在腳本內，以檔為單位，每條附理由；白名單上的檔已經掃不到本機路徑時算過時，也會失敗，提醒刪掉那條。CI 的 `docs-lint` 會跑這支。

跑法（在 repo 根目錄）：

```sh
python3 script/repo/check_local_paths.py
```

輸出一行 JSON：`ok`、`hits`（每筆 `file`、`line`、`rule`）、`stale_allow`。有命中或過時的白名單就以 1 結束；載不到 hook 規則以 2 結束。

## 測試

測試在 [test/test_check_script_layout.py](test/test_check_script_layout.py) 與 [test/test_check_local_paths.py](test/test_check_local_paths.py)，跑法：

```sh
python3 -m unittest discover -s script/repo/test
```
