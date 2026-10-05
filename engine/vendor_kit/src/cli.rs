//! 參數分派。

use std::ffi::OsString;
use std::io::Write;

use diagnostics::{Diagnostic, Diagnostics};
use output::{Output, SHORT_USAGE};

/// 引擎版本；版本行印 `vendor_kit v<X.Y.Z>`，與 tag 的寫法一致。
pub const VERSION: &str = concat!("v", env!("CARGO_PKG_VERSION"));

/// 跑一次引擎，回傳結束碼。寫入 stdout／stderr 失敗時無處可報，
/// 仍回同一個結束碼。
pub fn run<O, E>(args: &[OsString], stdout: O, stderr: E) -> u8
where
    O: Write,
    E: Write + Clone,
{
    let mut out = Output::new(stdout, stderr.clone());
    let mut diags = Diagnostics::new(stderr);
    let Some(first) = args.first() else {
        // 03 輸出：只打 `just vendor_kit` 時，stderr 依序印版本行、VK0024、簡短用法，以 2 結束。
        let _ = out.stderr_line(&output::version_line(VERSION));
        let _ = diags.emit(&Diagnostic::new(&messages::VK0024));
        let _ = out.stderr_line(SHORT_USAGE);
        let _ = out.flush();
        return diags.exit_code();
    };
    // 04 指令表的指令都還沒實作，所以還沒註冊任何指令。依 04 說明與用法錯誤，
    // 不認得的名稱由 just 擋下、到不了引擎；直接呼叫引擎時沒有契約定的診斷，
    // 暫以 VK0026（不認得的參數）回報並附用法，待決議（#457）。
    let _ = diags.emit(&Diagnostic::new(&messages::VK0026).arg("value", first.to_string_lossy()));
    let _ = out.stderr_line(SHORT_USAGE);
    let _ = out.flush();
    diags.exit_code()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;
    use std::cell::RefCell;
    use std::io;
    use std::rc::Rc;

    /// stdout、stderr 各一份可共用的緩衝，讓輸出與診斷寫進同一條 stderr。
    #[derive(Clone, Default)]
    struct Buf(Rc<RefCell<Vec<u8>>>);

    impl Write for Buf {
        fn write(&mut self, data: &[u8]) -> io::Result<usize> {
            self.0.borrow_mut().extend_from_slice(data);
            Ok(data.len())
        }
        fn flush(&mut self) -> io::Result<()> {
            Ok(())
        }
    }

    impl Buf {
        fn text(&self) -> String {
            String::from_utf8(self.0.borrow().clone()).unwrap()
        }
    }

    fn call(args: &[&str]) -> (u8, String, String) {
        let (out, err) = (Buf::default(), Buf::default());
        let args: Vec<OsString> = args.iter().map(OsString::from).collect();
        let code = run(&args, out.clone(), err.clone());
        (code, out.text(), err.text())
    }

    #[test]
    fn no_command_prints_version_diagnostic_and_usage() {
        let (code, stdout, stderr) = call(&[]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert_eq!(
            stderr,
            format!(
                "vendor_kit {VERSION}\nvendor_kit: error[VK0024]: No command was specified.\nUsage: just vendor_kit <cmd> [arguments] [options]\n"
            )
        );
    }

    #[test]
    fn unregistered_command_is_rejected_without_stdout() {
        let (code, stdout, stderr) = call(&["foo"]);
        assert_eq!(code, 2);
        assert_eq!(stdout, "");
        assert!(stderr.starts_with("vendor_kit: error[VK0026]: "));
    }
}
