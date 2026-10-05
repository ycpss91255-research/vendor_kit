//! 印出建引擎 image 用的 build-arg（[`compat::image_build_args`]）。
//!
//! `image/Dockerfile` 的 test stage 把輸出存成 `/out/image_labels.env`；`just build` 讀它帶 `--build-arg`，
//! 最終 stage 再與同一份檔比對，不一致就建不出 image。

use std::io::Write;
use std::process::ExitCode;

fn main() -> ExitCode {
    match std::io::stdout().write_all(compat::image_build_args().as_bytes()) {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("image_labels: {e}");
            ExitCode::FAILURE
        }
    }
}
