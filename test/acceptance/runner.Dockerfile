# check=skip=InvalidDefaultArgInFrom
# 驗收層的測試端 image（test/acceptance/run.sh 建，用完即刪）：以 image/Dockerfile 的 test stage 為 base
# （ADR-0011 的分層：驗收接在前面各層之後），補上 docker CLI 與 buildx，經 DOCKER_HOST 操作另起的 docker:dind。
# test stage 已有 bats、git、just（下限版 1.33.0）、/src 的原始碼與 /out 的訊息片段、image_labels.env。
# 兩個 ARG 都由 run.sh 帶入、沒有預設值，所以關掉 InvalidDefaultArgInFrom 這條建置檢查。
ARG VK_TEST_IMAGE
ARG VK_DOCKER_VERSION
FROM docker:${VK_DOCKER_VERSION}-cli AS cli

FROM ${VK_TEST_IMAGE}
COPY --from=cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=cli /usr/local/libexec/docker/cli-plugins/docker-buildx /usr/local/libexec/docker/cli-plugins/docker-buildx
