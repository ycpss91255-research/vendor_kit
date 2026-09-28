只准用 search_web 與 read_url_content 兩個工具，不要用 run_command。不要執行任何 shell 指令，不要讀寫本機檔案。這是純網路資料調查任務。

# 任務：just（casey/just）1.33.0 之後有哪些重大變更
背景：我們的工具 vendor_kit 要求使用者機器 just ≥ 1.33.0（理由：[group] 放在 mod 上需 1.33，PR #2263），並用 lint 禁止使用比 1.33 新的功能；但若新版有「重大功能」值得把下限提高，就允許調整。我們用到：mod/mod?、import/import?、[group]、set positional-arguments、justfile_directory()、[no-cd]、--list --list-submodules、set allow-duplicate-recipes、recipe 內 cd "{{justfile_directory()}}"。
請讀 https://github.com/casey/just/releases 與 https://github.com/casey/just/blob/master/CHANGELOG.md，列出 1.33.0（含）之後每個版本的：
1. 新功能（含哪一版、PR 號）— 特別標出與我們用法相關的：模組（mod）行為、import、group、working-directory 屬性（[working-directory]、set working-directory）、[script]、[default]、[parallel]、[exit-message]、require()/which()、submodule 相依（a: sub::r）、--list 行為、set unstable、JUST_JUSTFILE_NAME、positional arguments 相關。
2. 破壞性變更或行為改變（breaking / behavior change）— 逐條列，這是最重要的：哪一版、改了什麼、對舊 justfile 的影響。
3. 最新穩定版號與日期。
4. 對「最低版本要不要從 1.33 提高」給事實依據：哪些新功能能明顯簡化「模組 recipe 回專案根目錄」「產生的 just 檔零 set」「fresh clone 缺模組檔」這幾個我們現在要繞的問題。
輸出：表格（版本｜日期｜新功能（與我們相關者標 ★）｜破壞性變更｜來源 URL），最後一段列「值得提高下限的候選功能」（只列事實：功能、版本、它解決我們哪個問題）。
