> 依新設計改寫這題（舊的 argv 旗標與四個凍結檔已廢除，那部分作廢；見 `dist_distribution_notes.md`、#20）。

## 新設計下真正要回答的相容性問題

1. **啟動器 ↔ 容器內 CLI 的契約**：`.vendor_kit/vendor.just`（版本由 `.version` 的 `vendor_kit` 行鎖）呼叫的是**工具 image 內建**的 vendor_kit（`FROM vendor_kit:vN`），兩者版本會漂移。啟動器傳的 argv（`--name / --self / --repo / --dist`、子命令名）、`.stamp` 格式（第一行 image 字串 + 逐檔 sha256）、`init.toml` schema 這三個介面，跨 vendor_kit 大／小版要承諾到什麼程度？誰檢查不相容（notes §6 只寫「launcher 帶契約版本號，過舊時提示」，未定）？工具要不要重 build image 才能拿到新 vendor_kit？
2. **使用者面 just recipe 的相容承諾**：vendor_kit 提供的 `init / diff / upgrade`（底線開頭的 `_ensure / _vk` 算不算私有？）與工具約定的 `build / run / exec / stop`，可不可以在小版移除或改名？使用者 justfile 只 import 不會壞，但 CI 與 hooks（`script/hooks/pre|post/<指令>.sh`）會硬編這些名字。

與 #20（`vendor_kit` 行獨立升級）直接相關。待 upgrade 流程那題定案後一起討論。
