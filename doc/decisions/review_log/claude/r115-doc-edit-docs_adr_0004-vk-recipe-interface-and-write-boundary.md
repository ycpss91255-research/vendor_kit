# r115 審查：docs/adr/0004-vk-recipe-interface-and-write-boundary.md

審查對象：r114（commit ebe85e3）的改動。`_backup/docs_adr_0004-…pre_r115.md` 不存在，`git diff HEAD` 為空，改看 `git diff ebe85e3~1 ebe85e3`。

已核對：
- 編號對照全對：6-13→M5、6-5→M3、6-28→M8（第 19、24 行），6-39、6-40→M11、M12，6-23→M7（第 26 行）；檔內已無 `6-N` 殘留。
- 沒有違反「已定案」第 1～29 條；第 23 條（M7、M11、M12 失敗不留執行紀錄）與第 26 行一致。
- 錨點 `02#3`、`02#4`、`02#6`、`02#8`、`03#訊息`、`03#結束碼`、`04#主機需求`、`04#命名空間` 都存在；ADR-0007 路徑存在。
- 第 23、31 行跟新版 02 第 4 條（零寫入限判定不合、回 `3` 的那次執行，救援路徑照常寫入）不衝突：升引擎是救援路徑，本來就寫入。

## 必改

### 1. 第 19 行「改號等於改介面」跟 03 新增的編號說明矛盾
- 位置：docs/adr/0004-vk-recipe-interface-and-write-boundary.md 第 19 行（Consequences 第 4 點）
- 問題：r114 在 03 加了「『編號』欄只供文件之間互相引用，不會印在訊息裡」（docs/contract/03_messages.md 第 43 行）。編號既然不印出、不是使用者看得到的輸出，改號就不是改對外介面；0004 這句沒跟著改，兩頁說法相反。要不要把編號印出來是 Q16，還在待討論，0004 不該先替它下結論。
- 建議：改成「需要寫進 git 的情境各有固定的訊息與結束碼，改訊息或結束碼等於改介面。[03 訊息與錯誤碼總表](../contract/03_messages.md)列了未完成導入（[訊息 M5](…)）、基準版落後（[訊息 M3](…)）與薄殼不符（[訊息 M8](…)）。」
- 證據：docs/contract/03_messages.md 第 43 行；doc/decisions/review_log/discussion_queue.md 第 171～174 行（Q16）。

## 建議

### 1. 第 26 行情境順序跟訊息編號順序相反
- 位置：第 26 行（可寫 recipe 時序第 1 步）
- 問題：「Docker 版本不足與偵測到 Podman……印訊息 M11、M12」，但 M11 是 Podman、M12 是 Docker 版本不足，讀的人會一對一對錯。改號前（6-39 Podman、6-40 Docker）就是這樣，不是 r114 造成的，但換號時是順手修正的機會。ADR-0007 第 16 行也一樣。
- 建議：改成「偵測到 Podman 與 Docker 版本不足……印訊息 M11、M12」，或維持原文字、改成「訊息 M12、M11」。
- 證據：docs/contract/03_messages.md 第 63、64 行；docs/adr/0007-host-thin-layer-and-shell-integrity.md 第 16 行。

### 2. 第 26 行太長
- 位置：第 26 行
- 問題：一句話包了兩種檢查、兩種首次或已有安裝目錄的情境、失敗後的處理與訊息，第一次讀要拆好幾次。
- 建議：拆成三個子項：「Docker 版本不足、偵測到 Podman」「just 版本不足（首次導入）」「just 版本不足（已有安裝目錄）」。
- 證據：docs/adr/0004-vk-recipe-interface-and-write-boundary.md 第 26 行。

### 3. 第 30 行「照不變量 4 處理」沒有連結
- 位置：第 30 行（時序第 5 步）；第 11 行「不變量 8」同樣
- 問題：同一檔其他地方引用不變量都有具名連結，這兩處沒有，找不到是哪一頁的第 4、8 條。
- 建議：改成「[不變量 4](../contract/02_invariants.md#4-永不靜默失敗)」、「[不變量 8](../contract/02_invariants.md#8-使用者介面不可取代寫法一致)」。
- 證據：docs/adr/0004-vk-recipe-interface-and-write-boundary.md 第 3、11、30 行。
