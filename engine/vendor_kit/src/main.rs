//! VK 引擎的單一入口。
//!
//! 參數由這裡解析並分派到各指令；指令清單照 04 指令，尚未實作的指令不註冊。
//! 不用 clap 之類的套件產生錯誤與用法：VK 的 stderr 格式由 03 固定，
//! 只能經 `diagnostics` 與 `output` 印出。

mod cli;

use std::process::ExitCode;

fn main() -> ExitCode {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    let stdout = std::io::stdout();
    let stderr = std::io::stderr();
    ExitCode::from(cli::run(&args, &stdout, &stderr))
}
