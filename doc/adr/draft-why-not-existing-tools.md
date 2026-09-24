# ADR-NNNN：為什麼不用現成工具（vendir／Copier／subtree／submodule／套件管理器）

> Serves: PRD 設計原則 P2（借主機已有的，不養第三方）——這份 ADR 記錄 P2 在「要不要引進現成的搬檔、範本、套件工具」這個問題上的應用，並固定將來重評的門檻。也服務不變量 5（主機只需 docker + git + just）。機制決議，不建立不變量。

- **Status:** 草稿，待編號
- **Date:** 2026-09-23
- **Related:** `doc/PRD.md` 設計原則 P2 與不變量 5、`doc/decisions/grilling.md` Q1（第一版不放 vendir/Copier）、`doc/decisions/prior_art.md`（前例研究）、`doc/decisions/review/01_purpose.md`（第 01 頁只留結論一句，完整比較在本檔）

## Context

vendor_kit 要同時做到四件事：搬檔、鎖版、初始檔升版不蓋掉使用者改的、工具作者能在本機邊改邊測。第 01 頁原本在正文裡逐條比較現有工具，審閱時判定那是決議內容、不是目的陳述，移進本檔；第 01 頁只留一句結論。

硬性限制來自 PRD：

- 設計原則 P2「借主機已有的，不養第三方」：拉與展開交給 docker（`create`／`cp`），文字三方合併交給引擎內的 `git merge-file`，版本追蹤交給 Renovate 一條 regex；vendir、crane、Copier 都不進引擎。
- 不變量 5「主機只需 docker + git + just；正確性不綁單一平台」：任何「主機要先裝 X」都會在 Jetson、WSL2、共用工作站其中一台失敗。

已定案的事實：`doc/decisions/grilling.md` Q1 定案「自寫 + 主機 docker（拉 image）+ 引擎內 git merge-file；第一版不放 vendir/Copier」。

## Decision

不引進 vendir、crane、Copier、cookiecutter，也不用 `git subtree`、`git submodule` 或語言套件管理器當搬檔機制。理由逐項如下。

### 1. `git subtree`、`git submodule`

把工具的 git 歷史綁進使用者的 repo：工具的 commit 與使用者的 commit 混在一起，正是 vendor_kit 要解的第一個痛點。`submodule` 另外還要求使用者自己記得初始化與更新，漏掉就拿到空目錄或舊版，而且是靜默的。

### 2. vendir

能宣告式同步檔案，方向與 vendor_kit 一致，但實際省下的只有 `docker create`／`docker cp` 那幾行；鎖版、初始檔的基準版合併、本機邊改邊測，vendir 都不做，仍要自己寫。換來的是主機或引擎多一個第三方 binary，與不變量 5 相衝。

### 3. Copier、cookiecutter

能做範本與升版合併，但要求範本是帶 tag 的 git repo——vendor_kit 的工具以純資料 image 出貨，不是 git repo；而且它們只在建立時產生一次檔案，不管後續的內容同步，四件事裡只覆蓋到一件的一半。

### 4. 語言的套件管理器（npm、pip、cargo）

只裝自己語言的產物。`justfile`、`Dockerfile`、`.gitignore` 這類純檔案不在它們的範圍內，而那正是 vendor_kit 要搬的東西。

### 5. 重評門檻

將來要把上列任何一個第三方工具放進引擎，必須先通過 PRD P2 的四項門檻：

1. 能展開現有的 scratch 純資料 image。
2. 完全服從宣告（不自作主張改版本或內容）。
3. 通過私有 registry／多架構／Jetson／WSL2 的驗收。
4. 確實刪掉一整塊自維護程式，而不是在既有程式旁邊再加一層。

將來要重評，先過這四項門檻。

## Consequences

- 得到：主機只需要 `docker`、`git`、`just`；沒有第三方 binary 的安裝、版本、平台支援問題要跟。
- 付出：拉與展開、鎖版、基準版合併、本機開發這幾塊由 vendor_kit 自己維護，bug 也自己修。
- 第 01 頁不再列這四條比較，只留一句結論並指向本檔；兩邊若要改，改本檔為準。
- 驗收：重評門檻第 3 項的私有 registry、多架構、Jetson、WSL2 由驗收層（見 ADR-0001 的 acceptance 層）涵蓋。

## Alternatives

- **用 vendir 當下載後端，其餘自寫。** 會滿足「宣告式同步」這一項，但只省 docker 幾行，卻讓主機或引擎多一個第三方相依；PRD 路線圖已把它排到 v2，且限定「只在通過 P2 的四項門檻後重評」。
- **用 Copier 管初始檔，image 只管搬檔。** 會滿足「初始檔升版合併」，代價是工具必須同時以 image 與帶 tag 的 git repo 兩種形式出貨，出貨端要維護兩份來源——違反一條規則一個擁有者（P5）。
- **用 `git submodule` 搬工具、自寫升級腳本。** 會滿足「鎖版」（submodule 記 commit），但工具歷史仍進使用者的 repo，且使用者要多記兩個 git 指令；痛點第一條沒有解決。
