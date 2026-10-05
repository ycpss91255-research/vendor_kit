# 工具 image 只搬不跑

工具 image 裡是別人寫的內容；VK 一旦執行它，就是在使用者主機上跑不可信輸入，而使用者沒同意過這件事。工具 image 若 `FROM vendor_kit`，升級程式又綁回工具本身，引擎每升一版所有工具都得跟著動（[不變量 7](../contract/02_invariants.md#7-工具-image-只承載交付資料引擎與工具不互相綁發版)）。所以工具 image 只是 `FROM scratch` 的純資料 image，主機用已有的 docker（`docker create` → `docker cp`）把檔讀出來、唯讀掛進引擎容器；引擎只有一個實作，不因工具分身（[不變量 6](../contract/02_invariants.md#6-引擎版本由安裝目錄鎖定啟動器不判斷-repo-內容的意義)），取件也不多要主機裝任何東西（[不變量 5](../contract/02_invariants.md#5-主機依賴最小除平台既有的基本工具外只需-dockergitjust)）。

## Considered Options

- **工具 image `FROM vendor_kit`，自帶升級程式**：要一整套協定號與相容矩陣才撐得住，引擎每升一版就要所有工具 repo 跟著動。
- **`docker run` 工具 image，讓它自己把檔吐出來**：取件程式很短，但那是在使用者主機上執行不可信輸入。
- **每個工具配一個內含引擎的專屬 image**：版本組合由出貨端固定，但「這個安裝目錄用哪一版引擎」就不再由它自己的版本鎖定行決定。
- **只鎖 digest，不做逐檔 sha256 與寫入前重驗**：digest 只證明拉到的是同一個 image，證不到取出來、寫進 repo 的那一份還是同一份。
- **用第三方 registry client（vendir、crane）取代 `docker create`／`cp`**：見 [ADR-0001](0001-why-not-existing-tools.md)。

## Consequences

- 出貨那一端只要交 `dist/` 與三行 `Dockerfile.dist`，不必知道引擎怎麼運作，也不必因引擎升級重發版；工具想在導入時做事，只能透過 `dist/` 裡的 recipe 由使用者自己呼叫。
- 認證與快取沿用使用者本來就在用的 docker 路徑：在支援的 registry 上，`docker pull` 成功的機器上取件就會成功；支援哪些 registry 由驗收決定。代價是要建一個暫存 container 再刪掉，也需要 docker daemon 在。
- 驗收：取件後逐檔比對出貨 image 與導入結果，以 `FROM scratch` 純資料 fixture image 走完整流程。
- 內部機制（之後搬到實作 issue）：
  - `Dockerfile.dist` 逐字三行：`FROM scratch` + LABEL + `COPY dist/`。沒有 entrypoint、shell 或可執行層，「能不能跑」在契約上不存在。
  - 取件：主機啟動器 `docker create` → `docker cp` 到這次呼叫專用、repo 外、由啟動器擁有的暫存處 → 唯讀掛進引擎容器，讀取與判斷都在引擎那一份實作裡做；不 `docker run` 工具 image；全部同意後由引擎重驗，再寫進 `cache/`。
  - 位元組相同靠三層：digest 鎖住 image 內容；取到暫存處時逐檔算 sha256，全部同意、寫入時才記進印記；寫入前再重驗一次。三層各擋一類失手：拉到的是不是同一個 image、取出來的是不是同一份檔、掛進來到落地之間有沒有被動過。同一份檔因此算兩次 sha256，檔多的工具會付出可觀察的時間。
  - 出貨端另由 CI 驗兩平台位元組一致（[ADR-0011](0011-test-layers-and-ci-matrix.md)）；導入端的三層驗不出兩個平台各自打包出不同東西。
  - 引擎以 `vendor_kit:vN` 發布；工具端不出現引擎程式，引擎端不出現工具專屬分支。
