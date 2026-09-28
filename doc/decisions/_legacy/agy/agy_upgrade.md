本篇前例研究報告針對 `vendor_kit` 的升級流程設計進行查證與跨專案對照。全文依 1～5 分節，每一項事實與結論均附官方文件、GitHub 原始碼或 Issue 來源，文末並附完整「來源清單」。

---

### 1. Renovate / Dependabot 對「GHCR image 以 tag@digest 記在自訂 TOML 檔」的支援

#### (1) Renovate 的自訂 Manager 支援與設定
Renovate 支援自訂正規表達式管理器（`customManagers`，原稱 `regexManagers`），可原生配合 `docker` datasource 追蹤 GHCR 容器映像檔（[Renovate Regex Manager 文件](https://docs.renovatebot.com/modules/manager/regex/)、[Renovate Docker Datasource 文件](https://docs.renovatebot.com/modules/datasource/docker/)）。

在 `.version`（TOML 格式）中，每一行的格式為：
`<name> = "ghcr.io/<org>/<name>:<tag>@sha256:<digest>"`

針對此格式的 `renovate.json` 設定範例如下：

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    "docker:pinDigests"
  ],
  "customManagers": [
    {
      "customType": "regex",
      "fileMatch": ["^\\.version$"],
      "matchStrings": [
        "(?<depName>[a-zA-Z0-9_.-]+)\\s*=\\s*\"(?<registryUrl>ghcr\\.io/[^:]+):(?<currentValue>[^@\\s\"]+)(?:@(?<currentDigest>sha256:[a-f0-9]+))?\""
      ],
      "datasourceTemplate": "docker",
      "depNameTemplate": "{{{registryUrl}}}",
      "versioningTemplate": "docker",
      "autoReplaceStringTemplate": "{{{packageName}}} = \"{{{depName}}}:{{{newValue}}}{{#if newDigest}}@{{{newDigest}}}{{/if}}\""
    }
  ],
  "packageRules": [
    {
      "matchDatasources": ["docker"],
      "pinDigests": true
    }
  ]
}
```

#### (2) 產生的 PR 樣貌（Tag 與 Digest 是否分開）
- **Tag 升級時**：當啟用 `pinDigests: true` 時，Renovate 查詢到新的 Tag（例如從 `v1.2.0` 到 `v1.3.0`），會自動向 Registry 查詢該新 Tag 的最新 SHA256 Digest，並在**同一個 PR 內同時更新 Tag 與 Digest**（[Renovate Pinning Digests 文件](https://docs.renovatebot.com/configuration-options/#pindigests)）。
- **Tag 不變但 Digest 改變時（Mutable Tag 重新發布）**：Renovate 預設將其歸類為 `digest` update type，會單獨開立 PR 更新 Digest。
- **避免多個 PR 的分組建議**：若希望無論是版本號躍升或純 Digest 變動都統一合併在該依賴的單一 PR 中，可在 `packageRules` 中設定 `groupName: "{{depName}} Docker updates"`（[Renovate Package Rules 文件](https://docs.renovatebot.com/configuration-options/#packagerules)）。

#### (3) Digest Pinning 與 Tag 同時更新的設定關鍵
- **`matchStrings` 捕獲組**：正規表達[agy] print timeout after 5m0s with turn in progress; returning partial output
