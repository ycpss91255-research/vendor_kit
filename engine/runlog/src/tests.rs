//! 單元與 golden 測試：每種事件的確切行，以及未完成首次導入的判定。

use std::time::{Duration, SystemTime, UNIX_EPOCH};

use diagnostics::{Diagnostic, Diagnostics};
use messages::{VK0002, VK0024};

use super::*;

/// 2026-10-05T01:02:03.000004Z
fn fixed_time() -> SystemTime {
    UNIX_EPOCH + Duration::new(1_791_162_123, 4_000)
}

fn header(component: Component) -> Header {
    Header {
        version: "0.0.0".to_owned(),
        component,
        invocation_id: "inv-1".to_owned(),
    }
}

fn writer(component: Component) -> Writer<Vec<u8>> {
    Writer::new(Vec::new(), header(component)).with_clock(fixed_time)
}

fn written(component: Component, event: &Event) -> String {
    let mut w = writer(component);
    w.write(event).unwrap();
    String::from_utf8(w.into_inner()).unwrap()
}

fn argv() -> Vec<String> {
    ["-y", "a b", "q\"\\"].map(str::to_owned).to_vec()
}

fn prompt_diag() -> Diagnostic {
    Diagnostic::new(&VK0002).arg("command_with_y", "./bootstrap.sh -y")
}

// ---- 註冊表 ----

#[test]
fn registry_matches_the_event_names() {
    let names: Vec<&str> = registry().collect();
    let expected: Vec<&str> = EventName::ALL.iter().map(|e| e.as_str()).collect();
    assert_eq!(names, expected);
    for name in EventName::ALL {
        assert_eq!(EventName::parse(name.as_str()), Some(name));
        assert!(is_registered(name.as_str()));
    }
    assert!(!is_registered("file_written"));
    assert!(!is_registered("# run_started"));
}

#[test]
fn internal_errors_map_to_vk0056() {
    assert_eq!(
        Error::Unregistered("x").message().map(|m| m.code),
        Some("VK0056")
    );
    assert_eq!(Error::Clock.message().map(|m| m.code), Some("VK0056"));
    assert!(Error::Io(io::Error::other("x")).message().is_none());
}

#[test]
fn each_side_writes_only_its_own_events() {
    let mut w = writer(Component::Engine);
    let argv = argv();
    let err = w
        .write(&Event::RunStarted {
            mode: Mode::Recipe,
            argv: &argv,
        })
        .unwrap_err();
    assert!(matches!(err, Error::WrongComponent { .. }));
    assert_eq!(err.message().map(|m| m.code), Some("VK0056"));
    let mut w = writer(Component::Launcher);
    assert!(matches!(
        w.write(&Event::WritesStarted),
        Err(Error::WrongComponent { .. })
    ));
    assert!(w.write(&Event::DiagnosticEmitted(&prompt_diag())).is_ok());
    assert!(w.into_inner().ends_with(b"\n"));
}

#[test]
fn a_clock_before_1970_is_refused() {
    let mut w = Writer::new(Vec::new(), header(Component::Engine))
        .with_clock(|| UNIX_EPOCH - Duration::from_secs(1));
    assert!(matches!(w.write(&Event::EngineStarted), Err(Error::Clock)));
    assert!(w.into_inner().is_empty());
}

// ---- golden：每種事件的確切行 ----

#[test]
fn golden_run_started() {
    let argv = argv();
    assert_eq!(
        written(
            Component::Launcher,
            &Event::RunStarted {
                mode: Mode::InitialImport,
                argv: &argv
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"run_started","body":"Run started.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"launcher","vendor_kit.invocation_id":"inv-1","vendor_kit.mode":"initial_import","vendor_kit.argv":["-y","a b","q\"\\"]}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_engine_started() {
    assert_eq!(
        written(Component::Engine, &Event::EngineStarted),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"engine_started","body":"Engine started.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_diagnostic_emitted() {
    assert_eq!(
        written(Component::Engine, &Event::DiagnosticEmitted(&prompt_diag())),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"error","severity_number":17,"event_name":"diagnostic_emitted","body":"Confirmation is required, but no terminal is available for interaction. No files were modified except the run log. Run from a terminal, or rerun with -y: ./bootstrap.sh -y","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.reason_code":"VK0002","vendor_kit.placeholder.command_with_y":"./bootstrap.sh -y"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_writes_started() {
    assert_eq!(
        written(Component::Engine, &Event::WritesStarted),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"writes_started","body":"Writes started.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_lock_line_write_started() {
    assert_eq!(
        written(
            Component::Engine,
            &Event::LockLineWriteStarted {
                target: Target::Engine
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"lock_line_write_started","body":"Lock line write started.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.target":"engine"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_lock_line_written() {
    assert_eq!(
        written(
            Component::Engine,
            &Event::LockLineWritten {
                target: Target::Tool
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"lock_line_written","body":"Lock line written.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.target":"tool"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_progress_removed() {
    assert_eq!(
        written(
            Component::Engine,
            &Event::ProgressRemoved {
                file: ".tmp.add.x1.toml"
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"progress_removed","body":"Progress file removed.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.progress_file":".tmp.add.x1.toml"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_engine_finished() {
    assert_eq!(
        written(Component::Engine, &Event::EngineFinished { exit_code: 2 }),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"engine_finished","body":"Engine finished.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.exit_code":2}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_run_finished() {
    assert_eq!(
        written(
            Component::Launcher,
            &Event::RunFinished {
                exit_code: 2,
                engine_exit_code: Some(2),
                stop_reason: StopReason::Code(&VK0002)
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"run_finished","body":"Run finished.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"launcher","vendor_kit.invocation_id":"inv-1","vendor_kit.exit_code":2,"vendor_kit.engine.exit_code":2,"vendor_kit.stop_reason_code":"VK0002"}}"#,
            "\n"
        )
    );
}

#[test]
fn golden_run_finished_without_engine() {
    assert_eq!(
        written(
            Component::Launcher,
            &Event::RunFinished {
                exit_code: 0,
                engine_exit_code: None,
                stop_reason: StopReason::None
            }
        ),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"info","severity_number":9,"event_name":"run_finished","body":"Run finished.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"launcher","vendor_kit.invocation_id":"inv-1","vendor_kit.exit_code":0,"vendor_kit.engine.exit_code":null,"vendor_kit.stop_reason_code":"none"}}"#,
            "\n"
        )
    );
}

// ---- diagnostics 的 sink ----

#[test]
fn one_diagnostic_is_one_diagnostic_emitted_line() {
    let mut d = Diagnostics::with_sink(Vec::new(), writer(Component::Engine));
    d.emit(&Diagnostic::new(&VK0024)).unwrap();
    let (stderr, w) = d.into_parts();
    assert_eq!(
        String::from_utf8(stderr).unwrap(),
        "vendor_kit: error[VK0024]: No command was specified.\n"
    );
    assert_eq!(
        String::from_utf8(w.into_inner()).unwrap(),
        concat!(
            r#"{"timestamp":"2026-10-05T01:02:03.000004Z","severity_text":"error","severity_number":17,"event_name":"diagnostic_emitted","body":"No command was specified.","resource":{"service.name":"vendor_kit","service.version":"0.0.0"},"attributes":{"vendor_kit.log_format":"1","vendor_kit.component":"engine","vendor_kit.invocation_id":"inv-1","vendor_kit.reason_code":"VK0024"}}"#,
            "\n"
        )
    );
}

#[test]
fn severity_numbers_follow_the_level() {
    assert_eq!(severity(None), ("info", 9));
    assert_eq!(severity(Some(Level::Warn)), ("warn", 13));
    assert_eq!(severity(Some(Level::Error)), ("error", 17));
    assert_eq!(severity(Some(Level::Fatal)), ("fatal", 21));
}

// ---- 判定未完成首次導入 ----

fn log(events: &[Event]) -> Vec<u8> {
    let mut out = String::new();
    for e in events {
        let component = if e.name().writable_by(Component::Engine) {
            Component::Engine
        } else {
            Component::Launcher
        };
        out.push_str(&format_line(
            &header(component),
            "2026-10-05T01:02:03.000004Z",
            e,
        ));
    }
    out.into_bytes()
}

fn started(mode: Mode) -> Event<'static> {
    Event::RunStarted { mode, argv: &[] }
}

fn finished(stop_reason: StopReason) -> Event<'static> {
    Event::RunFinished {
        exit_code: 2,
        engine_exit_code: Some(2),
        stop_reason,
    }
}

/// 停在 VK0002、沒寫任何檔的首次導入。
fn stopped_at_prompt(diag: &Diagnostic) -> Vec<u8> {
    log(&[
        started(Mode::InitialImport),
        Event::EngineStarted,
        Event::DiagnosticEmitted(diag),
        Event::EngineFinished { exit_code: 2 },
        finished(StopReason::Code(&VK0002)),
    ])
}

fn no(reason: Reason) -> Verdict {
    Verdict::NotApplicable(reason)
}

#[test]
fn condition_a_stopped_at_prompt_without_writes() {
    let d = prompt_diag();
    assert_eq!(
        assess(&stopped_at_prompt(&d), false),
        Verdict::Applies(Condition::StoppedAtPrompt)
    );
}

#[test]
fn a_readable_engine_lock_line_wins() {
    let d = prompt_diag();
    assert_eq!(
        assess(&stopped_at_prompt(&d), true),
        no(Reason::EngineLockLineReadable)
    );
}

#[test]
fn condition_b_ended_before_the_engine_lock_line() {
    let d = Diagnostic::new(&VK0024);
    let text = log(&[
        started(Mode::InitialImport),
        Event::EngineStarted,
        Event::WritesStarted,
        Event::LockLineWriteStarted {
            target: Target::Tool,
        },
        Event::LockLineWritten {
            target: Target::Tool,
        },
        Event::DiagnosticEmitted(&d),
        Event::EngineFinished { exit_code: 2 },
        finished(StopReason::Code(&VK0024)),
    ]);
    assert_eq!(
        assess(&text, false),
        Verdict::Applies(Condition::BeforeEngineLockLine)
    );
}

#[test]
fn condition_b_when_only_the_launcher_saw_the_end() {
    // 引擎被殺掉、沒寫 engine_finished，啟動器照樣收尾。
    let text = log(&[
        started(Mode::InitialImport),
        Event::EngineStarted,
        Event::WritesStarted,
        Event::RunFinished {
            exit_code: 3,
            engine_exit_code: Some(137),
            stop_reason: StopReason::None,
        },
    ]);
    assert_eq!(
        assess(&text, false),
        Verdict::Applies(Condition::BeforeEngineLockLine)
    );
}

#[test]
fn prompt_stop_after_writes_falls_back_to_condition_b() {
    let d = prompt_diag();
    let text = log(&[
        started(Mode::InitialImport),
        Event::WritesStarted,
        Event::DiagnosticEmitted(&d),
        finished(StopReason::Code(&VK0002)),
    ]);
    assert_eq!(
        assess(&text, false),
        Verdict::Applies(Condition::BeforeEngineLockLine)
    );
}

#[test]
fn engine_lock_line_already_written() {
    let text = log(&[
        started(Mode::InitialImport),
        Event::WritesStarted,
        Event::LockLineWriteStarted {
            target: Target::Engine,
        },
        Event::LockLineWritten {
            target: Target::Engine,
        },
        Event::EngineFinished { exit_code: 0 },
    ]);
    assert_eq!(assess(&text, false), no(Reason::EngineLockLineWritten));
}

#[test]
fn started_without_written_is_not_applicable() {
    for target in Target::ALL {
        let text = log(&[
            started(Mode::InitialImport),
            Event::WritesStarted,
            Event::LockLineWriteStarted { target },
            Event::EngineFinished { exit_code: 2 },
        ]);
        assert_eq!(
            assess(&text, false),
            no(Reason::LockLineWriteUnconfirmed),
            "{target:?}"
        );
    }
}

#[test]
fn file_changes_before_writes_started_are_not_unique() {
    // 停在 VK0002 卻已寫過鎖定行：不能當成 (a)「除紀錄外沒改檔」。
    let d = prompt_diag();
    let lock_first = log(&[
        started(Mode::InitialImport),
        Event::LockLineWriteStarted {
            target: Target::Engine,
        },
        Event::LockLineWritten {
            target: Target::Engine,
        },
        Event::DiagnosticEmitted(&d),
        finished(StopReason::Code(&VK0002)),
    ]);
    assert_eq!(assess(&lock_first, false), no(Reason::NotUnique));
    let progress_first = log(&[
        started(Mode::InitialImport),
        Event::ProgressRemoved {
            file: ".tmp.install.x1.toml",
        },
        Event::DiagnosticEmitted(&d),
        finished(StopReason::Code(&VK0002)),
    ]);
    assert_eq!(assess(&progress_first, false), no(Reason::NotUnique));
}

#[test]
fn written_without_started_is_not_unique() {
    let text = log(&[
        started(Mode::InitialImport),
        Event::LockLineWritten {
            target: Target::Engine,
        },
        Event::EngineFinished { exit_code: 0 },
    ]);
    assert_eq!(assess(&text, false), no(Reason::NotUnique));
}

#[test]
fn missing_run_started() {
    let d = prompt_diag();
    let text = log(&[
        Event::EngineStarted,
        Event::DiagnosticEmitted(&d),
        Event::EngineFinished { exit_code: 2 },
        finished(StopReason::Code(&VK0002)),
    ]);
    assert_eq!(assess(&text, false), no(Reason::MissingRunStarted));
}

#[test]
fn run_started_twice_or_late_is_not_unique() {
    let twice = log(&[
        started(Mode::InitialImport),
        started(Mode::InitialImport),
        Event::EngineFinished { exit_code: 0 },
    ]);
    assert_eq!(assess(&twice, false), no(Reason::NotUnique));
    let late = log(&[
        Event::EngineStarted,
        started(Mode::InitialImport),
        Event::EngineFinished { exit_code: 0 },
    ]);
    assert_eq!(assess(&late, false), no(Reason::NotUnique));
}

#[test]
fn two_invocations_in_one_log_are_not_unique() {
    let d = prompt_diag();
    let text = String::from_utf8(stopped_at_prompt(&d)).unwrap();
    let mut lines: Vec<String> = text.lines().map(|l| format!("{l}\n")).collect();
    lines[3] = lines[3].replace("\"inv-1\"", "\"inv-2\"");
    assert_eq!(
        assess(lines.concat().as_bytes(), false),
        no(Reason::NotUnique)
    );
}

#[test]
fn other_modes_are_not_initial_import() {
    for mode in [Mode::Check, Mode::Repair, Mode::Recipe] {
        let text = log(&[started(mode), Event::EngineFinished { exit_code: 0 }]);
        assert_eq!(assess(&text, false), no(Reason::NotInitialImport));
    }
}

#[test]
fn no_end_event_is_not_finished() {
    let text = log(&[
        started(Mode::InitialImport),
        Event::EngineStarted,
        Event::WritesStarted,
    ]);
    assert_eq!(assess(&text, false), no(Reason::NotFinished));
}

#[test]
fn stop_reason_needs_a_matching_diagnostic() {
    let text = log(&[
        started(Mode::InitialImport),
        Event::EngineFinished { exit_code: 2 },
        finished(StopReason::Code(&VK0002)),
    ]);
    assert_eq!(assess(&text, false), no(Reason::StopReasonNotDiagnosed));
}

#[test]
fn empty_log() {
    assert_eq!(assess(b"", false), no(Reason::Empty));
}

#[test]
fn truncated_last_line() {
    let d = prompt_diag();
    let mut text = stopped_at_prompt(&d);
    text.truncate(text.len() - 10);
    assert_eq!(assess(&text, false), no(Reason::Truncated { line: 5 }));
    // 只少了最後的 LF 也算截斷。
    let mut text = stopped_at_prompt(&d);
    text.pop();
    assert_eq!(assess(&text, false), no(Reason::Truncated { line: 5 }));
}

#[test]
fn unsupported_log_format() {
    let d = prompt_diag();
    let text = String::from_utf8(stopped_at_prompt(&d)).unwrap();
    let mut lines: Vec<String> = text.lines().map(|l| format!("{l}\n")).collect();
    lines[1] = lines[1].replace(
        "\"vendor_kit.log_format\":\"1\"",
        "\"vendor_kit.log_format\":\"2\"",
    );
    assert_eq!(
        assess(lines.concat().as_bytes(), false),
        no(Reason::UnsupportedFormat { line: 2 })
    );
}

/// 改一行的函式。
type Edit = fn(&str) -> String;

/// 把停在 VK0002 的紀錄第 `n` 行（從 1 起算）換成 `f` 的結果，回判定。
fn with_line(n: usize, f: impl Fn(&str) -> String) -> Verdict {
    let d = prompt_diag();
    let text = String::from_utf8(stopped_at_prompt(&d)).unwrap();
    let mut lines: Vec<String> = text.lines().map(|l| format!("{l}\n")).collect();
    lines[n - 1] = f(&lines[n - 1]);
    assess(lines.concat().as_bytes(), false)
}

#[test]
fn malformed_lines_are_invalid() {
    let cases: [(usize, Edit); 12] = [
        // CRLF
        (1, |l| l.replace('\n', "\r\n")),
        // 多了空白
        (2, |l| l.replacen("\":\"", "\": \"", 1)),
        // 鍵序不同
        (2, |l| {
            l.replacen(
                "\"severity_text\":\"info\",\"severity_number\":9",
                "\"severity_number\":9,\"severity_text\":\"info\"",
                1,
            )
        }),
        // 非正規的跳脫
        (2, |l| l.replace("Engine started.", "Engine started\\u002e")),
        // mode 拼錯（封閉列舉）
        (1, |l| l.replace("initial_import", "initial-import")),
        // stop_reason_code 不在訊息表
        (5, |l| l.replace("\"VK0002\"", "\"VK9999\"")),
        // 未登錄的事件名
        (2, |l| l.replace("engine_started", "engine_begun")),
        // 啟動器事件由引擎寫
        (1, |l| l.replace("\"launcher\"", "\"engine\"")),
        // 嚴重度跟訊息表不符
        (3, |l| {
            l.replace(
                "\"error\",\"severity_number\":17",
                "\"warn\",\"severity_number\":13",
            )
        }),
        // 時間戳不是六位小數
        (2, |l| l.replace(".000004Z", ".0004Z")),
        // 不是 UTF-8 文字也不是 JSON
        (4, |_| "not json\n".to_owned()),
        // 多一個未知 attribute
        (4, |l| {
            l.replace(
                "\"vendor_kit.exit_code\":2",
                "\"vendor_kit.exit_code\":2,\"x\":1",
            )
        }),
    ];
    for (n, f) in cases {
        assert_eq!(with_line(n, f), no(Reason::InvalidLine { line: n }));
    }
}

#[test]
fn target_spelled_wrong_is_invalid() {
    let text = String::from_utf8(log(&[
        started(Mode::InitialImport),
        Event::WritesStarted,
        Event::LockLineWriteStarted {
            target: Target::Engine,
        },
        Event::LockLineWritten {
            target: Target::Engine,
        },
        Event::EngineFinished { exit_code: 0 },
    ]))
    .unwrap()
    .replacen(
        "\"vendor_kit.target\":\"engine\"",
        "\"vendor_kit.target\":\"Engine\"",
        1,
    );
    assert_eq!(
        assess(text.as_bytes(), false),
        no(Reason::InvalidLine { line: 3 })
    );
}

#[test]
fn every_golden_line_reads_back() {
    // 寫出來的每種事件都要讀得回去（寫與讀用同一份正規形）。
    let argv = argv();
    let d = prompt_diag();
    let events = [
        Event::RunStarted {
            mode: Mode::InitialImport,
            argv: &argv,
        },
        Event::EngineStarted,
        Event::DiagnosticEmitted(&d),
        Event::WritesStarted,
        Event::LockLineWriteStarted {
            target: Target::Tool,
        },
        Event::LockLineWritten {
            target: Target::Tool,
        },
        Event::ProgressRemoved {
            file: ".tmp.add.x1.toml",
        },
        Event::EngineFinished { exit_code: 2 },
        finished(StopReason::Code(&VK0002)),
    ];
    assert_eq!(
        assess(&log(&events), false),
        Verdict::Applies(Condition::BeforeEngineLockLine)
    );
}
