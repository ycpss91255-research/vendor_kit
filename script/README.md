# script — 審閱與圖面工具

## 審閱頁的改動標示（`mark_changes.py`）

審閱頁（`doc/decisions/review/0N_*.md`）每改一輪，就產一份標示版讓人只看差異：改動處底線 `<ins>`、被取代的舊文字刪除線 `<del>`。

### 一輪的流程

1. **改之前先備份**。每輪一個後綴，依序遞增：

   ```sh
   cp doc/decisions/review/03_invariants.md \
      doc/decisions/_backup/review/03_invariants.pre_r65.md
   ```

2. **改**（派子代理做，主對話只協調）。

3. **產標示版**：

   ```sh
   python3 script/mark_changes.py pre_r65 01_purpose 02_terms 03_invariants
   ```

   輸出到 `doc/decisions/review/_marked/<name>.marked.md`。後綴就是步驟 1 用的那個，決定「跟哪一版比」。

4. **只把標示版交給審閱者**。定案之後才給完整檔。

5. **定案就 commit**。commit 之後下一輪的比較基準改成 git：

   ```sh
   git show HEAD:doc/decisions/review/03_invariants.md \
     > doc/decisions/_backup/review/03_invariants.pre_r66.md
   ```

### 標示規則

- 表格列在儲存格內標記，不把整列包起來。整列包住會讓那一列不再是合法的表格列，GitHub 與 VS Code 都會把表格切斷。
- 標題、清單、引言的行首記號留在標籤外（`## <ins>目錄</ins>`），否則標題會變成普通文字。
- 粗體不拿來標改動，它的用途是名詞首次出現。

## 圖面工具

見 [`diagram/README.md`](diagram/README.md)。
