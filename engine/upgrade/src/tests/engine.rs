//! `upgrade --engine` 第一段（[`crate::engine`]）：假啟動器回帶 LABEL 的 inspect 與 pull，假 registry 回
//! `tags/list` 與 HEAD manifest。

use super::online::{Registry, public};
use super::*;
use crate::engine::{self, ENGINE_REPO};

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

/// 跑一次 `upgrade --engine`：`argv` 是 `just vendor_kit` 之後的參數，tag 與 `-y` 從裡面取。
fn run_engine(fx: &Fx, argv: &[&str], registry: &Client) -> Out {
    let tag = argv
        .iter()
        .find_map(|a| a.strip_prefix("--engine="))
        .map(|t| Tag::parse(t).unwrap());
    let req = engine::Request {
        tag,
        yes: argv.contains(&"-y"),
    };
    let argv: Vec<String> = argv.iter().map(|s| (*s).to_owned()).collect();
    fx.assert_fresh_session();
    let mut channel = Channel::new(&fx.ctl, header());
    let mut stdin = Cursor::new(Vec::new());
    let mut stdout = Vec::new();
    let shared = Shared::default();
    let mut prompt = shared.clone();
    let mut diags = Diagnostics::with_sink(shared.clone(), NoSink);
    let mut log = runlog::Writer::new(
        Vec::new(),
        runlog::Header {
            version: WRITTEN_BY.to_owned(),
            component: runlog::Component::Engine,
            invocation_id: "r1".to_owned(),
        },
    );
    let code = {
        let mut env = Env {
            dir: &fx.dir,
            host_root: "/h/proj",
            run_log: "/h/proj/.vendor_kit/log/r1.jsonl",
            inbox: &fx.inbox,
            channel: &mut channel,
            poll: Duration::from_millis(1),
            registry,
            tty: tty(false),
            argv: &argv,
            run_id: "r1",
            written_by: WRITTEN_BY,
            stdin: &mut stdin,
            stdout: &mut stdout,
            prompt: &mut prompt,
            diags: &mut diags,
            log: &mut log,
        };
        engine::run(&req, &mut env)
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

#[test]
fn the_same_tag_as_the_lock_line_is_the_second_stage_gap() {
    let fx = Fx::new();
    let before = fx.snapshot();
    let out = run_engine(&fx, &["upgrade", "--engine=v1.0.0"], &unused_registry());
    assert_gap(&out, "which the engine lock version line already names");
    assert_eq!(fx.snapshot(), before);
}

#[test]
fn residual_progress_files_stop_before_any_docker_action() {
    // 第一段做完再跑一次：第二段還沒做，停下，不再建第二份進度檔。
    let fx = Fx::new();
    let peer = Peer::start(&fx, TARGET);
    let argv = ["upgrade", "--engine=v1.2.0"];
    run_engine(&fx, &argv, &unused_registry());
    peer.finish();
    let before = fx.snapshot();
    fx.new_session();
    let out = run_engine(&fx, &argv, &unused_registry());
    assert_gap(
        &out,
        "completing the engine upgrade recorded in .vendor_kit/.tmp.upgrade.r1.toml",
    );
    assert_eq!(fx.snapshot(), before);

    let fx = Fx::new();
    residual(&fx, "tool", &new_locked(), false);
    let out = run_engine(&fx, &argv, &unused_registry());
    assert_gap(
        &out,
        "upgrade --engine while the incomplete upgrade operation",
    );
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
