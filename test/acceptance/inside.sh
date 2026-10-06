#!/usr/bin/env bash
# 驗收層的測試端（run.sh 在測試端容器裡執行）：等 dind 起來，把剛建好的引擎 image 做成首次導入要的 OCI tar 與
# 同名 .digest，組出內嵌這個引用的 bootstrap.sh，再跑 test/acceptance/*.bats（參數原樣轉給 bats）。
#
# 環境：DOCKER_HOST 指向 dind；/acc 是跟 dind 共用、兩邊同一路徑的 volume；/in/engine-src.tar 是主機 docker save 的
# 引擎 image（tag 是 VK_ACC_SOURCE_IMAGE）；/src、/out 來自 image/Dockerfile 的 test stage。
#
# - OCI tar（ADR-0010:22，受測的是剛建好的 image）：引擎 image 載進 dind 後，以只有 FROM 的 Dockerfile 經 buildx
#   輸出成 OCI tar，name 是 `<ENGINE_REPO>:<VK_VERSION>`（引擎在首次導入核對這兩段，engine/install 的 release）。
#   BUILDKIT_MULTI_PLATFORM=1 讓頂層描述是 image index（同發佈的多架構 image 的形狀，這裡只有本機一個平台）。
#   index.json 唯一那筆描述的 digest 寫成同名 .digest（ADR-0009）。輸出後刪掉 dind 裡的 image 與建置快取，
#   首次導入時引擎只能從 tar 載入。
# - bootstrap.sh：用 test stage 的組裝腳本（image/bootstrap/assemble.sh，同 `just bootstrap`）與訊息片段組，
#   內嵌引用是 `<ENGINE_REPO>:<VK_VERSION>@<index digest>`，P 是 image_labels.env 的 VK_PROTOCOL_CURRENT。
set -euo pipefail

acc=/acc
export TMPDIR=$acc/tmp
mkdir -p "$TMPDIR"

for _ in $(seq 120); do
    if docker info >/dev/null 2>&1; then
        break
    fi
    sleep 1
done
docker info --format 'dind: docker {{.ServerVersion}}, storage driver {{.Driver}} {{.DriverStatus}}'

# 引擎 repo 只寫在 engine/install（release::ENGINE_REPO），這裡從原始碼讀。
repo=$(sed -n 's/^pub const ENGINE_REPO: &str = "\(.*\)";$/\1/p' /src/engine/install/src/release.rs)
version=$(sed -n 's/^VK_VERSION=//p' /out/image_labels.env)
proto=$(sed -n 's/^VK_PROTOCOL_CURRENT=//p' /out/image_labels.env)
if [[ -z $repo || -z $version || -z $proto ]]; then
    echo "inside.sh: cannot read ENGINE_REPO, VK_VERSION or VK_PROTOCOL_CURRENT" >&2
    exit 1
fi

docker load -q -i /in/engine-src.tar
mkdir -p "$acc/build"
printf 'FROM %s\n' "$VK_ACC_SOURCE_IMAGE" >"$acc/build/Dockerfile"
docker buildx build -q --build-arg BUILDKIT_MULTI_PLATFORM=1 \
    --output "type=oci,dest=$acc/engine.tar,name=$repo:$version" "$acc/build" >/dev/null
digests=$(tar -xOf "$acc/engine.tar" index.json | grep -o '"digest":"sha256:[0-9a-f]\{64\}"' || true)
if [[ $(wc -l <<<"$digests") != 1 || -z $digests ]]; then
    echo "inside.sh: index.json of the OCI tar does not hold exactly one descriptor" >&2
    exit 1
fi
digest=${digests#'"digest":"'}
digest=${digest%'"'}
printf '%s\n' "$digest" >"$acc/engine.digest"
docker image rm "$VK_ACC_SOURCE_IMAGE" >/dev/null
docker builder prune -af >/dev/null

ref="$repo:$version@$digest"
bash /src/image/bootstrap/assemble.sh "$ref" "$proto" /out/bootstrap_messages.sh "$acc/bootstrap.sh"
echo "engine under test: $ref"

export VK_ACC_REF=$ref
export VK_ACC_TAR=$acc/engine.tar
export VK_ACC_BOOTSTRAP=$acc/bootstrap.sh
bats "$@" /src/test/acceptance
