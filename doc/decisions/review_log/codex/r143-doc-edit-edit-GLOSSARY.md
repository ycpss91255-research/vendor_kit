已完成，僅修改 [GLOSSARY.md](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/GLOSSARY.md)，未執行任何 git 寫入、commit 或 push。

備份已建立：
`doc/decisions/_backup/GLOSSARY.pre_r143.md`

驗證結果：

- `check_terms.py`：通過
- `check_context.py`：通過
- `check_review_pages.py`：失敗；`04_interface.md:20` 的 `#追蹤新版` 錨點尚不存在
- `check_messages.py`：失敗；`04_interface.md:308` 尚引用已退役的 `VK0003`
- `check_typography.py`：通過
- 單元測試：151 項全部通過

兩項失敗均來自其他代理正在修改的 `04_interface.md`，未代為修正。

變更清單：

- `GLOSSARY.md:81`：縮短 `tag` 定義，詳細規則連至 04。
- `GLOSSARY.md:121`：補強「自描述標頭」定義及 04 連結。
- `GLOSSARY.md:135`：補強「鎖定版本」定義及 04 連結。
- `GLOSSARY.md:138`：補強「本機覆寫」定義及 04 連結。
- `GLOSSARY.md:162`：補強「合併衝突」定義及處理規則連結。
- `GLOSSARY.md:180` 前：刪除「選項」與「CI 模式」詞條。
- `GLOSSARY.md:199`：縮短「警告」、「原因代碼」、「結束碼」，細節連至 03。
- `GLOSSARY.md:210`：補強 `add`／`remove`、`dev`／`undev`、`sync`、`prune`、`install`／`uninstall` 定義及 04 連結。
- `GLOSSARY.md:229`：將 `test` 移至 VK recipe 群組，改為不提 CI 模式的定義。
- `GLOSSARY.md:243`：補強「救援路徑」定義及 04 連結。