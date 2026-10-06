//! golden 測試：每種 op、result、done 的確切位元組，自由文字欄的跳脫，非法輸入的拒絕，
//! 入口 argv，控制目錄的往返，以及救援路徑常數的釘住。

use std::ffi::OsString;
use std::fs;
use std::path::PathBuf;

use super::*;

const A: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const B: &str = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef";

fn header(p: u32) -> Header {
    Header::new(p, RunId::parse("r1").unwrap()).unwrap()
}

fn field(s: &str) -> Field {
    Field::new(s.as_bytes()).unwrap()
}

fn image(s: &str) -> ImageRef {
    ImageRef::parse(s).unwrap()
}

fn seq(n: u16) -> Seq {
    Seq::new(n).unwrap()
}

fn req(op: &Op, n: u16) -> String {
    String::from_utf8(op.encode_request(&header(1), seq(n)).unwrap()).unwrap()
}

fn pinned() -> String {
    format!("ghcr.io/acme/ros_tools@sha256:{A}")
}

/// 每種 op 的範例與它在 P=1、seq=3 的確切位元組。
fn golden_ops() -> Vec<(Op, String)> {
    vec![
        (
            Op::Pull(image(&pinned())),
            format!("vk-resolve/1 r1 3\npull ghcr.io/acme/ros_tools@sha256:{A}\n"),
        ),
        (
            Op::Load(field("/srv/u/my proj/my tools.tar")),
            "vk-resolve/1 r1 3\nload e:/srv/u/my\\040proj/my\\040tools.tar\n".to_owned(),
        ),
        (
            Op::Inspect(image(&pinned())),
            format!("vk-resolve/1 r1 3\ninspect ghcr.io/acme/ros_tools@sha256:{A}\n"),
        ),
        (
            Op::Extract(
                ImageId::parse(&format!("sha256:{B}")).unwrap(),
                Slot::parse("x1").unwrap(),
            ),
            format!("vk-resolve/1 r1 3\nextract sha256:{B} x1\n"),
        ),
        (
            Op::Stage(field("/srv/u/.ghcr token"), Slot::parse("t1").unwrap()),
            "vk-resolve/1 r1 3\nstage e:/srv/u/.ghcr\\040token t1\n".to_owned(),
        ),
        (Op::Ps, "vk-resolve/1 r1 3\nps\n".to_owned()),
        (
            Op::RmContainer(Container::parse(B).unwrap()),
            format!("vk-resolve/1 r1 3\nrm-container {B}\n"),
        ),
        (
            Op::Runner {
                image: image("ghcr.io/u/test:1"),
                command: field("pytest"),
                args: vec![field("-q"), field(""), field("tests/a\\b.py")],
            },
            "vk-resolve/1 r1 3\nrunner ghcr.io/u/test:1 e:pytest e:-q e: e:tests/a\\134b.py\n"
                .to_owned(),
        ),
    ]
}

#[test]
fn every_op_has_exact_request_bytes_and_round_trips() {
    let ops = golden_ops();
    let kinds: Vec<OpKind> = ops.iter().map(|(op, _)| op.kind()).collect();
    assert_eq!(kinds, OpKind::ALL, "每種 op 都要有 golden");
    for (op, want) in ops {
        assert_eq!(req(&op, 3), want);
        assert_eq!(
            Op::parse_request(want.as_bytes(), &header(1)).unwrap(),
            (seq(3), op)
        );
    }
}

#[test]
fn op_names_are_the_closed_set() {
    let names: Vec<&str> = OpKind::ALL.iter().map(|k| k.name()).collect();
    assert_eq!(names, OPS);
    assert_eq!(
        OPS,
        [
            "pull",
            "load",
            "inspect",
            "extract",
            "stage",
            "ps",
            "rm-container",
            "runner"
        ]
    );
}

// ---- 自由文字欄 ----

#[test]
fn field_encoding_is_exact() {
    let cases: &[(&[u8], &str)] = &[
        (b"", "e:"),
        (b"abc", "e:abc"),
        (b"a\\b", "e:a\\134b"),
        (b"\\", "e:\\134"),
        (b"a b", "e:a\\040b"),
        (b"\t\n\r", "e:\\011\\012\\015"),
        (b"\x01\x7f\xff", "e:\\001\\177\\377"),
        ("é".as_bytes(), "e:\\303\\251"),
        (b"e:", "e:e:"),
        (b"!~[]\"'$`", "e:!~[]\"'$`"),
    ];
    for &(raw, enc) in cases {
        let f = Field::new(raw).unwrap();
        assert_eq!(f.encode(), enc, "{raw:?}");
        assert_eq!(Field::decode(enc).unwrap(), f, "{enc}");
    }
}

#[test]
fn field_escapes_every_byte_outside_printable_ascii_and_backslash() {
    for b in 1u8..=255 {
        let enc = Field::new([b]).unwrap().encode();
        let plain = (0x21..=0x7E).contains(&b) && b != b'\\';
        if plain {
            assert_eq!(enc.len(), 3, "{b:#x}");
        } else {
            assert_eq!(enc, format!("e:\\{b:03o}"), "{b:#x}");
        }
        assert_eq!(Field::decode(&enc).unwrap().as_bytes(), [b]);
    }
}

#[test]
fn field_rejects_nul_and_bad_syntax() {
    assert_eq!(Field::new(*b"a\0b"), Err(FieldError::Nul));
    for bad in [
        "", "abc", "E:abc", "e:a\\b", "e:\\", "e:\\12", "e:\\000", "e:\\400", "e:\\777", "e:\\08a",
        "e:a b", "e:\t", "e:\u{7f}", "e:é",
    ] {
        assert!(Field::decode(bad).is_err(), "{bad:?}");
    }
}

#[test]
fn field_decoding_accepts_any_grammar_valid_escape() {
    // 編碼端只寫一種形式，解碼端照文法收：可讀字元寫成八進位也合法。
    assert_eq!(Field::decode("e:\\101").unwrap().as_bytes(), b"A");
}

// ---- request 的拒絕 ----

#[test]
fn request_rejects_malformed_bytes() {
    let h = header(1);
    let pull = format!("pull {}", pinned());
    let bad: Vec<String> = vec![
        // 整體形式
        String::new(),
        format!("vk-resolve/1 r1 1\n{pull}"),
        format!("vk-resolve/1 r1 1\r\n{pull}\r\n"),
        format!("vk-resolve/1 r1 1\n{pull}\n\n"),
        "vk-resolve/1 r1 1\n\n".to_owned(),
        format!("vk-resolve/1 r1 1\n{pull}\nps\n"),
        format!("vk-resolve/1 r1 1\n {pull}\n"),
        format!("vk-resolve/1 r1 1\n{pull} \n"),
        format!("vk-resolve/1  r1 1\n{pull}\n"),
        format!("vk-resolve/1 r1 1\npull\t{}\n", pinned()),
        format!("vk-resolve/1 r1 1\n{pull}\0\n"),
        // header 與 seq
        format!("vk-resolve/2 r1 1\n{pull}\n"),
        format!("vk-resolve/01 r1 1\n{pull}\n"),
        format!("VK-RESOLVE/1 r1 1\n{pull}\n"),
        format!("vk-resolve/1 r2 1\n{pull}\n"),
        format!("vk-resolve/1 r1\n{pull}\n"),
        format!("vk-resolve/1 r1 0\n{pull}\n"),
        format!("vk-resolve/1 r1 01\n{pull}\n"),
        format!("vk-resolve/1 r1 10000\n{pull}\n"),
        format!("vk-resolve/1 r1 1 2\n{pull}\n"),
        format!("vk-resolve/1 r1 done 0\n{pull}\n"),
        // op 名
        "vk-resolve/1 r1 1\nrm-image x\n".to_owned(),
        "vk-resolve/1 r1 1\nPS\n".to_owned(),
        "vk-resolve/1 r1 1\nps x\n".to_owned(),
        // pull 只收帶 digest 的引用
        "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools:v1.2.0\n".to_owned(),
        format!("vk-resolve/1 r1 1\npull ghcr.io/a@b@sha256:{A}\n"),
        format!(
            "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools@sha256:{}\n",
            &A[1..]
        ),
        format!(
            "vk-resolve/1 r1 1\npull ghcr.io/acme/ros_tools@sha256:{}\n",
            A.to_uppercase()
        ),
        format!("vk-resolve/1 r1 1\npull GHCR.io/acme/ros_tools@sha256:{A}\n"),
        format!("vk-resolve/1 r1 1\npull {} {}\n", pinned(), pinned()),
        // extract 只收 image ID
        "vk-resolve/1 r1 1\nextract ghcr.io/acme/ros_tools:v1.2.0 x1\n".to_owned(),
        format!("vk-resolve/1 r1 1\nextract {} x1\n", pinned()),
        format!("vk-resolve/1 r1 1\nextract {B} x1\n"),
        format!(
            "vk-resolve/1 r1 1\nextract sha256:{} x1\n",
            B.to_uppercase()
        ),
        format!("vk-resolve/1 r1 1\nextract sha256:{B}\n"),
        format!("vk-resolve/1 r1 1\nextract sha256:{B} X1\n"),
        format!("vk-resolve/1 r1 1\nextract sha256:{B} abcdefghijklmnopq\n"),
        // 主機路徑
        "vk-resolve/1 r1 1\nload e:my\\040tools.tar\n".to_owned(),
        "vk-resolve/1 r1 1\nload e:\n".to_owned(),
        "vk-resolve/1 r1 1\nload /srv/u/a.tar\n".to_owned(),
        "vk-resolve/1 r1 1\nstage e:token t1\n".to_owned(),
        // rm-container
        format!("vk-resolve/1 r1 1\nrm-container {}\n", &B[..12]),
        // runner 至少要有 command
        "vk-resolve/1 r1 1\nrunner ghcr.io/u/test:1\n".to_owned(),
        "vk-resolve/1 r1 1\nrunner ghcr.io/u/test:1 pytest\n".to_owned(),
    ];
    for b in bad {
        assert!(
            Op::parse_request(b.as_bytes(), &h).is_err(),
            "should reject {b:?}"
        );
    }
}

#[test]
fn encoding_refuses_ops_the_grammar_rejects() {
    let h = header(1);
    for op in [
        Op::Pull(image("ghcr.io/acme/ros_tools:v1.2.0")),
        Op::Load(field("rel/a.tar")),
        Op::Load(field("")),
        Op::Stage(field("token"), Slot::parse("t1").unwrap()),
    ] {
        assert!(op.encode_request(&h, seq(1)).is_err(), "{op:?}");
    }
}

#[test]
fn identifiers_are_validated() {
    assert!(ImageId::parse(&format!("sha256:{B}")).is_some());
    assert!(ImageId::parse(B).is_none());
    assert!(ImageId::parse(&format!("sha512:{B}")).is_none());
    assert!(Container::parse(&format!("{B}0")).is_none());
    assert!(Slot::parse("").is_none());
    assert!(Slot::parse("abcdefghijklmnop").is_some());
    assert!(Slot::parse("a-b").is_none());
    assert!(RunId::parse("").is_none());
    assert!(RunId::parse(&"a".repeat(65)).is_none());
    assert!(RunId::parse("R1").is_none());
    assert!(RunId::parse("20261005-ab12").is_some());
    assert!(ImageRef::parse("-x").is_none());
    assert!(ImageRef::parse("").is_none());
    assert!(ImageRef::parse("a b").is_none());
    assert!(!image("ghcr.io/a:v1").is_pinned());
    assert!(Header::new(0, RunId::parse("r1").unwrap()).is_none());
    assert_eq!(Seq::new(9999).unwrap().next(), None);
    assert!(Seq::new(0).is_none());
}

// ---- result ----

fn golden_outcomes() -> Vec<(Outcome, &'static str)> {
    vec![
        (Outcome::Ok, "ok"),
        (Outcome::Failed(1), "failed 1"),
        (Outcome::Failed(0), "failed 0"),
        (Outcome::Failed(255), "failed 255"),
        (
            Outcome::Runner(RunnerOutcome::NotStarted),
            "runner notstarted",
        ),
        (Outcome::Runner(RunnerOutcome::Exited(0)), "runner exited 0"),
        (
            Outcome::Runner(RunnerOutcome::Exited(130)),
            "runner exited 130",
        ),
        (
            Outcome::Runner(RunnerOutcome::Stopped(Some(137))),
            "runner stopped 137",
        ),
        (
            Outcome::Runner(RunnerOutcome::Stopped(None)),
            "runner stopped unavailable",
        ),
    ]
}

#[test]
fn every_result_has_exact_bytes_and_round_trips() {
    let h = header(1);
    for (outcome, line) in golden_outcomes() {
        let want = format!("vk-resolve/1 r1 7\n{line}\n");
        assert_eq!(outcome.encode_response(&h, seq(7)), want.as_bytes());
        let kind = if matches!(outcome, Outcome::Runner(_)) {
            OpKind::Runner
        } else {
            OpKind::Pull
        };
        assert_eq!(
            Outcome::parse_response(want.as_bytes(), &h, seq(7), kind).unwrap(),
            outcome
        );
    }
}

#[test]
fn runner_outcome_carries_three_facts_and_reason_code() {
    use RunnerOutcome::*;
    let rows = [
        // (結果, started, process-rc, stopped-by-vk, 原因代碼)
        (NotStarted, false, None, false, Some("VK0066")),
        (Exited(0), true, Some(0), false, None),
        (Exited(1), true, Some(1), false, Some("VK0067")),
        (Exited(130), true, Some(130), false, Some("VK0067")),
        (Stopped(Some(137)), true, Some(137), true, Some("VK0066")),
        (Stopped(None), true, None, true, Some("VK0066")),
    ];
    for (o, started, rc, stopped, code) in rows {
        assert_eq!(o.started(), started, "{o:?}");
        assert_eq!(o.process_rc(), rc, "{o:?}");
        assert_eq!(o.stopped_by_vk(), stopped, "{o:?}");
        assert_eq!(o.failure().map(|m| m.code), code, "{o:?}");
    }
}

#[test]
fn result_rejects_malformed_or_mismatched() {
    let h = header(1);
    let cases: &[(&str, OpKind)] = &[
        ("vk-resolve/1 r1 6\nok\n", OpKind::Pull),
        ("vk-resolve/1 r1 07\nok\n", OpKind::Pull),
        ("vk-resolve/1 r2 7\nok\n", OpKind::Pull),
        ("vk-resolve/2 r1 7\nok\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nok", OpKind::Pull),
        ("vk-resolve/1 r1 7\nOK\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nok 0\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nfailed\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nfailed 256\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nfailed 01\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nfailed -1\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nfailed unavailable\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nrunner exited 1\n", OpKind::Pull),
        ("vk-resolve/1 r1 7\nok\n", OpKind::Runner),
        ("vk-resolve/1 r1 7\nfailed 125\n", OpKind::Runner),
        ("vk-resolve/1 r1 7\nrunner stopped\n", OpKind::Runner),
        (
            "vk-resolve/1 r1 7\nrunner exited unavailable\n",
            OpKind::Runner,
        ),
        ("vk-resolve/1 r1 7\nrunner notstarted 1\n", OpKind::Runner),
        ("vk-resolve/1 r1 7\nrunner exited 1 \n", OpKind::Runner),
        ("vk-resolve/1 r1 7\nrunner\n", OpKind::Runner),
    ];
    for &(bytes, kind) in cases {
        assert!(
            Outcome::parse_response(bytes.as_bytes(), &h, seq(7), kind).is_err(),
            "should reject {bytes:?} for {kind:?}"
        );
    }
}

// ---- done ----

#[test]
fn done_has_exact_bytes_and_rejects_malformed() {
    let h = header(1);
    for code in 0..=3 {
        let exit = Exit::new(code).unwrap();
        let want = format!("vk-resolve/1 r1 done {code}\n");
        assert_eq!(exit.encode_done(&h), want.as_bytes());
        assert_eq!(Exit::parse_done(want.as_bytes(), &h).unwrap(), exit);
    }
    assert!(Exit::new(4).is_none());
    for bad in [
        "vk-resolve/1 r1 done 4\n",
        "vk-resolve/1 r1 done 00\n",
        "vk-resolve/1 r1 done\n",
        "vk-resolve/1 r1 done 0",
        "vk-resolve/1 r1 done 0\n\n",
        "vk-resolve/1 r1 1 0\n",
        "vk-resolve/1 r2 done 0\n",
    ] {
        assert!(Exit::parse_done(bad.as_bytes(), &h).is_err(), "{bad:?}");
    }
}

// ---- 入口 argv ----

fn os(v: &[&str]) -> Vec<OsString> {
    v.iter().map(OsString::from).collect()
}

fn launcher_argv(rest: &[&str]) -> Vec<OsString> {
    let mut v = os(&[
        "--protocol",
        "1",
        "--run-id",
        "r1",
        "--host-root",
        "/srv/u/my proj",
        "--host-cwd",
        "/srv/u/my proj/sub",
        "--run-log",
        ".vendor_kit/log/r1.jsonl",
        "--tty",
        "101",
        "--no-color",
        "1",
        "--",
    ]);
    v.extend(os(rest));
    v
}

#[test]
fn argv_parses_context_and_passes_rest_verbatim() {
    let inv = Invocation::parse(&launcher_argv(&["add", "--", "-h", "", "a b"])).unwrap();
    assert_eq!(
        inv,
        Invocation {
            protocol: 1,
            run_id: RunId::parse("r1").unwrap(),
            host_root: PathBuf::from("/srv/u/my proj"),
            host_cwd: PathBuf::from("/srv/u/my proj/sub"),
            run_log: PathBuf::from(".vendor_kit/log/r1.jsonl"),
            tty: Tty {
                stdin: true,
                stdout: false,
                stderr: true,
            },
            no_color: true,
            rest: os(&["add", "--", "-h", "", "a b"]),
        }
    );
    // `just vendor_kit` 的用法呼叫：`--` 之後沒有參數。
    assert!(
        Invocation::parse(&launcher_argv(&[]))
            .unwrap()
            .rest
            .is_empty()
    );
}

#[test]
fn argv_without_protocol_is_not_a_launcher_call() {
    for v in [vec![], os(&["add", "x"]), os(&["--run-id", "r1"])] {
        let e = Invocation::parse(&v).unwrap_err();
        assert_eq!(e, ArgvError::NoProtocol);
        assert!(e.message().is_none());
    }
}

#[test]
fn argv_rejects_wrong_order_missing_or_invalid_values() {
    let base = launcher_argv(&["sync"]);
    let with = |i: usize, v: &str| {
        let mut a = base.clone();
        a[i] = OsString::from(v);
        a
    };
    let invalid = |option| move |e: &ArgvError| matches!(e, ArgvError::Invalid { option: o, .. } if *o == option);
    let expected = |option| move |e: &ArgvError| *e == ArgvError::Expected(option);
    type Check = Box<dyn Fn(&ArgvError) -> bool>;
    let cases: Vec<(Vec<OsString>, Check)> = vec![
        (with(1, "0"), Box::new(invalid(argv::PROTOCOL))),
        (with(1, "01"), Box::new(invalid(argv::PROTOCOL))),
        (with(1, "x"), Box::new(invalid(argv::PROTOCOL))),
        (with(1, ""), Box::new(invalid(argv::PROTOCOL))),
        (with(3, "R1"), Box::new(invalid(argv::RUN_ID))),
        (with(5, "home/u"), Box::new(invalid(argv::HOST_ROOT))),
        (with(7, ""), Box::new(invalid(argv::HOST_CWD))),
        (with(9, "/abs/r1.jsonl"), Box::new(invalid(argv::RUN_LOG))),
        (
            with(9, ".vendor_kit/../x"),
            Box::new(invalid(argv::RUN_LOG)),
        ),
        (with(9, ""), Box::new(invalid(argv::RUN_LOG))),
        (with(11, "11"), Box::new(invalid(argv::TTY))),
        (with(11, "1111"), Box::new(invalid(argv::TTY))),
        (with(11, "112"), Box::new(invalid(argv::TTY))),
        (with(13, "2"), Box::new(invalid(argv::NO_COLOR))),
        (with(13, "true"), Box::new(invalid(argv::NO_COLOR))),
        (with(2, "--host-root"), Box::new(expected(argv::RUN_ID))),
        (with(14, "sync"), Box::new(expected(argv::END))),
        (base[..14].to_vec(), Box::new(expected(argv::END))),
        (base[..13].to_vec(), Box::new(expected(argv::NO_COLOR))),
        (base[..2].to_vec(), Box::new(expected(argv::RUN_ID))),
        (os(&["--protocol"]), Box::new(expected(argv::PROTOCOL))),
    ];
    for (a, check) in cases {
        let e = Invocation::parse(&a).unwrap_err();
        assert!(check(&e), "{a:?} → {e:?}");
        assert_eq!(e.message().map(|m| m.code), Some("VK0056"));
    }
}

// ---- 控制目錄的往返 ----

fn listing(dir: &std::path::Path) -> Vec<String> {
    let mut v: Vec<String> = fs::read_dir(dir)
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect();
    v.sort();
    v
}

#[test]
fn channel_round_trip_writes_and_reads_control_files() {
    let dir = tempfile::tempdir().unwrap();
    let h = header(1);
    let mut ch = Channel::new(dir.path(), h.clone());

    let pull = Op::Pull(image(&pinned()));
    assert_eq!(ch.send(&pull).unwrap(), seq(1));
    assert_eq!(
        fs::read_to_string(dir.path().join("req.1")).unwrap(),
        format!("vk-resolve/1 r1 1\npull {}\n", pinned())
    );
    assert_eq!(listing(dir.path()), ["req.1"], "暫存檔要 rename 掉");

    // 結果到之前：收不到、也不能送下一個或結束。
    assert!(ch.try_receive().unwrap().is_none());
    assert!(matches!(ch.send(&Op::Ps), Err(ChannelError::Pending(s)) if s == seq(1)));

    fs::write(
        ch.response_path(seq(1)),
        Outcome::Ok.encode_response(&h, seq(1)),
    )
    .unwrap();
    assert_eq!(
        ch.try_receive().unwrap().unwrap(),
        Reply {
            seq: seq(1),
            kind: OpKind::Pull,
            outcome: Outcome::Ok,
        }
    );
    assert!(matches!(ch.try_receive(), Err(ChannelError::Idle)));

    assert_eq!(ch.send(&Op::Ps).unwrap(), seq(2));
    assert_eq!(ch.output_path(seq(2)), dir.path().join("res.2.out"));
    // 配不上 op 的結果算協定不合，且 request 仍未完成。
    fs::write(
        ch.response_path(seq(2)),
        Outcome::Runner(RunnerOutcome::NotStarted).encode_response(&h, seq(2)),
    )
    .unwrap();
    let e = ch.try_receive().unwrap_err();
    assert!(matches!(e, ChannelError::Protocol(_)), "{e:?}");
    assert_eq!(e.message().code, "VK0056");
    fs::write(
        ch.response_path(seq(2)),
        Outcome::Failed(1).encode_response(&h, seq(2)),
    )
    .unwrap();
    assert_eq!(
        ch.receive(std::time::Duration::ZERO).unwrap().outcome,
        Outcome::Failed(1)
    );

    ch.finish(Exit::new(2).unwrap()).unwrap();
    assert_eq!(
        fs::read_to_string(dir.path().join("done")).unwrap(),
        "vk-resolve/1 r1 done 2\n"
    );
    assert_eq!(
        listing(dir.path()),
        ["done", "req.1", "req.2", "res.1", "res.2"]
    );
}

#[test]
fn channel_refuses_to_finish_with_a_pending_request() {
    let dir = tempfile::tempdir().unwrap();
    let mut ch = Channel::new(dir.path(), header(1));
    ch.send(&Op::Ps).unwrap();
    assert!(matches!(
        ch.finish(Exit::new(0).unwrap()),
        Err(ChannelError::Pending(_))
    ));
    assert!(!dir.path().join("done").exists());
}

#[test]
fn channel_does_not_write_invalid_requests() {
    let dir = tempfile::tempdir().unwrap();
    let mut ch = Channel::new(dir.path(), header(1));
    let e = ch.send(&Op::Load(field("rel.tar"))).unwrap_err();
    assert!(matches!(e, ChannelError::Protocol(_)));
    assert!(listing(dir.path()).is_empty());
    // 沒送出就不佔 seq。
    assert_eq!(ch.send(&Op::Ps).unwrap(), seq(1));
}

#[test]
fn channel_restricted_to_rescue_only_sends_rescue_ops() {
    let dir = tempfile::tempdir().unwrap();
    let h = header(7);
    let mut ch = Channel::new(dir.path(), h.clone());
    ch.restrict_to_rescue();
    let e = ch.send(&Op::Ps).unwrap_err();
    assert!(matches!(e, ChannelError::NotRescue(OpKind::Ps)), "{e:?}");
    assert_eq!(e.message().code, "VK0056");
    assert!(listing(dir.path()).is_empty());
    // 救援路徑的 op 照常送，header 用呼叫方的 P；被拒的 op 不佔 seq。
    assert_eq!(ch.send(&Op::Pull(image(&pinned()))).unwrap(), seq(1));
    assert_eq!(
        fs::read_to_string(dir.path().join("req.1")).unwrap(),
        format!("vk-resolve/7 r1 1\npull {}\n", pinned())
    );
}

// ---- 救援路徑：跨介面版永久不變 ----

#[test]
fn rescue_constants_are_pinned() {
    assert_eq!(GRAMMAR, "vk-resolve");
    assert_eq!(RESCUE_OPS, ["pull", "load", "inspect", "extract", "stage"]);
    assert!(RESCUE_OPS.iter().all(|o| OPS.contains(o)));
    assert_eq!(
        argv::ORDER,
        [
            "--protocol",
            "--run-id",
            "--host-root",
            "--host-cwd",
            "--run-log",
            "--tty",
            "--no-color"
        ]
    );
    assert_eq!(argv::END, "--");
    assert_eq!(
        [mount::ROOT, mount::CTL, mount::IN],
        ["/vk/root", "/vk/ctl", "/vk/in"]
    );
    assert_eq!(
        [
            files::REQ_PREFIX,
            files::RES_PREFIX,
            files::OUT_SUFFIX,
            files::DONE,
            files::TMP_SUFFIX
        ],
        ["req.", "res.", ".out", "done", ".tmp"]
    );
    // in/ 裡啟動器寫的引擎引用檔（launcher/wire.sh 的 vk_wire_in_engine）。
    assert_eq!(files::IN_ENGINE, "engine");
    // `--` 之後只有 bootstrap.sh 會送的保留入口（只檢查、修復）。
    assert_eq!(
        [entry::SHELL_CHECK, entry::SHELL_REPAIR],
        ["@shell-check", "@shell-repair"]
    );
}

#[test]
fn rescue_wire_format_only_differs_by_protocol_number() {
    // 救援 op、ok／failed 與 done 在任何 P 下都是同一份位元組，只有 header 的 P 不同。
    for p in [1, 2, 7, 42] {
        let h = header(p);
        let hdr = format!("vk-resolve/{p} r1");
        for (op, golden) in golden_ops() {
            if !RESCUE_OPS.contains(&op.kind().name()) {
                continue;
            }
            let want = golden.replacen("vk-resolve/1 r1", &hdr, 1);
            assert_eq!(op.encode_request(&h, seq(3)).unwrap(), want.as_bytes());
            assert_eq!(Op::parse_request(want.as_bytes(), &h).unwrap().1, op);
        }
        for (outcome, line) in [(Outcome::Ok, "ok"), (Outcome::Failed(1), "failed 1")] {
            let want = format!("{hdr} 3\n{line}\n");
            assert_eq!(outcome.encode_response(&h, seq(3)), want.as_bytes());
        }
        assert_eq!(
            Exit::new(2).unwrap().encode_done(&h),
            format!("{hdr} done 2\n").as_bytes()
        );
    }
}
