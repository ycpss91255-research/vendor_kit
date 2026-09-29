# vendor_kit

vendor_kit（VK）把一套工具（開發環境設定、共用腳本、初始檔）送進很多個 repo：鎖定用哪一版、升版與退版、初始檔升版時不蓋掉使用者改過的地方。主機只需要 [Docker](https://www.docker.com/)、[Git](https://git-scm.com/)、[just](https://github.com/casey/just)。

為什麼要做、對使用者承諾什麼，見 [`doc/decisions/review/01_purpose.md`](doc/decisions/review/01_purpose.md)。名詞見 [`CONTEXT.md`](CONTEXT.md)。

## just 指令

所有指令都在 `just vendor_kit` 底下，不佔頂層 recipe 名。總覽見 [#47](https://github.com/ycpss91255-research/vendor_kit/issues/47)，每個指令各有一個 issue。

### 常用

| 指令 | 做什麼 | 反向 | issue |
|---|---|---|---|
| `just vendor_kit add <repo>` | 把一個工具納入這個安裝目錄 | `remove` | [#48](https://github.com/ycpss91255-research/vendor_kit/issues/48) |
| `just vendor_kit upgrade <repo>[@<tag>]` | 把鎖定版本換成新版或指定版本；指定舊 tag 就是退版 | — | [#49](https://github.com/ycpss91255-research/vendor_kit/issues/49) |
| `just vendor_kit dev <repo> -p <dir>` | 讓工具改用本機目錄 | `undev` | [#50](https://github.com/ycpss91255-research/vendor_kit/issues/50) |
| `just vendor_kit dev vendor_kit -i <image>` | 讓引擎改用本機 image | `undev` | [#50](https://github.com/ycpss91255-research/vendor_kit/issues/50) |

### 進階

| 指令 | 做什麼 | 反向 | issue |
|---|---|---|---|
| `just vendor_kit remove <repo>` | 把一個工具解除；不刪初始檔，只收回當初插入的行 | `add` | [#51](https://github.com/ycpss91255-research/vendor_kit/issues/51) |
| `just vendor_kit undev <repo>` | 回到鎖定版本 | `dev` | [#52](https://github.com/ycpss91255-research/vendor_kit/issues/52) |
| `just vendor_kit update` | 只查有沒有新版，不改任何檔 | — | [#53](https://github.com/ycpss91255-research/vendor_kit/issues/53) |
| `just vendor_kit sync` | 使本機的工具內容與版本鎖定行一致；每次 `just` 都會自動先跑 | — | [#54](https://github.com/ycpss91255-research/vendor_kit/issues/54) |
| `just vendor_kit install` | 把 VK 裝進 repo 的一個目錄 | `uninstall` | [#55](https://github.com/ycpss91255-research/vendor_kit/issues/55) |
| `just vendor_kit uninstall` | 把 VK 從那個目錄移除 | `install` | [#56](https://github.com/ycpss91255-research/vendor_kit/issues/56) |
| `just vendor_kit prune` | 清掉已不再使用的本機資源 | — | [#57](https://github.com/ycpss91255-research/vendor_kit/issues/57) |
| `just vendor_kit help` | 印出使用說明 | — | [#58](https://github.com/ycpss91255-research/vendor_kit/issues/58) |

沒有反向的 `update`、`sync`、`prune`、`help` 必須無害：不改任何進 git 的檔。

第一次導入時 repo 裡還沒有 VK，先跑 `bootstrap.sh`：它下載引擎，再呼叫 `install`；再跑一次就是修復。見 [#27](https://github.com/ycpss91255-research/vendor_kit/issues/27)。

### 常見選項

- `-y`：免問，照樣印出改了什麼。它只省略詢問，不授權覆蓋使用者的檔。
- `--dry-run`：只預覽要做什麼，不寫任何檔。

## 結束碼

每個指令結束時回一個數字，流程圖終點裡的數字就是它：

| 結束碼 | 意思 |
|---|---|
| `0` | 成功（可能帶 warn） |
| `1` | 失敗，或需要人處理；一定會印出原因和下一步 |
| `2` | 做完了，但要人接手：有合併衝突要解，或 `update --exit-code` 查到新版 |
| `3` | 現有薄殼、檔案、引擎的版本組合不合，要先升級或退回才能繼續；不動任何檔 |

出處：[`doc/decisions/review/02_invariants.md`](doc/decisions/review/02_invariants.md) 第 4 條。
