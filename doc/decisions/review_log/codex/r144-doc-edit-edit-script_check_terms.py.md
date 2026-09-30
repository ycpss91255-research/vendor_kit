已完成，未 commit、未 push，也未執行任何 git 寫入指令。

驗證結果：

- 五支 lint 全數通過。
- `python3 -m unittest discover -s script/test`：157 項通過。
- `git diff --check` 通過。
- r144 備份與改前版本逐位元一致。

改動：

- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:112)：禁止對外文件殘留 `<ins>`，更新 `<u>` 診斷，並排除 Markdown 行內程式碼範例。
- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:153)：解析 GLOSSARY 粗體詞條、`A / B` 名稱及所屬分群錨點。
- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:180)：限定 README 與 01～04 對外頁，排除標題、程式碼區塊、行內碼及一般連結文字。
- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:226)：按正文順序辨識名詞，同位置優先最長名稱，避免重疊誤判。
- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:251)：驗證首次名詞連到 GLOSSARY，且錨點確實是該名詞所在分群。
- [script/check_terms.py](/home/cyc/Desktop/vendor-kit_ws/worktree/pr/59/script/check_terms.py:324)：將名詞連結錯誤納入主流程、失敗狀態與統計輸出。
- `doc/decisions/_backup/script_check_terms.pre_r144.md`：保存本輪修改前的完整原檔。