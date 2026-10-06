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

# 驗收層（test/acceptance/run.sh，ADR-0010）：另起一個不連外網的 docker:dind，用剛建好的引擎 image 走公開入口
# 跑生命週期；需要 daemon，所以不在 image/Dockerfile 的 stage 鏈裡。args 原樣轉給 bats（例如 --filter sync）。
[positional-arguments]
acceptance *args:
    bash test/acceptance/run.sh "$@"

# ---- release（#372 的 N1）：tag 觸發，建置端只輸出；推送、發 Release 由 release workflow 決定。不做 vN、latest 浮動 tag。----

# release 的支援平台（ADR-0011）。
release_platforms := "linux/amd64 linux/arm64"

# tag 要是 `vX.Y.Z` 且等於 Cargo workspace version（`[workspace.package]` 的 version；引擎版 compat::ENGINE_VERSION 由它加 `v`）。
release-check tag:
    #!/usr/bin/env bash
    set -euo pipefail
    tag={{ quote(tag) }}
    version=$(awk '/^\[/ { in_pkg = ($0 == "[workspace.package]") } in_pkg && /^version = "/ { gsub(/^version = "|"$/, ""); print; exit }' Cargo.toml)
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "release-check: cannot read [workspace.package] version from Cargo.toml" >&2
        exit 1
    fi
    if [[ ! $tag =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "release-check: tag $tag is not vX.Y.Z" >&2
        exit 1
    fi
    if [[ $tag != "v$version" ]]; then
        echo "release-check: tag $tag differs from the Cargo workspace version v$version" >&2
        exit 1
    fi
    echo "release-check: $tag"

# buildx 一次建 release_platforms 的引擎 image（每個平台各自跑完整 stage 鏈，測試沒過就建不出來）。
# output 原樣交給 --output，推不推由呼叫端決定（例如 `type=oci,dest=<檔>`，或 `type=image,name=<repo>,push-by-digest=true,push=true`）。
# LABEL 值同 build 先從 labels stage 取出。不產 provenance 與 SBOM：index 只含各平台的 image。
# 多平台要 docker-container 等支援多平台的 builder；以環境變數 BUILDX_BUILDER 指定，不改目前的 builder。
# 最後一行印 `index sha256:<digest>`（多架構 index digest）。
release-image output:
    #!/usr/bin/env bash
    set -euo pipefail
    dir=$(mktemp -d)
    trap 'rm -rf "$dir"' EXIT
    docker build --target labels --output "type=local,dest=$dir" -f image/Dockerfile .
    args=()
    while IFS= read -r line; do
        args+=(--build-arg "$line")
    done <"$dir/image_labels.env"
    platforms=$(tr ' ' ',' <<<{{ quote(release_platforms) }})
    docker buildx build "${args[@]}" --platform "$platforms" --provenance=false --sbom=false \
        --output {{ quote(output) }} --metadata-file "$dir/metadata.json" -f image/Dockerfile .
    index=$(sed -n 's/.*"containerimage.digest"[[:space:]]*:[[:space:]]*"\(sha256:[0-9a-f]\{64\}\)".*/\1/p' \
        "$dir/metadata.json" | head -n 1)
    if [[ -z $index ]]; then
        echo "release-image: no index digest in the buildx metadata" >&2
        exit 1
    fi
    echo "index $index"

# 比對 ref（多架構 index，例如 `<repo>@sha256:<digest>`）裡各平台的 protocol 與 schema LABEL（ADR-0011）：
# ref 要是 image index、平台剛好是 release_platforms（取不到 index 也算不符），vendor_kit.protocol.floor、
# vendor_kit.protocol.current、vendor_kit.schema.max 每個平台都要有值且彼此一致。只讀 registry，不 pull。
release-verify ref:
    #!/usr/bin/env bash
    set -euo pipefail
    ref={{ quote(ref) }}
    keys=(vendor_kit.protocol.floor vendor_kit.protocol.current vendor_kit.schema.max)
    format='{{{{range $p, $i := .Image}}{{{{$p}}'
    for key in "${keys[@]}"; do
        format+=" {{{{index \$i.Config.Labels \"$key\"}}"
    done
    format+='{{{{"\n"}}{{{{end}}'
    want=$(tr ' ' '\n' <<<{{ quote(release_platforms) }} | sort)
    got=$(docker buildx imagetools inspect "$ref" \
        --format '{{{{range .Manifest.Manifests}}{{{{.Platform.OS}}/{{{{.Platform.Architecture}}{{{{"\n"}}{{{{end}}' 2>/dev/null |
        awk 'NF' | sort || true)
    if [[ $got != "$want" ]]; then
        echo "release-verify: $ref is not an index of exactly [$(tr '\n' ' ' <<<"$want")]; it has [$(tr '\n' ' ' <<<"$got")]" >&2
        exit 1
    fi
    out=$(docker buildx imagetools inspect "$ref" --format "$format")
    first=
    while read -r platform values; do
        [[ -n $platform ]] || continue
        read -ra vals <<<"$values"
        if ((${#vals[@]} != ${#keys[@]})); then
            echo "release-verify: $platform lacks one of ${keys[*]}" >&2
            exit 1
        fi
        echo "$platform ${vals[*]}"
        if [[ -z $first ]]; then
            first=$values
        elif [[ $values != "$first" ]]; then
            echo "release-verify: LABELs differ across platforms (${keys[*]})" >&2
            exit 1
        fi
    done <<<"$out"
    echo "release-verify: ${keys[*]} agree across platforms"

# 發佈資產（ADR-0009）放到 dest（不在就建；已有東西就停，免得混進別次的檔）：每個平台一份 image tar（以該平台的 manifest digest pull，tag 成
# `<repo>:<version>` 後 docker save，存完即刪本機 tag）、旁邊同名 `.digest`（一行多架構 index digest，不是 tar 的雜湊）；
# 內嵌 `<repo>:<version>@<digest>` 的 bootstrap.sh（同 `just bootstrap`）；最後是其餘資產的 `SHA256SUMS`。
# digest 是已推上 registry 的多架構 index digest；repo 預設是 engine/install 的 ENGINE_REPO，只在演練時換成別的 registry
# （bootstrap.sh 的內嵌引用不收帶 port 的 registry，演練用的 registry 要開在預設 port，例如 `localhost/<路徑>`）。
release-assets digest dest repo="":
    #!/usr/bin/env bash
    set -euo pipefail
    digest={{ quote(digest) }}
    dest={{ quote(dest) }}
    repo={{ quote(repo) }}
    if [[ ! $digest =~ ^sha256:[0-9a-f]{64}$ ]]; then
        echo "release-assets: digest $digest is not sha256:<64 hex>" >&2
        exit 1
    fi
    if [[ -z $repo ]]; then
        repo=$(sed -n 's/^pub const ENGINE_REPO: &str = "\(.*\)";$/\1/p' engine/install/src/release.rs)
    fi
    dir=$(mktemp -d)
    trap 'rm -rf "$dir"' EXIT
    docker build --target labels --output "type=local,dest=$dir" -f image/Dockerfile .
    version=$(sed -n 's/^VK_VERSION=//p' "$dir/image_labels.env")
    if [[ -z $repo || -z $version ]]; then
        echo "release-assets: cannot read ENGINE_REPO or VK_VERSION" >&2
        exit 1
    fi
    if [[ -e $dest && -n $(ls -A -- "$dest") ]]; then
        echo "release-assets: $dest is not empty" >&2
        exit 1
    fi
    mkdir -p -- "$dest"
    for platform in {{ release_platforms }}; do
        manifest=$(docker buildx imagetools inspect "$repo@$digest" \
            --format "{{{{range .Manifest.Manifests}}{{{{if eq (printf \"%s/%s\" .Platform.OS .Platform.Architecture) \"$platform\"}}{{{{.Digest}}{{{{end}}{{{{end}}")
        if [[ ! $manifest =~ ^sha256:[0-9a-f]{64}$ ]]; then
            echo "release-assets: $repo@$digest has no single manifest for $platform" >&2
            exit 1
        fi
        docker pull --quiet --platform "$platform" "$repo@$manifest" >/dev/null
        actual=$(docker image inspect --format '{{{{.Os}}/{{{{.Architecture}}' "$repo@$manifest")
        if [[ $actual != "$platform" ]]; then
            echo "release-assets: $repo@$manifest is $actual, expected $platform" >&2
            exit 1
        fi
        name="vendor_kit-$version-${platform//\//-}"
        docker tag "$repo@$manifest" "$repo:$version"
        docker save -o "$dest/$name.tar" "$repo:$version"
        docker image rm "$repo:$version" >/dev/null
        # 拿掉 tag 後只剩 digest 引用的 image 可能已一起刪掉（classic store），所以這裡不在意 No such image。
        docker image rm "$repo@$manifest" >/dev/null 2>&1 || true
        printf '%s\n' "$digest" >"$dest/$name.digest"
        echo "$platform $manifest -> $name.tar"
    done
    {{ quote(just_executable()) }} --justfile {{ quote(justfile()) }} bootstrap "$repo:$version@$digest" "$dest"
    (
        cd -- "$dest"
        sha256sum -- * >"$dir/SHA256SUMS"
        mv -- "$dir/SHA256SUMS" SHA256SUMS
    )
    echo "release-assets: $dest"
