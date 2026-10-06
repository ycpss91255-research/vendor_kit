# 驗收 fixture

驗收層用的工具 fixture（#372 的 N22）。每個子目錄是一個工具 repo 的出貨端：`dist/` 加三行 `Dockerfile.dist`（ADR-0006），建成 `FROM scratch` 的純資料 image 後推到 GHCR，由驗收案例當成真的工具導入。發布由 `ci:fixtures` 做，已發布的 tag 不覆蓋、不刪（ADR-0009）。

| 目錄 | 用途 | `<ns>` |
|---|---|---|
| `fixture-public/` | 公開 package，不帶憑證就拉得到 | `fixture-public`、`fixture-public-extra` |
| `fixture-private/` | 私有 package，要憑證才拉得到 | `fixture-private`、`fixture-private-extra` |

- 每組都有多個 `<ns>`：`dist/just/<ns>.just` 每檔一個頂層命名空間，含跟目錄同名的 `<repo>.just`；另放一個一般檔（`dist/share/<repo>/message.txt`），驗逐檔比對與印記。
- 兩組的 `<ns>` 不重疊，也不用保留名 `vendor_kit`，同一個安裝目錄可以兩個都導入。
- 不含 `init.toml`：欄位名還沒定（N3）。
- 文字檔一律 LF（ADR-0012）。
- 目錄名就是預定的 `<repo>`；GHCR 上的 package 路徑怎麼對應 `<repo>` 還沒定（N2）。

`Dockerfile.dist` 逐字三行，build context 是 fixture 目錄：

```dockerfile
FROM scratch
LABEL org.opencontainers.image.source=https://github.com/ycpss91255-research/vendor_kit
COPY dist/ /dist/
```

LABEL 只當來源資訊，取件不拿它判斷相容性或可信度（N7）。

工具端多架構建置範本（草稿）在 `../template/`：`publish_dist.sh` 用同一次 buildx 建 amd64 與 arm64、只以 digest 推送，兩平台以 `docker create`／`docker cp` 展開後逐檔比對、再跟本機 `dist/` 比對，一致才用 `imagetools create` 上 tag（#26）；`dist.yml` 是呼叫它的 GitHub Actions workflow。正式文件位置（工具端契約文件）還沒定。
