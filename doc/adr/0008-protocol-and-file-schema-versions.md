# 介面版與檔案版分開計數，版本組合不合的執行零寫入並以 fatal（結束碼 3）結束

同一個 X 之內不能悄悄改掉原本能用的東西，退版也要退得回（[不變量 10](../contract/02_invariants.md#10-相容性與演進同一個-x-內不破壞x-變動才可能不相容且先公告)）；但若把引擎內部也算進契約，內部一動就是破壞性變更。所以用兩個與 release 版號分開的整數：介面版 P 只描述薄殼與引擎之間的公開介面，檔案版 schema 只描述 VK 寫的每個 TOML 的格式。新舊一律以這兩個整數比，不以版本字串比：字串沒有可靠的比較關係，介面沒變的 Y 版也會被誤判成介面變動。介面版不合要在拉 image、起容器之前判定；檔案版要讀 VK 檔才判得出，由引擎在起容器之後、任何寫入之前判定（VK0008）；判定出版本組合不合而以 fatal（結束碼 `3`）結束的那次執行不動 repo 檔與 VK 檔，執行紀錄例外（[不變量 4](../contract/02_invariants.md#4-永不靜默失敗)）。救援路徑在版本組合不合時仍然可用，並照原有行為寫入。離線判定的資料由引擎寫在版本鎖定行旁，啟動器先比對介面版列表，通過後才取得 image 並核對 LABEL；資料的寫入與核對責任見下面的內部機制（來源：[離線介面版判定討論 #42](https://github.com/ycpss91255-research/vendor_kit/issues/42)）。

## Considered Options

- **只用 release 版號 `X.Y.Z` 當判準**：少維護兩個數字，但引擎要取得對方版號並比較 SemVer，介面沒變的 Y 版會被判成介面變動。
- **讓 `written_by` 也當讀取門檻**：同一個判斷交給兩個欄位，違反[設計原則 P5](../decisions/design_principles.md#p5-一條規則一個擁有者)；其中一個遲早漏更新，而且是靜默的。
- **鏈式遷移（v1 → v2 → v3 逐級套用）**：路徑少，但每一級的中間結果都得永遠正確，任何一級的 bug 會污染之後所有版本。
- **讀到未知欄位就拒絕**：新一版寫的檔在舊引擎上立刻不可讀。
- **讀時忽略未知欄位、寫時丟掉**：舊引擎跑過一次就把新欄位刪了，之後退回去也拿不回來。
- **起容器之後才判介面版**：判定前 image 已經拉了、容器已經起了，引擎有機會動檔。

## Consequences

- 介面改動跟 release 節奏脫鉤：修 bug 的版可以連著發，P 不動，薄殼與引擎的配對不受影響。
- P 的觸發條件要靠人記得；改了卻忘了 P+1，當下不報錯，要靠測試或 lint 把清單釘住。
- 不鏈式遷移表示每個舊檔案版都要維護自己那條到現版的路徑。
- `floor_P` 只能經 ADR 提高，舊介面的支援期間是明確的維護成本。
- 使用者會在 TOML 裡看到 `schema` 與 `written_by`，只有前者是門檻；文件與訊息要講明，否則 `written_by` 會被當成可以改的旋鈕。
- 介面版列表從引擎接受的區間展開，不另立相容性規則；由引擎寫入、啟動器比對，避免在主機重做版本規則。本機沒有引擎 image 時也能先離線判定，再取得鎖定的 image；取得後核對 LABEL，避免列表與鎖定的內容漂移。
- 驗收各有一個黑箱案例：檔案版高於引擎、P 落在區間外、降版到讀不回來的引擎，三個都看結束碼 `3` 與零寫入。
- 內部機制（之後搬到實作 issue）：
  - 薄殼每次呼叫附 `--protocol P`。引擎接受 `[floor_P, current_P]` 區間內的呼叫，並以呼叫方那個 P 回應；`floor_P` 是固定的 release 常數。
  - P 的升版觸發清單（任一項 → P+1，要加一項改本檔）：新增 recipe、新增選項、新增記錄種類、新增欄位、改結束碼語意、改印記第一行語意或位置。印記放在 `cache/<repo>.stamp.toml`，metadata 放在 `baseline/<repo>.toml`；檔名集中由引擎的 `layout` 模組管理。
  - 救援路徑（`install`、`upgrade --engine`、`sync` 的不符判定與四種印用法呼叫，清單見 [ADR-0007](0007-host-thin-layer-and-shell-integrity.md)）用到的薄殼與引擎之間的協定動作與文法，跨介面版永久不變；其他協定內容照原本的 P 規則演進。凍結項另含：
    - 啟動器交給引擎的 `in/engine`：檔名與位置固定為容器內 `/vk/in/engine`，內容是一行帶 tag 與 digest 的 image 引用，加結尾 LF。
    - `bootstrap.sh` 經入口 argv 的 `--` 之後呼叫的保留入口 `@shell-check`、`@shell-repair`，且 `--` 之後只能有那一個參數。
    - `install --dry-run [-y]` 與 `upgrade --engine[=<tag>] --dry-run [-y]` 的救援呼叫文法。
    - `load` 的 stdout 回傳檔 `res.<seq>.out` 是後來新增的協定資料；引擎讀取時必須容許檔案不存在，才能配合尚未寫出它的舊啟動器。
  - 引擎把介面版列表寫在 `version.toml` 的引擎版本鎖定行旁，形式見 [ADR-0002 的鎖定行規則](0002-vendor-kit-dir-layout-and-lock-line-form.md)：`install` 首次導入時寫入；`upgrade --engine` 第一段寫目標引擎的區間，第二段寫本引擎的區間。
  - 一般路徑由啟動器先離線拿薄殼的 P 與列表逐項做字串相等比對，不碰 Docker、不連 registry。列表缺漏或格式錯以 `VK0070` 停下（結束碼 `2`）；P 低於列表下限以 `VK0009`、高於上限以 `VK0076` 結束（結束碼 `3`）。比對通過、本機缺 image 時才 pull 鎖定的 digest；起容器之前拿 LABEL 核對列表頭尾，不符以 `VK0080` 停下（結束碼 `2`）。`VK0070` 與 `VK0080` 都是 error：這兩種是版本檔本身壞掉或跟鎖定的 image 對不上，不是版本組合不合，所以是 `2`；兩者都在起容器之前停下，除執行紀錄外不動檔。救援呼叫跳過介面版比對、不讀列表。
  - 引擎 image 用 `vendor_kit.protocol.floor`、`vendor_kit.protocol.current` 公告介面版區間，用 `vendor_kit.schema.max` 公告檔案版上限，並以 `org.opencontainers.image.version` 公告 release 版號。LABEL 值由[引擎的相容常數](../../engine/compat/src/lib.rs)產生。介面版的離線檢查先於任何上網，LABEL 核對則在取得 image 後、起容器前完成。
  - 每個 VK 寫的 TOML 記 `schema` 與 `written_by`；`written_by` 只供回報與診斷，讀取門檻只看 `schema`。
  - 未知欄位讀時忽略、寫時保留，保留不了就拒絕、不悄悄少寫。同一個 X 之內新欄位的上線順序是先讓舊引擎讀得過，才開始寫。
  - 同一個 X 之內新增欄位不提高檔案版；只有不相容的格式變動才提高，而那只准在 X 變動時做。所以檔案版過高的拒絕只發生在跨 X：檔案版高於本引擎時，除執行紀錄外，任何寫入之前就回 `3`（[訊息](../contract/reason_codes.csv) `VK0008`）。
  - 跨檔案版直接遷移、不鏈式。
  - 引擎降版（`upgrade --engine=<tag>` 指定舊 tag）只在目標引擎能無損讀現有檔時才做，否則改檔前回 `3`（[訊息](../contract/reason_codes.csv) `VK0007`）、零寫入；執行紀錄不算在零寫入內（[不變量 4](../contract/02_invariants.md#4-永不靜默失敗)）。工具降版（`upgrade <repo>@<tag>`）時引擎不變，不做這項檢查（[不變量 7](../contract/02_invariants.md#7-工具-image-只承載交付資料引擎與工具不互相綁發版)）。
