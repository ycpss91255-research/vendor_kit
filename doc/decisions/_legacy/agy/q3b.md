### 3b. 「自我升級」與「工具升級」的順序（rustup、uv）與常見坑
- rustup `self update`：與 `rustup update` 的關係（`rustup update` 是否自動 self update；`--no-self-update`；`self-update` 設定值 `enable/disable/check-only`）。
- `uv self update`：與 `uv python upgrade` / `uv lock --upgrade` 分開的理由；uv 是否會在其他命令中自動檢查新版。
- 常見坑（找 GitHub issue 前例）：舊 launcher 不認識新格式的版本檔（例如 Bazelisk、mise、Gradle wrapper 讀新格式 properties）；bootstrapping 順序；Windows 上無法覆寫執行中的 exe（rustup/uv/cargo 的處理方式）。
