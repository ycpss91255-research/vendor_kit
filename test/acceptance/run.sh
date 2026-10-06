#!/usr/bin/env bash
# 驗收層（#372 的 N22、N51；ADR-0010、ADR-0011）：另起一個 docker:dind，用剛建好的引擎 image 走公開入口跑生命週期。
# `just acceptance` 與 CI（.github/workflows/test.yml 的 acceptance job）都跑這支，主機只需要 Docker。
#
# 用法：run.sh [bats 參數]...（例如 --filter sync；預設跑 test/acceptance/*.bats 全部）
#
# 流程：
#   1. 在主機建引擎 image（同 justfile 的 build：先取 labels stage 的 image_labels.env 當 --build-arg）與
#      test stage，再以 runner.Dockerfile 疊出測試端 image；三個 tag 都帶這次的 id，用完即刪。
#   2. 引擎 image 以 docker save 存成 tar，交給測試端載入 dind（inside.sh 再用 buildx 輸出成 OCI tar）。
#   3. 建 --internal 網路（不連外網：需要 registry 的步驟會失敗，不會悄悄通過）與共用 volume，起 docker:dind。
#   4. 測試端容器跟 dind 共用網路命名空間（DOCKER_HOST=tcp://127.0.0.1:2375），共用 volume 掛在兩邊同一個路徑
#      /acc：引擎與 test runner 的 bind mount 由 dind 解析路徑，fixture repo 與 session 目錄（TMPDIR）都要在兩邊看得到。
#   5. 結束時（成功、失敗或中斷）刪掉這次建的容器、volume、網路與 image tag；docker:dind、docker:cli 等
#      共用的 base image 不刪。
set -euo pipefail

# dind 與測試端 docker CLI 的版本：dind 預設用 containerd image store（docker 29 起），OCI tar 才載得進去。
vk_acc_docker=29.8.0

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
root=$(cd -- "$here/../.." && pwd)

id="vk-acceptance-$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')"
engine="vendor_kit:$id"
test_image="vendor_kit:$id-test"
runner="vendor_kit:$id-runner"
net="$id-net"
vol="$id-vol"
dind="$id-dind"
client="$id-client"
tmp=$(mktemp -d)

cleanup() {
    docker rm -fv "$client" "$dind" >/dev/null 2>&1 || true
    docker volume rm "$vol" >/dev/null 2>&1 || true
    docker network rm "$net" >/dev/null 2>&1 || true
    docker image rm "$engine" "$test_image" "$runner" >/dev/null 2>&1 || true
    rm -rf -- "$tmp"
}
trap cleanup EXIT

cd -- "$root"

# 1. 引擎 image（同 justfile 的 build）、test stage 與測試端 image。
docker build --target labels --output "type=local,dest=$tmp/labels" -f image/Dockerfile .
args=()
while IFS= read -r line; do
    args+=(--build-arg "$line")
done <"$tmp/labels/image_labels.env"
docker build "${args[@]}" -t "$engine" -f image/Dockerfile .
docker build --target test -t "$test_image" -f image/Dockerfile .
docker build --build-arg "VK_TEST_IMAGE=$test_image" --build-arg "VK_DOCKER_VERSION=$vk_acc_docker" \
    -t "$runner" -f test/acceptance/runner.Dockerfile test/acceptance

# 2. 交給測試端的引擎 image。
mkdir -p "$tmp/in"
docker save -o "$tmp/in/engine-src.tar" "$engine"
chmod -R a+rX "$tmp/in"

# 3. 不連外網的 dind。
docker network create --internal "$net" >/dev/null
docker volume create "$vol" >/dev/null
docker run -d --privileged --name "$dind" --network "$net" -e DOCKER_TLS_CERTDIR= \
    -v "$vol:/acc" "docker:$vk_acc_docker-dind" >/dev/null

# 4. 測試端：準備 OCI tar 與 bootstrap.sh，跑 bats。
docker run --rm --name "$client" --network "container:$dind" -e DOCKER_HOST=tcp://127.0.0.1:2375 \
    -e VK_ACC_SOURCE_IMAGE="$engine" \
    -v "$vol:/acc" -v "$tmp/in:/in:ro" "$runner" \
    bash /src/test/acceptance/inside.sh "$@"
