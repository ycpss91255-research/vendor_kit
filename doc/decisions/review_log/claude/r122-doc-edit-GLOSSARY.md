# r122 doc-edit 審查：GLOSSARY.md

範圍：`diff -u doc/decisions/_backup/GLOSSARY.pre_r122.md GLOSSARY.md`（只動第 125～127 行）。

## 必改

無。

- 已定案：改動符合 discussion_queue.md 定案第 32 條（`test` 跑全部檢查、`test dist` 只檢查交付內容、本機與 CI 用同一個、名稱不叫 `ci`）。沒有抵觸其他定案條。
- 對外承諾：沒有改到 01／02 的承諾，也沒有加入 ask 以外的介面（沒列其他子命令，也沒提 `CI=1`）。
- 做完沒：「CI 檢查腳本」條目已換成 `test`；GLOSSARY 裡已經沒有 `check.sh`、`ci/check`、「CI 檢查腳本」（grep 結果為 0）。「薄殼」條目（第 30～31 行）原本就沒列檔案清單，不用改。GLOSSARY 內沒有別處引用舊條目。
- 連結：diff 沒有新增或改動連結。現行文件（不含 _backup、_marked、review_log、research）裡沒有指向 `GLOSSARY.md#ci-檢查腳本` 的錨點。

## 建議

1. 位置：GLOSSARY.md 第 125～127 行（`test` 條目），目前放在「### repo 內的檔與狀態」。
   問題：舊條目是一個檔（`ci/check.sh`），放在這一群合理；新條目是 VK recipe，其他 VK recipe（`add`／`remove`、`update`、`sync`、`install` 等）都在「### VK recipe 與用途」（第 207 行起）。另外，條目用到的「VK recipe」要到第 172 行才定義，這裡等於先用後定義。
   建議：移到「### VK recipe 與用途」群（例如放在 `install` / `uninstall` 之後）。ask 寫了「分群照舊」，所以列為建議，由維護者決定。
   證據：GLOSSARY.md 第 88、125～127、172～173、207～227 行。

2. 位置：GLOSSARY.md 第 126 行「`test dist` 只檢查工具在 `dist/` 交付的內容」。
   問題：第 62～63 行已經定義了「工具內容」＝「工具在 `dist/` 交付、展開後放進 `cache/` 的那些檔」。這裡換了一種說法講同一件事，跟不變量 8（一個概念一種寫法）有衝突。
   建議：如果 `test dist` 檢查的就是工具內容，改成「`test dist` 只檢查工具內容」；如果檢查的是還沒打包的 `dist/`，不是工具內容，就保留現在的寫法，並在 ADR／04 講清楚兩者的差別。
   證據：GLOSSARY.md 第 62～63、126 行；discussion_queue.md 第 58 行（定案第 32 條引用不變量 8）。
