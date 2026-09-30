# r122 審查：doc/adr/0007-host-thin-layer-and-shell-integrity.md

範圍：`diff -u doc/decisions/_backup/doc_adr_0007-host-thin-layer-and-shell-integrity.pre_r122.md doc/adr/0007-host-thin-layer-and-shell-integrity.md`，只改第 28 行一處（「薄殼五檔 … `ci/check.sh`」→「薄殼四檔：`entry.just`、`vendor.just`、`log.sh`、`.gitignore`」）。

核對結果：
- 已定案：符合 discussion_queue.md 第 58 行（定案第 32 條）「薄殼少掉 `ci/check.sh`」。沒有違反其他條。
- 對外承諾：沒有改 01、02；沒有改 03／04 的介面。
- 做完沒：ask 對本檔的要求只有「薄殼五檔改四檔、拿掉 `ci/check.sh`」，已做。全檔 grep `check.sh`、`CI 檢查`、`--dist`、`CI=`、`五檔` 都沒有殘留（第 8 行的「CI 的乾淨 checkout」是 CI 環境，不是檢查腳本，不用改）。
- 連結：第 28 行的 `../contract/03_messages.md#結束碼`、`#訊息` 用腳本算 slug 比對 03 的標題，兩個錨點都存在。
- 跨檔：四檔清單跟 ADR-0004 第 21 行「薄殼四檔」一致。

## 必改

無。

## 建議

1. 位置：repo 根目錄 `discussion.drawio`、`dist_distribution.drawio`（這兩個都進 git，不在本檔範圍）。
   問題：圖上還畫著 `ci/check.sh`、「薄殼五檔：.gitignore、entry.just、vendor.just、log.sh、ci/check.sh」、`check.sh --dist` 等舊寫法。CLAUDE.md 規定「決議改動架構圖時，同一個 PR 一起更新圖」；這兩份如果算架構圖，這個 PR 沒改到就跟 ADR-0007 第 28 行不一致。
   建議：確認這兩份是現行圖還是歷史討論稿；現行就在同一個 PR 裡把 `ci/check.sh` 改成 `just vendor_kit test`、薄殼改成四檔；歷史稿就在圖上或說明檔寫明是歷史。
   證據：`grep -o 'ci/check.sh' discussion.drawio`（例：cell `i4f_4`「薄殼五檔：.gitignore、entry.just、vendor.just、log.sh、ci/check.sh」）；`dist_distribution.drawio` cell `vk_n10`「ci/check.sh」；CLAUDE.md「決議改動架構圖時，同一個 PR 一起更新圖」。
