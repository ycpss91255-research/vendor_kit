//! 單元測試：digest、dist 格式、逐檔指紋（指紋不符、多檔、少檔）、`<ns>` 撞名的三種來源。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;

use super::*;

const LOCK: &str = "ghcr.io/acme/tool:v1.2.3@sha256:3333333333333333333333333333333333333333333333333333333333333333";
const REPO_DIGEST: &str =
    "ghcr.io/acme/tool@sha256:3333333333333333333333333333333333333333333333333333333333333333";

fn locked() -> ImageRef {
    ImageRef::parse(LOCK).unwrap()
}

fn tree(files: &[(&str, &[u8])]) -> tempfile::TempDir {
    let dir = tempfile::tempdir().unwrap();
    for (path, contents) in files {
        let full = dir.path().join(path);
        fs::create_dir_all(full.parent().unwrap()).unwrap();
        fs::write(full, contents).unwrap();
    }
    dir
}

/// 一個交付兩個 `<ns>`（tool、tool_ext）的工具。
fn staged_tree() -> tempfile::TempDir {
    tree(&[
        ("just/tool.just", b"default:\n    echo tool\n"),
        ("just/tool_ext.just", b"x:\n    echo x\n"),
        ("templates/a.txt", b"a\n"),
    ])
}

fn run(
    root: &Path,
    repo: &str,
    digests: &[String],
    taken: &Taken,
    previous: Option<&Stamp>,
) -> Result<Candidate, Error> {
    let locked = locked();
    let staged = Staged {
        repo,
        locked: &locked,
        root,
        repo_digests: digests,
    };
    verify(&staged, taken, previous)
}

fn ok_digests() -> Vec<String> {
    vec![REPO_DIGEST.to_owned()]
}

fn verify_ok(root: &Path) -> Candidate {
    run(root, "tool", &ok_digests(), &Taken::new(), None).unwrap()
}

// ---------------------------------------------------------------------------
// 正常情況

#[test]
fn verified_candidate_has_fingerprints_and_namespaces() {
    let dir = staged_tree();
    let c = verify_ok(dir.path());
    assert_eq!(c.repo(), "tool");
    assert_eq!(c.version(), LOCK);
    assert_eq!(c.locked(), &locked());
    assert_eq!(c.root(), dir.path());
    assert_eq!(c.namespaces(), ["tool", "tool_ext"]);
    let paths: Vec<&str> = c.entries().iter().map(|e| e.path.as_str()).collect();
    assert_eq!(
        paths,
        ["just/tool.just", "just/tool_ext.just", "templates/a.txt"]
    );
    assert_eq!(c.entries()[2].sha256, stamp::Digest::of(b"a\n"));
    assert!(c.recheck().is_ok());
}

#[test]
fn verify_writes_nothing() {
    let dir = staged_tree();
    let before = Stamp::compute(LOCK, dir.path()).unwrap();
    verify_ok(dir.path());
    let after = Stamp::compute(LOCK, dir.path()).unwrap();
    assert!(before.compare(&after).is_match());
}

#[test]
fn any_matching_repo_digest_is_enough() {
    let dir = staged_tree();
    let digests = vec![
        "ghcr.io/other/tool@sha256:3333333333333333333333333333333333333333333333333333333333333333"
            .to_owned(),
        REPO_DIGEST.to_owned(),
    ];
    assert!(run(dir.path(), "tool", &digests, &Taken::new(), None).is_ok());
}

// ---------------------------------------------------------------------------
// digest（G1）

#[test]
fn digest_mismatch_has_no_code() {
    let dir = staged_tree();
    for digests in [
        vec![],
        vec![
            "ghcr.io/acme/tool@sha256:4444444444444444444444444444444444444444444444444444444444444444"
                .to_owned(),
        ],
        // 同一個 digest、不同的 image 名稱也不算。
        vec![
            "ghcr.io/acme/other@sha256:3333333333333333333333333333333333333333333333333333333333333333"
                .to_owned(),
        ],
    ] {
        let err = run(dir.path(), "tool", &digests, &Taken::new(), None).unwrap_err();
        match &err {
            Error::DigestMismatch { expected, found } => {
                assert_eq!(expected, REPO_DIGEST);
                assert_eq!(found, &digests);
            }
            other => panic!("{other}"),
        }
        assert_eq!(err.message(), None);
    }
}

// ---------------------------------------------------------------------------
// 逐檔指紋：指紋不符、多檔、少檔（G1）

fn fingerprint_diff(err: Error) -> Diff {
    assert_eq!(err.message(), None, "{err}");
    match err {
        Error::Fingerprint(d) => d,
        other => panic!("{other}"),
    }
}

#[test]
fn recheck_reports_changed_content() {
    let dir = staged_tree();
    let c = verify_ok(dir.path());
    fs::write(dir.path().join("templates/a.txt"), b"A\n").unwrap();
    let d = fingerprint_diff(c.recheck().unwrap_err());
    assert_eq!(d.changed, ["templates/a.txt"]);
    assert!(d.extra.is_empty() && d.missing.is_empty());
}

#[test]
fn recheck_reports_extra_file() {
    let dir = staged_tree();
    let c = verify_ok(dir.path());
    fs::write(dir.path().join("templates/b.txt"), b"b\n").unwrap();
    let d = fingerprint_diff(c.recheck().unwrap_err());
    assert_eq!(d.extra, ["templates/b.txt"]);
    assert!(d.changed.is_empty() && d.missing.is_empty());
}

#[test]
fn recheck_reports_missing_file() {
    let dir = staged_tree();
    let c = verify_ok(dir.path());
    fs::remove_file(dir.path().join("templates/a.txt")).unwrap();
    let d = fingerprint_diff(c.recheck().unwrap_err());
    assert_eq!(d.missing, ["templates/a.txt"]);
    assert!(d.changed.is_empty() && d.extra.is_empty());
}

#[test]
fn previous_stamp_of_same_version_must_match() {
    let dir = staged_tree();
    let previous = Stamp::compute(LOCK, dir.path()).unwrap();
    assert!(
        run(
            dir.path(),
            "tool",
            &ok_digests(),
            &Taken::new(),
            Some(&previous)
        )
        .is_ok()
    );

    fs::write(dir.path().join("templates/a.txt"), b"A\n").unwrap();
    fs::write(dir.path().join("templates/b.txt"), b"b\n").unwrap();
    fs::remove_file(dir.path().join("just/tool_ext.just")).unwrap();
    let err = run(
        dir.path(),
        "tool",
        &ok_digests(),
        &Taken::new(),
        Some(&previous),
    )
    .unwrap_err();
    let d = fingerprint_diff(err);
    assert_eq!(d.changed, ["templates/a.txt"]);
    assert_eq!(d.extra, ["templates/b.txt"]);
    assert_eq!(d.missing, ["just/tool_ext.just"]);
}

#[test]
fn previous_stamp_of_another_version_is_not_compared() {
    let dir = staged_tree();
    let other = tree(&[("just/tool.just", b"old\n")]);
    let previous = Stamp::compute(
        "ghcr.io/acme/tool:v1.0.0@sha256:5555555555555555555555555555555555555555555555555555555555555555",
        other.path(),
    )
    .unwrap();
    assert!(
        run(
            dir.path(),
            "tool",
            &ok_digests(),
            &Taken::new(),
            Some(&previous)
        )
        .is_ok()
    );
}

#[test]
fn symlink_in_staged_content_is_rejected() {
    let dir = staged_tree();
    std::os::unix::fs::symlink("a.txt", dir.path().join("templates/link")).unwrap();
    let err = run(dir.path(), "tool", &ok_digests(), &Taken::new(), None).unwrap_err();
    assert!(matches!(err, Error::Fingerprints(_)), "{err}");
    assert_eq!(err.message(), None);
}

// ---------------------------------------------------------------------------
// dist 格式（G2）

fn format_error(root: &Path) -> FormatError {
    let err = run(root, "tool", &ok_digests(), &Taken::new(), None).unwrap_err();
    assert_eq!(err.message(), None, "{err}");
    match err {
        Error::Format(e) => e,
        other => panic!("{other}"),
    }
}

#[test]
fn missing_just_dir_is_a_format_error() {
    let dir = tree(&[("templates/a.txt", b"a\n")]);
    assert!(matches!(format_error(dir.path()), FormatError::NoJustDir));
    let file = tree(&[("just", b"not a dir\n")]);
    assert!(matches!(format_error(file.path()), FormatError::NoJustDir));
}

#[test]
fn missing_repo_just_is_a_format_error() {
    let dir = tree(&[("just/other.just", b"x\n")]);
    match format_error(dir.path()) {
        FormatError::MissingRepoJust(repo) => assert_eq!(repo, "tool"),
        other => panic!("{other}"),
    }
}

#[test]
fn bad_entries_under_just_are_format_errors() {
    let sub = tree(&[("just/tool.just", b"x\n"), ("just/sub/a.just", b"x\n")]);
    assert!(matches!(format_error(sub.path()), FormatError::NotAFile(n) if n == "sub"));

    let ext = tree(&[("just/tool.just", b"x\n"), ("just/README.md", b"x\n")]);
    assert!(matches!(format_error(ext.path()), FormatError::NotJustFile(n) if n == "README.md"));

    let bad = tree(&[("just/tool.just", b"x\n"), ("just/9bad.just", b"x\n")]);
    assert!(
        matches!(format_error(bad.path()), FormatError::InvalidNamespace(n) if n == "9bad.just")
    );

    let link = tree(&[("just/tool.just", b"x\n")]);
    std::os::unix::fs::symlink("tool.just", link.path().join("just/alias.just")).unwrap();
    assert!(matches!(format_error(link.path()), FormatError::NotAFile(n) if n == "alias.just"));
}

#[test]
fn invalid_repo_name_is_rejected() {
    let dir = staged_tree();
    let err = run(dir.path(), "../tool", &ok_digests(), &Taken::new(), None).unwrap_err();
    assert!(matches!(err, Error::InvalidRepo(_)), "{err}");
}

#[test]
fn namespace_names() {
    for ok in ["a", "_x", "tool", "ros_tools", "a-b", "A9"] {
        assert!(is_namespace(ok), "{ok}");
    }
    for bad in ["", "9a", "-a", "a.b", "a b", "a/b", "é"] {
        assert!(!is_namespace(bad), "{bad}");
    }
}

// ---------------------------------------------------------------------------
// <ns> 撞名：已裝工具、根 justfile 的 recipe 或 module、保留名

fn collisions(err: Error) -> Vec<Collision> {
    assert_eq!(err.message().map(|m| m.code), Some("VK0030"), "{err}");
    match err {
        Error::Collision { repo, collisions } => {
            assert_eq!(repo, "tool");
            collisions
        }
        other => panic!("{other}"),
    }
}

#[test]
fn collision_with_installed_tool() {
    let dir = staged_tree();
    let mut taken = Taken::new();
    taken.tool("other", ["tool_ext", "other"]);
    let err = run(dir.path(), "tool", &ok_digests(), &taken, None).unwrap_err();
    assert_eq!(
        collisions(err),
        [Collision {
            ns: "tool_ext".to_owned(),
            owner: Owner::Tool("other".to_owned()),
        }]
    );
}

#[test]
fn collision_with_root_justfile_recipe_and_module() {
    let dir = staged_tree();
    let mut taken = Taken::new();
    taken.root_recipe("tool").root_module("tool_ext");
    let err = run(dir.path(), "tool", &ok_digests(), &taken, None).unwrap_err();
    assert_eq!(
        collisions(err),
        [
            Collision {
                ns: "tool".to_owned(),
                owner: Owner::RootRecipe,
            },
            Collision {
                ns: "tool_ext".to_owned(),
                owner: Owner::RootModule,
            },
        ]
    );
}

#[test]
fn collision_with_reserved_name() {
    let dir = tree(&[("just/tool.just", b"x\n"), ("just/vendor_kit.just", b"x\n")]);
    let err = run(dir.path(), "tool", &ok_digests(), &Taken::new(), None).unwrap_err();
    assert_eq!(
        collisions(err),
        [Collision {
            ns: RESERVED.to_owned(),
            owner: Owner::Reserved,
        }]
    );
}

#[test]
fn every_collision_is_listed_at_once() {
    let dir = tree(&[
        ("just/tool.just", b"x\n"),
        ("just/a.just", b"x\n"),
        ("just/vendor_kit.just", b"x\n"),
    ]);
    let mut taken = Taken::new();
    taken.tool("other", ["a"]).root_module("tool");
    let err = run(dir.path(), "tool", &ok_digests(), &taken, None).unwrap_err();
    let names: Vec<(String, Owner)> = collisions(err)
        .into_iter()
        .map(|c| (c.ns, c.owner))
        .collect();
    assert_eq!(
        names,
        [
            ("a".to_owned(), Owner::Tool("other".to_owned())),
            ("tool".to_owned(), Owner::RootModule),
            (RESERVED.to_owned(), Owner::Reserved),
        ]
    );
}

#[test]
fn own_installed_namespaces_do_not_collide() {
    let dir = staged_tree();
    let mut taken = Taken::new();
    taken.tool("tool", ["tool", "tool_ext"]);
    assert!(run(dir.path(), "tool", &ok_digests(), &taken, None).is_ok());
}

#[test]
fn installed_namespaces_can_be_read_from_cache() {
    let cache = staged_tree();
    let mut taken = Taken::new();
    taken.tool("other", namespaces(cache.path()).unwrap());
    let dir = tree(&[("just/tool.just", b"x\n")]);
    let err = run(dir.path(), "tool", &ok_digests(), &taken, None).unwrap_err();
    assert_eq!(collisions(err).len(), 1);
}

#[test]
fn owner_fills_vk0030_owner() {
    assert_eq!(Owner::Tool("other".to_owned()).to_string(), "other");
    assert_eq!(Owner::Reserved.to_string(), "vendor_kit");
    assert!(Owner::RootRecipe.to_string().contains("recipe"));
    assert!(Owner::RootModule.to_string().contains("module"));
}

// ---------------------------------------------------------------------------
// 已裝工具的 cache/<repo>/（N4）

#[test]
fn cached_namespaces_reads_an_installed_cache() {
    let dir = staged_tree();
    let ns = cached_namespaces(dir.path()).unwrap();
    assert_eq!(ns, vec!["tool".to_owned(), "tool_ext".to_owned()]);
}

#[test]
fn cached_namespaces_reports_a_missing_cache_as_missing() {
    let dir = tempfile::tempdir().unwrap();
    let got = cached_namespaces(&dir.path().join("cache/tool"));
    assert!(matches!(got, Err(CacheError::Missing)), "{got:?}");
}

#[test]
fn cached_namespaces_keeps_the_reason_of_a_broken_cache() {
    // cache/<repo>/ 在，但 just/ 是一般檔：不是「還沒 sync」，保留實際原因。
    let dir = tree(&[("just", b"not a dir")]);
    let got = cached_namespaces(dir.path());
    match got {
        Err(CacheError::Unreadable(FormatError::NoJustDir)) => {}
        other => panic!("{other:?}"),
    }
    // cache/<repo> 本身是一般檔。
    let file = tree(&[("tool", b"x")]);
    let got = cached_namespaces(&file.path().join("tool"));
    assert!(matches!(got, Err(CacheError::Unreadable(_))), "{got:?}");
}

#[test]
fn cache_check_lists_every_missing_tool_in_one_reason_and_each_broken_one_apart() {
    let mut check = CacheCheck::default();
    assert!(check.is_empty());
    check.push("alpha", CacheError::Missing);
    check.push("beta", CacheError::Unreadable(FormatError::NoJustDir));
    check.push("gamma", CacheError::Missing);
    assert!(!check.is_empty());
    assert_eq!(
        check.reasons(),
        vec![
            format!(
                "the cache of installed tools is missing: .vendor_kit/cache/alpha/, \
                 .vendor_kit/cache/gamma/; run just vendor_kit sync first; {DRAFT_CACHE_MISSING}"
            ),
            format!(
                "the cache of installed tool beta (.vendor_kit/cache/beta/) cannot be read: \
                 dist has no just/ directory; {DRAFT_CACHE_UNREADABLE}"
            ),
        ]
    );
}
