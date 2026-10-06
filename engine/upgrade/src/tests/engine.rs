//! `upgrade --engine` 的兩段（[`crate::engine`]）：第一段由假啟動器回帶 LABEL 的 inspect 與 pull，假 registry 回
//! `tags/list` 與 HEAD manifest；第二段不送 op，薄殼模板與要問的事直接給。

use super::online::{Registry, public};
use super::*;
use crate::engine::{self, ENGINE_REPO};
use shell::Shell;

/// 假 registry 裡引擎 image 的路徑（[`ENGINE_REPO`] 去掉 `ghcr.io/`）。
const ENGINE_PATH: &str = "ycpss91255-research/vendor_kit";
const TARGET_TAG: &str = "v1.2.0";

fn target_ref() -> String {
    format!("{ENGINE_REPO}:{TARGET_TAG}")
}

fn target_locked() -> String {
    format!("{}@{DIGEST}", target_ref())
}

fn pinned() -> String {
    format!("{ENGINE_REPO}@{DIGEST}")
}

/// 目標引擎 v1.2.0：介面版 [1, 2]、檔案版上限 1。
const LABELS: &str = r#""vendor_kit.protocol.floor":"1","vendor_kit.protocol.current":"2","vendor_kit.schema.max":"1","org.opencontainers.image.version":"v1.2.0""#;

const TARGET: Script = Script {
    namespaces: &[],
    fail: None,
    digests: &[
        "ghcr.io/ycpss91255-research/vendor_kit@sha256:2222222222222222222222222222222222222222222222222222222222222222",
    ],
    local: true,
    labels: LABELS,
};

/// 一次執行的其餘輸入。
struct Opts<'a> {
    run_id: &'a str,
    templates: Option<&'a engine::ShellTemplates>,
    questions: &'a [&'a str],
    interactive: bool,
    stdin: &'a str,
}

const OPTS: Opts<'static> = Opts {
    run_id: "r1",
    templates: None,
    questions: &[],
    interactive: false,
    stdin: "",
};

/// 跑一次 `upgrade --engine`：`argv` 是 `just vendor_kit` 之後的參數，tag 與 `-y` 從裡面取。
fn run_engine(fx: &Fx, argv: &[&str], registry: &Client) -> Out {
    run_engine_with(fx, argv, registry, &OPTS)
}

fn run_engine_with(fx: &Fx, argv: &[&str], registry: &Client, opts: &Opts) -> Out {
    let tag = argv
        .iter()
        .find_map(|a| a.strip_prefix("--engine="))
        .map(|t| Tag::parse(t).unwrap());
    let req = engine::Request {
        tag,
        yes: argv.contains(&"-y"),
        shell_templates: opts.templates,
    };
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    fx.assert_fresh_session();
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdin = Cursor::new(opts.stdin.as_bytes().to_vec());
    let mut stdout = Vec::new();
    let shared = Shared::default();
    let mut prompt = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
    let mut log = runlog::Writer::new(
        Vec::new(),
        runlog::Header {
            version: WRITTEN_BY.to_owned(),
            component: runlog::Component::Engine,
            invocation_id: opts.run_id.to_owned(),
        },
    );
    let questions: Vec<String> = opts.questions.iter().map(|q| (*q).to_owned()).collect();
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(1),
            registry,
            tty: tty(opts.interactive),
            argv: &argv,
            run_id: opts.run_id,
            written_by: WRITTEN_BY,
            stdin: &mut stdin,
            stdout: &mut stdout,
            prompt: &mut prompt,
            diags: &mut diags,
            log: &mut log,
        };
        engine::run_with(&req, &mut env, &|| questions.clone())
    };
    Out {
        code,
        stdout: String::from_utf8(stdout).unwrap(),
        stderr: shared.text(),
        log: String::from_utf8(log.into_inner()).unwrap(),
    }
}

fn events(out: &Out) -> Vec<&str> {
    out.log
        .lines()
        .map(|l| {
            let rest = l.split_once("\"event_name\":\"").unwrap().1;
            rest.split_once('"').unwrap().0
        })
        .collect()
}

/// 第一段做完：引擎鎖定行與介面版列表換成目標，工具鎖定行不動，進度檔留著（記目標與原指令），以 VK0023 停下。
fn assert_switched(fx: &Fx, out: &Out, argv: &[&str], again: &str) {
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert_eq!(out.stdout, "");
    assert_eq!(
        out.stderr,
        format!(
            "vendor_kit: error[VK0023]: Engine {TARGET_TAG} is now installed. Run again: {again}\n"
        )
    );
    assert_eq!(
        fx.lock_text(),
        format!(
            "vendor_kit = \"{}\"\nvendor_kit_protocols = \"1 2\"\nschema = 1\nwritten_by = \"{WRITTEN_BY}\"\n\n[tools]\ntool = \"{OLD}\"\n",
            target_locked()
        )
    );
    let entries = progress::find(&fx.dir).unwrap();
    assert_eq!(entries.len(), 1);
    let p = entries[0].load().unwrap();
    assert_eq!(p.verb(), VERB);
    assert_eq!(p.id(), "r1");
    assert_eq!(p.command(), argv);
    assert_eq!(table::field(&p, table::TARGET), Some(table::ENGINE_TARGET));
    assert_eq!(
        table::field(&p, table::IMAGE),
        Some(target_locked().as_str())
    );
    assert_eq!(
        events(out),
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written"
        ]
    );
    // 工具內容與入口檔都不動。
    assert_eq!(
        fs::read_to_string(fx.dir.cache_dir().join("tool/just/tool.just")).unwrap(),
        "old:\n"
    );
    assert!(!fx.dir.gen_dir().join("tools.just").exists());
}

fn assert_rescue_only(ops: &[String]) {
    for line in ops {
        let op = line.split(' ').next().unwrap();
        assert!(plan::RESCUE_OPS.contains(&op), "{line}");
    }
}

#[test]
fn with_a_local_tag_the_lock_line_is_switched_and_vk0023_asks_to_run_again() {
    let fx = Fx::new();
    let peer = Peer::start(&fx, TARGET);
    let argv = ["upgrade", "--engine=v1.2.0", "-y"];
    let out = run_engine(&fx, &argv, &unused_registry());
    let ops = peer.finish();
    assert_eq!(ops, [format!("inspect {}", target_ref())]);
    assert_rescue_only(&ops);
    assert_switched(
        &fx,
        &out,
        &argv,
        "just vendor_kit upgrade --engine=v1.2.0 -y",
    );
}

#[test]
fn a_tag_that_is_not_local_is_pulled_by_digest() {
    let fx = Fx::new();
    let registry = Registry::start(ENGINE_PATH, public(&["v1.2.0"]));
    let peer = Peer::start(
        &fx,
        Script {
            local: false,
            ..TARGET
        },
    );
    let argv = ["upgrade", "--engine=v1.2.0"];
    let out = run_engine(&fx, &argv, &registry.client());
    let ops = peer.finish();
    assert_eq!(
        ops,
        [
            format!("inspect {}", target_ref()),
            format!("pull {}", pinned()),
            format!("inspect {}", pinned()),
        ]
    );
    assert_rescue_only(&ops);
    // 指定 tag 不列 tag，只取那個 tag 的 digest。
    assert_eq!(
        registry.requests(),
        [format!("HEAD /v2/{ENGINE_PATH}/manifests/v1.2.0")]
    );
    assert_switched(&fx, &out, &argv, "just vendor_kit upgrade --engine=v1.2.0");
}

#[test]
fn without_a_tag_the_latest_engine_in_the_registry_is_the_target() {
    let fx = Fx::new();
    let registry = Registry::start(
        ENGINE_PATH,
        public(&["v1.0.0", "v1.2.0", "v1.1.9", "latest"]),
    );
    let peer = Peer::start(&fx, TARGET);
    let argv = ["upgrade", "--engine"];
    let out = run_engine(&fx, &argv, &registry.client());
    let ops = peer.finish();
    assert_eq!(ops, [format!("inspect {}", target_ref())]);
    assert_eq!(
        registry.requests(),
        [
            format!("GET /v2/{ENGINE_PATH}/tags/list?n=100"),
            format!("HEAD /v2/{ENGINE_PATH}/manifests/v1.2.0"),
        ]
    );
    // 原指令照原樣，不補上解析出來的 tag。
    assert_switched(&fx, &out, &argv, "just vendor_kit upgrade --engine");
}

#[test]
fn a_private_engine_repository_is_vk0055_not_vk0001() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let mut repo = public(&["v1.2.0"]);
    repo.private = true;
    let registry = Registry::start(ENGINE_PATH, repo);
    let peer = Peer::start(&fx, TARGET);
    let out = run_engine(&fx, &["upgrade", "--engine"], &registry.client());
    assert!(peer.finish().is_empty());
    assert_eq!(out.code, 2);
    assert!(
        out.stderr.starts_with(&format!(
            "vendor_kit: error[VK0055]: Cannot access {ENGINE_REPO} for vendor_kit: "
        )),
        "{}",
        out.stderr
    );
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn a_target_that_cannot_read_the_existing_files_is_vk0007_without_writes() {
    let fx = Fx::new();
    // 某個 VK 檔的檔案版（2）高於目標引擎的上限（1）。
    fs::write(
        stamp::tool_file(&fx.dir, "tool"),
        "schema = 2\nwritten_by = \"v9.0.0\"\n",
    )
    .unwrap();
    let before = fx.snapshot();
    let peer = Peer::start(&fx, TARGET);
    let out = run_engine(&fx, &["upgrade", "--engine=v1.2.0"], &unused_registry());
    peer.finish();
    assert_eq!(out.code, 3, "{}", out.stderr);
    assert_eq!(
        out.stderr,
        "vendor_kit: fatal[VK0007]: Target engine v1.2.0 (interface version 2, schema version 1) cannot read the existing files (schema version 2) without loss. No files were modified except the run log. Specify a version that can read schema version 2: just vendor_kit upgrade --engine=<tag>\n"
    );
    assert_eq!(fx.snapshot(), before);
    assert_eq!(out.log, "");
}

// ---- 第二段 ----

/// 第二段的引擎就是這個測試的引擎（[`WRITTEN_BY`]）：目標 tag 與它的 LABEL。
const SELF_LABELS: &str = r#""vendor_kit.protocol.floor":"1","vendor_kit.protocol.current":"1","vendor_kit.schema.max":"1","org.opencontainers.image.version":"v0.0.0""#;

const SELF_TARGET: Script = Script {
    labels: SELF_LABELS,
    ..TARGET
};

fn self_locked() -> String {
    format!("{ENGINE_REPO}:{WRITTEN_BY}@{DIGEST}")
}

/// 測試用的薄殼模板（順序同 `layout::SHELL_FILES`）。
fn templates() -> engine::ShellTemplates {
    [
        b"# entry\n".to_vec(),
        b"# vendor\n".to_vec(),
        b"# log\n".to_vec(),
        b"cache/\n".to_vec(),
    ]
}

/// 本引擎產生的薄殼四檔。
fn rendered() -> Shell {
    let t = templates();
    Shell::render(
        compat::THIS.current_protocol,
        WRITTEN_BY,
        [&t[0][..], &t[1][..], &t[2][..], &t[3][..]],
    )
    .unwrap()
}

/// 第一段換到本引擎（v1.0.0 → v0.0.0，檔案版上限相同，降版照樣過），以 `argv` 停在 VK0023。
fn first_stage(fx: &Fx, argv: &[&str]) {
    let peer = Peer::start(fx, SELF_TARGET);
    let out = run_engine(fx, argv, &unused_registry());
    peer.finish();
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert!(out.stderr.contains("error[VK0023]"), "{}", out.stderr);
    fx.new_session();
}

/// 第二段做完：薄殼四檔是本引擎的、`gen/.stamp` 是鎖定行的值、介面版列表是本引擎的，沒有進度檔。
fn assert_completed(fx: &Fx, out: &Out, wrote: &[&str]) {
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stderr, "");
    let mut expected: String = wrote
        .iter()
        .map(|n| format!("Wrote .vendor_kit/{n}\n"))
        .collect();
    expected.push_str(&format!(
        "Completed the engine upgrade to {WRITTEN_BY} ({}).\n",
        self_locked()
    ));
    assert_eq!(out.stdout, expected);
    let report = rendered().check(&fx.dir).unwrap();
    assert!(report.is_consistent(), "{report:?}");
    assert_eq!(
        fs::read_to_string(fx.dir.stamp()).unwrap(),
        format!("{}\n", self_locked())
    );
    assert_eq!(
        fx.lock_text(),
        format!(
            "vendor_kit = \"{}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"{WRITTEN_BY}\"\n\n[tools]\ntool = \"{OLD}\"\n",
            self_locked()
        )
    );
    assert!(progress::find(&fx.dir).unwrap().is_empty());
    assert_eq!(
        events(out),
        [
            "writes_started",
            "lock_line_write_started",
            "lock_line_written",
            "progress_removed",
        ]
    );
}

fn second_opts<'a>(run_id: &'a str, t: &'a engine::ShellTemplates) -> Opts<'a> {
    Opts {
        run_id,
        templates: Some(t),
        ..OPTS
    }
}

#[test]
fn the_rerun_completes_the_second_stage_without_any_docker_action() {
    let fx = Fx::new();
    let argv = ["upgrade", "--engine=v0.0.0", "-y"];
    first_stage(&fx, &argv);
    let t = templates();
    // 沒有假啟動器：第二段送任何 op 都會卡住。
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r2", &t));
    assert_completed(
        &fx,
        &out,
        &["entry.just", "vendor.just", "log.sh", ".gitignore"],
    );
    // 工具內容與入口檔都不動。
    assert_eq!(
        fs::read_to_string(fx.dir.cache_dir().join("tool/just/tool.just")).unwrap(),
        "old:\n"
    );
    assert!(!fx.dir.gen_dir().join("tools.just").exists());

    // 再跑一次：都已是這一版，說明未變更，不建進度檔、不寫任何檔。
    let before = fx.snapshot();
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r3", &t));
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(
        out.stdout,
        "vendor_kit is already at v0.0.0; no changes were made.\n"
    );
    assert_eq!(out.log, "");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn without_a_tag_the_rerun_does_not_ask_the_registry() {
    let fx = Fx::new();
    first_stage(&fx, &["upgrade", "--engine=v0.0.0"]);
    let t = templates();
    let out = run_engine_with(
        &fx,
        &["upgrade", "--engine"],
        &unused_registry(),
        &second_opts("r2", &t),
    );
    assert_completed(
        &fx,
        &out,
        &["entry.just", "vendor.just", "log.sh", ".gitignore"],
    );
}

#[test]
fn only_mismatched_shell_files_are_rewritten() {
    let fx = Fx::new();
    let shell = rendered();
    shell.write(&fx.dir).unwrap();
    // log.sh 是別版引擎的模板，.gitignore 被改過。
    let t = templates();
    let other = Shell::render(
        compat::THIS.current_protocol,
        "v9.9.9",
        [&t[0][..], &t[1][..], &t[2][..], &t[3][..]],
    )
    .unwrap();
    fs::write(
        fx.dir.vk_dir().join("log.sh"),
        other.file("log.sh").unwrap(),
    )
    .unwrap();
    fs::write(fx.dir.vk_dir().join(".gitignore"), "edited\n").unwrap();
    let argv = ["upgrade", "--engine=v0.0.0", "-y"];
    first_stage(&fx, &argv);
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r2", &t));
    assert_completed(&fx, &out, &["log.sh", ".gitignore"]);
}

/// N21：鎖定行已是目標版、沒有進度檔，但薄殼還是舊的：直接做第二段，不回「已是最新」。
#[test]
fn a_lock_line_already_at_the_target_with_old_shell_files_does_the_second_stage() {
    for argv in [
        &["upgrade", "--engine=v0.0.0"][..],
        &["upgrade", "--engine"][..],
    ] {
        let fx = Fx::new();
        fs::write(
            fx.dir.version_toml(),
            format!(
                "vendor_kit = \"{}\"\nvendor_kit_protocols = \"1\"\nschema = 1\nwritten_by = \"v0.0.0\"\n\n[tools]\ntool = \"{OLD}\"\n",
                self_locked()
            ),
        )
        .unwrap();
        let registry = Registry::start(ENGINE_PATH, public(&["v0.0.0"]));
        let t = templates();
        let out = run_engine_with(&fx, argv, &registry.client(), &second_opts("r2", &t));
        assert_completed(
            &fx,
            &out,
            &["entry.just", "vendor.just", "log.sh", ".gitignore"],
        );
        // 帶 tag 不連 registry；不帶 tag 只列 tag，不取 digest。
        let listed: Vec<String> = if argv.len() == 2 && argv[1] == "--engine" {
            vec![format!("GET /v2/{ENGINE_PATH}/tags/list?n=100")]
        } else {
            Vec::new()
        };
        assert_eq!(registry.requests(), listed);
    }
}

#[test]
fn answering_no_keeps_the_first_stage() {
    let fx = Fx::new();
    let argv = ["upgrade", "--engine=v0.0.0"];
    first_stage(&fx, &argv);
    let before = fx.snapshot();
    let t = templates();
    let out = run_engine_with(
        &fx,
        &argv,
        &unused_registry(),
        &Opts {
            questions: &["Replace .vendor_kit/config.toml?"],
            interactive: true,
            stdin: "n\n",
            ..second_opts("r2", &t)
        },
    );
    assert_eq!(out.code, 0, "{}", out.stderr);
    assert_eq!(out.stdout, "No changes were made.\n");
    assert!(out.stderr.contains("Replace .vendor_kit/config.toml?"));
    // 鎖定行與第一段的進度檔都還在，沒有任何寫入。
    assert_eq!(fx.snapshot(), before);
    assert_eq!(out.log, "");

    // 不能互動：VK0002，同樣不寫。
    let out = run_engine_with(
        &fx,
        &argv,
        &unused_registry(),
        &Opts {
            questions: &["Replace .vendor_kit/config.toml?"],
            ..second_opts("r3", &t)
        },
    );
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert!(out.stderr.contains("error[VK0002]"), "{}", out.stderr);
    assert_eq!(fx.snapshot(), before);

    // -y：全部同意。
    let out = run_engine_with(
        &fx,
        &["upgrade", "--engine=v0.0.0", "-y"],
        &unused_registry(),
        &Opts {
            questions: &["Replace .vendor_kit/config.toml?"],
            ..second_opts("r4", &t)
        },
    );
    assert_completed(
        &fx,
        &out,
        &["entry.just", "vendor.just", "log.sh", ".gitignore"],
    );
}

/// 第二段中途停下的樣子：第一段（`r1`）與第二段（`r2`）的進度檔都在，薄殼寫了一半，`gen/.stamp` 還沒寫。
#[test]
fn an_interrupted_second_stage_is_completed_by_the_rerun() {
    let fx = Fx::new();
    let argv = ["upgrade", "--engine=v0.0.0", "-y"];
    first_stage(&fx, &argv);
    let vk = fx.dir.vk_dir();
    fs::copy(
        vk.join(".tmp.upgrade.r1.toml"),
        vk.join(".tmp.upgrade.r2.toml"),
    )
    .unwrap();
    let shell = rendered();
    for name in ["entry.just", "vendor.just"] {
        fs::write(vk.join(name), shell.file(name).unwrap()).unwrap();
    }
    let t = templates();
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r3", &t));
    assert_completed(&fx, &out, &["log.sh", ".gitignore"]);
}

#[test]
fn the_second_stage_stops_where_it_cannot_tell_what_to_do() {
    let t = templates();
    let argv = ["upgrade", "--engine=v0.0.0"];

    // 沒有薄殼模板。
    let fx = Fx::new();
    first_stage(&fx, &argv);
    let before = fx.snapshot();
    let out = run_engine_with(
        &fx,
        &argv,
        &unused_registry(),
        &Opts {
            run_id: "r2",
            ..OPTS
        },
    );
    assert_gap(&out, "without the shell templates");
    assert_eq!(fx.snapshot(), before);

    // 帶的 tag 跟版本鎖定行不同。
    let out = run_engine_with(
        &fx,
        &["upgrade", "--engine=v1.2.0"],
        &unused_registry(),
        &second_opts("r2", &t),
    );
    assert_gap(
        &out,
        "upgrade --engine=v1.2.0 while the engine upgrade to v0.0.0 recorded in .vendor_kit/.tmp.upgrade.r1.toml is incomplete",
    );

    // 引擎開著本機覆寫。
    fs::write(
        fx.dir.version_local_toml(),
        "vendor_kit = \"vendor_kit:dev\"\nschema = 1\nwritten_by = \"v0.0.0\"\n",
    )
    .unwrap();
    let before = fx.snapshot();
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r2", &t));
    assert_gap(&out, "while the engine has a local override");
    assert_eq!(fx.snapshot(), before);

    // 這次的 run-id 跟殘留的進度檔撞名。
    fs::remove_file(fx.dir.version_local_toml()).unwrap();
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r1", &t));
    assert_gap_or_internal(&out, "has this run's id r1");
}

#[test]
fn the_second_stage_runs_only_on_the_engine_the_lock_line_names() {
    // 第一段換到 v1.2.0，重跑時起的還是本引擎（v0.0.0）：停下，不寫任何檔。
    let fx = Fx::new();
    let peer = Peer::start(&fx, TARGET);
    let argv = ["upgrade", "--engine=v1.2.0"];
    run_engine(&fx, &argv, &unused_registry());
    peer.finish();
    let before = fx.snapshot();
    fx.new_session();
    let t = templates();
    let out = run_engine_with(&fx, &argv, &unused_registry(), &second_opts("r2", &t));
    assert_gap_or_internal(
        &out,
        "this engine is v0.0.0, but the engine lock version line names v1.2.0",
    );
    assert_eq!(fx.snapshot(), before);

    // 鎖定行跟目標同 tag、但不是本引擎：同樣停下。
    let fx = Fx::new();
    let out = run_engine_with(
        &fx,
        &["upgrade", "--engine=v1.0.0"],
        &unused_registry(),
        &second_opts("r2", &t),
    );
    assert_gap_or_internal(
        &out,
        "this engine is v0.0.0, but the engine lock version line names v1.0.0",
    );
}

#[test]
fn residual_progress_files_that_are_not_this_engine_upgrade_stop() {
    let argv = ["upgrade", "--engine=v1.2.0"];
    // 工具的 upgrade。
    let fx = Fx::new();
    residual(&fx, "tool", &new_locked(), false);
    let out = run_engine(&fx, &argv, &unused_registry());
    assert_gap(
        &out,
        "upgrade --engine while the incomplete upgrade operation",
    );

    // 引擎升級記的目標不是版本鎖定行（鎖定行之後被手改過）。
    let fx = Fx::new();
    residual(&fx, table::ENGINE_TARGET, &target_locked(), false);
    let before = fx.snapshot();
    let out = run_engine(&fx, &argv, &unused_registry());
    assert_gap(&out, "whose target is not the engine lock version line");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn target_labels_must_describe_the_target_engine() {
    for (labels, needle) in [
        ("", "has no vendor_kit.protocol.floor label"),
        (
            r#""vendor_kit.protocol.floor":"1","vendor_kit.protocol.current":"1","org.opencontainers.image.version":"v1.2.0""#,
            "has no vendor_kit.schema.max label",
        ),
        (
            r#""vendor_kit.protocol.floor":"2","vendor_kit.protocol.current":"1","vendor_kit.schema.max":"1","org.opencontainers.image.version":"v1.2.0""#,
            "above vendor_kit.protocol.current",
        ),
        (
            r#""vendor_kit.protocol.floor":"01","vendor_kit.protocol.current":"1","vendor_kit.schema.max":"1","org.opencontainers.image.version":"v1.2.0""#,
            "vendor_kit.protocol.floor=\"01\"",
        ),
        (
            r#""vendor_kit.protocol.floor":"1","vendor_kit.protocol.current":"1","vendor_kit.schema.max":"1","org.opencontainers.image.version":"v1.3.0""#,
            "announces org.opencontainers.image.version=\"v1.3.0\", not v1.2.0",
        ),
    ] {
        let fx = Fx::new();
        let before = fx.snapshot();
        let peer = Peer::start(&fx, Script { labels, ..TARGET });
        let out = run_engine(&fx, &["upgrade", "--engine=v1.2.0"], &unused_registry());
        peer.finish();
        assert_gap_or_internal(&out, needle);
        assert_eq!(fx.snapshot(), before);
    }
}

/// VK0056（缺口或內部錯誤）且原因含 `needle`。
fn assert_gap_or_internal(out: &Out, needle: &str) {
    assert_eq!(out.code, 2, "{}", out.stderr);
    assert!(
        out.stderr
            .starts_with("vendor_kit: error[VK0056]: Internal vendor_kit error: "),
        "{}",
        out.stderr
    );
    assert!(out.stderr.contains(needle), "{needle}: {}", out.stderr);
}

#[test]
fn original_command_quotes_each_argument() {
    assert_eq!(
        engine::original_command(&["upgrade", "--engine=v1.2.0", "-y"]),
        "just vendor_kit upgrade --engine=v1.2.0 -y"
    );
    assert_eq!(
        engine::original_command(&["a b", "it's"]),
        "just vendor_kit 'a b' 'it'\\''s'"
    );
}
