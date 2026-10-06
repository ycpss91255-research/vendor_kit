# syntax=docker/dockerfile:1
# VK 引擎 image。stage 串成一條鏈（ADR-0011）：本機 `just test` 停在 test，
# `just build` 與 CI 走同一條鏈建到最後，測試沒過就建不出 image。

# Rust 版本只寫在 rust-toolchain.toml；這裡用浮動的官方 image，由 rustup 依該檔裝指定版本與元件。
FROM rust:1-slim AS toolchain
WORKDIR /src
COPY rust-toolchain.toml ./
RUN rustup toolchain install && rustc --version

FROM toolchain AS source
COPY Cargo.toml Cargo.lock ./
COPY engine engine
COPY test test
COPY doc/contract/reason_codes.csv doc/contract/reason_codes.csv
# test/boundary 讀架構圖檢查模組邊界（ADR-0014）。
COPY doc/diagram doc/diagram

# 檢查與靜態編譯：產物與訊息表一致、格式、clippy、musl 靜態執行檔，再以該執行檔跑全部測試；
# 接著跑啟動器（launcher/）的 shellcheck、命令白名單 lint 與 bats。
# 主機端 bash（bootstrap.sh、啟動器）用的訊息片段與最終 stage 的 LABEL 值（image_labels.env）只寫到 /out，不進 git。
FROM source AS test
# engine/merge 的 unit 測試要呼叫 git merge-file，rust:1-slim 不帶 git。
# musl-tools（musl-gcc）：引擎經 update 連到 engine/registry，它的 TLS（rustls 的 ring）要編 C，
# musl 靜態編譯要 musl 的 C 編譯器（#577）；只有這個 stage 編執行檔，其他 stage 不裝。
# bats 與 shellcheck 取 base（Debian trixie）的套件；bats 版本固定在 1.11.x，換 base 時版本變了就在這裡停。
RUN apt-get update \
    && apt-get install -y --no-install-recommends git musl-tools bats shellcheck \
    && rm -rf /var/lib/apt/lists/* \
    && bats --version | grep -q '^Bats 1\.11\.' \
    && shellcheck --version
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    set -eu; \
    target="$(uname -m)-unknown-linux-musl"; \
    cargo run --locked -q -p msggen -- \
        --csv doc/contract/reason_codes.csv \
        --rust engine/messages/src/generated.rs \
        --check --bash-out /out/bootstrap_messages.sh; \
    cargo fmt --all --check; \
    cargo clippy --locked --workspace --all-targets -- -D warnings; \
    cargo build --locked --release -p vendor_kit --target "$target"; \
    cp "target/$target/release/vendor_kit" /out/vendor_kit; \
    VK_BIN=/out/vendor_kit cargo test --locked --workspace; \
    cargo run --locked -q -p compat --bin image_labels >/out/image_labels.env
# 啟動器：shellcheck（啟動器本體與白名單 lint）、命令白名單 lint、bats。
# bats 的訊息文字取自上一步 msggen 產生的片段（VK_MESSAGES）。launcher/ 在 cargo 之後才 COPY，
# 只改啟動器時不必重跑 Rust 的建置與測試。
COPY launcher launcher
RUN set -eu; \
    shellcheck -x launcher/*.sh launcher/lint/check_commands.sh; \
    launcher/lint/check_commands.sh; \
    VK_MESSAGES=/out/bootstrap_messages.sh bats launcher/test
# bootstrap.sh 的組裝（image/bootstrap/assemble.sh）：用固定的假引用與介面版 1 組一份，跑「內嵌清單 ⊆ 真本」檢查
# （msggen --embedded：內嵌片段跟訊息表一致，入口走得到的代碼都是 source 含 bootstrap 的 active 代碼）、
# shellcheck 與 bats 的 smoke。發佈用的那份由下面的 bootstrap stage 以同一支腳本組。
# 組好的單一檔的 shellcheck 只關掉合併成一檔才出現的誤報（各檔本身已在上一步全規則檢查）：SC2034 是片段的
# vk_msg_* 由 diag.sh 以間接展開讀；SC2128、SC2178 是不同函式各自 local 的同名變數（host.sh 的陣列 want）。
ENV VK_BOOTSTRAP_SHELLCHECK_EXCLUDE=SC2034,SC2128,SC2178
COPY image/bootstrap image/bootstrap
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    set -eu; \
    shellcheck -x image/bootstrap/assemble.sh; \
    bash image/bootstrap/assemble.sh \
        ghcr.io/ycpss91255-research/vendor_kit:v0.0.0@sha256:0000000000000000000000000000000000000000000000000000000000000000 \
        1 /out/bootstrap_messages.sh /out/bootstrap_smoke.sh; \
    cargo run --locked -q -p msggen -- \
        --csv doc/contract/reason_codes.csv \
        --rust engine/messages/src/generated.rs \
        --check --embedded /out/bootstrap_smoke.sh; \
    shellcheck -e "$VK_BOOTSTRAP_SHELLCHECK_EXCLUDE" /out/bootstrap_smoke.sh; \
    VK_BOOTSTRAP=/out/bootstrap_smoke.sh VK_MESSAGES=/out/bootstrap_messages.sh bats image/bootstrap

# 薄殼模板（ADR-0007：模板隨 image 出貨）：用 test stage 產生的訊息片段跑 launcher/shell/assemble.sh，
# 組出薄殼四檔的模板本文（不含自描述標頭，標頭由引擎寫進安裝目錄時加）。
FROM test AS shell
RUN bash launcher/shell/assemble.sh /out/bootstrap_messages.sh /out/shell

# 發佈用的 bootstrap.sh（#372 的 N1）：`just bootstrap` 以 build-arg 帶內嵌引擎的 pinned 引用（VK_ENGINE_REF）與
# 介面版 P（VK_PROTOCOL_CURRENT，取自 image_labels.env），組好後同 test stage 跑 msggen --embedded 與 shellcheck（排除同一組規則）。
# 引用的 tag 要等於這次建置的版本（image_labels.env 的 VK_VERSION），P 要等於 VK_PROTOCOL_CURRENT；
# 引用的 <registry>/<路徑> 由引擎在首次導入時核對（engine/install 的 release）。
# 這兩個 stage 放在最終 image 之前：`just build` 不帶 --target，建的是最後一個 stage。
FROM test AS bootstrap-build
ARG VK_ENGINE_REF VK_PROTOCOL_CURRENT
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    set -eu; \
    version=$(sed -n 's/^VK_VERSION=//p' /out/image_labels.env); \
    proto=$(sed -n 's/^VK_PROTOCOL_CURRENT=//p' /out/image_labels.env); \
    case $VK_ENGINE_REF in \
        *:"$version"@*) ;; \
        *) echo "VK_ENGINE_REF must be tagged $version (this build's version); build with: just bootstrap <ref> <dest>" >&2; exit 1 ;; \
    esac; \
    if [ "$VK_PROTOCOL_CURRENT" != "$proto" ]; then \
        echo "VK_PROTOCOL_CURRENT must be $proto (compat::image_build_args); build with: just bootstrap <ref> <dest>" >&2; \
        exit 1; \
    fi; \
    bash image/bootstrap/assemble.sh "$VK_ENGINE_REF" "$VK_PROTOCOL_CURRENT" \
        /out/bootstrap_messages.sh /out/bootstrap.sh; \
    cargo run --locked -q -p msggen -- \
        --csv doc/contract/reason_codes.csv \
        --rust engine/messages/src/generated.rs \
        --check --embedded /out/bootstrap.sh; \
    shellcheck -e "$VK_BOOTSTRAP_SHELLCHECK_EXCLUDE" /out/bootstrap.sh

# bootstrap.sh 的出口：`just bootstrap` 以 --output 取出 /bootstrap.sh。
FROM scratch AS bootstrap
COPY --from=bootstrap-build /out/bootstrap.sh /bootstrap.sh

# LABEL 值的出口：`just build` 先建這個 stage 取出 image_labels.env，再把每行當 --build-arg 帶給最終 stage。
FROM scratch AS labels
COPY --from=test /out/image_labels.env /image_labels.env

# 最終 image：引擎是 musl 靜態執行檔，不需要 libc；但引擎在容器內要用 git（ADR-0007 的 git merge-file），
# 帶得到 git 的最小 base 是 alpine。工具 image 只搬不跑（ADR-0006），這裡不放其他工具。
FROM alpine:3.24 AS engine
RUN apk add --no-cache git
# 容器內的語言與時區寫死（ADR-0012）。
ENV LC_ALL=C.UTF-8 TZ=UTC
COPY --from=test /out/vendor_kit /usr/local/bin/vendor_kit
# install 與 sync 從這裡讀薄殼模板；路徑與 engine/install 的 release::SHIPPED_DIR 加 SHELL_DIR 一致。
COPY --from=shell /out/shell/ /usr/share/vendor_kit/shell/
# 啟動器讀介面版區間與版本這三個 LABEL 判介面版（ADR-0008:27），鍵與 launcher/launch.sh 的 vk_label_* 一致。
# vendor_kit.schema.max 公告檔案版上限，啟動器現在不讀；留給判引擎降版（VK0007）與比對兩平台的 LABEL。
# 值由 build-arg 帶入，來源只有 engine/compat 的 THIS 與 Cargo workspace version（compat::image_build_args）；
# 這裡與 test stage 產出的 image_labels.env 逐位元組比對，沒帶或不一致就建不出 image。
ARG VK_PROTOCOL_FLOOR VK_PROTOCOL_CURRENT VK_SCHEMA_MAX VK_VERSION
RUN --mount=type=bind,from=test,source=/out/image_labels.env,target=/tmp/image_labels.env \
    printf 'VK_PROTOCOL_FLOOR=%s\nVK_PROTOCOL_CURRENT=%s\nVK_SCHEMA_MAX=%s\nVK_VERSION=%s\n' \
        "$VK_PROTOCOL_FLOOR" "$VK_PROTOCOL_CURRENT" "$VK_SCHEMA_MAX" "$VK_VERSION" \
        | cmp -s - /tmp/image_labels.env \
    || { echo "build-args differ from compat::image_build_args; build with: just build" >&2; exit 1; }
LABEL vendor_kit.protocol.floor=$VK_PROTOCOL_FLOOR \
      vendor_kit.protocol.current=$VK_PROTOCOL_CURRENT \
      vendor_kit.schema.max=$VK_SCHEMA_MAX \
      org.opencontainers.image.version=$VK_VERSION
ENTRYPOINT ["/usr/local/bin/vendor_kit"]
