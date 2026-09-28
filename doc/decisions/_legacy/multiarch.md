# multiarch

## 一致
- arm64 用原生 hosted runner（GitHub ubuntu-24.04-arm / GitLab saas-linux-small-arm64）當正式閘門；QEMU 只當備援或本機便利，因為它共用 amd64 kernel、host 的 just 也還是 amd64，驗不到 docker run -u、bind mount、flock 這些本設計最在意的行為。
- 自架 Jetson runner 只當補強（nightly／手動），不當 PR 必要閘門；一般 arm64 runner 不能宣稱「Jetson 已測」。
- 「GitLab 拉 GHCR 用 deploy token」是錯的：GHCR 只認 GitHub classic PAT（read:packages），fine-grained PAT 不行；PAT 綁個人帳號、有到期日，要有 bot 帳號與輪換流程。
- 第一版只推單一 registry（GHCR），不雙推；日後需要鏡像時用保 digest 的複製（crane copy / imagetools），不重 build。
- GitLab docker executor + dind 下 `docker run -v $PWD:/repo` 掛不到 job 容器的工作目錄（volume 是 daemon 主機語境），是 GitLab 支援的第一號風險，草稿完全沒提，必須先 spike 或改用 shell executor。
- check.sh 用 POSIX sh 成立，但只是入口的可攜性；走契約①就必須裝 just，這是硬性限制本來就要求的，不能拿來當取消 just 測試的理由。
- release 不能靠單一 `bake release --push` 帶 release-test 就宣稱「測試失敗就不發佈」：要分架構各自 build/測試，最後由單一 job 用 `imagetools create` 合併 index；兩個 runner 各自 push 同一 tag 會互相覆蓋。
- agy 的 Renovate 資料不能直接用：matchStrings 寫死 ghcr.io 前綴不支援 GitLab registry；pinDigests 是「補 digest」不是「更新既有 digest」的關鍵設定。
- Renovate 對私有 GHCR image 需要獨立的 hostRules，CI 的 docker login 對 Renovate 沒用；agy 完全沒提。
- 現有 ci.yaml 在 runner 主機 `pip install pytest` 跑 system/acceptance，和「主機只有 docker+git+just」的限制有張力；下游 check.sh 絕不能依賴 Python。

## 分歧（含判斷）
- agy 附件到底有沒有可用內容：兩者互補而非矛盾。結論：這題的 CI/registry 部分等於「零前例」，全靠兩位審查員自行查證；Renovate 那段則要照 codex 的清單重寫並用 fixture 驗兩條路徑（新 tag+新 digest、同 tag digest 更新）。
- 工具 repo 的 CI 要不要 arm64 runner：Claude 的 COPY-only 是讓矩陣真正「最小」的關鍵，值得採用；但 codex 的提醒也對：COPY-only 只省掉 build 端的 QEMU，dist 內容仍要在 amd64 跑一次 install+verify smoke，而且只適用 <name>-dist 這類純檔案 image，工作負載 image 另議。
- release 流程的形狀：codex 的觀察正確：bake 一條命令同時帶 release 和 release-test，不保證失敗就不 push。但 Claude 的版本其實是「兩步」（先 bake 測、綠了才另一次 bake push），只要分成兩個 step 就沒有這問題。折衷：採 Claude 的 push-by-digest 兩架構分建，但加入 codex 的「兩架構 /dist 逐檔等同性檢查」當合併前閘門；candidate tag 不是必要，push-by-digest 的 untagged digest 已能達到同樣效果，也符合「tag 不覆蓋」。
- arm64 要跑多少測試：取 Claude 的最小集合，但把 codex 的「一條完整主機流程 smoke」列為 arm64 必跑（這正是 pytest system/acceptance 在 arm64 跑的意義）。unit/integration 不在 arm64 重跑，除非日後出現架構相關 bug。
- check.sh 的交付方式：Claude 的交付點解決下游漂移，但沒回答 codex 的兩個洞：(a) clean checkout 時 .vendor_kit/ 存不存在（若 .vendor_kit 已進版控就存在；否則 CI 要先跑 bootstrap）；(b) 工具 repo 沒有 bootstrap，得從 release assets 依 VK 版本 curl。建議：下游走 Claude 的路，工具 repo 走 release assets + 固定版本。
- GitLab 第一版怎麼支援：兩者都對，差在成本假設：shell executor 意味著自架 GitLab runner，不是 GitLab.com hosted。若目前沒有任何確定的 GitLab 下游，採 Claude：GitHub 先出範本、GitLab 標「待驗證」；真要支援時，自架 shell executor 是最省事的正解，不要為了 hosted dind 去改契約。

## 對前例資料的更正
- agy_upgrade_all.md 對本題（arm64 runner、QEMU、GHCR 授權、GitLab、buildx 多平台）零覆蓋，不要在文件裡引用它當依據。
- Renovate customManagers 的 matchStrings 範例要重寫：不要以 ^ 當每行開頭（regex manager 是整份檔案匹配）、depName 改成 `(?<depName>[^:"]+)` 不寫死 ghcr.io、考慮 registry 帶 port 與行尾註解、fileMatch 只掃根目錄 .version 避免碰到 .version.local。
- pinDigests 的說法錯：它是替沒 digest 的參照補 digest，matchStrings 已擷取 currentDigest 時 Renovate 換 tag 本來就會一併換 digest；不要把它當關鍵設定。
- autoReplaceStringTemplate 不是必填；先驗證預設替換夠不夠，再決定要不要覆寫。
- agy 沒提 Renovate 拉私有 GHCR 需要 hostRules（matchHost ghcr.io + classic PAT）；這是 GitLab 上跑 Renovate 的直接前置條件。
- agy「PR body 固定、附 Release Notes」只是單一案例，對自訂 TOML + 多架構 index + 私有 registry 不保證成立。
- agy 隱含「upstream 重建導致 tag digest 改變是正常更新」，與本專案「tag 不覆蓋」決議衝突：自家正式 tag 的 digest 變動要視為異常。
- agy §1.2 引用的 mise PR #6258、Renovate issue #10993/#24942 本次未驗證，使用時視為未查證。

## 最終建議
五個傾向的最終判定：(1) amd64 跑全部、arm64 用原生 hosted runner 跑 env-test + release-test + 一條完整主機流程 smoke（非 root UID/GID、真 bind mount、真 just init）；QEMU 只留本機便利，不當閘門；Jetson 用 release checklist 手動驗收，日後有需要再自架 nightly runner。(2) multi-arch 方向成立，實作改為：兩個 runner 各自單平台 bake release + release-test（分兩個 step，先測後推），綠了才 push-by-digest；merge job 先做兩架構 /dist 逐檔等同性檢查（路徑、型別、hash、權限、禁 symlink、禁 ELF、init.toml 一致），再 imagetools create 合成 index，inspect 斷言含 linux/amd64 與 linux/arm64（濾掉 attestation），index digest 寫進 release notes 與 bootstrap 的 VK_IMAGE 預設值；現有 ci.yaml 的 `bake release --load` 維持單平台。(3) vendor_kit 提供工具 repo CI 範本成立；先把 Dockerfile.dist 改成 COPY-only（VERSION 由 CI 寫成檔案再 COPY），工具 repo 的 build 就不需要 QEMU 或 arm64 runner，只需 amd64 一個 job：login → buildx build --platform 兩架構 --push → 在 amd64 對當次候選 image 跑 install+verify smoke → inspect 斷言兩平台 → dist 政策 lint。(4) GitLab 拉 GHCR 改用 bot 帳號的 GitHub classic PAT（read:packages）放 masked variable，由 CI 檔 `docker login --password-stdin`；job script 內的 docker run 不靠 DOCKER_AUTH_CONFIG；不雙推 registry。(5) check.sh 用 POSIX sh，但 CI 檔仍要裝 just（Ubuntu 24.04 apt 有、22.04/Jetson 要下載 binary）；腳本由 bootstrap 寫進 .vendor_kit/ci/check.sh 隨 .version 升級並納入 verify，工具 repo 從 release assets 依固定版本取得；腳本要正確處理 diff 的 0/1/2 回傳值，不依賴 Python/jq/curl。CI 檔（GitHub / GitLab）只做三件事：登入 registry、裝 just、呼叫 check.sh。GitLab 第一版標「待驗證」：GitLab.com hosted docker executor + dind 的 bind mount 語意與本設計衝突，真要支援時走自架 shell executor，或先做一次真機 spike。Renovate 那段依 agy_corrections 重寫並用 fixture 驗證。

## 要問使用者
- GitLab 要不要在第一版支援？目前有沒有任何確定會在 GitLab 的下游？若要，runner 拓樸是 GitLab.com hosted（docker executor + dind）還是自架 shell executor？
- vendor_kit repo 與 15 個工具 repo 是 public 還是 private？決定 arm64 runner 是否計費、GHCR 拉取是否需要 token、Renovate 是否需要 hostRules。
- GHCR 的 classic PAT 掛在誰名下？要不要建 bot 帳號？到期輪換由誰負責、寫在哪份 runbook？
- Dockerfile.dist 能否接受改成 COPY-only（VERSION 由 CI 先寫檔再 COPY）？「工具 image 一律 multi-arch」是只指 <name>-dist 還是也含工具的工作負載 image？
- check.sh 的交付方式：下游由 bootstrap 寫進 .vendor_kit/ci/、工具 repo 從 release assets 固定版本取得，可接受嗎？.vendor_kit/ 目前有沒有進版控（決定 clean checkout 時入口是否存在）？
- Jetson 承諾到哪一層：只保證 vendor_kit 分發與安裝，還是含 GPU/X11/CUDA 工作流程？JetPack 5（Ubuntu 20.04、Docker 20.10、無 apt just）還要不要支援？最低驗證是 release checklist 手動跑一次，還是自架 nightly runner？
- CI 是否也嚴格遵守「主機只裝 docker+git+just」？若是，現有 ci.yaml 在 runner 主機 pip install pytest 跑 system/acceptance 要改成容器內跑或改寫。
- release index 要不要保留 provenance/SBOM attestation？保留則 .version 鎖的 index digest 含 attestation manifest，日後鏡像要一起搬。
- Docker 最低能力下限是什麼（Engine、Buildx、BuildKit、Compose 版本）？rootless、userns-remap、遠端 daemon 要不要支援？
- 已發布 tag 的 digest 是否絕對不允許改變？若 Renovate 偵測到同 tag digest 變動，要開 PR 還是直接告警？