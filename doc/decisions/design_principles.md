# 設計原則與衝突優先序

> 每條原則將來各自併入服務它的 ADR，這份檔是併入前的集中處。
> 本檔提到的「不變量 N」指 [`doc/contract/02_invariants.md`](../contract/02_invariants.md) 的第 N 條。

## 設計原則

在不變量之下、個別決議之上。不變量是任何 ADR 不得違反的**性質**；設計原則是**判準**——兩個看起來都對的選項並存時，vendor_kit 怎麼選。原則刻意比不變量弱：一個 ADR 可以在說明理由後偏離原則，那份 ADR 就是紀錄；不變量不能被偏離。每條附「寫在哪裡」與「服務哪條不變量」。

### P1. 對齊 base 的 just 慣例；base 反過來對齊 vendor_kit 的檔案佈局

命名空間、`--option` 收窄（帶值選項皆有短選項、不用複合值 positional）、`update` 只查／`upgrade` 套用——這些借 base。反方向：檔案佈局（`.vendor_kit/`、根 `justfile` 一行 import）由 vendor_kit 定，base 遷移時對齊，所以「與 base 共存」不是 vendor_kit 要解的問題。只借慣例不抄行為：base 的 `update` 吞結束碼、`upgrade` 自己 commit，都不繼承。
*寫在哪裡：* [`../adr/0004-vk-recipe-interface-and-write-boundary.md`](../adr/0004-vk-recipe-interface-and-write-boundary.md)；base ADR-00000011。*服務：* 不變量 8。

### P2. 借主機已有的，不養第三方

拉與展開交給 docker（`create`／`cp`），文字基準版合併交給引擎內的 `git merge-file`，版本追蹤交給 Renovate 一條 regex。vendir、crane、Copier 都不進引擎；要進，須通過 `../adr/0001-why-not-existing-tools.md` §5 的十項門檻（前四項即本原則原本的四項）。
*寫在哪裡：* [`../adr/0001-why-not-existing-tools.md`](../adr/0001-why-not-existing-tools.md)；主機薄層見 [`../adr/0007-host-thin-layer-and-shell-integrity.md`](../adr/0007-host-thin-layer-and-shell-integrity.md)。*服務：* 不變量 5、6。

### P3. 每個逃生口顯式、有名字、印出它做了什麼

`-y`（免詢問）、`--no-justfile`（不碰根檔只印指示）、`.vendor_kit/config.toml` 的 `lock_enabled = false`（鎖不支援的檔案系統）、`--dry-run`（只印會動哪些檔）。取逃生口是可見的動作；沒有靜默的逃生口，也沒有「偵測到就自動放寬」。
*寫在哪裡：* [`../adr/0004-vk-recipe-interface-and-write-boundary.md`](../adr/0004-vk-recipe-interface-and-write-boundary.md)、[`../adr/0003-baseline-merge-and-line-records.md`](../adr/0003-baseline-merge-and-line-records.md)。*服務：* 不變量 1、4。

### P4. 先加後退

會破壞使用者的改動拆成兩步：新路徑先與舊路徑並存，退場是另一個可獨立排程、公告、回退的決議。升級契約（宣告格式、`init.toml` 格式、結束狀態）只加不改；recipe 改名走別名期。
*寫在哪裡：* [`../adr/0004-vk-recipe-interface-and-write-boundary.md`](../adr/0004-vk-recipe-interface-and-write-boundary.md)。*服務：* 不變量 4、8——repo 在 vendor_kit 不決定的時間點升級，一步到位的「加+刪」是它們走不到一半的一步。

### P5. 一條規則一個擁有者

規則在引擎實作一次；啟動器、`just vendor_kit test`、工具 just 模組只轉發。兩個必須一致的實作是延遲發作的漂移。
*寫在哪裡：* [`../adr/0007-host-thin-layer-and-shell-integrity.md`](../adr/0007-host-thin-layer-and-shell-integrity.md)、[`../adr/0006-tool-image-as-data-only.md`](../adr/0006-tool-image-as-data-only.md)。*服務：* 不變量 6、4。

### P6. 母體用推導，不列清單

要支援哪些初始檔類型，看工具實際用了什麼；要驗哪些平台，看使用者實際跑在哪；哪些 ADR 存在，看檔案系統。手寫清單從第一個在別處新增的項目起就是錯的，而且錯得靜默。
*寫在哪裡：* [`doc/decisions/scope_roadmap.md`](scope_roadmap.md)「範圍」；`doc/adr/README.md`。*服務：* 不變量 4；文件與決議流程見 `../../AGENTS.md`。

## 衝突優先序

這個順序**只用於**：兩個 vendor_kit 都持有的正當性質，在某個決議裡不能兼得，順序說誰讓步。它**不是**把「這很難做」排在任何東西之上的許可：**難做不是理由**——難度不在下列性質之中、永遠不進比較；一個難以安全實作的改動是程式碼的發現，不是一個競爭的主張。引用這個順序的決議必須點名兩個相衝的性質，並證明在此處確實不能兩全；做不到，衝突就是想像的，順序不適用。

高者勝。

**① 使用者的檔與 repo 跑的東西正確。** 使用者的檔只在使用者同意下改變；repo 的 `just` 跑到的工具內容與宣告一致。*立於不變量 1、2、5。*

**② 缺陷大聲且早。** 有錯，在第一個有人在場的時間點說出來，而不是繼續跑然後回報綠燈。*立於不變量 4。*

**③ 一個來源、一個擁有者。** 宣告一份、規則在引擎一份、其餘轉發。*立於不變量 2、6；這是 P5 作為性質而非判準。*

**④ 使用便利。** 少打幾個字、少問一次、少知道一件事。*不立於任何不變量——這是它排最後的原因，不是它不重要。*

### 實例：詢問 vs `-y`

`upgrade` 對某個已納管初始檔判定「使用者沒改、新版有變」。④ 說直接換掉——使用者沒改，換了也不會壞；① 說那是使用者的檔，vendor_kit 不能未經同意寫入。① 勝：預設**詢問**。但 ④ 沒有被丟掉，而是被給了一扇有名字的門（P3）：`-y` 免問，且仍印出改了哪些檔。CI 下沒有人回答問題：無 `-y` 時 ② 勝過 ④——以 1 結束並印出「請在本機執行 `just vendor_kit upgrade base` 後提交」，而不是 EOF 當同意、也不是靜默跳過然後綠燈。三個性質各得其所，是順序讓它成為一個決議而不是三條互相矛盾的規則。

### 第二例：`sync` 發現基準版落後

Renovate 的 PR 改了宣告、merge 後有人打 `just docker build`。④ 說 `sync` 順手把初始檔合併掉最省事；③ 說 tracked 寫入只能來自明確 recipe（不變量 3）；② 說這個狀態要被說出來。結果：本機 warn 提示 `upgrade`、CI 以 1 結束——③ 與 ② 都在 ④ 之上，而它們彼此不衝突。

### 順序排不出時

同一階的兩個性質不由這份清單決定；不變量與任何東西的衝突也不由它決定——不變量不是可以讓步的性質，這正是它叫不變量的原因。一個決議發現自己在拿一條不變量換另一條，它發現的是不變量的缺陷，產物是 [`doc/contract/02_invariants.md`](../contract/02_invariants.md) 的修訂，不是一份挑贏家的 ADR。
