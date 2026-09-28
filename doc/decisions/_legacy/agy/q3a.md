### 3a. 「啟動器自我升級」的做法（Batect、Gradle wrapper）
舊版啟動器去升級新版工具時，新版可能需要新的參數／掛載，怎麼辦？請查：
- Batect：`./batect --upgrade` 如何換自己（wrapper script vs. jar）；是否先換 wrapper 再換 jar；wrapper 與 jar 版本如何綁定。
- Gradle wrapper：`gradle wrapper` 任務由「當前版本」跑，會產生新的 wrapper script+jar+properties，順序如何；官方是否建議「用新版本再跑一次 wrapper」（double-run）；wrapper jar 何時更新。
