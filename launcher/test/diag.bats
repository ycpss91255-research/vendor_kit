#!/usr/bin/env bats
# 診斷輸出（03 輸出的訊息格式）：第一行固定前綴、續行原樣、占位符照原樣換進、結束碼取最大。

load helper

setup() {
    common_setup
}

@test "the first line has the fixed prefix and stdout stays empty" {
    vk 'vk_diag VK0033'
    [ "$status" -eq 2 ]
    [ "$output" = "" ]
    [ "$stderr" = 'vendor_kit: error[VK0033]: Docker was not found on the host. Install Docker and retry.' ]
}

@test "continuation lines are printed as they are" {
    vk 'vk_diag VK0034 download_url https://d.invalid install_command "x y"'
    [ "${#stderr_lines[@]}" -eq 3 ]
    [ "${stderr_lines[0]}" = 'vendor_kit: error[VK0034]: just was not found on the host. Use the GitHub release.' ]
    [ "${stderr_lines[1]}" = 'Download: https://d.invalid' ]
    [ "${stderr_lines[2]}" = 'Install: x y' ]
}

@test "placeholder values are inserted literally" {
    vk 'vk_diag VK0012 version '\''a&b\1 * $x <version>'\'''
    [ "$stderr" = 'vendor_kit: error[VK0012]: Docker 19.03 or later is required; the current version is a&b\1 * $x <version>. Upgrade Docker and retry.' ]
}

@test "the exit code is the highest of all diagnostics" {
    vk 'vk_diag VK0033; vk_diag VK0040 bootstrap_X 1 engine_X 2; vk_diag VK0035'
    [ "$status" -eq 3 ]
    [ "${stderr_lines[1]}" = 'vendor_kit: fatal[VK0040]: This bootstrap.sh is for major version 1, but the locked engine requires major version 2. No files were modified. Download bootstrap.sh for major version 2 from the Release and retry.' ]
}

@test "no diagnostics means exit code 0" {
    vk ':'
    [ "$status" -eq 0 ]
    [ "$stderr" = "" ]
}

@test "a code missing from the fragment is reported as VK0056" {
    vk 'vk_diag VK9999'
    [ "$status" -eq 2 ]
    [ "$stderr" = 'vendor_kit: error[VK0056]: Internal vendor_kit error: unknown reason code VK9999. This is a VK bug. Report it at https://github.com/ycpss91255-research/vendor_kit/issues and attach run log none.' ]
}
