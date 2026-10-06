# VK repo 作者用的 recipe（不是使用者的 VK recipe）。主機只需 Docker 與 just，Rust 全在 image/Dockerfile 的建置 stage 裡跑。

image := "vendor_kit:dev"

# 格式、clippy、全部測試（停在 image/Dockerfile 的 test stage）
test:
    docker build --target test -f image/Dockerfile .

# 建引擎 image（含 test stage，測試沒過就建不出來）。
# LABEL 值先從 labels stage 取出（engine/compat 的常數與 Cargo workspace version），再當 --build-arg 帶入。
build:
    #!/usr/bin/env bash
    set -euo pipefail
    dir=$(mktemp -d)
    trap 'rm -rf "$dir"' EXIT
    docker build --target labels --output "type=local,dest=$dir" -f image/Dockerfile .
    args=()
    while IFS= read -r line; do
        args+=(--build-arg "$line")
    done <"$dir/image_labels.env"
    docker build "${args[@]}" -t {{image}} -f image/Dockerfile .

# 組出發佈用的 bootstrap.sh，放到 dest 目錄（不在就建）。ref 是內嵌引擎的 pinned 引用
# `<registry>/<路徑>:vX.Y.Z@sha256:<digest>`，tag 要等於 Cargo workspace version；
# 介面版 P 先從 labels stage 取出（compat 的 THIS），再跟 ref 一起當 --build-arg 帶給 bootstrap stage。
bootstrap ref dest:
    #!/usr/bin/env bash
    set -euo pipefail
    dir=$(mktemp -d)
    trap 'rm -rf "$dir"' EXIT
    docker build --target labels --output "type=local,dest=$dir" -f image/Dockerfile .
    proto=$(sed -n 's/^VK_PROTOCOL_CURRENT=//p' "$dir/image_labels.env")
    docker build --target bootstrap \
        --build-arg VK_ENGINE_REF={{ quote(ref) }} --build-arg "VK_PROTOCOL_CURRENT=$proto" \
        --output type=local,dest={{ quote(dest) }} -f image/Dockerfile .
