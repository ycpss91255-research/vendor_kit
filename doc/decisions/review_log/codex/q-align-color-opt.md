## 結論

不開 `--color=auto|always|never`。人讀訊息預設依各自輸出 stream 是否為 TTY 決定著色；非空的 `NO_COLOR` 一律關閉；機器輸出與執行紀錄永遠不含 ANSI。這可由既定原則推出，不需再問維護者。

## 理由

- `--color=auto` 重複預設行為，`--color=never` 重複 `NO_COLOR`；只有 `always` 新增「重導向時強制著色」，目前契約沒有這項需求。開一組三值選項會違反「能做到同一件事的第二種寫法就不開」及「一個概念一種寫法」。證據：[02_invariants.md:150](/home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:150)、[issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71)。

- repo 已把上述原則實際用來拒絕重疊介面：拿掉 `help` recipe，只保留 `-h`／`--help`；也拒絕功能重疊的別名。這不是抽象偏好，而是已採用的判準。證據：[ADR-0004:58](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:58)、[ADR-0004:93](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0004-vk-recipe-interface-and-write-boundary.md:93)。

- 新增 `--color` 不是免費的內部細節：新增任何選項都會觸發介面版 `P+1`，形成永久相容成本。沒有不可取代需求時，不應增加。證據：[ADR-0008:25](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0008-protocol-and-file-schema-versions.md:25)。

- 機器判讀已有唯一介面：JSONL 執行紀錄與 `vk-resolve/<P>`；人讀訊息不承擔機器介面。因此應直接規定這兩種機器輸出無 ANSI，而不是用 `--color` 改變它們。證據：[ADR-0005:17](/home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0005-run-log-and-event-registry.md:17)。

- GNU／POSIX 慣例沒有要求提供 `--color`。GNU 只明定所有程式應提供 `--help`、`--version`，其他長選項是在「功能存在時」統一名稱；POSIX 的 Utility Syntax Guidelines 也只規範選項形式。證據：[GNU Command-Line Interfaces](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html)、[POSIX Utility Conventions](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)。

- `NO_COLOR` 的約定正是：非空時抑制預設 ANSI 顏色；它沒有要求每個工具都必須另開逐次覆寫選項。故採 `TTY + NO_COLOR` 足以形成單一、跨工具的關閉方式。證據：[NO_COLOR 規格](https://no-color.org/)。

## 風險或反例

- Cargo、just、GNU `ls` 的 `--color=always` 能在 pipe、pager 或擷取輸出時強制保留顏色；不開選項就沒有這項能力。這是實際功能差異，不只是別名。反例：[just manual](https://just.systems/man/en/functions.html)、[GNU Coreutils `ls`](https://www.gnu.org/software/coreutils/manual/coreutils.html)。

- GNU Coding Standards 原則上反對讓程式核心行為依輸出裝置改變，並建議不同重要行為用選項選擇；但它容許終端上的錯誤呈現有所不同。把顏色嚴格限制為不承載語意的呈現層，才不會踩到這個反例。[GNU Standards for Interfaces Generally](https://www.gnu.org/prep/standards/standards.html#User-Interfaces)。「顏色屬於容許的呈現差異」是推論。

- 若將來出現經驗證的需求，例如 pager 必須保留 VK 顏色，`always` 才取得不可取代性；屆時應另開決策並承擔 `P+1`，不能因 Cargo／just 有此選項就預先加入。