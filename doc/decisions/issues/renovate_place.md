> 待 ci_bridge repo 做完再定；此 issue 先記錄結論與待決點。

## 已確定：Renovate 設定是通用的

- Renovate 是同一個工具，在 GitHub 與 GitLab 上讀的 repo 設定**格式相同**；平台差異只在「機器人怎麼跑」（GitHub 裝 Mend App；GitLab 自架 renovate-runner），不在 repo 裡的檔。
- 檔名由 Renovate 固定：`renovate.json`／`renovate.json5`／`.renovaterc(.json)`／`.github/renovate.json`／`.gitlab/renovate.json`，不能自訂。
- 內容只有一行 extends 指向 vendor_kit 的共用 preset（`github>ycpss91255-research/vendor_kit//renovate/preset`；GitLab 端跑的 Renovate 也能抓 `github>` preset，需給 GitHub token 避免限流）。
- Dependabot 做不到（不支援自訂檔），所以沒有「第二種機器人格式」的問題。

## 待 ci_bridge 定案

- 放置方式：通用資料夾 + symlink 到平台要的位置（`.github/renovate.json`／`.gitlab/renovate.json`），還是直接放根目錄 `renovate.json`（兩平台都認）。
- bootstrap 生成時要不要問 CI 平台（目前不問，先放根目錄）。
- 與 ci_bridge 的 CI 檔（GitHub workflow／GitLab CI）如何共存：CI 檔只呼叫 vendor_kit 出貨的 `test/ci/check.sh`（第 12 頁），Renovate 設定與 CI 檔是兩件事。

## 目前原型

bootstrap 生成 `renovate.json` 於專案根目錄；`doc/contract/bootstrap.md` 註明位置待定。
