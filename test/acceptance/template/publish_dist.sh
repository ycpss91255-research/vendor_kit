#!/usr/bin/env bash
# 工具端多架構建置範本（草稿）：把工具 repo 的 dist/ 建成多架構純資料 image，兩平台逐檔一致才上 tag。
# 正式文件位置（工具端契約文件）還沒定；定了以後這份移過去，這裡只留驗收 fixture 用的那份。
#
# 用法：publish_dist.sh <image> <tag> [<context>]
#   <image>   不含 tag 的 image 名稱，例如 ghcr.io/<owner>/<package>
#   <tag>     要發布的 tag；registry 上已經有這個 tag 就停下，不覆蓋（已發布的不改）
#   <context> 含 Dockerfile.dist 與 dist/ 的目錄，預設是目前目錄
#
# 步驟（#26）：
#   1. 同一次 `docker buildx build --platform linux/amd64,linux/arm64` 建兩平台，只以 digest 推送、不上 tag。
#      Dockerfile.dist 只有 COPY，不需要 qemu。
#   2. 從 index 讀出每個平台的 manifest digest，各自用 `docker create`（入口設成不存在的檔，永遠不 run）
#      加 `docker cp <容器>:/dist/.` 展開，跟 VK 取件走同一條路（ADR-0006）。以平台 manifest digest 建，
#      不以 index 加 --platform，免得本機已有另一個平台的 image 時被拿去重用、比成同一個平台。
#   3. 兩平台展開結果逐檔比對，再跟 <context>/dist/ 比對一次；任何差異就失敗，不上 tag。
#   4. 全部一致才用 `docker buildx imagetools create` 把 index 掛上 <tag>。
#
# 需要：docker 與 buildx，builder 要能建多平台（GitHub Actions 用 docker/setup-buildx-action 建的
# docker-container builder 即可），而且已登入 <image> 所在的 registry。
set -euo pipefail

platforms=(linux/amd64 linux/arm64)
never_run=/__vk_never_run__

die() {
    printf 'publish_dist: %s\n' "$*" >&2
    exit 1
}

[[ $# -ge 2 && $# -le 3 ]] || die "usage: publish_dist.sh <image> <tag> [<context>]"
image=$1
tag=$2
context=${3:-.}
[[ -f $context/Dockerfile.dist && -d $context/dist ]] ||
    die "$context must contain Dockerfile.dist and dist/"

if docker buildx imagetools inspect "$image:$tag" >/dev/null 2>&1; then
    die "$image:$tag already exists; published tags are never overwritten"
fi

work=$(mktemp -d)
containers=()
cleanup() {
    local c
    for c in "${containers[@]}"; do
        docker rm "$c" >/dev/null 2>&1 || true
    done
    rm -rf "$work"
}
trap cleanup EXIT

# 1. 兩平台同一次建置，只以 digest 推送。
platform_list=$(
    IFS=,
    printf '%s' "${platforms[*]}"
)
docker buildx build \
    --platform "$platform_list" \
    --file "$context/Dockerfile.dist" \
    --provenance=false --sbom=false \
    --output "type=image,name=$image,push-by-digest=true,name-canonical=true,push=true" \
    --metadata-file "$work/metadata.json" \
    "$context"
index=$(sed -n 's/.*"containerimage.digest"[[:space:]]*:[[:space:]]*"\(sha256:[0-9a-f]\{64\}\)".*/\1/p' \
    "$work/metadata.json" | head -n 1)
[[ -n $index ]] || die "no index digest in buildx metadata"
printf 'index %s@%s\n' "$image" "$index"

# 2. 每個平台以自己的 manifest digest 展開。
for platform in "${platforms[@]}"; do
    manifest=$(docker buildx imagetools inspect "$image@$index" \
        --format "{{range .Manifest.Manifests}}{{if eq (printf \"%s/%s\" .Platform.OS .Platform.Architecture) \"$platform\"}}{{.Digest}}{{end}}{{end}}")
    [[ $manifest =~ ^sha256:[0-9a-f]{64}$ ]] || die "index has no single manifest for $platform"
    docker pull --quiet "$image@$manifest" >/dev/null
    actual=$(docker image inspect --format '{{.Os}}/{{.Architecture}}' "$image@$manifest")
    [[ $actual == "$platform" ]] || die "$image@$manifest is $actual, expected $platform"
    c=$(docker create --entrypoint "$never_run" "$image@$manifest")
    containers+=("$c")
    out=$work/${platform//\//_}
    mkdir "$out"
    docker cp "$c:/dist/." "$out" >/dev/null
    printf '%s %s\n' "$platform" "$manifest"
done

# 3. 兩平台逐檔一致，且跟本機 dist/ 一致。
first=$work/${platforms[0]//\//_}
for platform in "${platforms[@]:1}"; do
    diff -r "$first" "$work/${platform//\//_}" ||
        die "${platforms[0]} and $platform differ; not tagging"
done
diff -r "$context/dist" "$first" || die "image content differs from $context/dist; not tagging"

# 4. 一致才上 tag。
docker buildx imagetools create --tag "$image:$tag" "$image@$index"
printf 'published %s:%s@%s\n' "$image" "$tag" "$index"
