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
# bats 與 shellcheck 取 base（Debian trixie）的套件；bats 版本固定在 1.11.x，換 base 時版本變了就在這裡停。
RUN apt-get update \
    && apt-get install -y --no-install-recommends git bats shellcheck \
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

# 薄殼模板（ADR-0007：模板隨 image 出貨）：用 test stage 產生的訊息片段跑 launcher/shell/assemble.sh，
# 組出薄殼四檔的模板本文（不含自描述標頭，標頭由引擎寫進安裝目錄時加）。
FROM test AS shell
RUN bash launcher/shell/assemble.sh /out/bootstrap_messages.sh /out/shell

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
# 啟動器讀這三個 LABEL 判介面版（ADR-0008:27），鍵與 launcher/launch.sh 的 vk_label_* 一致。
# 值由 build-arg 帶入，來源只有 engine/compat 的 THIS 與 Cargo workspace version（compat::image_build_args）；
# 這裡與 test stage 產出的 image_labels.env 逐位元組比對，沒帶或不一致就建不出 image。
ARG VK_PROTOCOL_FLOOR VK_PROTOCOL_CURRENT VK_VERSION
RUN --mount=type=bind,from=test,source=/out/image_labels.env,target=/tmp/image_labels.env \
    printf 'VK_PROTOCOL_FLOOR=%s\nVK_PROTOCOL_CURRENT=%s\nVK_VERSION=%s\n' \
        "$VK_PROTOCOL_FLOOR" "$VK_PROTOCOL_CURRENT" "$VK_VERSION" | cmp -s - /tmp/image_labels.env \
    || { echo "build-args differ from compat::image_build_args; build with: just build" >&2; exit 1; }
LABEL vendor_kit.protocol.floor=$VK_PROTOCOL_FLOOR \
      vendor_kit.protocol.current=$VK_PROTOCOL_CURRENT \
      org.opencontainers.image.version=$VK_VERSION
ENTRYPOINT ["/usr/local/bin/vendor_kit"]
