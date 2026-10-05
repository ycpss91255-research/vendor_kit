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

# 檢查與靜態編譯：產物與訊息表一致、格式、clippy、musl 靜態執行檔，再以該執行檔跑全部測試。
# bootstrap.sh 用的訊息片段只寫到 /out，不進 git。
FROM source AS test
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
    VK_BIN=/out/vendor_kit cargo test --locked --workspace

# 最終 image：引擎是 musl 靜態執行檔，不需要 libc；但引擎在容器內要用 git（ADR-0007 的 git merge-file），
# 帶得到 git 的最小 base 是 alpine。工具 image 只搬不跑（ADR-0006），這裡不放其他工具。
FROM alpine:3.24 AS engine
RUN apk add --no-cache git
# 容器內的語言與時區寫死（ADR-0012）。
ENV LC_ALL=C.UTF-8 TZ=UTC
COPY --from=test /out/vendor_kit /usr/local/bin/vendor_kit
ENTRYPOINT ["/usr/local/bin/vendor_kit"]
