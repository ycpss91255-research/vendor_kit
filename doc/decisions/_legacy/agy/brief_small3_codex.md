你是設計審查員。vendor_kit 背景：工具 dist 打包成 GHCR image（可公開或私有，由工具 repo 自決）；下游專案 `.vendor_kit/version.toml` 鎖 tag@digest；引擎在 docker 容器內跑，主機只需 docker+git+just；主機的 docker 登入資訊（credential helper）容器內拿不到；`update` = 只查有沒有新版、`upgrade [-t <tag>]` = 套用；不變量「使用者的檔：可以建（明說）、要改先問（-y 免問）、永不刪、永不覆蓋」；初始檔有 copy 模式（整檔）與 append 模式（往使用者已有的檔加幾行，問後加，upgrade 用原文比對找上次加的行）。
請逐題裁定（同意／反對／有條件）+ 理由 + 證據或前例：
Q-a 私有工具 image 的「查最新版」（列 tag 需 registry API，主機 docker CLI 做不到）：
  (a) 提供 `VENDOR_KIT_REGISTRY_TOKEN` 環境變數給引擎查 registry；
  (b) 預設不支援私有 image 的「查最新」：update 對私有工具回 1 印「私有 image 請用 upgrade <repo> -t <tag>」；拉 image 仍走主機 docker 認證；(a) 為選配。
  我方傾向 (b) 預設、(a) 選配。請評估：GHCR 對私有 package 列 tag 的 API 與 token 種類（PAT scope read:packages）；有沒有第三條路（例如主機端用 `docker manifest inspect`／`docker buildx imagetools inspect` 取指定 tag 的 digest 但仍無法列 tag；或讀取 ~/.docker/config.json 的 auth 掛進容器——安全性？）。
Q-b init.toml 欄位名：`[[file]] src="…" dest="…" mode="copy"|"append"`（預設 copy）。有沒有更通用的命名前例（例如 Ansible copy/blockinfile/lineinfile、Copier `_skip_if_exists`、chezmoi modify_）？`append` 這個字會不會讓人以為每次都加？替代：`strategy`、`merge`、`kind`。
Q-c append 行的比對嚴格度：第一版「原文完全相同」才視為我們加的行（CRLF、尾端空白、縮排差異都算不同 → 不動只 warn）。這會不會在 Windows/WSL2 編輯器（autocrlf）下讓 upgrade/remove 幾乎永遠找不到？建議：忽略行尾 CR 與尾端空白但不忽略其他差異？請給裁定。
最後一張表：題｜裁定｜一句理由｜建議寫法。50 行內。
