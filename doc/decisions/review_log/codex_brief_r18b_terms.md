# r18b：補正上一輪（r18）兩處

你在目錄 `/tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/` 工作（repo 的複本；不要碰這個目錄以外的任何東西）。上一輪你已把 `doc/decisions/review/terms.md` 改寫完、建了 `doc/decisions/review/terms_moved.md`、改了 `script/diagram/disc_v1_a.py` 的 v1p0 區塊。本輪只做下面兩件事，只能動這三個檔；不 commit、不 git 操作。

## 1. `terms_moved.md`：每條必須帶「原文」

現在的條目只寫了「××原文 → 去向頁」的描述，沒有把原文貼上——這樣之後審到去向頁時內容就沒了。請重寫成每條都完整引用原文（來源 = `doc/decisions/_backup/review/terms.pre_r18.md`，一字不改、含反引號），格式：

```
- 【<原條目名或段落名>】<原文整段或整格，逐字> → <去向頁>
```

要求：
- 被刪或被縮寫的每一條（模組表 8 列、常用詞裡被移走的規則細節、其他既有詞裡被移走的細節、專案檔四原則、預檢、resolve／apply、救援路徑、佔位符、symlink、hash、tty、語法記法表 6 列、選項清單 12 條、動詞表 11 列的原文、升引擎原句、「記法與顏色見主圖第 0 頁……」句）都要有一條，原文完整貼上。表格列的原文寫成「中文名｜英文｜定義」一行。
- 一條原文若拆到多個去向頁（例如版本鎖定行：正規形 → 07、`<repo>` 名稱規則 → 07），一條寫完整原文、去向可列多個（「→ 07 schema（正規形）；→ 07 schema（`<repo>` 名稱規則）」）。
- 「語法記法」那條：先貼原表原文 → 主圖第 0 頁，再另起一條「【語法記法（POSIX 版改寫）】」放你上一輪寫的 POSIX 版與來源連結。
- 「## 附錄原文」一節維持不動。
- 原文裡本來就有的「／」照抄（那是原文），但你自己寫的字不得用「／」。

## 2. 可寫動詞／唯讀動詞兩條改順句子（`terms.md` 與 `disc_v1_a.py` v1p0 區塊同步、逐字一致）

現在的「指會不會動進 git 的檔與進度檔；可寫動詞是 …」不通順。改成：
- 可寫動詞｜writing verb｜會動進 git 的檔或進度檔的動詞：install、uninstall、add、remove、upgrade、dev、undev、prune；可寫與唯讀的分別只看會不會動進 git 的檔與進度檔。
- 唯讀動詞｜read-only verb｜不動進 git 的檔、也不動進度檔的動詞：update、sync、help；仍可寫 `cache/`、`gen/`。

改完跑 `python3 /tmp/claude-1000/-home-cyc-Desktop-vendor-kit-ws-src/967c6f9c-af39-4968-aabd-776e65300710/scratchpad/ws/script/diagram/gen_disc.py` 確認不報錯。最後輸出：terms_moved.md 條數、有沒有偏離。
