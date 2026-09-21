# 我方草稿（主對話整理，供雙軌審查）

## 方案 A（傾向）：一次執行一檔 JSONL、OTel 欄位名、計數保留
- 位置 `.vendor_kit/log/`；根 `.gitignore`／`.dockerignore` 由 install 加一行（與 cache/ 同列）；目錄內自帶 `.gitignore`（`*`／`!.gitignore`）。
- 檔名 `<YYYYMMDDTHHMMSSZ>-<verb>-<id8>.jsonl`；`<id>` = 交易 id（與進度日誌同一個 id，方便對照）；不做 latest symlink（Windows／CIFS 上 symlink 不可靠，用檔名排序即可）。
- 每行欄位：`timestamp`（ISO 8601 UTC 微秒）、`severity_text`（INFO／WARN／ERROR）、`event_name`（有限集合，對齊現行 OTel Data Model 的 EventName）、`body`（人讀一句話，可省）、`trace_id`（= 交易 id，32 hex）、`attributes{component: launcher|engine, verb, phase: resolve|apply, path, action: create|modify|delete|append, exit_code, duration_ms, prompt, answer, ...}`。
- 事件集合（第一版）：launcher_start／launcher_exit、docker_pull_start／finish、docker_extract（create/cp）、engine_start／exit、resolve_start／finish、apply_start／finish、lock_acquired、fingerprint_verified、journal_created／deleted、prompt_asked／answered、file_created／modified／appended／deleted、progress_recovered、error。
- 啟動器（POSIX sh）：先 `mkdir -p .vendor_kit/log`，產 id（`/proc/sys/kernel/random/uuid` 缺則 `od /dev/urandom`），自己以 `printf` 寫 launcher_*／docker_* 事件（欄位值只放固定字串與已知安全的值；argv 類值先做最小 JSON 跳脫：`\`→`\\`、`"`→`\"`，含控制字元則替換）；以 `-e VENDOR_KIT_TRACE_ID -e VENDOR_KIT_LOG_FILE=/repo/.vendor_kit/log/<檔>` 傳給引擎，引擎追加寫同一檔（`open('a')` + 每筆 flush；同一次執行內只有一個寫者在寫）。
- 保留：計數制，啟動器結束時保留最近 N 檔（N 先訂 50，可由 version.toml `[log] keep = N` 覆寫？——待審），刪最舊；不做大小上限（單次執行筆數有限）。
- 憑證：registry token 永不進 log；attributes 不收 env；URL 去 userinfo。
- 寫失敗：**所有動詞都不因 log 寫不進而改變結束碼**（對齊 apt／dpkg／npm 前例）；但 stderr 明確印一行 `6-xx 無法寫入操作紀錄 <path>：<原因>`，並在結束摘要再提醒一次；不提供 `--no-log`。理由：never fail silently 是「不能悄悄失敗」，不是「必須失敗」；狀態變更的可追溯性由進度日誌與 git diff 保證。
- 唯讀動詞（help、update、sync 快路徑）也寫（一檔幾行），使用者要求「每個動作都要有明確記錄」。sync 每次工具 recipe 都跑 → 快路徑一次 3～4 行、一檔；N=50 會被 sync 洗掉？→ 待審：sync 快路徑（無變更）是否只寫、不佔保留名額，或改 N 較大／分目錄。
- lnav format 檔隨 release 附（`docs/lnav/vendor_kit.json`），`opid-field: trace_id`。

## 方案 B：單檔追加 `vendor_kit.jsonl` + 自輪替（大小或筆數）
- 優：`tail -f`、一檔看全部歷史。缺：多終端同時跑要 flock；輪替（rename）與正在寫的行競態；壞行污染後續；回報 issue 要節錄。

## 方案 C：logfmt 單檔
- 優：sh 最好寫、人眼可讀。缺：無規範、無巢狀、lnav 支援差；使用者筆記已選 JSONL+OTel。

## 想請審查員特別判斷
1. `event_name` vs `body` 當事件名（agy 摘要指出現行 OTel Data Model 有頂層 EventName）。
2. 寫失敗一律不改結束碼（我方）vs 寫入動詞 fail-closed（agy）。
3. sync 快路徑高頻執行與計數保留的互動；N 值。
4. 啟動器用 printf 拼 JSON 的最小跳脫是否足夠；還是啟動器只寫 logfmt/純文字、引擎啟動後把啟動器事件補進 JSONL？
5. 保留策略要不要可設定；放哪（version.toml 進 git 會被 Renovate／CI 看到，或 version.local.toml）。
