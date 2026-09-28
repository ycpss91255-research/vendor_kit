# vendor_kit CI 架構前例研究（2026-09-19）

> 研究流程說明：agy 完整題目跑兩次都在 570 s 逾時（`Error: interrupted`）；拆成三段小題再跑，第一段回 `Eligibility check failed: UNAVAILABLE (503)`，後兩段結果見文末「agy 的建議」一節（若該節標示「agy 無輸出」即表示改由 Claude 以 `gh api` + WebFetch 自查）。
> **本文所有「抽查結果」欄位都是 Claude 直接用 `gh api repos/<o>/<r>/contents/.github/workflows/<f>` 下載原始 yaml 核對過的**（共 11 個 repo 的目錄清單、26 個 workflow 檔），原始檔存在 `decisions/wf/`。

## 前例對照表

| 專案 | workflow 檔（`.github/workflows/`） | PR／push 分支跑什麼 | push main 跑什麼 | tag／release 跑什麼 | 共用方式 | 來源 | 抽查結果 |
|---|---|---|---|---|---|---|---|
| **docker/buildx** | `build.yml`、`validate.yml`、`e2e.yml`、`codeql.yml`、`docs-*.yml`、`labeler.yml`、`pr-assign-author.yml`、`zizmor.yml` | `build.yml`：test-integration（buildkit×worker×mode matrix）、test-unit、govulncheck、binaries（不簽章）、bin-image（`push: ${{ github.event_name != 'pull_request' }}` → PR 只 build）；`validate.yml`：lint matrix；`e2e.yml`：driver/bake e2e | 同上，但 bin-image `push=true`（tag `type=ref,event=branch` → `:master`）、binaries 簽章、`scout` 掃描只在 master | `build.yml` 同一檔：`on.push.tags: v*`；`release` job `if: startsWith(github.ref,'refs/tags/v')` 用 `softprops/action-gh-release`（draft）；image 推 `type=semver` | 跨 repo reusable workflow `docker/github-builder/.github/workflows/bake.yml@sha`（多平台 bake + push + OIDC 登入）；`needs:` 鏈；matrix | https://github.com/docker/buildx/tree/master/.github/workflows ；https://github.com/docker/buildx/blob/master/.github/workflows/build.yml | ✅ 已讀 build.yml／validate.yml／e2e.yml 原檔。**沒有** pr.yml/main.yml/release.yml 分檔，是「一檔多事件＋`if:` 分流」 |
| **docker/cli** | `build.yml`、`test.yml`、`validate.yml`、`e2e.yml`、`codeql.yml`、`validate-pr.yml`、`validate-milestone.yml`、`sync-release-branch.yml`、`pr-review*.yml`、`zizmor.yml` | `build.yml`（push master／`[0-9]+.[0-9]+`／tags v*／PR）：prepare→build matrix、plugins；`bin-image` `if: github.event_name != 'pull_request'` | bin-image `push: true` | tags v* 也走 build.yml | `needs:` 鏈、matrix | https://github.com/docker/cli/blob/master/.github/workflows/build.yml | ✅ 已讀 build.yml 觸發區與 bin-image job |
| **moby/moby** | `ci.yml`、`test.yml`、`bin-image.yml`、`buildkit.yml`、`vm.yml`、`windows-*.yml`、`.dco.yml`、`.test.yml`、`.test-unit.yml`、`.vm.yml`、`.windows.yml`（點開頭＝reusable）、`codeql.yml`、`validate-pr.yml`… | `ci.yml`：validate-dco → build（ubuntu-26.04 + **ubuntu-26.04-arm 原生**）、cross（QEMU matrix）、build-dind、success（彙總）；`test.yml`：build-dev → `test`（reusable，amd64 全 matrix／arm64 只跑一組）、`test-unit`、validate、smoke。PR 貼 `ci/validate-only` 標籤可跳過重測 | 同一組檔（`on.push.branches: master`），差別只有 `bin-image.yml` 的 `push: ${{ github.event_name != 'pull_request' }}` 與 govulncheck 上傳 SARIF | `bin-image.yml`：`on.push.tags: v*, docker-v*`；`type=semver,pattern={{version}},match=docker-(.*)` 推 `:23.0.0/:23.0/:23`；master 推 `:master` | 本 repo reusable（`uses: ./.github/workflows/.test.yml` 配 matrix 呼叫）、composite action `./.github/actions/setup-runner`、跨 repo `docker/github-builder/.github/workflows/bake.yml` | https://github.com/moby/moby/blob/master/.github/workflows/ci.yml ；https://github.com/moby/moby/blob/master/.github/workflows/test.yml ；https://github.com/moby/moby/blob/master/.github/workflows/bin-image.yml | ✅ 已讀 4 檔。「點開頭檔名＝reusable」慣例確認 |
| **kubernetes-sigs/kind** | `docker.yaml`、`podman.yml`、`nerdctl.yaml`、`vm.yaml`（僅 4 檔） | 全部 `on: pull_request (branches: main) + workflow_dispatch`，e2e matrix（ipv4/ipv6 × single/multi/multiMaster） | **GHA 不跑 push main**；主 CI／release 走 Kubernetes prow（不確定細節，未查 prow 設定） | GHA 無 release workflow | composite action `./.github/actions/setup-env` | https://github.com/kubernetes-sigs/kind/tree/main/.github/workflows ；https://github.com/kubernetes-sigs/kind/blob/main/.github/workflows/docker.yaml | ✅ 已讀 docker.yaml、vm.yaml 觸發區。kubernetes/kubernetes 本身 GHA 幾乎只做雜務（未逐檔核對，標不確定） |
| **casey/just** | `ci.yaml`、`release.yaml`（僅 2 檔） | `ci.yaml`（PR 任何分支 + push master）：lint、msrv、pages、test（3 OS matrix；順便測 `install.sh`） | 同 `ci.yaml`（無差異） | `release.yaml`：`on.push.tags: '*'`；prerelease 判定 → package matrix（10 target，交叉編譯）→ `softprops/action-gh-release@v2`；正式版才 checksum 等 | 無 reusable／composite；純 matrix | https://github.com/casey/just/blob/master/.github/workflows/ci.yaml ；https://github.com/casey/just/blob/master/.github/workflows/release.yaml | ✅ 已讀全文。最小型「ci + release 兩檔」範本 |
| **astral-sh/uv** | 46 檔：`ci.yml`（總控）+ `plan.yml`、`check-*.yml`、`test*.yml`、`build-*.yml`、`publish-*.yml`（全部 `workflow_call`）+ `release.yml`、`release-prepare.yml` + 雜務 | `ci.yml`（push main／PR／dispatch）：`plan`（reusable，看 diff 與 PR 標籤決定要跑什麼）→ 各 check-*/test*/build-* 皆 `uses: $/.github/workflows/xxx.yml` + `if: needs.plan.outputs.*`；PR 預設不跑 integration/system/docker（需 `test:integration`、`test:system`、`build:push-docker` 標籤）；`required-checks-passed` 彙總 job（`if: github.ref != 'refs/heads/main'`） | 同 ci.yml，`plan` 對 `on_main_branch` 把 test_integration/test_system/test_publish/bench 打開 | `release.yml`：**`workflow_dispatch(tag)`** 手動，非 tag 觸發；`release-gate` job 綁 environment 需第二人核准；cargo-dist 產 plan → build-release-binaries／build-docker（reusable）→ sign → publish-docker/pypi/crates/github/docs（各自 reusable）；`release-prepare.yml` 另外開 PR 改版號 | 大量本 repo reusable（`$/` 新語法）、`secrets: inherit`、matrix in reusable；docker 用 Depot 原生多平台 build（`platforms: linux/amd64,linux/arm64`），tag 用 `docker/metadata-action`（`type=pep440`、`type=sha` for dev、`dry-run` for PR） | https://github.com/astral-sh/uv/blob/main/.github/workflows/ci.yml ；https://github.com/astral-sh/uv/blob/main/.github/workflows/plan.yml ；https://github.com/astral-sh/uv/blob/main/.github/workflows/build-docker.yml ；https://github.com/astral-sh/uv/blob/main/.github/workflows/release.yml | ✅ 已讀 5 檔。「總控分派」最完整的實例 |
| **astral-sh/ruff** | 22 檔：`ci.yaml`（單一大檔，1504 行）、`release.yml`、`build-*.yml`、`publish-*.yml`、`daily_fuzz.yaml`… | `ci.yaml`（push main／PR）：`determine_changes` job → 30+ job 全部 `needs: determine_changes` + `if:`（非 reusable，job 直接寫在同檔） | 同檔 | `release.yml`：`workflow_dispatch(tag)` + `pull_request`（PR 上 dry-run），cargo-dist 產生 | 只有 `needs:` + matrix；沒把 job 拆成 reusable | https://github.com/astral-sh/ruff/blob/main/.github/workflows/ci.yaml ；https://github.com/astral-sh/ruff/blob/main/.github/workflows/release.yml | ✅ 已讀觸發區與 job 清單。同一組織兩種風格：ruff 單大檔、uv 總控+reusable |
| **renovatebot/renovate** | `build.yml`（單一大檔 1049 行）+ 十幾個雜務（`codeql-analysis.yml`、`lock.yml`、`scorecard.yml`、`cancel-stale-merge-queue-workflows.yml`…） | `build.yml`（push main/next/maint/**、PR、**`merge_group`**、dispatch）：setup（算 OS matrix：PR 只 Linux，`ci:fulltest` 標籤或非 PR 才全 OS）→ lint-*、test（shard matrix）、build、build-docs、test-e2e；`build-docker` `if: github.event_name != 'pull_request' || 有 ci:fulltest`；`test-success` 彙總 | 同檔；`build-docker` 跑 `--platform linux/amd64,linux/arm64 --load` 後 `docker run --version` 煙霧測 | **無 tag 觸發**：`release` job `if: github.event_name != 'pull_request'`，用 **semantic-release** 依 commit 決定版本並推 image／npm；`DO_RELEASE` 依分支名（main/next/maint/*） | composite action `./.github/actions/setup-node`、`setup-docker`、`calculate-prefetch-matrix`；`needs:` 鏈 | https://github.com/renovatebot/renovate/blob/main/.github/workflows/build.yml | ✅ 已讀。唯一有 `merge_group` + semantic-release 的樣本 |
| **cli/cli (gh)** | `go.yml`、`lint.yml`、`codeql.yml`、`govulncheck.yml`、`acceptance.yml`、`deployment.yml`、`bump-go.yml`、triage 類 | `go.yml`（push trunk／PR）：3 OS matrix 跑 unit+integration；`lint.yml` 帶 `paths:` 過濾 | 同上（無差別） | `deployment.yml`：**`workflow_dispatch(tag_name, environment, dry_run)`** 手動；goreleaser 3 平台 job → `release` job `gh release create`；`acceptance.yml` 只 `workflow_dispatch`，綁 environment `gh-acceptance-testing` | 純 matrix；無 reusable | https://github.com/cli/cli/blob/trunk/.github/workflows/go.yml ；https://github.com/cli/cli/blob/trunk/.github/workflows/deployment.yml ；https://github.com/cli/cli/blob/trunk/.github/workflows/acceptance.yml | ✅ 已讀 4 檔。acceptance 獨立 workflow、手動觸發＋environment 保護 |
| **python/cpython** | `build.yml`（總控）+ `reusable-context.yml`、`reusable-ubuntu.yml`、`reusable-macos.yml`、`reusable-windows.yml`、`reusable-docs.yml`、`reusable-san.yml`、`reusable-wasi.yml`…（11 個 reusable）+ `lint.yml`、`mypy.yml`、`jit.yml`、`stale.yml`… | `build.yml`（push main/3.*／PR main/3.*／dispatch）：`build-context`（reusable，看 changed files 輸出 run-tests/run-docs/run-ubuntu/...）→ 每個平台 job `uses: ./.github/workflows/reusable-xxx.yml` + `if:`；`all-required-green` 用 `re-actors/alls-green` 彙總，含 allowed-failures／allowed-skips | 同檔（無差別） | 無 release workflow（CPython release 由 release manager 另外流程） | 本 repo reusable + `needs:` + matrix | https://github.com/python/cpython/blob/main/.github/workflows/build.yml | ✅ 已讀 build.yml、reusable-ubuntu.yml、reusable-context.yml |
| **rust-lang/cargo** | `main.yml`、`release.yml`、`audit.yml`、`contrib.yml`（4 檔） | `main.yml`：**`on: merge_group + pull_request`（沒有 push）**；rustfmt、clippy、test（含 `ubuntu-24.04-arm`、`windows-11-arm` 原生）、docs…；`conclusion` job `if: !cancelled()` 用 jq 檢查 needs 全 success | 不跑（merge 前已在 merge queue 跑過完整） | `release.yml`：`on.push.tags: 0.*`，只做 crates.io publish（environment `release`），tag 由 promote-release 推 | 純 `needs:` + matrix | https://github.com/rust-lang/cargo/blob/master/.github/workflows/main.yml ；https://github.com/rust-lang/cargo/blob/master/.github/workflows/release.yml | ✅ 已讀全文。「merge queue 取代 push main CI」的範例 |

## 切法模式歸納

| 模式 | 誰在用 | 優點 | 缺點 |
|---|---|---|---|
| **A. 單一大檔 + `if:` 分流**（`ci.yml`/`build.yml` 同時掛 push/PR/tag，靠 `github.event_name`、`startsWith(github.ref,'refs/tags/')`、PR 標籤決定 job 開關） | docker/buildx、docker/cli、ruff（1504 行）、renovate（1049 行）、cli/cli 的 go.yml | 同一份 DAG，PR／main／tag 行為差異一眼可見；required checks 名稱固定；不用學 reusable 的限制 | 檔案巨大；`if:` 條件散在各 job 容易漏；改一處全 workflow 重跑；YAML 錨點不能用 |
| **B. 依「任務」多檔**（`ci.yml` + `release.yml` [+ `e2e.yml`／`validate.yml`／`nightly`]，每檔自帶觸發） | casey/just（2 檔）、cargo（main+release）、docker/buildx（build/validate/e2e）、moby（ci/test/bin-image/vm/windows）、cli/cli（go/lint/deployment/acceptance） | 觸發事件與檔案一一對應，最直觀；release 檔權限可獨立（`contents: write` 只給 release）；慢的 e2e 可獨立 concurrency | 同一事件多檔並行 → required checks 要跨檔列；共用步驟得靠 composite action 或 reusable |
| **C. 總控分派 + reusable workflow**（一個入口 `ci.yml`/`build.yml`：先 `plan`/`build-context` job 算 changed-files／標籤／分支，再 `uses: ./.github/workflows/xxx.yml` + `if: needs.plan.outputs.*`，最後一個彙總 job 給 branch protection） | astral-sh/uv（`plan.yml` + 30 個 reusable）、python/cpython（`reusable-context.yml` + 11 個 reusable）、moby（`.test.yml`、`.test-unit.yml` 以 matrix 呼叫） | 單一 required check（`required-checks-passed`／`all-required-green`）；每個 reusable 可被 release.yml 重用（uv 的 build-docker.yml 同時被 ci.yml 與 release.yml 叫）；PR 依 diff 只跑相關 job；reusable 各自 permissions | reusable 限制：`env` 不能傳進 `with`（buildx 為此多開 `bin-image-prepare` job）、`on.workflow_call` 不支援 `environment`、環境 secret 要 `secrets: inherit`、巢狀最多 10 層；UI 多一層；skipped job 視為成功，彙總 job 得自己處理（cpython `allowed-skips`、uv `CONDITIONAL_JOBS` jq） |
| **D. 沒有 push-main CI，改用 merge queue** | rust-lang/cargo（`on: merge_group + pull_request`） | main 永遠是「merge queue 跑過完整測試」的結果，省一次 push 重跑 | 需要 merge queue（GitHub 組織／付費方案限制）；忘了加 `merge_group` 就會卡死 |

觀察：
- 「PR 跑快的、main 跑完整」實際是靠 **PR 標籤** 或 **changed-files 計畫 job** 做的，不是靠分檔：moby `ci/validate-only`、renovate `ci:fulltest`、uv `test:integration`/`test:system`/`build:push-docker`、ruff `no-test`。main 上 uv/moby/renovate 一律全開。
- 「PR 上 build image 但不 push」是共通慣例：`push: ${{ github.event_name != 'pull_request' }}`（buildx、moby、docker/cli）；uv 甚至在 PR 給 `dry-run` tag、只 `save` 不 push。
- 大家都有一個 **彙總 job**（moby `success`、uv `required-checks-passed`、cpython `all-required-green`、cargo `conclusion`、renovate `test-success`）做為唯一 required check，並且用 `if: always()`／`!cancelled()` + 自己檢查 `needs.*.result`（因為 skipped 會被 GitHub 當成功）。
- reusable workflow 檔命名慣例：moby 用 `.` 開頭（`.test.yml`），cpython 用 `reusable-` 前綴，uv 直接功能名（`check-lint.yml`）。

## 分支保護／merge queue／required checks 對應

- required check 只能指 **job 名稱**（含 reusable 內部 job 會顯示成 `caller / callee-job` 路徑），因此前例都收斂成單一彙總 job：cpython 註解直說 `all-required-green: This job does nothing and is only used for the branch protection`；cargo 註解 `ALL THE PREVIOUS JOBS NEED TO BE ADDED TO THE needs SECTION`。來源：上表各檔。
- 條件式 job 的處理：uv 把 `test-system` 列進 `CONDITIONAL_JOBS`（只有 PR 有 `test:system` 標籤才要求成功）；cpython 用 `re-actors/alls-green` 的 `allowed-skips`／`allowed-failures`（build-android、cifuzz 允許失敗）。
- merge queue：GitHub 文件明訂「必須用 `merge_group` 事件觸發，否則 required status check 不會回報、merge 會失敗」，可設 CI 逾時（https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue ）。實例：renovate `on: merge_group` + `concurrency.cancel-in-progress` 對 PR/merge_group 皆 cancel；cargo 完全以 merge_group 取代 push；renovate 還有 `cancel-stale-merge-queue-workflows.yml`。
- PR 快／main 完整的實例（已核對）：
  - moby：PR 貼 `ci/validate-only` → cross、build-dind、test、test-unit、smoke 全跳過，只留 validate。
  - renovate：PR 只跑 Linux matrix、不 build docker；`ci:fulltest` 或 push 才全 OS + docker。
  - uv：PR 依 diff 決定；integration/system/docker/bench 預設關，main 全開。
  - cli/cli：acceptance 完全不在 PR/main 上跑，只能手動 dispatch（綁 environment）。
- 反向（PR 跑完整、main 不跑）：cargo（merge queue 已跑）、kind（GHA 只有 PR，main 交給 prow）。

## 多架構 image 的 build/test/push 慣例

| 面向 | 前例 | 來源 |
|---|---|---|
| PR 只 build 不 push | buildx/moby/docker-cli `push: ${{ github.event_name != 'pull_request' }}`；uv PR 給 `type=raw,value=dry-run` 且 `save` 不 push；renovate PR 預設不 build docker | 上表 |
| main 推什麼 tag | `docker/metadata-action` `type=ref,event=branch` → `:master`（buildx、moby）；uv dev image 用 `type=sha` 推到 `ghcr.io/astral-sh/uv-dev`；`edge` 命名在這 9 個專案沒看到（不確定其他專案） | buildx build.yml、moby bin-image.yml、uv build-docker.yml |
| tag 推什麼 | `type=semver,pattern={{version}}`／`{{major}}.{{minor}}`／`{{major}}`（moby，含 `match=docker-(.*)` 去前綴）；uv `type=pep440` | 同上 |
| 多平台建置方式 | (1) 單 job QEMU：buildx e2e.yml、`docker/setup-qemu-action` + `platforms:`；(2) 跨 repo reusable `docker/github-builder/.github/workflows/bake.yml`（buildx、moby 都用；預設把 arm 平台送到 `ubuntu-24.04-arm` 原生 runner，再合 manifest）；(3) uv 用 Depot 雲端原生 builder；(4) renovate 單 job `--platform linux/amd64,linux/arm64 --load` | https://docs.docker.com/build/ci/github-actions/multi-platform/ ；各檔 |
| 跨架構測試 | **原生 arm runner 為主流**：moby build 與 test 用 `ubuntu-26.04-arm`（arm64 只跑縮小 matrix）；cargo `ubuntu-24.04-arm`、`windows-11-arm`；buildx cross job 用 QEMU 只做「能不能 build」不跑測試 | moby ci.yml/test.yml、cargo main.yml |
| image 煙霧測 | renovate build 後 `docker run --rm renovate/renovate --version` + `--dry-run=lookup`；buildx bin-image 後接 `scout`（只在 master） | renovate build.yml、buildx build.yml |
| 供應鏈 | buildx/moby/uv 皆 `sbom: true`、`provenance`、OIDC 登入 registry（`id-token: write`），PR 不簽 | 同上 |

## release 慣例

| 方式 | 誰 | 細節 |
|---|---|---|
| **tag 觸發** | just（`on.push.tags: '*'`）、buildx/docker-cli（同一 build.yml 掛 `tags: v*`）、moby bin-image（`docker-v*`）、cargo（`tags: 0.*`，只 publish crates.io） | 上傳用 `softprops/action-gh-release`（just v2、buildx v3 `draft: true`）；just 用 tag 是否符合 `^\d+\.\d+\.\d+$` 判 prerelease |
| **手動 `workflow_dispatch(tag)`** | uv、ruff（cargo-dist 生成，`release-gate` job 綁 environment 需另一人核准；dry-run 也要）、cli/cli（`deployment.yml` 輸入 tag_name/environment/dry_run，goreleaser + `gh release create`） | 大型專案偏好手動觸發 + environment 審核，而非 push tag 即發 |
| **semantic-release／conventional commits** | renovate（push main 即自動判版、發 npm + image；`DO_RELEASE` 依分支） | release-please 在這 9 個專案 **沒有** 使用者（不確定其他） |
| **版本 PR 先行** | uv `release-prepare.yml`（dispatch 開 PR 改版號；`plan.yml` 偵測 `is_release_pr` 才跑 crates policy check） | |
| **acceptance 獨立** | cli/cli `acceptance.yml` 只 dispatch、綁 environment | |

## agy 的建議與理由

**agy 無輸出。** 執行紀錄：
- 完整 brief（`ci_brief.txt`）以 `timeout 570 agy --sandbox -p ...` 跑兩次，皆 exit 124（逾時），stdout 只有 `Error: interrupted`（`ci_agy.md`）。
- 拆成三段小題（`ci_brief_a/b/c.txt`，各 570 s）：a 段 exit 1 → `Eligibility check failed: UNAVAILABLE (code 503)`；b、c 段再度逾時 `Error: interrupted`（`ci_agy_a/b/c.md`）。
- 對照：同一時段用一句話小題（「workflow_call 是什麼」）agy 90 s 內正常回答，判定是 **多 URL 逐檔閱讀類任務在 570 s 內跑不完**，非權限／設定問題。未給 command 權限、未動 `~/.gemini/antigravity-cli/settings.json`。
- 因此本文件全部改由 Claude 以 `gh api`（原始 yaml）＋ WebFetch（GitHub／Docker 官方文件）自查，下節建議標「Claude 自查」。

### Claude 自查：對 vendor_kit 的建議架構

依前例，vendor_kit（Python 引擎 → 多架構 image + POSIX sh 啟動器 + just；lint→unit→integration→release build→system→acceptance）建議採 **模式 B + C 混合：兩個入口檔 + 少量 reusable**，理由是 repo 規模接近 just/cargo（小），但有 image 與 system/acceptance 兩層慢測試（像 moby/uv 需要分流）：

```
.github/workflows/
  ci.yml          on: pull_request, push(main), merge_group(若之後開 merge queue), workflow_dispatch
                  jobs: lint → unit → integration → build-image(PR: 不 push; main: push :main + sha)
                        → system (PR: 需 label `ci:full`；main: 必跑) → ci-green (彙總, 唯一 required check)
  release.yml     on: push tags v*（或 workflow_dispatch(tag) + environment 審核，看團隊）
                  jobs: 重用 build-image.yml → 推 semver tag → acceptance → gh-release 上傳啟動器/檔案
  build-image.yml on: workflow_call  （被 ci.yml 與 release.yml 共用：buildx + QEMU 或 native arm matrix + imagetools 合併）
  nightly.yml     on: schedule  → 叫 build-image.yml + system/acceptance 全跑（可選）
```
- 共用：`build-image.yml` 用 `workflow_call`（同 uv `build-docker.yml` 被 ci/release 共用）；重複的環境設定（安裝 just、uv、buildx）做成 `.github/actions/setup-env` composite action（kind、renovate 做法）。
- 分流用 `if:` + PR 標籤而不是多檔（moby/renovate/uv 慣例）；`push:` 一律 `github.event_name != 'pull_request'`。
- required check 只設 `ci-green` 一個 job，內部用 `if: always()` 自己檢查 `needs.*.result`（cargo/uv 寫法），標籤條件 job 列入 allowed-skips。
- image tag：`docker/metadata-action` `type=ref,event=branch`（main）、`type=sha`、`type=semver`（tag）；`edge` 只是別名選擇，前例多用分支名。
- 跨架構測試：arm64 用 `ubuntu-24.04-arm` 原生 runner 跑 unit/integration（moby、cargo 慣例），QEMU 只留給 build。
- release：小專案先用 tag 觸發 + `softprops/action-gh-release`（just 範本）；等需要審核再改成 `workflow_dispatch` + environment（uv/cli 範本）。release-please／semantic-release 在前例中只有 renovate 用，且它是 npm 生態；vendor_kit 沒必要。

## 我認為 agy 可疑或無來源的地方

agy 沒有產出，故無可挑。以下改列 **Claude 自查中仍不確定／證據較弱** 的點，供 decision-review 雙軌時重點複核：

1. **kind／kubernetes 的 push-main 與 release 流程**：只確認 kind 的 GHA 4 檔都是 `pull_request`-only，且 `hack/release/` 有 `create.sh`／`push-node.sh` 手動腳本；prow 設定在 kubernetes/test-infra，未讀。kubernetes/kubernetes 的 workflows 未逐檔核對。
2. **`:edge` tag 慣例**：9 個專案原檔 grep `edge` 只命中 `SETUP_BUILDX_VERSION: edge`（buildx 版本），沒有任何 image 用 `type=edge`／`:edge`；「main 推 `:edge`」是 docker/metadata-action 文件提供的選項，不是這批前例的做法（前例用 `:master`／`:main` 分支名或 `sha`）。
3. **required check 名稱如何顯示 reusable 內部 job**：GitHub 文件頁（reusing-workflows）沒講；我依前例（全部收斂成一個彙總 job）推論，沒有直接文件證據。
4. **release-please**：9 個專案沒人用，不代表其他 Python 專案不用；只能說「這批前例裡零」。
5. **`$/` reusable 語法**：uv 已在用，GitHub 文件也已列出（且註明 GHES 不支援），但此語法很新，若 vendor_kit 需相容自架 runner／GHES 應用 `./.github/workflows/`。
6. **docker/github-builder `bake.yml`** 把 arm 平台送到 `ubuntu-24.04-arm` 的說法來自 Docker 文件摘要（WebFetch），沒有讀該 reusable workflow 的原檔。
7. **moby 的 runner 標籤 `ubuntu-26.04-arm`**、cargo `windows-11-arm` 是原檔所寫（2026-09 當下），若 GitHub 之後改名需更新。
8. cli/cli `lint.yml` 有 `paths:` 過濾，這會讓 required check 在不相干 PR 上「不出現」而非「skipped」；若把它列為 required 會卡 merge——前例中它是否被設為 required 無法從 yaml 得知（branch protection 設定不在 repo 內）。
