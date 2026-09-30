## 結論

保留 02 的無條件承諾，但改寫成純概念：「已由主機成功取得的 image，其使用不因 registry 不同而改變。」04 再把操作邊界寫清楚：目前只驗證 GHCR；其他 registry 未驗證，但若主機 Docker 能以鎖定的完整 image 引用取得 image，而 VK 仍因 registry 身分不同而失敗，仍屬 VK 違約；只有 registry、認證、網路及版本列舉本身失敗不在此承諾內。

04 的「別家出問題不在承諾內」應刪除或限縮，不能用「未測過」取消 02 已經作出的承諾。

## 理由

1. 02 是全域、不容 ADR 違反的性質；04 只能具體化，不能反向縮限。

   02 明定每條都是「全域必須成立的性質」，且只寫概念、不寫實現方式：[02_invariants.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:3)。04 自己也宣告永久規則以 02 為準，只能寫「依第 N 條」：[04_interface.md:3](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:3)、[04_interface.md:5](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:5)。

   因此 04 第 54 行不能排除 02 第 70 行已涵蓋的案例；否則就是後頁推翻前頁，也違反已定案的只能向前依賴規則：[discussion_queue.md:14](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review_log/discussion_queue.md:14)。

2. 02 應保留的是「取得後的可用性」，不是 Docker 指令或特定 registry 的測試矩陣。

   現行 02 把認證責任交給主機與 CI，並承諾「主機拉得到的 image，VK 就用得了」：[02_invariants.md:70](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:70)。但「docker 拉得到」仍是具體機制；若嚴格遵守 02 只寫概念，建議改成：

   > image 的取得與使用不綁特定 registry；主機已成功取得的鎖定 image，VK 必須能使用。

   「鎖定 image」已有前置概念：版本鎖定行鎖內容，而且同一份鎖定行必須能重建相同內容：[02_invariants.md:57](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:57)、[02_invariants.md:64](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:64)。完整 image 引用本身也包含 registry、tag 與 digest：[CONTEXT.md:193](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:193)。

3. 04 應分開「VK 使用 image」與「VK 直接查 registry」兩種能力。

   04 已經存在一個明確例外：未提供憑證時，不支援需要認證的版本列舉，使用者可以改成直接指定 `@<tag>`：[04_interface.md:50](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:50)。這表示「列舉可用版本」與「使用已指定的 image」本來就是不同能力。

   建議 04 寫成：

   > 認證與 image 取得由主機及 CI 處理。主機 Docker 能以版本鎖定行中的完整 image 引用取得 image 時，VK 必須能使用，不因 registry 不同而改變。  
   > 目前端到端測試只涵蓋 GHCR；其他 registry 尚未列入測試矩陣。registry 拒絕請求、認證失敗、網路失敗，或未提供憑證而無法列舉版本，不表示 VK 能取得該 image；這些情況不適用前述承諾。

   第一段是對 02 的向前引用與具體操作界線；第二段只是揭露測試覆蓋及判定「主機是否取得成功」，沒有另立較窄契約。

4. 這不是放大承諾，而是恢復 r105 前兩句能成立的唯一一致解讀。

   r105 前的 02 同時寫了「只有 GHCR 實際測過」和「主機 docker 拉得到就能用」：[pre_r105.md:103](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r105.md:103)、[pre_r105.md:106](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/_backup/doc_decisions_review_02_invariants.pre_r105.md:106)。前者是驗證證據，後者是契約邊界；把前者解讀成排除後者，兩句從當時起就已矛盾。

   此外，01 已承諾同一個 major 內原有用法繼續可用：[01_purpose.md:82](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:82)、[01_purpose.md:88](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:88)。現在把 02 縮成「只保證 GHCR」，會使原先符合「Docker 拉得到」的其他 registry 用法失去承諾；依 01，這不能作為普通文件整理悄悄發生。

5. registry 中立與 01 的既有範圍相容，不等於承諾多 registry 同時推送。

   01 說 VK 會把工具 image 推到 registry：[01_purpose.md:23](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:23)，但第一版不做的是「多個 registry 同時推送」：[01_purpose.md:34](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/01_purpose.md:34)。因此「一次使用任一可取得的 registry image」和「同時向多個 registry 發布」不是同一承諾。

   這是依文件語義作出的推論：前者是導入端相容性，後者是出貨端的多目標發布功能。

## 風險或反例

- 「主機拉得到」必須以版本鎖定行中的完整 `tag@digest` 引用為準。若只證明 `docker pull example/tool:tag` 成功，卻無法取得鎖定 digest，不能算符合承諾；VK 承諾的是內容鎖定，不只是 tag 可拉取：[02_invariants.md:59](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:59)、[CONTEXT.md:193](/home/cyc/Desktop/vendor-kit_ws/src/CONTEXT.md:193)。

- Docker 能拉取某個已知引用，不代表 VK 一定能列舉該 registry 的 tags。私有 registry 缺少列舉憑證就是現成反例；04 已將其列為不支援情況：[04_interface.md:50](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/04_interface.md:50)。因此承諾不得擴寫成「任何 Docker 能登入的 registry，VK 的最新版查詢都必定可用」。

- 只寫「其他 registry 未測試」而不寫判責界線，讀者仍無法判斷故障歸屬。應以可觀察前提切割：同一完整引用由主機 Docker 取得失敗，屬 registry／環境端；取得成功後 VK 因 registry 名稱或來源而不能處理，屬 VK。這個判責方式是推論，但符合 02 要求對外承諾可驗證的原則：[02_invariants.md:15](/home/cyc/Desktop/vendor-kit_ws/src/doc/decisions/review/02_invariants.md:15)。

- 若目前實作其實解析 `ghcr.io` 專屬 API、路徑或認證回應，即使 `docker pull` 成功仍會失敗；在上述統一方式下，那是需要修復的 VK 缺陷，不能再由 04 的免責句掩蓋。這是推論；現有題示文件沒有提供跨 registry 的實測結果。