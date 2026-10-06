//! 互動詢問（04 共同選項的 `-y` 與詢問規則、02 不變量第 1 條）。
//!
//! - stdin 與 stderr 都是終端才能互動；管線不算，不另從 `/dev/tty` 讀答案。終端狀態由呼叫端經
//!   [`Terminal`] 傳入，這裡不自己判斷：之後由啟動器傳進容器（協定未定）。
//! - 每次呼叫先收集全部問題，[`ask_all`] 一次問完、回傳全部答案；答否之後仍問完其餘問題。
//!   全部同意才寫入由呼叫端照 [`Answers::all_yes`] 決定。
//! - 每題的提示是 `<question> [y/N] `，印到注入的 stderr；答案從注入的 stdin 一行一行讀。
//!   去掉前後空白後不分大小寫是 `y` 或 `yes` 才算同意；空白 Enter 與其他輸入都算否。
//! - 讀到輸入結束 (EOF) 不算同意：依訊息表 VK0002，它跟沒有終端一樣算不能互動，回
//!   [`PromptError::NotInteractive`]，不當成答否。
//! - 帶 `-y`（[`Consent::AssumeYes`]）時全部同意，不看終端、不讀輸入、不印提示；改動仍由呼叫端印到 stdout。
//! - 沒帶 `-y` 又不能互動時回 [`PromptError::NotInteractive`]（VK0002），一個提示都不印；
//!   重跑指令 `<command_with_y>` 由 [`command_with_y`] 產生。
//! - 預演（`--dry-run`，#372 N11）不經這裡：可寫 recipe 算出完整計畫後不問、不寫（執行紀錄除外），
//!   把會改的內容逐行印到 stdout，最後印 [`DRY_RUN_DONE`]、以 0 結束；`-y` 並用時沒有作用。
//!   殘留進度檔的恢復也只印、不落地，進度檔照留。
//!
//! 這裡不印診斷；要怎麼印由呼叫端經 `diagnostics` 決定。

use std::fmt;
use std::io::{self, BufRead, Write};

use messages::Message;

/// 提示在問題後面接的字。
pub const PROMPT_SUFFIX: &str = " [y/N] ";

/// 預先回答詢問的選項（04 共同選項）。
pub const YES_FLAG: &str = "-y";

/// 預演印完計畫之後，stdout 的最後一行（各可寫 recipe 共用）。
pub const DRY_RUN_DONE: &str = "Dry run: no changes were made.";

/// 這次執行的終端狀態。由呼叫端提供，這裡不自己判斷。
pub trait Terminal {
    /// stdin 是不是終端。
    fn stdin_is_tty(&self) -> bool;
    /// stderr 是不是終端。
    fn stderr_is_tty(&self) -> bool;
}

/// 已知的終端狀態，例如啟動器傳進來的值。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct TtyState {
    pub stdin: bool,
    pub stderr: bool,
}

impl Terminal for TtyState {
    fn stdin_is_tty(&self) -> bool {
        self.stdin
    }

    fn stderr_is_tty(&self) -> bool {
        self.stderr
    }
}

/// 這次呼叫有沒有帶 `-y`。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Consent {
    /// 沒帶 `-y`：要問。
    Ask,
    /// 帶了 `-y`：全部同意，不問。
    AssumeYes,
}

/// 一題的答案。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Answer {
    Yes,
    No,
}

/// 全部問題的答案，順序同問題。
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct Answers(Vec<Answer>);

impl Answers {
    /// 每一題都同意；沒有問題時也是 `true`。
    pub fn all_yes(&self) -> bool {
        self.0.iter().all(|a| *a == Answer::Yes)
    }

    pub fn as_slice(&self) -> &[Answer] {
        &self.0
    }

    pub fn into_vec(self) -> Vec<Answer> {
        self.0
    }
}

/// 不能互動的原因。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NotInteractive {
    /// stdin 或 stderr 不是終端；欄位是各自的狀態。
    NoTerminal { stdin: bool, stderr: bool },
    /// 問到一半讀到輸入結束；`answered` 是已讀到答案的題數。
    EndOfInput { answered: usize },
}

/// 詢問失敗時正在做的動作。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Op {
    /// 印提示到 stderr。
    WritePrompt,
    /// 從 stdin 讀答案。
    ReadAnswer,
}

/// 詢問失敗。不論哪一種都沒有取得同意，呼叫端不得做需詢問的修改。
#[derive(Debug)]
pub enum PromptError {
    /// 沒帶 `-y` 又不能互動（VK0002）。
    NotInteractive(NotInteractive),
    /// 印提示或讀答案失敗。訊息表沒有對應代碼，由呼叫端當內部錯誤處理。
    Io { op: Op, source: io::Error },
}

impl PromptError {
    /// 對應的訊息表條目；`Io` 沒有代碼，回 `None`。
    pub fn message(&self) -> Option<&'static Message> {
        match self {
            PromptError::NotInteractive(_) => Some(&messages::VK0002),
            PromptError::Io { .. } => None,
        }
    }
}

impl fmt::Display for PromptError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PromptError::NotInteractive(NotInteractive::NoTerminal { stdin, stderr }) => {
                let tty = |b: &bool| if *b { "a terminal" } else { "not a terminal" };
                write!(
                    f,
                    "cannot prompt: stdin is {}, stderr is {}",
                    tty(stdin),
                    tty(stderr)
                )
            }
            PromptError::NotInteractive(NotInteractive::EndOfInput { answered }) => {
                write!(f, "cannot prompt: end of input after {answered} answer(s)")
            }
            PromptError::Io { op, source } => {
                let op = match op {
                    Op::WritePrompt => "write prompt",
                    Op::ReadAnswer => "read answer",
                };
                write!(f, "{op}: {source}")
            }
        }
    }
}

impl std::error::Error for PromptError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            PromptError::NotInteractive(_) => None,
            PromptError::Io { source, .. } => Some(source),
        }
    }
}

/// 一次問完全部問題，回傳全部答案。
///
/// `input` 是 stdin、`prompt` 是 stderr，都由呼叫端注入。沒有問題時直接回空答案，不需要終端；
/// 帶 `-y` 時全部同意。其他情況先確認能互動才印第一個提示。
pub fn ask_all<Q: AsRef<str>>(
    questions: &[Q],
    consent: Consent,
    terminal: &dyn Terminal,
    input: &mut dyn BufRead,
    prompt: &mut dyn Write,
) -> Result<Answers, PromptError> {
    if consent == Consent::AssumeYes {
        return Ok(Answers(vec![Answer::Yes; questions.len()]));
    }
    if questions.is_empty() {
        return Ok(Answers::default());
    }
    let (stdin, stderr) = (terminal.stdin_is_tty(), terminal.stderr_is_tty());
    if !(stdin && stderr) {
        return Err(PromptError::NotInteractive(NotInteractive::NoTerminal {
            stdin,
            stderr,
        }));
    }
    let mut answers = Vec::with_capacity(questions.len());
    let mut line = String::new();
    for q in questions {
        write!(prompt, "{}{PROMPT_SUFFIX}", q.as_ref())
            .and_then(|()| prompt.flush())
            .map_err(|source| PromptError::Io {
                op: Op::WritePrompt,
                source,
            })?;
        line.clear();
        let n = read_line(input, &mut line)?;
        if n == 0 {
            return Err(PromptError::NotInteractive(NotInteractive::EndOfInput {
                answered: answers.len(),
            }));
        }
        answers.push(parse_answer(&line));
    }
    Ok(Answers(answers))
}

/// 讀一行；被訊號打斷時重讀。
fn read_line(input: &mut dyn BufRead, line: &mut String) -> Result<usize, PromptError> {
    loop {
        match input.read_line(line) {
            Ok(n) => return Ok(n),
            Err(e) if e.kind() == io::ErrorKind::Interrupted => {}
            Err(source) => {
                return Err(PromptError::Io {
                    op: Op::ReadAnswer,
                    source,
                });
            }
        }
    }
}

/// 去掉前後空白後不分大小寫是 `y` 或 `yes` 才算同意，其他都算否。
fn parse_answer(line: &str) -> Answer {
    let s = line.trim();
    if s.eq_ignore_ascii_case("y") || s.eq_ignore_ascii_case("yes") {
        Answer::Yes
    } else {
        Answer::No
    }
}

/// 產生 VK0002 的 `<command_with_y>`：`words` 是這次執行的指令逐項（含開頭的
/// `just vendor_kit` 或 bootstrap.sh 的 `$0`，由呼叫端給），每項依 POSIX shell 規則加引號，
/// `-y` 插在第一個單獨的 `--` 之前，沒有 `--` 時放在最後。
pub fn command_with_y<S: AsRef<str>>(words: &[S]) -> String {
    let split = words
        .iter()
        .position(|w| w.as_ref() == "--")
        .unwrap_or(words.len());
    let (before, after) = words.split_at(split);
    before
        .iter()
        .map(|w| shell_quote(w.as_ref()))
        .chain(std::iter::once(YES_FLAG.to_owned()))
        .chain(after.iter().map(|w| shell_quote(w.as_ref())))
        .collect::<Vec<_>>()
        .join(" ")
}

/// POSIX shell 引號：只含安全字元的字原樣留下；其他（含空字串）包單引號，`'` 換成 `'\''`。
fn shell_quote(s: &str) -> String {
    let safe = |c: char| c.is_ascii_alphanumeric() || "_@%+=:,./-".contains(c);
    if !s.is_empty() && s.chars().all(safe) {
        return s.to_owned();
    }
    format!("'{}'", s.replace('\'', r"'\''"))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    const TTY: TtyState = TtyState {
        stdin: true,
        stderr: true,
    };

    /// 用給定的終端狀態與 stdin 內容問，回傳結果與印到 stderr 的字。
    fn ask(
        questions: &[&str],
        consent: Consent,
        terminal: TtyState,
        stdin: &str,
    ) -> (Result<Answers, PromptError>, String) {
        let mut input = stdin.as_bytes();
        let mut stderr = Vec::new();
        let got = ask_all(questions, consent, &terminal, &mut input, &mut stderr);
        (got, String::from_utf8(stderr).unwrap())
    }

    fn answers(got: Result<Answers, PromptError>) -> Vec<Answer> {
        got.unwrap().into_vec()
    }

    #[test]
    fn asks_every_question_on_stderr_and_returns_every_answer() {
        let (got, stderr) = ask(
            &["Overwrite a?", "Overwrite b?"],
            Consent::Ask,
            TTY,
            "y\nyes\n",
        );
        assert_eq!(answers(got), [Answer::Yes, Answer::Yes]);
        assert_eq!(stderr, "Overwrite a? [y/N] Overwrite b? [y/N] ");
    }

    #[test]
    fn keeps_asking_after_a_no() {
        let (got, stderr) = ask(&["a?", "b?", "c?"], Consent::Ask, TTY, "n\ny\n\n");
        let got = got.unwrap();
        assert_eq!(got.as_slice(), [Answer::No, Answer::Yes, Answer::No]);
        assert!(!got.all_yes());
        assert_eq!(stderr, "a? [y/N] b? [y/N] c? [y/N] ");
    }

    #[test]
    fn only_y_or_yes_is_consent() {
        for (line, want) in [
            ("y\n", Answer::Yes),
            ("Y\n", Answer::Yes),
            ("yes\n", Answer::Yes),
            ("YeS\n", Answer::Yes),
            ("  y \r\n", Answer::Yes),
            ("y", Answer::Yes),
            ("\n", Answer::No),
            ("   \n", Answer::No),
            ("n\n", Answer::No),
            ("no\n", Answer::No),
            ("yy\n", Answer::No),
            ("ye\n", Answer::No),
            ("yes please\n", Answer::No),
            ("1\n", Answer::No),
        ] {
            let (got, _) = ask(&["q?"], Consent::Ask, TTY, line);
            assert_eq!(answers(got), [want], "answer {line:?}");
        }
    }

    #[test]
    fn end_of_input_is_not_consent() {
        let (got, stderr) = ask(&["a?", "b?"], Consent::Ask, TTY, "y\n");
        let err = got.unwrap_err();
        assert!(matches!(
            err,
            PromptError::NotInteractive(NotInteractive::EndOfInput { answered: 1 })
        ));
        assert_eq!(err.message(), Some(&messages::VK0002));
        assert_eq!(stderr, "a? [y/N] b? [y/N] ");

        let (got, _) = ask(&["a?"], Consent::Ask, TTY, "");
        assert!(matches!(
            got.unwrap_err(),
            PromptError::NotInteractive(NotInteractive::EndOfInput { answered: 0 })
        ));
    }

    #[test]
    fn no_terminal_is_vk0002_without_printing() {
        for (stdin, stderr) in [(false, true), (true, false), (false, false)] {
            let tty = TtyState { stdin, stderr };
            let (got, printed) = ask(&["a?"], Consent::Ask, tty, "y\n");
            let err = got.unwrap_err();
            assert!(
                matches!(
                    err,
                    PromptError::NotInteractive(NotInteractive::NoTerminal { stdin: i, stderr: e })
                        if i == stdin && e == stderr
                ),
                "{tty:?}: {err:?}"
            );
            assert_eq!(err.message(), Some(&messages::VK0002));
            assert_eq!(printed, "", "{tty:?}");
        }
    }

    #[test]
    fn assume_yes_skips_terminal_input_and_prompt() {
        let (got, stderr) = ask(
            &["a?", "b?"],
            Consent::AssumeYes,
            TtyState::default(),
            "n\n",
        );
        let got = got.unwrap();
        assert_eq!(got.as_slice(), [Answer::Yes, Answer::Yes]);
        assert!(got.all_yes());
        assert_eq!(stderr, "");
    }

    #[test]
    fn no_questions_need_no_terminal() {
        let (got, stderr) = ask(&[], Consent::Ask, TtyState::default(), "");
        let got = got.unwrap();
        assert!(got.as_slice().is_empty());
        assert!(got.all_yes());
        assert_eq!(stderr, "");
    }

    #[test]
    fn write_failure_is_io_without_code() {
        struct Broken;
        impl Write for Broken {
            fn write(&mut self, _: &[u8]) -> io::Result<usize> {
                Err(io::Error::from(io::ErrorKind::BrokenPipe))
            }
            fn flush(&mut self) -> io::Result<()> {
                Ok(())
            }
        }
        let mut input = "y\n".as_bytes();
        let err = ask_all(&["a?"], Consent::Ask, &TTY, &mut input, &mut Broken).unwrap_err();
        assert!(matches!(
            err,
            PromptError::Io {
                op: Op::WritePrompt,
                ..
            }
        ));
        assert_eq!(err.message(), None);
    }

    #[test]
    fn y_goes_before_the_first_standalone_double_dash() {
        assert_eq!(
            command_with_y(&["just", "vendor_kit", "upgrade", "--", "-x", "--"]),
            "just vendor_kit upgrade -y -- -x --"
        );
        assert_eq!(
            command_with_y(&["just", "vendor_kit", "--", "a"]),
            "just vendor_kit -y -- a"
        );
    }

    #[test]
    fn y_goes_last_without_double_dash() {
        assert_eq!(
            command_with_y(&[
                "just",
                "vendor_kit",
                "upgrade",
                "--engine=v1.2.0",
                "a--",
                "---"
            ]),
            "just vendor_kit upgrade --engine=v1.2.0 a-- --- -y"
        );
        assert_eq!(command_with_y(&["./bootstrap.sh"]), "./bootstrap.sh -y");
        assert_eq!(command_with_y::<&str>(&[]), "-y");
    }

    #[test]
    fn words_are_quoted_by_posix_shell_rules() {
        assert_eq!(
            command_with_y(&[
                "/opt/my repo/bootstrap.sh",
                "",
                "it's",
                "$HOME",
                "~",
                "a*b",
                "line\nbreak",
                "é",
                "user@host:1,2%+=_"
            ]),
            "'/opt/my repo/bootstrap.sh' '' 'it'\\''s' '$HOME' '~' 'a*b' 'line\nbreak' 'é' user@host:1,2%+=_ -y"
        );
    }
}
