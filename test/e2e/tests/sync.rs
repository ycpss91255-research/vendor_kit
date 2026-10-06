//! `sync`（04 sync 節、03 輸出）：經假的啟動器跑完整的 `sync`。
//!
//! 每個測試在暫存目錄建好安裝目錄與 session 的 `ctl/`、`in/`，以 [`MOUNT_PREFIX_ENV`] 讓引擎把它們
//! 當成 `/vk/root`、`/vk/ctl`、`/vk/in`；假啟動器在背景回 inspect、pull 與 extract。
//! 工具有兩個（`tool` 交付兩個 `<ns>`、`other` 一個），`tool` 的 image 一開始不在本機，要先 pull。
//! 安裝目錄裡放好跟這一版引擎一致的薄殼，引擎以測試用的 [`shell::RELEASE_DIR_ENV`] 從 fixture 目錄讀模板
//! （[`e2e::shell`]）。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::collections::BTreeSet;
use std::fs;
use std::path::Path;
use std::sync::{Arc, Mutex};

use assert_cmd::Command;
use e2e::launcher::{self, Mounts, Reply, Request, Seen};
use e2e::{MOUNT_PREFIX_ENV, VERSION, shell, vendor_kit_bin};
use snapbox::assert_data_eq;

const RUN_ID: &str = "r1";
const HOST_ROOT: &str = "/srv/proj";
const RUN_LOG: &str = ".vendor_kit/log/r1.jsonl";
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
const TOOL_DIGEST: &str = "sha256:2222222222222222222222222222222222222222222222222222222222222222";
const OTHER_DIGEST: &str =
    "sha256:3333333333333333333333333333333333333333333333333333333333333333";
const TOOL_JUST: &str = "hello:\n    echo hi\n";

fn tool_pinned() -> String {
    format!("ghcr.io/acme/tool@{TOOL_DIGEST}")
}

fn other_pinned() -> String {
    format!("ghcr.io/acme/other@{OTHER_DIGEST}")
}

/// 出貨輸入的 fixture 目錄。
fn release_dir(m: &Mounts) -> std::path::PathBuf {
    m.prefix.join("release")
}

/// 全新 checkout：`version.toml` 有兩個工具、跟這一版引擎一致的薄殼，沒有 `cache/`、`gen/`。
fn checkout(m: &Mounts) {
    let vk = m.root.join(".vendor_kit");
    fs::create_dir_all(vk.join("log")).unwrap();
    shell::install(&m.root, VERSION).unwrap();
    shell::release(&release_dir(m)).unwrap();
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\n\
             other = \"ghcr.io/acme/other:v2.0.0@{OTHER_DIGEST}\"\n\
             tool = \"ghcr.io/acme/tool:v1.2.0@{TOOL_DIGEST}\"\n"
        ),
    )
    .unwrap();
    fs::write(
        m.root.join("justfile"),
        "import '.vendor_kit/entry.just'\n\nbuild:\n    echo build\n",
    )
    .unwrap();
}

/// 工具內容：`just/<ns>.just` 各一檔，外加一個一般檔。
fn tool_content(dir: &Path, namespaces: &[&str]) {
    fs::create_dir_all(dir.join("just")).unwrap();
    for ns in namespaces {
        fs::write(dir.join("just").join(format!("{ns}.just")), TOOL_JUST).unwrap();
    }
    fs::create_dir_all(dir.join("share")).unwrap();
    fs::write(dir.join("share/readme.txt"), "tool files\n").unwrap();
}

/// 假啟動器：`local` 是本機已有的 image（pinned 引用）；inspect 本機沒有的回 failed，pull 之後才有。
/// image ID 就是 digest。
/// `header` 是 `vk-resolve/<P> r1`。
fn launcher(
    m: &Mounts,
    header: &str,
    local: Arc<Mutex<BTreeSet<String>>>,
) -> std::thread::JoinHandle<Seen> {
    let (ctl, inbox) = (m.ctl.clone(), m.inbox.clone());
    launcher::serve(&m.ctl, header, move |req: &Request| match req.op.as_str() {
        "inspect" if !local.lock().unwrap().contains(&req.args[0]) => Reply::Failed(1),
        "inspect" => {
            let reference = &req.args[0];
            let (_, digest) = reference.split_once('@').unwrap();
            fs::write(
                ctl.join(format!("res.{}.out", req.seq)),
                launcher::inspect_json(digest, &[reference.as_str()]),
            )
            .unwrap();
            Reply::Ok
        }
        "pull" => {
            local.lock().unwrap().insert(req.args[0].clone());
            Reply::Ok
        }
        // 啟動器不收已存在的 slot（launcher/launch.sh 的 vk_launch_extract）。
        "extract" if inbox.join(&req.args[1]).exists() => Reply::Failed(1),
        "extract" if req.args[0] == TOOL_DIGEST => {
            tool_content(&inbox.join(&req.args[1]), &["tool", "tool-extra"]);
            Reply::Ok
        }
        "extract" if req.args[0] == OTHER_DIGEST => {
            tool_content(&inbox.join(&req.args[1]), &["other"]);
            Reply::Ok
        }
        _ => Reply::Failed(1),
    })
}

/// 跑一次 `sync`。每次執行的 session 目錄與執行紀錄都是新的（啟動器建好空的執行紀錄）。
fn run(m: &Mounts, local: &Arc<Mutex<BTreeSet<String>>>) -> (i32, String, String, Seen) {
    run_at(m, 1, local)
}

/// [`run`]，薄殼的介面版是 `protocol`。
fn run_at(
    m: &Mounts,
    protocol: u32,
    local: &Arc<Mutex<BTreeSet<String>>>,
) -> (i32, String, String, Seen) {
    for d in [&m.ctl, &m.inbox] {
        fs::remove_dir_all(d).unwrap();
        fs::create_dir_all(d).unwrap();
    }
    fs::write(m.root.join(RUN_LOG), "").unwrap();
    let peer = launcher(
        m,
        &format!("vk-resolve/{protocol} {RUN_ID}"),
        Arc::clone(local),
    );
    let protocol = protocol.to_string();
    let args = [
        "--protocol",
        protocol.as_str(),
        "--run-id",
        RUN_ID,
        "--host-root",
        HOST_ROOT,
        "--host-cwd",
        HOST_ROOT,
        "--run-log",
        RUN_LOG,
        "--tty",
        "000",
        "--no-color",
        "1",
        "--",
        "sync",
    ];
    let out = Command::new(vendor_kit_bin().unwrap())
        .args(args)
        .env(MOUNT_PREFIX_ENV, &m.prefix)
        .env(shell::RELEASE_DIR_ENV, release_dir(m))
        .write_stdin("")
        .output()
        .unwrap();
    let seen = peer.join().unwrap();
    (
        out.status.code().unwrap(),
        String::from_utf8(out.stdout).unwrap(),
        String::from_utf8(out.stderr).unwrap(),
        seen,
    )
}

/// 執行紀錄裡依序的事件名。
fn events(m: &Mounts) -> Vec<String> {
    fs::read_to_string(m.root.join(RUN_LOG))
        .unwrap()
        .lines()
        .map(|l| {
            let rest = l.split_once("\"event_name\":\"").unwrap().1;
            rest.split_once('"').unwrap().0.to_owned()
        })
        .collect()
}

/// `.vendor_kit/` 下所有路徑（相對、排序），不含執行紀錄。
fn vk_tree(m: &Mounts) -> Vec<String> {
    fn walk(root: &Path, dir: &Path, out: &mut Vec<String>) {
        for entry in fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            out.push(path.strip_prefix(root).unwrap().display().to_string());
            if path.is_dir() {
                walk(root, &path, out);
            }
        }
    }
    let root = m.root.join(".vendor_kit");
    let mut out = Vec::new();
    walk(&root, &root, &mut out);
    out.retain(|p| !p.starts_with("log"));
    out.sort();
    out
}

/// `.vendor_kit/` 下每個一般檔的內容（不含執行紀錄）。
fn vk_contents(m: &Mounts) -> Vec<(String, Vec<u8>)> {
    let vk = m.root.join(".vendor_kit");
    vk_tree(m)
        .into_iter()
        .filter(|p| vk.join(p).is_file())
        .map(|p| {
            let bytes = fs::read(vk.join(&p)).unwrap();
            (p, bytes)
        })
        .collect()
}

const SYNCED_TREE: [&str; 20] = [
    ".gitignore",
    "cache",
    "cache/other",
    "cache/other.stamp.toml",
    "cache/other/just",
    "cache/other/just/other.just",
    "cache/other/share",
    "cache/other/share/readme.txt",
    "cache/tool",
    "cache/tool.stamp.toml",
    "cache/tool/just",
    "cache/tool/just/tool-extra.just",
    "cache/tool/just/tool.just",
    "cache/tool/share",
    "cache/tool/share/readme.txt",
    "entry.just",
    "gen",
    "gen/tools.just",
    "vendor.just",
    "version.toml",
];

#[test]
fn fresh_checkout_then_resync_without_changes() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    let lock_before = fs::read(m.root.join(".vendor_kit/version.toml")).unwrap();
    let local = Arc::new(Mutex::new(BTreeSet::from([other_pinned()])));

    let (code, stdout, stderr, seen) = run(&m, &local);

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Fetched other v2.0.0 (ghcr.io/acme/other:v2.0.0@sha256:3333333333333333333333333333333333333333333333333333333333333333).
Fetched tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).
Updated .vendor_kit/gen/tools.just.

"#]]
    );
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        [
            format!("inspect {}", other_pinned()),
            format!("extract {OTHER_DIGEST} tool1"),
            format!("inspect {}", tool_pinned()),
            format!("pull {}", tool_pinned()),
            format!("inspect {}", tool_pinned()),
            format!("extract {TOOL_DIGEST} tool2"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));

    let vk = m.root.join(".vendor_kit");
    assert_eq!(vk_tree(&m), SYNCED_TREE);
    assert_data_eq!(
        fs::read_to_string(vk.join("gen/tools.just")).unwrap(),
        snapbox::str![[r#"
mod? other '../cache/other/just/other.just'
mod? tool '../cache/tool/just/tool.just'
mod? tool-extra '../cache/tool/just/tool-extra.just'

"#]]
    );
    assert_eq!(
        fs::read_to_string(vk.join("cache/tool/just/tool.just")).unwrap(),
        TOOL_JUST
    );
    let stamp = fs::read_to_string(vk.join("cache/tool.stamp.toml")).unwrap();
    assert!(
        stamp.contains(&format!(
            "version = \"ghcr.io/acme/tool:v1.2.0@{TOOL_DIGEST}\""
        )),
        "{stamp}"
    );
    // sync 不改追蹤檔：版本鎖定行逐位元組不變，也沒有鎖定行的事件。sync 是唯讀 recipe，不建進度檔，
    // 所以沒有 progress_removed（SYNCED_TREE 裡也沒有 .tmp.sync.*）。
    assert_eq!(fs::read(vk.join("version.toml")).unwrap(), lock_before);
    assert_eq!(
        events(&m),
        ["engine_started", "writes_started", "engine_finished",]
    );

    // 已同步再 sync：不取件、不寫檔、stdout 不印。
    let before = vk_contents(&m);
    let (code, stdout, stderr, seen) = run(&m, &local);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(stderr, "");
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 0\n"));
    assert_eq!(vk_contents(&m), before);
    assert_eq!(events(&m), ["engine_started", "engine_finished"]);
}

/// 救援路徑跨介面版可用（ADR-0008:26、#372 N61）：薄殼的 P 超出引擎的區間（這一版引擎只收 P=1），
/// `sync` 照常跑完，往返與 `done` 都以薄殼的 P 回應。
#[test]
fn sync_still_works_when_the_shell_protocol_is_outside_the_engine_range() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    let local = Arc::new(Mutex::new(BTreeSet::from([other_pinned()])));

    let (code, _, stderr, seen) = run_at(&m, 2, &local);

    assert_eq!(code, 0, "stderr: {stderr}");
    assert_data_eq!(stderr, "");
    assert_eq!(
        seen.requests,
        [
            format!("inspect {}", other_pinned()),
            format!("extract {OTHER_DIGEST} tool1"),
            format!("inspect {}", tool_pinned()),
            format!("pull {}", tool_pinned()),
            format!("inspect {}", tool_pinned()),
            format!("extract {TOOL_DIGEST} tool2"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/2 r1 done 0\n"));
    assert_eq!(vk_tree(&m), SYNCED_TREE);
}

/// 薄殼被改過一個位元組（ADR-0007 驗收案例）：在逐工具處理前回 VK0006，不取件、不寫檔。
#[test]
fn a_modified_shell_is_vk0006_before_any_fetch() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    let entry = m.root.join(".vendor_kit/entry.just");
    let mut bytes = fs::read(&entry).unwrap();
    let last = bytes.len() - 2;
    bytes[last] ^= 0x01;
    fs::write(&entry, bytes).unwrap();
    let before = vk_contents(&m);
    let local = Arc::new(Mutex::new(BTreeSet::from([other_pinned()])));

    let (code, stdout, stderr, seen) = run(&m, &local);

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: error[VK0006]: Shell files do not match this engine version's templates: .vendor_kit/entry.just (modified). No shell files were regenerated. Review the following differences; download bootstrap.sh again from the Release, run chmod +x bootstrap.sh, then run ./bootstrap.sh --repair in the install directory.

"#]]
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 2\n"));
    assert_eq!(vk_contents(&m), before);
}

/// 引擎沒有薄殼模板可比（image 沒出貨）：VK0056，不取件、不寫檔。
#[test]
fn sync_without_shell_templates_is_vk0056() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    fs::remove_dir_all(release_dir(&m)).unwrap();
    let before = vk_contents(&m);
    let local = Arc::new(Mutex::new(BTreeSet::from([other_pinned()])));

    let (code, stdout, stderr, seen) = run(&m, &local);

    assert_eq!(code, 2, "stderr: {stderr}");
    assert_data_eq!(stdout, "");
    assert!(
        stderr.starts_with(
            "vendor_kit: error[VK0056]: Internal vendor_kit error: \
             sync without the shell templates, which this engine image does not ship"
        ),
        "{stderr}"
    );
    assert!(seen.requests.is_empty(), "{:?}", seen.requests);
    assert_eq!(vk_contents(&m), before);
}

#[test]
fn modified_cache_is_refetched_with_a_warning() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    let local = Arc::new(Mutex::new(BTreeSet::from([tool_pinned(), other_pinned()])));
    let (code, _, stderr, _) = run(&m, &local);
    assert_eq!(code, 0, "stderr: {stderr}");
    let synced = vk_contents(&m);

    // 改一個檔、多放一個檔（04 sync 表：判定檔案集合與逐檔指紋，包括多出的檔案）。
    let cache = m.root.join(".vendor_kit/cache/tool");
    fs::write(cache.join("just/tool.just"), "edited:\n    echo edited\n").unwrap();
    fs::write(cache.join("share/extra.txt"), "extra\n").unwrap();

    let (code, stdout, stderr, seen) = run(&m, &local);

    assert_eq!(code, 1, "stderr: {stderr}");
    assert_data_eq!(
        stdout,
        snapbox::str![[r#"
Fetched tool v1.2.0 (ghcr.io/acme/tool:v1.2.0@sha256:2222222222222222222222222222222222222222222222222222222222222222).

"#]]
    );
    assert_data_eq!(
        stderr,
        snapbox::str![[r#"
vendor_kit: warn[VK0015]: The file set or per-file digests in cache/ for tool did not match; refetched according to the lock version line.

"#]]
    );
    assert_eq!(
        seen.requests,
        [
            format!("inspect {}", tool_pinned()),
            format!("extract {TOOL_DIGEST} tool1"),
        ]
    );
    assert_eq!(seen.done.as_deref(), Some("vk-resolve/1 r1 done 1\n"));
    // 內容回到版本鎖定行那一版：每個檔逐位元組與第一次同步後相同，多出的檔已不在。
    assert_eq!(vk_contents(&m), synced);
    assert_eq!(
        events(&m),
        [
            "engine_started",
            "writes_started",
            "diagnostic_emitted",
            "engine_finished",
        ]
    );
}

/// `cache/<repo>/` 不在時（prune、手動刪除、sync 中斷），`gen/tools.just` 每行都是 `mod?`，just 仍解析得了，
/// 救援用的 `just vendor_kit sync` 跑得起來（ADR-0007）。主機有 `just` 就實際解析一次；
/// image 的 test stage 不帶 `just`，那裡只比對字面內容（各版 just 的實測在驗收矩陣，ADR-0011）。
#[test]
fn entry_file_still_parses_when_a_tool_cache_is_missing() {
    let tmp = tempfile::tempdir().unwrap();
    let m = Mounts::create(tmp.path());
    checkout(&m);
    let local = Arc::new(Mutex::new(BTreeSet::from([other_pinned()])));
    let (code, _, stderr, _) = run(&m, &local);
    assert_eq!(code, 0, "stderr: {stderr}");

    let vk = m.root.join(".vendor_kit");
    fs::remove_dir_all(vk.join("cache/tool")).unwrap();
    let gen_file = vk.join("gen/tools.just");
    let text = fs::read_to_string(&gen_file).unwrap();
    assert_data_eq!(
        text.as_str(),
        snapbox::str![[r#"
mod? other '../cache/other/just/other.just'
mod? tool '../cache/tool/just/tool.just'
mod? tool-extra '../cache/tool/just/tool-extra.just'

"#]]
    );
    assert!(text.lines().all(|l| l.starts_with("mod? ")), "{text}");

    let parsed = match std::process::Command::new("just")
        .arg("--justfile")
        .arg(&gen_file)
        .arg("--working-directory")
        .arg(vk.join("gen"))
        .arg("--summary")
        .output()
    {
        Ok(out) => out,
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
            eprintln!("just not on PATH; checked the literal content only");
            return;
        }
        Err(e) => panic!("{e}"),
    };
    assert!(
        parsed.status.success(),
        "{}",
        String::from_utf8_lossy(&parsed.stderr)
    );
    assert_eq!(String::from_utf8(parsed.stdout).unwrap(), "other::hello\n");
}
