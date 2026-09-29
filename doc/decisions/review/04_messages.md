# 04 訊息與錯誤碼總表

> 共 8 條：待審 8

這一頁列出 <ins>VK</ins> 會印出、要<ins>使用者</ins>動手處理的訊息。每條訊息有固定編號，[不變量](02_invariants.md)、[使用者介面](03_interface.md)與 [ADR](../../adr/) 都用這個編號引用它。結束碼的意思見[使用者介面](03_interface.md)的[結束碼](03_interface.md#結束碼)一節，這裡不重述。

- 名詞見[名詞表](../../../CONTEXT.md)
- 類別用名詞表裡的三種結果：<ins>需人處理</ins>、<ins>失敗</ins>、<ins>警告</ins>
- 「意思」欄是訊息本文，逐字照印；`<…>` 是占位符，印出時換成實際的值
- 「下一步」欄是訊息裡可以直接複製來執行的指令；訊息裡沒有指令的標「—」
- 狀態只有兩種：待審（還沒送維護者定案）、定案

| 編號 | 結束碼 | 類別 | 時機 | 意思 | 下一步 | 出處 | 狀態 |
|---|---|---|---|---|---|---|---|
| 6-3 | `1` | 需人處理 | `update`、`upgrade`、`add` 要列出某個<ins>工具</ins>有哪些版本，但沒有給 <ins>registry</ins> 憑證，而那個 registry 要求認證 | `無法列舉 <repo> 的版本：需要 registry 讀取權限。可設定 VENDOR_KIT_REGISTRY_TOKEN（或 VENDOR_KIT_REGISTRY_TOKEN_FILE），或直接指定版本：just vendor_kit upgrade <repo>@<tag>（拉取使用主機 docker 認證）` | `just vendor_kit upgrade <repo>@<tag>` | [02 第 2 條](02_invariants.md#2-一個來源版本鎖定行只有一份進-git) | 待審 |
| 6-5 | `1` | 需人處理 | <ins>CI 模式</ins>下，<ins>基準版</ins>落後<ins>版本鎖定行</ins>（本機不印這條，只 warn、結束碼 `0`） | `請在本機執行 just vendor_kit upgrade <repo> -y 後 commit 並 push` | `just vendor_kit upgrade <repo> -y` | [02 第 3 條](02_invariants.md#3-自動化只碰不進-git-的東西) | 待審 |
| 6-10 | `3` | 需人處理 | `upgrade <repo>@<tag>` 或 `upgrade --engine@<tag>` 降版，但目標<ins>引擎</ins>無法無損讀取現有的 <ins>VK 檔</ins>；在任何寫入之前結束 | `目標引擎 <vY>（介面版 <P>、檔案版 <M>）無法無損讀取現有檔（檔案版 <N>）。未修改任何檔。請改指定能讀取檔案版 <N> 的版本：just vendor_kit upgrade <對象>@<tag>` | `just vendor_kit upgrade <對象>@<tag>`（`<對象>` 是這次降版的 `<repo>` 或 `--engine`） | [ADR-0008](../../adr/0008-protocol-and-file-schema-versions.md) §7 | 待審 |
| 6-13 | `1` | 需人處理 | `sync` 發現某個工具未完成<ins>導入</ins>；本機與 CI 模式都一樣 | `<repo> 未完成導入，請執行：just vendor_kit add <repo>` | `just vendor_kit add <repo>` | [02 第 3 條](02_invariants.md#3-自動化只碰不進-git-的東西)、[ADR-0004](../../adr/0004-vk-recipe-interface-and-write-boundary.md) §5 | 待審 |
| 6-19 | `3` | 需人處理 | 引擎讀到的 VK 檔，<ins>檔案版</ins>高於這個引擎支援的上限；在任何寫入之前結束 | `無法讀取 <file>：檔案版 <N> 高於本引擎支援的 <M>；寫入者為 vendor_kit <written_by>。請升級引擎：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | [ADR-0008](../../adr/0008-protocol-and-file-schema-versions.md) §6 | 待審 |
| 6-23 | `1` | 需人處理 | `bootstrap.sh` 發現主機的 just 低於 1.33.0；在任何寫入之前結束 | `需要 just ≥ 1.33.0，目前為 <version>。請使用 GitHub release 版。`<br>`下載：<平台對應的下載網址>`<br>`安裝：<安裝指令>`<br>（安裝指令不覆蓋主機既有的 just，也不要求主機另裝其他工具） | 訊息第三行的 `<安裝指令>` | [ADR-0007](../../adr/0007-host-thin-layer-and-shell-integrity.md) §1 | 待審 |
| 6-36 | `3` | 需人處理 | 舊的<ins>薄殼</ins>遇上 X 較新的引擎，執行<ins>救援路徑</ins>以外的 recipe（含其他 recipe 的 `-h`／`--help`）；不動 <ins>repo 檔</ins>與 VK 檔 | `薄殼介面版 <P_shell> 低於引擎 <vY> 的一般 recipe 需求。請先執行：just vendor_kit upgrade --engine` | `just vendor_kit upgrade --engine` | [ADR-0007](../../adr/0007-host-thin-layer-and-shell-integrity.md) §7 與修訂（2026-09-30） | 待審 |
| 6-39 | `1` | 失敗 | `docker --version` 的輸出含 `podman`；在任何寫入之前結束 | `偵測到 podman（docker --version）。vendor_kit 只支援 docker，不支援 Podman。請改用 docker（rootful 或 rootless）後重試。` | — | [ADR-0007](../../adr/0007-host-thin-layer-and-shell-integrity.md) §1 | 待審 |
