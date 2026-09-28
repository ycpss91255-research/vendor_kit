我方傾向（請獨立判斷）：
A：A3 混合（沒有 justfile 就 symlink 接管 + justfile.local；已有就加一行），但擔心兩種模式讓文件變複雜；A2 純 base 式最乾淨但對已有 justfile 的專案侵入最大；A1 最保守。base 下游根 justfile 已是 symlink 進 .base/，vendor_kit 接管後 base 的 docker/base 命名空間改由 gen/tools.just mod 進來——這是否等於 vendor_kit 必須接管根檔（A2）才能與 base 共存？
B：(b) 全收進 .vendor_kit/：根目錄只剩一個點目錄、Renovate regex 唯一、避免 .<repo>/ 與 base 的 .base/ subtree 撞名；代價 mod 路徑長（使用者看不到）、grep 多一層（無感）。
C：C1 + C2 短路 + C5 標頭，C4 只對 compose/justfile/GitLab CI 開放且由工具作者選；C3 不採（.new 殘留檔比衝突標記更難處理，且 git 使用者熟悉標記）。
