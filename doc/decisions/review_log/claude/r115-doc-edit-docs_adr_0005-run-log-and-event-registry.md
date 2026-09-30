# r115 審查：docs/adr/0005-run-log-and-event-registry.md（Claude）

審查範圍：r114（ebe85e3）對本檔的改動只有第 23 行 `訊息 6-23、6-39、6-40` → `訊息 M7、M11、M12`。`_backup/` 沒有 `pre_r115` 備份，`git diff HEAD` 為空，這一輪沒有新改動。

## 必改

無。

- 編號對照正確：6-23→M7（just 低於 1.33.0，03_messages.md 第 59 行）、6-39→M11（podman，第 63 行）、6-40→M12（Docker 低於 19.03，第 64 行），跟 ADR-0004 第 26 行、ADR-0007 第 16～17 行一致。
- 沒有違反已定案第 1～29 條；第 23 條（主機前置檢查 M7、M11、M12 不留執行紀錄、以 `2` 結束）跟本檔第 23 行一致。
- 本檔沒有改 01 的承諾、02 的不變量，也沒有改 03／04 的介面；02 第 4 條的零寫入改寫跟本檔沒有衝突（本檔只說執行紀錄早於寫入、建不出就以 `2` 結束，跟 02 第 99、102 行一致）。
- 錨點都存在：`02_invariants.md#4-永不靜默失敗`（02 第 88 行）、`03_messages.md#結束碼`（第 15 行）、`03_messages.md#訊息`（第 41 行）、`design_principles.md#p5-一條規則一個擁有者`（第 30 行）、`0004-vk-recipe-interface-and-write-boundary.md` 存在。所有連結都有名字，也沒有「出處：」行。

## 建議

1. **第 23 行：just 檢查沒區分首次導入與已有安裝目錄**
   - 問題：本行說三項前置檢查「失敗時……只在 stderr 印訊息、以 `2` 結束」，讀起來像 just 低於下限一律由 VK 印 M7、回 `2`。但 ADR-0004 第 26 行與 ADR-0007 第 17 行都寫明：just 檢查只有首次導入由 `bootstrap.sh` 做；已有安裝目錄時由 just 解析 justfile 時自己拒絕，不承諾 VK 的訊息與結束碼。03 第 59 行的 M7 時機也只寫 `bootstrap.sh`。本行跟這三處對不上（不是 r114 造成的，是 r112 把 just 下限分兩種情況時漏改）。
   - 建議：在括號後補一句，例如「……以 `2` 結束；just 版本只有首次導入由 `bootstrap.sh` 檢查，已有安裝目錄時由 just 自己拒絕，見 ADR-0004。」或乾脆只寫「主機前置檢查的範圍與訊息見 ADR-0004」，不在本檔複述。
   - 證據：docs/adr/0005-run-log-and-event-registry.md 第 23 行；docs/adr/0004-vk-recipe-interface-and-write-boundary.md 第 26 行；docs/adr/0007-host-thin-layer-and-shell-integrity.md 第 17 行；docs/contract/03_messages.md 第 59 行。

2. **第 23 行：括號裡檢查項目跟編號的順序不對應**
   - 問題：「just、Docker 版本、Podman；訊息 M7、M11、M12」看起來是一對一，但 M11 是 Podman、M12 是 Docker 版本，第一次看的人會把 Docker 版本對到 M11。
   - 建議：改成「just、Podman、Docker 版本；訊息 M7、M11、M12」，或逐項寫「just（M7）、Podman（M11）、Docker 版本（M12）」。
   - 證據：docs/adr/0005-run-log-and-event-registry.md 第 23 行；docs/contract/03_messages.md 第 63～64 行。

3. **名詞：事件註冊表、真本、讀取端不在 GLOSSARY.md**
   - 問題：「事件註冊表」「真本」「讀取端」是本檔的核心詞，GLOSSARY.md 沒有收錄（「執行紀錄」在第 128 行有）。本檔是內部 ADR，第 20 行已就地定義事件註冊表，所以不擋；但若其他 ADR 也用這些詞，就該進名詞表。
   - 建議：確認其他文件有沒有用到；有就補進 GLOSSARY.md，沒有就維持就地定義。
   - 證據：GLOSSARY.md（grep 無「事件註冊表」「真本」「讀取端」）；docs/adr/0005-run-log-and-event-registry.md 第 3、16、20 行。
