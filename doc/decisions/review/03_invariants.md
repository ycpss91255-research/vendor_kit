# 03 不變量

本頁是 01 頁承諾背後的固定性質；名詞見 02 頁。

每條都是 vendor_kit 全域必須成立的性質，**任何未來的 ADR 不得違反**。「機制」是目前實現它的方式，可以被新 ADR 換掉；性質不行。列在各條下的 ADR 是建立或服務它的決議——它們記錄「怎麼做」與「為什麼這樣做」，本頁只記「它必須永遠成立」。標「> ⚠ 待拍板」的段落是尚未定案的項目，不得當成已定引用。

## 1. 使用者的檔歸使用者：可以建、要改先問、永不刪、永不覆蓋

**性質：** vendor_kit 對使用者的檔（根 `justfile`、初始檔、任何進 repo 的 git 且不在 `.vendor_kit/` 薄殼內的東西）只有四種行為：**可以建**（但要明確印出建立或修改了什麼）；**要改先問**（`-y` 免問，仍印出改了什麼；非互動且無 `-y` = 不改並以 1 結束印出該打的指令，EOF 不算同意）；**永不刪**（含新版工具不再提供的初始檔，只 warn 並列清單）；**永不覆蓋**。

「永不覆蓋」的定義：**不用工具版本取代使用者的客製內容**。只有兩個明定例外，且都不是取代：(a) 根 `justfile` 加一行 `import`（無檔則建、有檔則詢問後 append）；(b) 已納管初始檔的基準版合併（沒改 → 詢問是否換新版；雙方都改 → 詢問是否合併，衝突留標記由使用者解）。`add` 遇到已存在的檔：不納管、不覆蓋、只 warn。`remove`／`uninstall`：不刪初始檔，只印清單。

**為什麼固定：** 初始檔建立後就是使用者的程式碼；base 時代 `init.sh` 的 `rm -f` 與 symlink 接管，正是使用者無法信任「跑一次 just 不會弄壞我的檔」的原因。一個會刪或覆蓋使用者檔的散播工具，使用者只會在每次升級前先備份、然後不升級。

**機制（可換）：** 基準版（baseline）全文 + `git merge-file --diff3` 逐檔狀態機；`adopted` 旗標；metadata 記錄「檔／行由我們建立」作為 uninstall 唯一刪除依據。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（初始檔合併）、待寫 ADR-xxxx（檔案佈局）。

## 2. 一個來源：`.vendor_kit/version.toml` 是 repo 的唯一宣告

**性質：** repo 對「用哪些工具、哪個版本（tag@digest）、哪個引擎」只有一份宣告，進 git。工具內容是**快取**（不進 repo 的 git），任何時候都能由宣告決定性重建；Renovate、`upgrade`、人手改的都是同一個檔。本機覆寫（`version.local.toml`）只覆蓋宣告中已存在的工具，不進 git，不是第二份真相。

**為什麼固定：** 兩份版本真相（例如 image tag 與另一個 lock 檔）會漂移，漂移是靜默的；digest 才鎖內容，tag 只給人與 Renovate 看。

**機制（可換）：** TOML；引擎行固定第一行讓啟動器用 `grep` 讀；Renovate 一條 regex manager 追 docker datasource。

> ⚠ 待拍板：檔名 `version.toml` vs `lock.toml`；工具 image 公開／私有（私有時主機 docker credential helper 是否為唯一認證路徑）。

**建立／服務它的 ADR：** ADR-0002（引擎與工具分離，在 proto）、待寫 ADR-xxxx（檔案佈局）。

## 3. 自動化只碰不進 git 的東西

**性質：** 每次 `just` 自動跑的前置（`sync`）只重建 `.vendor_kit/cache/` 與 `.vendor_kit/gen/`；任何要進 git 的寫入（宣告、初始檔、基準版、薄殼）都必須是使用者明確打的動詞。CI 下若判斷需要 tracked 寫入，以 1 結束並印出該打的指令，不偷補。

**為什麼固定：** 自動寫 tracked 檔的工具（npm 寫 lock、terraform 寫 lock）能成立，是因為那些檔「機器擁有、可由 tracked 輸入決定性重生、CI 有 frozen 模式」三條同時滿足；初始檔第一條就不過（建立後歸使用者）。一個在 `git pull` 後靜默建出未提交檔的工具，會讓 CI 測到跟開發者不同的內容。

**機制（可換）：** `sync` 只寫 `.vendor_kit/.gitignore` 涵蓋的路徑；`CI=1` 自動 frozen。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）。

## 4. 永不靜默失敗

**性質：** 結束狀態 `0`／`1`／`2` 是契約（0 成功；1 失敗且不留半成品、宣告不動；2 完成但有衝突待人處理）。`sync` 發現「未完成導入」→ 1 提示 `add`；「基準版落後宣告」→ 本機 warn 提示 `upgrade`、CI 下 1；`verify` 失敗 → 重裝並 warn，不靜默通過。任何 warn 都要說出是哪個檔、該打什麼。

**為什麼固定：** vendor_kit 站在每個 repo 的 `just` 指令的最前面；它靜默失敗，錯誤就傳到每個 repo 而沒人知道。可信任是這個產品本身。

**機制（可換）：** 引擎統一映射結束碼（`git merge-file` 的原生狀態不直接當產品狀態）；`--porcelain` 給機器讀；metadata 記中間狀態讓重跑可續作。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）、待寫 ADR-xxxx（初始檔合併）。

## 5. 主機只需 docker + git + just；正確性不綁單一平台

**性質：** 使用者的主機只需要 `docker`、`git`、`just`（最低版本待定）。支援 Linux amd64 與 arm64（含 Jetson）；WSL2 視同 Linux。不引進第三方 binary：只借主機已有的 docker 與引擎容器內的 `git merge-file`。任何被當作正確性依據的機制（鎖、路徑、symlink、行尾）都不得只在一個平台成立。

**為什麼固定：** 這是把安裝程式從 base 抽離的初衷：base 的使用者有 Jetson、有 WSL2、有共用工作站，任何「主機要先裝 X」都會在其中一台失敗。

**機制（可換）：** 引擎 image 多架構（amd64 + arm64）；主機薄啟動器用 `docker create`／`docker cp` 抓 image 內容，享 daemon 快取與同一條認證路徑。

> ⚠ 待拍板：`just` 最低版本（ADR-0002 寫 1.33；需在 CI 用該版本重跑所有 just 實測後定案）；工具 image 是否單架構 `linux/amd64` 固定 `--platform` 拉（一份內容一個 digest）。

**建立／服務它的 ADR：** ADR-0002（在 proto）。

## 6. 引擎版本由 repo 鎖定；啟動器是不含邏輯的薄殼

**性質：** 一個 repo 只用宣告第一行指定的那一版引擎；引擎在容器內跑。repo 裡進 git 的啟動器（`.vendor_kit/entry.just`、`vendor.just`、`ci/check.sh`）只做轉發：讀那一行、拉 image、起容器、原樣傳參數（`"$@"`）。規則只有一個擁有者——引擎；啟動器與 `check.sh` 不判斷、不修補。

**為什麼固定：** 啟動器一旦有邏輯，它跟引擎就是兩個要對齊的實作，而啟動器進了 repo 的 git、由使用者決定何時升級；漂移是必然的。薄殼可以永久凍結，引擎可以隨時升級。

**機制（可換）：** POSIX sh + `docker` + `grep`／`sed`；`gen/.stamp` 記錄薄殼對應的引擎 digest，不符就換薄殼並要求重跑。

**建立／服務它的 ADR：** ADR-0002（在 proto）、待寫 ADR-xxxx（bootstrap 薄層）。

## 7. 工具 image 純資料；引擎與工具分離

**性質：** 工具 image 是 `FROM scratch` 只放檔案的純資料，不含程式、不會被執行；引擎只有一份（`vendor_kit:vN`）。工具 repo 永遠不必因為 vendor_kit 升級而重發版；vendor_kit 升級也不必等工具重發版。

**為什麼固定：** 甲版（工具 image `FROM vendor_kit`）把升級工具的程式綁回工具本身，需要一整套協定號與相容矩陣才撐得住——這正是當初把安裝程式抽離 base 要擺脫的東西。

**機制（可換）：** `Dockerfile.dist` = `FROM scratch` + `COPY dist/`；主機 `docker create` → `docker cp` → 唯讀掛進引擎容器。

**建立／服務它的 ADR：** ADR-0002（在 proto）。

## 8. 使用者介面極少；動詞語意跟 base

**性質：** 常用三個：`add`／`upgrade`／`dev`；進階六個：`remove`／`undev`／`update`／`sync`／`install`／`uninstall`；一支薄腳本 `bootstrap.sh`（下載引擎 + 呼叫 `install`，再跑 = 修復）。全部在 `just vendor_kit` 命名空間，不佔頂層。動詞語意與 base 一致：`update` 只查不改任何檔、`upgrade` 套用（含安裝、基準版合併、推基準版）。成對動詞成對出現（`add`↔`remove`、`dev`↔`undev`、`install`↔`uninstall`）。不加 `init`／`diff`／`accept`／`rollback`／`check` 等別名——各自由既有動詞的選項或 git 接手。

**為什麼固定：** 同一批使用者在同一個 `justfile` 裡同時打 `just base …` 與 `just vendor_kit …`；兩個命名空間語意相反，比偏離生態系更糟。動詞少，每個動詞就能有完整的 `--help`、成對的反向、明確的結束狀態。

**機制（可換）：** 動詞 recipe 一行 `verb *args` 轉發、放 tracked 的 `vendor.just`；`[group('常用')]`／`[group('進階')]` 分段；`help` recipe 補命名空間層說明。

> ⚠ 待拍板：一個工具可否輸出多個 just 命名空間（base 現有 `docker`／`base`／`template`）；`.gitignore` 這類幾乎必已存在的初始檔（base 的 ignore 條目永遠進不去）只 warn 還是另立「標記區塊 append」動詞。

**建立／服務它的 ADR：** 待寫 ADR-xxxx（介面動詞）。

## 9. 驗收 = 真引擎、乾淨 repo、完整流程；dev 自身與驗收用同一機制

**性質：** vendor_kit 的驗收測試用**剛 build 出來、已通過前面所有測試層**的引擎 image，在一個乾淨的 fixture repo 跑完整流程：`install` → `add` → `upgrade` → `dev`／`undev` → `remove` → `uninstall`，並以結束狀態與檔案系統為斷言，不 import vendor_kit。在本機開發 vendor_kit 自身（`dev vendor_kit -i <image>`）與驗收走的是同一條「用指定 image 當引擎」的路。

**為什麼固定：** 引擎在容器內、使用者只看得到 `just` 與檔案；只有黑箱驗收能證明「使用者看到的」是對的。dev 自身若另闢機制，驗收測的就不是開發者實際跑的東西。

**機制（可換）：** `version.local.toml` 的 `vendor_kit = "<本機 image tag>"` 覆寫；Docker multi-stage 測試分層（smoke → lint／unit → integration → system → acceptance）。

**建立／服務它的 ADR：** ADR-0001（測試分層，在 proto）、待寫 ADR-xxxx（dev 自身與驗收）。

## 10. 決議記 issue，定案寫 ADR，ADR 回連不變量；架構圖是測試依據

**性質：** 每個設計決議先在 issue 討論（中文）；定案後寫成 ADR，ADR 檔頭一行 `> Serves:` 回連本頁的不變量、[`doc/decisions/design_principles.md`](../design_principles.md) 的設計原則或 [`doc/decisions/scope_roadmap.md`](../scope_roadmap.md) 的範圍項目；ADR 記機制與理由，本頁記性質。架構圖（`.drawio`）不是插圖，是測試的依據：圖上畫的模組邊界與泳道由 lint（import-linter、鏡射、黑箱）強制。

**為什麼固定：** 沒有回連的 ADR 會在幾次修改後與產品目標脫鉤；沒有被測試強制的圖，會在幾次修改後跟程式脫鉤。兩者都是靜默的。

**機制（可換）：** `doc/adr/NNNN-<slug>.md` 檔案系統即登錄；必要段落由 lint 管（見 [`doc/adr/README.md`](../../adr/README.md)）。

**建立／服務它的 ADR：** ADR-0001（在 proto）；本頁與 `doc/adr/README.md` 的規則本身。
