## 結論

不要改弱不變量。應把引擎接受的介面區間 `floor_P`／`current_P` 連同 image 引用放進 `version.toml` 的同一條引擎版本鎖定行；啟動器離線比較薄殼標頭的 `P` 與該區間，image 拉到後再核對 LABEL，一致才允許啟動。

例如（具體欄位名稱是推論）：

```toml
vendor_kit = { image = "<tag>@sha256:<digest>", protocol_min = 3, protocol_max = 5 }
```

## 理由

- 現行 ADR 的判斷來源在 image 裡，因此 image 不在本機時根本不存在可讀資料。ADR 明訂「引擎 image 用 LABEL 公告自己的區間」及啟動器讀 LABEL 判定，但沒有第二個離線來源。[ADR-0008:38](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:38)、[ADR-0008:79](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:79)

- Docker 的 LABEL 必須透過 `docker image inspect` 查看；缺少本機 image 時，取得 image 必須使用會從 registry 下載的 `docker image pull`。因此「缺 image、讀 LABEL、又不連 registry」三者不能同時成立。[Docker `image inspect`](https://docs.docker.com/reference/cli/docker/image/inspect/)、[Docker `image pull`](https://docs.docker.com/reference/cli/docker/image/pull/)

- 離線比較所需的另一半已經存在：薄殼自描述標頭包含薄殼介面版；介面版也明確定義為薄殼與引擎間的整數版號。[CONTEXT.md:248](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:248)、[CONTEXT.md:382](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:382)  
  **推論：**只缺「尚未下載之目標引擎接受哪個區間」這份本機資料，不需要新增相容矩陣或改用 SemVer。

- `version.toml` 是最合適的承載處：它進 git並存放全部版本鎖定行；版本鎖定行本來就是引擎到鎖定版本的對應。[CONTEXT.md:207](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:207)、[CONTEXT.md:266](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:266) 目的頁又規定每個安裝目錄只有一份版本鎖定資料，換它即可升退版與重建。[01_purpose.md:16](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:16)  
  **推論：**把區間放在同一 TOML 項目的 inline table，比另設 manifest/cache 更能保證 image digest 與區間原子更新，也仍維持「一條版本鎖定行」。

- 不變量要求的是可觀察能力：「任何上網前」判定不合並零寫入；它不是多寫了不可能做到的目標，缺的是 ADR 機制資料。[02_invariants.md:313](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:313) ADR-0007 也把責任明確放在起引擎前的薄殼判定。[ADR-0007:66](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0007-host-thin-layer-and-shell-integrity.md:66)  
  因此應修 ADR-0008，而不是把 02 改成「拉完才判」。

- LABEL 仍有用途：拉取後、啟動前，核對 LABEL 與鎖定行宣告完全相同；不同即拒絕執行。  
  **推論：**這能抓到 release／Renovate／人工改鎖定行時的配對錯誤，同時避免讓尚未驗證的引擎取得寫檔機會。

## 風險或反例

- **鎖定行的區間宣告可能寫錯或被竄改。** Digest 只鎖 image，並不自動替旁邊的 `protocol_min/max` 背書；本專案第一版又明確不做數位簽章。[01_purpose.md:27](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:27) 所以離線階段能做的是依 repo 內鎖定資料判斷，真正執行前仍須以 LABEL 交叉驗證。

- **若把資料放在獨立 compatibility manifest，會產生雙檔不同步窗口。**  
  **推論：**除非 manifest 與版本鎖定行有共同交易式更新及強制 lint，否則它不如同一 TOML 項目可靠。

- **只從 image tag 或 `X.Y.Z` 推導不可行。** ADR 已決定介面版與 release 版號分開，且比較新舊不使用版本字串。[ADR-0008:21](/home/cyc/Desktop/vendor-kit_ws/src/doc/adr/0008-protocol-and-file-schema-versions.md:21)

- **若要求的是敵對環境下、在完全不信任 repo 鎖定資料時仍證明區間屬於該 digest，單加欄位不夠。**  
  **推論：**那就必須把由 digest 可驗證的 OCI manifest＋config metadata 一併保存於 repo，或引入簽章；前者明顯較重，後者超出第一版既定範圍。