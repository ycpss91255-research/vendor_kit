## 結論

工具 tag 應限定為 canonical `vX.Y.Z`，而且「最新版」明定為所有合法 tag 中，將 `X`、`Y`、`Z` 當非負整數依序比較所得的最大值；不可用字串順序、發布時間或 registry 回傳順序判定。Pre-release 不接受，因此不參與最新版；日後真有需求，應另開明確介面，不應讓它自動進入一般升級路徑。

## 理由

- `update`、`upgrade <repo>` 與未指定 tag 的 bootstrap 已承諾「新版／最新版」，但現行文件沒有排序規則；不補規則，對同一組 tag 可以有不同合法答案，無法黑箱驗證。[docs/contract/04_interface.md:84](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:84)、[docs/contract/04_interface.md:95](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:95)、[docs/contract/04_interface.md:190](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:190)、[docs/contract/04_interface.md:195](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:195)、[docs/contract/04_interface.md:197](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:197)

- `X.Y.Z` 已是對外版本語言，且三段各自有明確意義；用數值三元組排序是現有契約直接支持的最小規則，不必再引入另一套版本概念。[docs/contract/01_purpose.md:82](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:82)、[docs/contract/01_purpose.md:84](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:84)、[docs/contract/02_invariants.md:180](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:180)、[docs/contract/02_invariants.md:182](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:182)

- 引擎已定為 `vX.Y.Z`，而介面原則要求「一個概念一種寫法」；讓工具版本另收任意 tag，會使同一個 `<tag>` 在 `--engine=<tag>` 與 `<repo>@<tag>` 中具有不同文法。[doc/decisions/review_log/discussion_queue.md:37](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:37)、[docs/contract/04_interface.md:140](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:140)、[docs/contract/04_interface.md:146](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:146)、[issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71)

- **推論：** canonical 格式應排除前導零，即 `v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)`。否則 `v1.02.3` 與 `v1.2.3` 是兩個 tag、卻代表同一個排序位置，最新版會產生平手；介面還得額外定義平手處置，違反介面最少。

- Pre-release 是 `X.Y.Z` 之外的額外語法與排序維度。SemVer 明定 pre-release 低於相同核心版本的正式版，且其識別子另有數字／ASCII／長度比較規則；一旦接受，就不能再把最新版簡單定義成三段數值最大值。[Semantic Versioning 2.0.0](https://semver.org/)

- **推論：** 一般 `update`／`upgrade` 不應把不穩定版本自動推薦給目前只使用正式版的使用者。既有相容性承諾只描述 `X.Y.Z`，沒有定義 pre-release 是否享有同一個 X 內的相容保證；納入會擴大目前沒有證據支持的承諾。[docs/contract/01_purpose.md:84](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:84)、[docs/contract/01_purpose.md:88](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:88)

- registry 的列舉順序不能代替版本順序。GitHub Packages 對 package version 提供的是建立時間排序，不是 tag 的語意版本排序；因此「最後推送」不能等同「最新版」。[GitHub Packages GraphQL 文件](https://docs.github.com/en/graphql/reference/packages)

## 風險或反例

- 限定 `vX.Y.Z` 會拒絕 `latest`、`main`、日期版號及 `v1.2.3-rc.1` 等既有發布習慣；這是縮小可導入工具的範圍，但換來可判定、可驗證的自動升級語意。若目標包含任意第三方 image，替代方案只能是「任意 tag 可明確指定，但只有 `vX.Y.Z` 參與最新版」；代價是同一個 `<tag>` 出現兩種有效性規則。

- tag 可以重新指向別的內容，而版本鎖定真正靠 digest；因此「最新版」只能判斷版本名稱，不能證明內容未被替換。[GLOSSARY.md:78](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:78)、[GLOSSARY.md:81](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:81)、[GLOSSARY.md:84](/home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:84) 同一個最高 tag 被重新指向新 digest 時，應視為「同版內容漂移」，不能謊稱出現新版；其告警或拒絕行為仍需另定。

- 數值比較不能用普通字串排序：例如 `v1.10.0` 必須高於 `v1.9.0`。這也表示實作必須解析三段整數，而不能直接採 registry 回傳次序或 shell lexical sort。