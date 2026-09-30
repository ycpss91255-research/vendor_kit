## 結論

保留 `--timeout <duration>`；未帶時不設時限。`<duration>` 採 POSIX `timeout` 的 duration 文法，限大於零；適用於所有會啟動引擎的 VK recipe 與 `bootstrap.sh`，逾時回 `2`，並明確指出哪個操作逾時、可能留下未完成狀態及執行紀錄位置。

## 理由

- **選項不能直接拿掉。** 已定案的 issue #71 把 `--timeout` 列為不常用、僅有長名稱的公開選項；ADR-0007 又明定由啟動器攔截，不交給引擎。刪除會推翻既有決議，不只是補齊 04 的空白。[issue #71](https://github.com/ycpss91255-research/vendor_kit/issues/71)、[ADR-0007](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:55>)、[04](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:200>)

- **寫法定為 `--timeout <duration>`，不另開短選項，也不承諾 `--timeout=<duration>`。** `--timeout` 已被歸為不常用選項，所以只有長名稱；帶值選項依 POSIX 慣例將選項與值分成兩個 argument。`=` 已經有一個必要例外：值可有可無的 `--engine=<tag>`；`--timeout` 的值是必要值，沒有理由複製該例外。[04](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:141>)、[POSIX Utility Syntax Guidelines 6、7](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html)

- **`<duration>` 使用 POSIX timeout 文法：十進位數，可有小數；後綴為 `s`、`m`、`h`、`d`，省略後綴就是秒。** 例如 `30`、`1.5m`、`2h`。這沿用既有標準概念，不另造 `30sec`、ISO 8601 或毫秒格式，符合「一個概念一種寫法」。[POSIX `timeout` operands](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/timeout.html)

- **合法範圍定為嚴格大於零的有限值，不另訂人為上限。** `0` 在 POSIX/GNU `timeout` 代表停用時限，但 VK 已經以「不帶選項」表達同一件事；若再接受 `0`，便為同一概念開第二種寫法，違反第 8 條。負數、空值、非十進位、未知後綴、NaN、Infinity 都是用法錯誤，回 `2`。[02 第 8 條](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:150>)、[04 用法錯誤](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/04_interface.md:129>)、[GNU `timeout`](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html)

- **預設值是「無時限」，不是某個秒數。** 現有契約沒有足以推導合理固定秒數的工作量上限；registry、image 大小和主機速度都會變。任意預設 30 秒或 10 分鐘會把正常的慢操作改成失敗，構成新的產品行為。這是推論。

- **適用範圍是所有會經啟動器啟動引擎的 VK recipe，以及 `bootstrap.sh`；不適用於純啟動器即可完成的 `-h`／`--help`、參數錯誤與版本組合的前置拒絕。** timeout 的擁有者已定為啟動器，而啟動器包含薄殼的 POSIX sh 片段與 `bootstrap.sh`；依第 8 條，同一概念不應逐 recipe 產生不同選項集合。[GLOSSARY](</home/cyc/Desktop/vendor-kit_ws/src/GLOSSARY.md:33>)、[ADR-0007](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:55>)、[02 第 8 條](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:154>)

- **時限量的是引擎執行的實際經過時間：從啟動器開始取得／啟動該次引擎，到引擎及其容器結束；逾時後仍要完成啟動器自己的停止與清理。** 否則「限制等待時間」無法判斷 image pull 算不算在內，也無法黑箱驗證。將 pull 納入是推論，理由是它同樣由啟動器執行且會阻塞使用者。

- **逾時回 `2`，不能照 GNU/POSIX 原樣回 `124`。** VK 對外只定義 `0`～`3`；逾時是未完成的失敗，不是「做完但要人接手」，也不是版本組合不合，因此只能映射為 `2`。[03 結束碼](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:14>)、[02 第 4 條](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:88>)。POSIX/GNU 的 `124` 可作為「逾時必須能與子程序原始結果區分」的外部前例，但不能穿透成 VK 結束碼。[POSIX `timeout` exit status](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/timeout.html)

- **訊息應新增固定條目，stderr 逐字格式建議為：**  
  `vendor_kit: 失敗: <operation> 超過時限 <duration>，已停止本次執行。這次操作可能未完成；請查看執行紀錄 <path>，修正原因後重試。`  
  不能宣稱「未修改任何檔」，因為逾時可能發生在副作用之後；必須指出未完成及紀錄位置，才符合「未完成狀態可辨識、說出下一步」。[02 第 4 條](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/02_invariants.md:97>)、[03 訊息格式](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/03_messages.md:30>)、[01 失敗承諾](</home/cyc/Desktop/vendor-kit_ws/src/docs/contract/01_purpose.md:67>)

## 風險或反例

- POSIX `timeout` 對整個 process group／後代程序如何送訊號容許不同實作；只殺前景 shell 可能留下 docker client 或 container。VK 必須黑箱驗證逾時後沒有仍在執行的該次引擎容器。[POSIX `timeout` process handling](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/timeout.html)

- POSIX/GNU 允許小數 duration，但主機側只准使用 POSIX sh 與既有白名單命令；若現有 `sleep`／算術實作無法跨支援平台一致處理小數，就應把合法文法收窄為正整數，而不是偷偷四捨五入。這是實作驗證後才可決定的風險。[ADR-0007 主機白名單](</home/cyc/Desktop/vendor-kit_ws/src/docs/adr/0007-host-thin-layer-and-shell-integrity.md:28>)

- 使用者可能以為 timeout 保證在指定瞬間返回；實際上停止容器與寫完執行紀錄仍需時間。因此文件應稱「到時開始停止」，不能承諾總牆鐘時間不超過 `<duration>`。這是推論。

- 若最後只讓少數 recipe 接受 `--timeout`，就必須證明其他 recipe 永遠不會等待；否則會破壞「同一概念一種寫法」。現有資料沒有這種證據。