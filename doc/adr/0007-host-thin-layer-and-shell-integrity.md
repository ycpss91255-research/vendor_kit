# 主機只留薄層：命令白名單、薄殼自描述標頭、引擎升級分兩段

主機依賴集合會自己長大（每次升級多借一個命令，沒人注意「只需三個」已經變成四個），薄殼進使用者的 git、升級時機不在 VK 手上，而且隨手就能改（[不變量 5](../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)、[不變量 6](../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)）。所以主機這一層只做不需要知道 repo 內容意義的事：啟動器只准呼叫白名單上的命令，由 lint 擋；薄殼帶自描述標頭，由引擎重算比對；規則全在容器內的引擎。升引擎分兩段，換上新引擎就停、要求重跑，剩下的步驟由新引擎的規則做；舊薄殼遇上新 major 時，少數救援路徑永久可用（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)）。

## Considered Options

- **`sync` 偵測到薄殼過期就自動重產**：`sync` 是唯讀 recipe，這會讓它改到進 git 的檔，與[不變量 3](../contract/02_invariants.md#3-自動化只碰不進-git-的東西)相衝。
- **薄殼的 hash 記在 `gen/.stamp`，不放薄殼自己的標頭**：`gen/` 不進 git，換機器、清快取、CI 的乾淨 checkout 都驗不了，而能改薄殼的人同樣能改 `gen/`。
- **支援 Podman 或其他 docker 相容 CLI**：驗收組合翻倍，而主機依賴集合是契約，要加得先修訂不變量 5。偵測到就明講不支援，不讓它半通半不通。
- **引擎升級一次跑完**：少跑一次指令，但剩下的步驟由舊引擎的規則執行，而那份規則正是這次要換掉的。
- **救援路徑也受介面版判定約束**：少一個例外，但薄殼太舊時使用者沒有任何出口，只剩手改 repo 裡的檔。

## Consequences

- 主機版本不足或裝的是 Podman，在第一次寫入之前就停下。這些前置檢查沒有副作用，一律排在建執行紀錄之前；失敗時不建執行紀錄、不動任何 VK 檔。[不變量 4](../contract/02_invariants.md#4-永不靜默失敗) 要求執行紀錄早於任何副作用，這些檢查本來就在副作用之前，所以不受影響。VK 自己的訊息與結束碼，承諾範圍分兩種：
  - Docker 版本不足與偵測到 Podman：首次導入與已有安裝目錄都由啟動器檢查，只在 stderr 印訊息、以[結束碼](../contract/03_messages.md#結束碼) `2`結束，訊息見[訊息總表](../contract/03_messages.md#訊息)。
  - just 版本不足：只有首次導入由 `bootstrap.sh` 在任何副作用之前檢查，只在 stderr 印訊息、以結束碼 `2` 結束，訊息見[訊息總表](../contract/03_messages.md#訊息)。已有安裝目錄時日常入口就是 `just vendor_kit …`，just 低於下限會在解析 justfile 時由 just 自己拒絕，VK 的啟動器沒機會執行，所以不承諾 VK 的訊息與結束碼，也不留執行紀錄。
- 薄殼被手改或跟引擎不是同一版，都會在寫入前抓出來並列出差異，包含無害的格式調整；想調薄殼格式只能改引擎的模板再重產。
- 薄殼與引擎脫節時，`sync` 不重產薄殼，只以 `2` 結束，並在診斷中列出下一步；診斷見[訊息總表](../contract/03_messages.md#訊息)，使用者要自己跑 `upgrade --engine`。
- 升引擎要跑兩次，指令歷史裡會看到同一行指令連著兩次。
- 白名單多一個支援平台既有的基礎 userland 命令，是改對外介面：改 [04 使用者介面](../contract/04_interface.md#主機需求)的明列清單與 lint。多一個要另外安裝的主機依賴，是改主機依賴集合，得先修訂不變量 5。
- 驗收案例（黑箱層）：低版本 docker、`docker --version` 含 `podman`、低版本 just 各一條；改一個位元組的薄殼；舊薄殼跑新 major 的一般 recipe；同一個不合組合下救援路徑仍然可用。
- 內部機制（之後搬到實作 issue）：
  - 主機依賴下限：`docker >= 19.03`、`just >= 1.33.0`（`[group]` 放在 `mod` 上要 1.33），都在建執行紀錄與任何寫入之前檢出：docker 由啟動器檢查；just 在首次導入由 `bootstrap.sh` 檢查，已有安裝目錄時由 just 解析 justfile 時自己報錯。提高下限會讓原本可用的主機不能再用，屬不相容變動：只能隨 X 變動，並事前公告、寫明要做哪些手動步驟（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)）；不動不變量 5 的性質。
  - 啟動器限 POSIX sh + `docker` + [04 使用者介面](../contract/04_interface.md#主機需求)列的基礎 userland；清單外的命令由 lint 擋。主機不呼叫 git；「安裝目錄在 git repo 裡」由啟動器往上找 `.git` 判斷。合併用的 `git merge-file` 在引擎容器內跑，不是主機依賴。引擎不讀 `.git`、不碰 index、不做 `git init`。
  - 啟動器只做：偵測主機環境；以字串相等比對讀版本鎖定行與印記；驗引擎回傳的執行計畫文法；照計畫呼叫 docker；寫執行紀錄；清掉自己建的容器與暫存。`sync` 快路徑、`prune` 的 docker 刪除也在啟動器，但都只依引擎給的計畫或純字串比對；比對一律保守，不確定就起引擎。
  - 已經有版本鎖定行時，啟動器一律用它指定的引擎：拉不到就是失敗，不改用啟動器內嵌的那一版。內嵌版本只用在還沒有版本鎖定行的第一次導入。
  - 薄殼四檔：`.vendor_kit/entry.just`、`vendor.just`、`log.sh`、`.gitignore`。薄殼帶自描述標頭（介面版、引擎版、其餘內容的 sha256），引擎重算比對、再與 image 內模板二次比對：前者抓「被改過」，後者抓「跟這一版引擎不是同一份」。不符就以[結束碼](../contract/03_messages.md#結束碼) `2`結束、列差異，除執行紀錄外不動 repo 檔與其他 VK 檔，訊息見[訊息總表](../contract/03_messages.md#訊息)。`gen/.stamp` 只記產生薄殼的引擎 ref 供快路徑比對，不承擔薄殼 hash。
  - 薄殼重產只由 `install`、`upgrade --engine` 做；`sync` 發現不符只回 `2`，並在診斷中列出下一步指令 `upgrade --engine`。
  - 升引擎兩段：新引擎換上後停下、以[結束碼](../contract/03_messages.md#結束碼) `2`結束並要求重跑，後續由新引擎接手。它是「版本鎖定行最後才改」（[ADR-0004](0004-vk-recipe-interface-and-write-boundary.md)）的明列例外：先改鎖定行再由新引擎接手；中途回 `2` 時鎖定行已經改了，進度檔記著目標版本，重跑 `upgrade --engine` 續作。
  - 舊薄殼跑新 major 的一般 recipe，由薄殼在起引擎之前擋下，乾淨回 `3`，訊息見[訊息總表](../contract/03_messages.md#訊息)，除執行紀錄外不動 repo 檔與 VK 檔；判定合不合的規則在 [ADR-0008](0008-protocol-and-file-schema-versions.md)。這裡與 [不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)、ADR-0008 說的「零寫入」，依[不變量 4](../contract/02_invariants.md#4-永不靜默失敗) 都不含執行紀錄。
  - 永久可用的救援路徑：`install`、`upgrade --engine`、`sync` 的不符判定，以及印用法。印用法只限這幾種確切形狀：`just vendor_kit`（不帶指令：stderr 第一行印 `vendor_kit <版本>`，第二行印 `vendor_kit: error[VK0024]: 未指定指令。`，接著印簡短用法，以[結束碼](../contract/03_messages.md#結束碼) `2`結束）；`just vendor_kit install -h`、`just vendor_kit upgrade --engine -h`、`just vendor_kit sync -h`（長選項 `--help` 同）。救援路徑以外的 recipe 的 `-h`／`--help` 在版本組合不合時回 `0` 還是 `3`，架構階段再定（[#106](https://github.com/ycpss91255-research/vendor_kit/issues/106)）。
