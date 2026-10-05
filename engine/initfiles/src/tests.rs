#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeMap;

use super::*;

/// 測試用的 repo：目前檔與基準版副本。
#[derive(Default)]
struct Repo {
    current: BTreeMap<String, Vec<u8>>,
    baseline: BTreeMap<String, Vec<u8>>,
}

impl Repo {
    fn file(mut self, path: &str, contents: &str) -> Self {
        self.current
            .insert(path.to_owned(), contents.as_bytes().to_vec());
        self
    }

    fn base(mut self, path: &str, contents: &str) -> Self {
        self.baseline
            .insert(path.to_owned(), contents.as_bytes().to_vec());
        self
    }

    fn plan(&self, command: Command, files: &[InitFile<'_>], md: &Metadata) -> Result<Plan, Error> {
        plan(
            command,
            files,
            md,
            |p| Ok(self.current.get(p).cloned()),
            |p| Ok(self.baseline.get(p).cloned()),
        )
    }
}

fn whole<'a>(path: &'a str, contents: &'a str) -> InitFile<'a> {
    InitFile {
        path,
        strategy: Strategy::Whole,
        contents: contents.as_bytes(),
    }
}

fn appended<'a>(path: &'a str, contents: &'a str) -> InitFile<'a> {
    InitFile {
        path,
        strategy: Strategy::Append,
        contents: contents.as_bytes(),
    }
}

fn record(path: &str, state: State) -> FileRecord {
    FileRecord::new(path, state)
}

fn metadata(records: Vec<FileRecord>) -> Metadata {
    let mut md = Metadata::new();
    for r in records {
        md.put(r).unwrap();
    }
    md
}

fn only(plan: &Plan) -> &FilePlan {
    assert_eq!(plan.files.len(), 1, "{plan:?}");
    &plan.files[0]
}

fn after(p: &FilePlan) -> &str {
    std::str::from_utf8(&p.write.as_ref().unwrap().after).unwrap()
}

const BASE: &str = "a\nb\nc\nd\ne\n";
const NEW: &str = "a\nb\nc\nd\nE\n";

// ---------------------------------------------------------------------------
// 沒有紀錄

#[test]
fn absent_file_is_created_without_asking() {
    let plan = Repo::default()
        .plan(Command::Add, &[whole("ci.toml", NEW)], &Metadata::new())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Create);
    assert_eq!(p.ask, None);
    assert!(plan.questions.is_empty());
    let w = p.write.as_ref().unwrap();
    assert_eq!(w.before, None);
    assert_eq!(w.after, NEW.as_bytes());
    assert_eq!(p.baseline.as_deref(), Some(NEW.as_bytes()));
    let r = p.record.as_ref().unwrap();
    assert_eq!(r.state, State::Managed);
    assert_eq!(r.hash, Some(FileHash::of(NEW.as_bytes())));
    assert!(r.lines.is_empty());
    assert_eq!(p.message(), None);
    assert!(!p.listed());
}

#[test]
fn upgrade_creates_new_init_file_that_is_absent() {
    let md = metadata(vec![]);
    let plan = Repo::default()
        .plan(Command::Upgrade, &[whole("new.toml", NEW)], &md)
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Create);
}

#[test]
fn add_existing_whole_file_is_left_unmanaged_with_vk0018() {
    let repo = Repo::default().file("ci.toml", "mine\n");
    let plan = repo
        .plan(Command::Add, &[whole("ci.toml", NEW)], &Metadata::new())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Existing);
    assert_eq!(p.write, None);
    assert_eq!(p.baseline, None);
    assert_eq!(p.ask, None);
    assert_eq!(p.record, Some(record("ci.toml", State::Unmanaged)));
    assert_eq!(p.message(), Some(&messages::VK0018));
}

#[test]
fn upgrade_existing_whole_file_without_record_is_a_gap() {
    let repo = Repo::default().file("ci.toml", "mine\n");
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &Metadata::new())
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::ExistingOnUpgrade));
    assert_eq!(only(&plan).record, None);
}

#[test]
fn existing_file_is_appended_after_asking() {
    let repo = Repo::default().file(".gitignore", "target/\n");
    let plan = repo
        .plan(
            Command::Add,
            &[appended(".gitignore", "/.vendor_kit/cache/\n/log/\n")],
            &Metadata::new(),
        )
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Append);
    assert_eq!(p.ask, Some(Ask::Append));
    assert_eq!(
        plan.questions,
        vec![Question {
            path: ".gitignore".into(),
            ask: Ask::Append
        }]
    );
    assert_eq!(after(p), "target/\n/.vendor_kit/cache/\n/log/\n");
    assert_eq!(
        p.write.as_ref().unwrap().before.as_deref(),
        Some(b"target/\n".as_slice())
    );
    assert_eq!(p.baseline, None);
    let r = p.record.as_ref().unwrap();
    assert_eq!(r.state, State::Appended);
    assert_eq!(r.lines, vec!["/.vendor_kit/cache/", "/log/"]);
    assert_eq!(r.hash, Some(FileHash::of(after(p).as_bytes())));
}

#[test]
fn append_follows_line_endings_and_adds_missing_newline() {
    let repo = Repo::default()
        .file("crlf", "a\r\nb\r\n")
        .file("noeol", "a");
    let plan = repo
        .plan(
            Command::Add,
            &[appended("crlf", "x\n"), appended("noeol", "x\r\n")],
            &Metadata::new(),
        )
        .unwrap();
    assert_eq!(after(&plan.files[0]), "a\r\nb\r\nx\r\n");
    assert_eq!(after(&plan.files[1]), "a\nx\n");
    assert_eq!(plan.files[1].record.as_ref().unwrap().lines, vec!["x"]);
}

#[test]
fn append_with_lines_already_present_is_a_gap() {
    let repo = Repo::default().file(".gitignore", "target/\r\n/log/\r\n");
    let plan = repo
        .plan(
            Command::Add,
            &[appended(".gitignore", "/cache/\n/log/\n")],
            &Metadata::new(),
        )
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Gap(Gap::LinesAlreadyPresent));
    assert_eq!((p.ask, &p.write, &p.record), (None, &None, &None));
    assert!(plan.questions.is_empty());
}

#[test]
fn append_target_missing_is_a_gap() {
    let plan = Repo::default()
        .plan(
            Command::Add,
            &[appended(".gitignore", "x\n")],
            &Metadata::new(),
        )
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::AppendTargetMissing));
    assert_eq!(only(&plan).write, None);
}

#[test]
fn empty_append_is_a_gap() {
    let repo = Repo::default().file(".gitignore", "x\n");
    let plan = repo
        .plan(
            Command::Add,
            &[appended(".gitignore", "")],
            &Metadata::new(),
        )
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::EmptyAppend));
}

#[test]
fn append_of_non_utf8_is_an_error() {
    let repo = Repo::default().file(".gitignore", "x\n");
    let file = InitFile {
        path: ".gitignore",
        strategy: Strategy::Append,
        contents: b"\xff\n",
    };
    let err = repo
        .plan(Command::Add, &[file], &Metadata::new())
        .unwrap_err();
    assert!(matches!(err, Error::NotUtf8 { ref path } if path == ".gitignore"));
    assert_eq!(err.message(), None);
}

#[test]
fn add_with_existing_record_is_a_gap() {
    let md = metadata(vec![record("ci.toml", State::Managed)]);
    let plan = Repo::default()
        .plan(Command::Add, &[whole("ci.toml", NEW)], &md)
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::RecordOnAdd));
}

// ---------------------------------------------------------------------------
// managed

fn managed_md() -> Metadata {
    let mut r = record("ci.toml", State::Managed);
    r.hash = Some(FileHash::of(BASE.as_bytes()));
    metadata(vec![r])
}

#[test]
fn managed_with_unchanged_upstream_is_left_alone() {
    let repo = Repo::default()
        .file("ci.toml", "mine\n")
        .base("ci.toml", BASE);
    let plan = repo
        .plan(
            Command::Upgrade,
            &[whole("ci.toml", "a\r\nb\r\nc\r\nd\r\ne\r\n")],
            &managed_md(),
        )
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::UpstreamUnchanged);
    assert_eq!(
        (p.ask, &p.write, &p.baseline, &p.record),
        (None, &None, &None, &None)
    );
}

#[test]
fn managed_unchanged_by_user_asks_to_replace() {
    let repo = Repo::default().file("ci.toml", BASE).base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Replace);
    assert_eq!(p.ask, Some(Ask::Replace));
    assert_eq!(plan.questions.len(), 1);
    assert_eq!(after(p), NEW);
    assert_eq!(
        p.write.as_ref().unwrap().before.as_deref(),
        Some(BASE.as_bytes())
    );
    assert_eq!(p.baseline.as_deref(), Some(NEW.as_bytes()));
    assert_eq!(p.record, None, "hash 由呼叫端經 record_write 更新");
    assert_eq!(p.message(), None);
}

#[test]
fn crlf_only_edit_counts_as_unchanged_and_keeps_line_endings() {
    let repo = Repo::default()
        .file("ci.toml", "a\r\nb\r\nc\r\nd\r\ne\r\n")
        .base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Replace);
    assert_eq!(after(p), "a\r\nb\r\nc\r\nd\r\nE\r\n");
    assert_eq!(p.baseline.as_deref(), Some(NEW.as_bytes()));
}

#[test]
fn managed_changed_on_both_sides_asks_to_merge() {
    let repo = Repo::default()
        .file("ci.toml", "A\nb\nc\nd\ne\n")
        .base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Merge { conflicts: None });
    assert_eq!(p.ask, Some(Ask::Merge));
    assert_eq!(after(p), "A\nb\nc\nd\nE\n");
    assert_eq!(p.baseline.as_deref(), Some(NEW.as_bytes()));
    assert_eq!(p.record, None);
    assert_eq!(p.message(), None);
}

#[test]
fn merge_conflict_writes_markers_pushes_baseline_and_reports_vk0021() {
    let repo = Repo::default()
        .file("ci.toml", "a\nb\nc\nd\nmine\n")
        .base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Merge { conflicts: Some(1) });
    assert_eq!(p.ask, Some(Ask::Merge));
    assert!(after(p).contains(merge::CONFLICT_MARKER), "{}", after(p));
    assert_eq!(p.baseline.as_deref(), Some(NEW.as_bytes()));
    assert_eq!(p.message(), Some(&messages::VK0021));
}

#[test]
fn managed_already_equal_to_new_is_a_gap() {
    let repo = Repo::default().file("ci.toml", NEW).base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Gap(Gap::CurrentIsNew));
    assert_eq!((p.ask, &p.write, &p.baseline), (None, &None, &None));
}

#[test]
fn managed_deleted_by_user_is_not_recreated() {
    let repo = Repo::default().base("ci.toml", BASE);
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::UserDeleted);
    assert_eq!((p.ask, &p.write, &p.baseline), (None, &None, &None));
    let r = p.record.as_ref().unwrap();
    assert_eq!(r.state, State::Deleted);
    assert_eq!(r.hash, Some(FileHash::of(BASE.as_bytes())), "其他欄位保留");
    assert!(p.listed());
}

#[test]
fn managed_without_baseline_copy_stops() {
    let repo = Repo::default().file("ci.toml", BASE);
    let err = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &managed_md())
        .unwrap_err();
    assert!(matches!(err, Error::BaselineMissing { ref path } if path == "ci.toml"));
    assert_eq!(err.message(), None);
}

#[test]
fn managed_switched_to_append_is_a_gap() {
    let repo = Repo::default().file("ci.toml", BASE).base("ci.toml", BASE);
    let plan = repo
        .plan(
            Command::Upgrade,
            &[appended("ci.toml", "x\n")],
            &managed_md(),
        )
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::StrategyChanged));
}

// ---------------------------------------------------------------------------
// appended

fn appended_md(lines: &[&str]) -> Metadata {
    let mut r = record(".gitignore", State::Appended);
    r.lines = lines.iter().map(|s| (*s).to_owned()).collect();
    r.hash = Some(FileHash::of(b"target/\n/log/\n"));
    metadata(vec![r])
}

#[test]
fn appended_with_same_lines_is_left_alone() {
    let repo = Repo::default().file(".gitignore", "target/\n/log/\n");
    let plan = repo
        .plan(
            Command::Upgrade,
            &[appended(".gitignore", "/log/\r\n")],
            &appended_md(&["/log/"]),
        )
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::UpstreamUnchanged);
    assert_eq!((p.ask, &p.write, &p.record), (None, &None, &None));
}

#[test]
fn appended_with_changed_lines_is_a_gap() {
    let repo = Repo::default().file(".gitignore", "target/\n/log/\n");
    let plan = repo
        .plan(
            Command::Upgrade,
            &[appended(".gitignore", "/log/\n/tmp/\n")],
            &appended_md(&["/log/"]),
        )
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::AppendedLinesChanged));
}

#[test]
fn appended_switched_to_whole_is_a_gap() {
    let repo = Repo::default().file(".gitignore", "target/\n/log/\n");
    let plan = repo
        .plan(
            Command::Upgrade,
            &[whole(".gitignore", "/log/\n")],
            &appended_md(&["/log/"]),
        )
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::StrategyChanged));
}

// ---------------------------------------------------------------------------
// unmanaged、declined、deleted

#[test]
fn unmanaged_is_not_processed_with_vk0019() {
    let md = metadata(vec![record("ci.toml", State::Unmanaged)]);
    let repo = Repo::default().file("ci.toml", "mine\n");
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &md)
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Unmanaged);
    assert_eq!(
        (p.ask, &p.write, &p.baseline, &p.record),
        (None, &None, &None, &None)
    );
    assert_eq!(p.message(), Some(&messages::VK0019));
}

#[test]
fn declined_same_version_is_not_asked_again_with_vk0020() {
    let mut r = record("ci.toml", State::Declined);
    r.declined_hash = Some(FileHash::of(b"a\r\nb\r\nc\r\nd\r\nE\r\n"));
    let repo = Repo::default().file("ci.toml", BASE).base("ci.toml", BASE);
    let plan = repo
        .plan(
            Command::Upgrade,
            &[whole("ci.toml", NEW)],
            &metadata(vec![r]),
        )
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::Declined);
    assert_eq!(
        (p.ask, &p.write, &p.baseline, &p.record),
        (None, &None, &None, &None)
    );
    assert!(plan.questions.is_empty());
    assert_eq!(p.message(), Some(&messages::VK0020));
}

#[test]
fn declined_other_version_or_no_hash_is_a_gap() {
    let mut other = record("a", State::Declined);
    other.declined_hash = Some(FileHash::of(b"old\n"));
    let no_hash = record("b", State::Declined);
    let plan = Repo::default()
        .plan(
            Command::Upgrade,
            &[whole("a", NEW), whole("b", NEW)],
            &metadata(vec![other, no_hash]),
        )
        .unwrap();
    for p in &plan.files {
        assert_eq!(
            p.verdict,
            Verdict::Gap(Gap::DeclinedOtherVersion),
            "{}",
            p.path
        );
    }
}

#[test]
fn deleted_stays_deleted() {
    let md = metadata(vec![record("ci.toml", State::Deleted)]);
    let plan = Repo::default()
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &md)
        .unwrap();
    let p = only(&plan);
    assert_eq!(p.verdict, Verdict::StillDeleted);
    assert_eq!((p.ask, &p.write, &p.record), (None, &None, &None));
    assert!(p.listed());
}

#[test]
fn deleted_file_that_reappeared_is_a_gap() {
    let md = metadata(vec![record("ci.toml", State::Deleted)]);
    let repo = Repo::default().file("ci.toml", "again\n");
    let plan = repo
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &md)
        .unwrap();
    assert_eq!(only(&plan).verdict, Verdict::Gap(Gap::DeletedReappeared));
}

// ---------------------------------------------------------------------------
// 整次

#[test]
fn file_no_longer_provided_is_a_gap_after_the_inputs() {
    let md = metadata(vec![
        record("gone", State::Managed),
        record("ci.toml", State::Unmanaged),
    ]);
    let plan = Repo::default()
        .plan(Command::Upgrade, &[whole("ci.toml", NEW)], &md)
        .unwrap();
    let verdicts: Vec<_> = plan
        .files
        .iter()
        .map(|f| (f.path.as_str(), f.verdict))
        .collect();
    assert_eq!(
        verdicts,
        vec![
            ("ci.toml", Verdict::Unmanaged),
            ("gone", Verdict::Gap(Gap::NoLongerProvided)),
        ]
    );
    assert_eq!(
        plan.gaps().collect::<Vec<_>>(),
        vec![("gone", Gap::NoLongerProvided)]
    );
}

#[test]
fn all_questions_are_collected_in_input_order() {
    let mut r1 = record("replace", State::Managed);
    r1.hash = Some(FileHash::of(BASE.as_bytes()));
    let mut r2 = record("merge", State::Managed);
    r2.hash = Some(FileHash::of(BASE.as_bytes()));
    let md = metadata(vec![r1, r2]);
    let repo = Repo::default()
        .file("replace", BASE)
        .base("replace", BASE)
        .file("merge", "A\nb\nc\nd\ne\n")
        .base("merge", BASE)
        .file(".gitignore", "target/\n");
    let plan = repo
        .plan(
            Command::Upgrade,
            &[
                whole("replace", NEW),
                whole("created", NEW),
                appended(".gitignore", "/log/\n"),
                whole("merge", NEW),
            ],
            &md,
        )
        .unwrap();
    let questions: Vec<_> = plan
        .questions
        .iter()
        .map(|q| (q.path.as_str(), q.ask))
        .collect();
    assert_eq!(
        questions,
        vec![
            ("replace", Ask::Replace),
            (".gitignore", Ask::Append),
            ("merge", Ask::Merge),
        ]
    );
    assert_eq!(plan.files[1].verdict, Verdict::Create);
}

#[test]
fn duplicate_init_file_path_is_an_error() {
    let err = Repo::default()
        .plan(
            Command::Add,
            &[whole("x", NEW), whole("x", BASE)],
            &Metadata::new(),
        )
        .unwrap_err();
    assert!(matches!(err, Error::DuplicatePath { ref path } if path == "x"));
}

#[test]
fn read_errors_propagate_with_side() {
    let failing = |_: &str| -> io::Result<Option<Vec<u8>>> {
        Err(io::Error::new(io::ErrorKind::PermissionDenied, "denied"))
    };
    let err = plan(
        Command::Add,
        &[whole("x", NEW)],
        &Metadata::new(),
        failing,
        |_| Ok(None),
    )
    .unwrap_err();
    assert!(matches!(
        err,
        Error::Read {
            side: Side::Current,
            ..
        }
    ));

    let err = plan(
        Command::Upgrade,
        &[whole("ci.toml", NEW)],
        &managed_md(),
        |_| Ok(Some(BASE.as_bytes().to_vec())),
        failing,
    )
    .unwrap_err();
    assert!(matches!(
        err,
        Error::Read {
            side: Side::Baseline,
            ..
        }
    ));
    assert!(err.to_string().contains("ci.toml"), "{err}");
}

#[test]
fn baseline_is_read_only_for_managed_records() {
    let md = metadata(vec![record("u", State::Unmanaged)]);
    let plan = plan(
        Command::Upgrade,
        &[whole("u", NEW), whole("created", NEW)],
        &md,
        |_| Ok(None),
        |p: &str| -> io::Result<Option<Vec<u8>>> { panic!("baseline read for {p}") },
    )
    .unwrap();
    assert_eq!(plan.files.len(), 2);
}
