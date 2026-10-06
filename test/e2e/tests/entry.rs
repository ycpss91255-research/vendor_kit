//! 薄殼入口（ADR-0007、04 主機需求）：用真的 just 解析 `launcher/shell/assemble.sh` 組好的薄殼模板，
//! 經 `.vendor_kit/log.sh` 走到啟動器；docker 是 `launcher/test/fixture/fake_docker.bash`，`start -ai`
//! 當引擎、只寫 `done`，不起真的引擎。
//!
//! 核對三件事（#372 的 N51、N118、N113）：
//! - `just vendor_kit`、`just vendor_kit <recipe> <args>...` 的參數原樣轉給引擎（`docker create` 的 argv
//!   在 `--` 之後的部分）。
//! - `gen/tools.just` 的 `mod?` 指到的 cache 缺失時 just 照樣解析，救援的 `just vendor_kit sync` 跑得起來；
//!   cache 在時 `mod?` 的路徑以 `gen/` 為基準。
//! - 正式路徑（不是救援呼叫）遇到薄殼介面版低於鎖定的引擎接受的介面版時印 VK0009，不起引擎。
//!
//! 這些測試要 just、`launcher/` 與 msggen 產的訊息片段（`VK_MESSAGES`），image/Dockerfile 的 test stage 在
//! 裝好 just、複製 `launcher/` 之後以 `cargo test -p e2e --test entry -- --ignored` 跑；工作區的
//! `cargo test` 那時還沒有這些，所以標成 ignored。缺任何一項就讓測試失敗，不跳過。
#![allow(clippy::unwrap_used, clippy::expect_used)]

use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};
use std::process::Command;

use e2e::{VERSION, shell};

const REPO: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/../..");
const ENGINE: &str = "ghcr.io/ycpss91255-research/vendor_kit:v1.0.0@sha256:1111111111111111111111111111111111111111111111111111111111111111";
/// 引擎容器的 ID（fake_docker.bash 的 `engine_cid`）。
const ENGINE_CID: &str = "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee";
/// `gen/tools.just` 的一行（engine/tools_just 的 `line`；這裡不能依賴 engine crate，照抄格式）。
const TOOLS_LINE: &str = "mod? ns '../cache/tool/just/ns.just'\n";

/// 一個安裝目錄：`root` 是專案根目錄，`fake` 是假 docker 的狀態目錄，`bin` 放假 docker，`tmp` 是 TMPDIR。
struct Project {
    _dir: tempfile::TempDir,
    root: PathBuf,
    fake: PathBuf,
    bin: PathBuf,
    tmp: PathBuf,
}

/// 組好的薄殼模板本文（不含自描述標頭）：跑 `launcher/shell/assemble.sh`。
fn assemble(out: &Path) {
    let messages = std::env::var_os("VK_MESSAGES")
        .expect("VK_MESSAGES must point to the msggen bash fragment (bootstrap_messages.sh)");
    let status = Command::new("bash")
        .arg(Path::new(REPO).join("launcher/shell/assemble.sh"))
        .arg(messages)
        .arg(out)
        .status()
        .expect("cannot run bash");
    assert!(status.success(), "assemble.sh failed");
}

/// 已安裝的專案：根目錄 justfile 只有 import 行，薄殼四檔是組好的模板加上介面版 `interface` 的標頭，
/// version.toml 鎖 [`ENGINE`]、旁記介面版列表 `protocols`。引擎 image 已在本機（LABEL 區間 1–1）。
fn project(interface: u32, protocols: &str) -> Project {
    let dir = tempfile::tempdir().unwrap();
    let base = dir.path().canonicalize().unwrap();
    let root = base.join("proj");
    let vk = root.join(".vendor_kit");
    let templates = base.join("templates");
    fs::create_dir_all(root.join(".git")).unwrap();
    fs::create_dir_all(root.join("sub")).unwrap();
    fs::create_dir_all(vk.join("gen")).unwrap();
    assemble(&templates);
    for name in ["entry.just", "vendor.just", "log.sh", ".gitignore"] {
        let body = fs::read_to_string(templates.join(name)).unwrap();
        fs::write(vk.join(name), shell::render(interface, VERSION, &body)).unwrap();
    }
    fs::write(
        vk.join("version.toml"),
        format!(
            "vendor_kit = \"{ENGINE}\"\nvendor_kit_protocols = \"{protocols}\"\nschema = 1\nwritten_by = \"{VERSION}\"\n"
        ),
    )
    .unwrap();
    fs::write(root.join("justfile"), "import '.vendor_kit/entry.just'\n").unwrap();

    let fake = base.join("fake");
    let bin = base.join("bin");
    let tmp = base.join("tmp");
    for d in [&fake, &bin, &tmp] {
        fs::create_dir_all(d).unwrap();
    }
    fs::write(fake.join("labels"), "1 1 v1.0.0").unwrap();
    fs::write(fake.join("runner.rc"), "0").unwrap();
    fs::write(fake.join("engine"), "finish 0\n").unwrap();
    let fixture = Path::new(REPO).join("launcher/test/fixture/fake_docker.bash");
    assert!(fixture.is_file(), "{} not found", fixture.display());
    let docker = bin.join("docker");
    fs::write(
        &docker,
        format!(
            "#!/usr/bin/env bash\nsource '{}'\n",
            fixture.canonicalize().unwrap().display()
        ),
    )
    .unwrap();
    fs::set_permissions(&docker, fs::Permissions::from_mode(0o755)).unwrap();
    Project {
        _dir: dir,
        root,
        fake,
        bin,
        tmp,
    }
}

impl Project {
    /// 在 `sub/` 下打 `just <args>...`。PATH 最前面是假 docker；環境只留 PATH、HOME、TMPDIR 與 VK_FAKE。
    fn just(&self, args: &[&str]) -> (i32, String, String) {
        let path = format!(
            "{}:{}",
            self.bin.display(),
            std::env::var("PATH").unwrap_or_default()
        );
        let out = Command::new("just")
            .args(args)
            .current_dir(self.root.join("sub"))
            .env_clear()
            .env("PATH", path)
            .env("HOME", &self.root)
            .env("TMPDIR", &self.tmp)
            .env("VK_FAKE", &self.fake)
            .output()
            .expect("cannot run just; image/Dockerfile's test stage installs it");
        (
            out.status.code().unwrap(),
            String::from_utf8(out.stdout).unwrap(),
            String::from_utf8(out.stderr).unwrap(),
        )
    }

    /// 假 docker 的呼叫紀錄（一行一次，參數以 `%q` 接起來）；沒有呼叫過是空字串。
    fn calls(&self) -> String {
        fs::read_to_string(self.fake.join("calls")).unwrap_or_default()
    }

    /// 引擎拿到的 argv 在 `--` 之後的部分（`docker create` 的參數，一個一行）。
    fn engine_args(&self) -> Vec<String> {
        let argv = fs::read_to_string(self.fake.join("engine.argv")).expect("engine not created");
        let argv: Vec<&str> = argv.lines().collect();
        let sep = argv.iter().position(|a| *a == "--").expect("no -- in argv");
        argv[sep + 1..].iter().map(|a| a.to_string()).collect()
    }

    /// 引擎起過、正常收尾：結束碼 0、容器刪掉、session 目錄不留。
    fn assert_ran(&self, code: i32, stderr: &str) {
        assert_eq!(code, 0, "stderr: {stderr}");
        assert!(self.calls().contains(&format!("start -ai {ENGINE_CID}")));
        assert!(self.calls().contains(&format!("rm {ENGINE_CID}")));
        assert_eq!(fs::read_dir(&self.tmp).unwrap().count(), 0);
    }
}

#[test]
#[ignore = "needs just, launcher/ and VK_MESSAGES; run by image/Dockerfile's test stage"]
fn no_command_reaches_the_engine_with_no_arguments() {
    let p = project(1, "1");
    let (code, _, stderr) = p.just(&["vendor_kit"]);
    p.assert_ran(code, &stderr);
    assert!(p.engine_args().is_empty());
}

#[test]
#[ignore = "needs just, launcher/ and VK_MESSAGES; run by image/Dockerfile's test stage"]
fn recipe_arguments_are_forwarded_verbatim() {
    let p = project(1, "1");
    let args = ["a b", "--x", "", "q'u\"o", "$HOME", "*", "--", "-y"];
    let mut cmd = vec!["vendor_kit", "add"];
    cmd.extend_from_slice(&args);
    let (code, _, stderr) = p.just(&cmd);
    p.assert_ran(code, &stderr);
    let mut want = vec!["add".to_string()];
    want.extend(args.iter().map(|a| a.to_string()));
    assert_eq!(p.engine_args(), want);
}

#[test]
#[ignore = "needs just, launcher/ and VK_MESSAGES; run by image/Dockerfile's test stage"]
fn rescue_sync_runs_when_a_mod_optional_target_is_missing() {
    let p = project(1, "1");
    let tools = p.root.join(".vendor_kit/gen/tools.just");
    // 對照：寫成 `mod` 時 cache 一缺，just 解析整份 justfile 就失敗，連救援的 sync 都起不來。
    fs::write(&tools, TOOLS_LINE.replacen("mod?", "mod", 1)).unwrap();
    let (code, _, stderr) = p.just(&["vendor_kit", "sync"]);
    assert_ne!(code, 0);
    assert!(stderr.contains("ns"), "stderr: {stderr}");
    assert_eq!(p.calls(), "");

    fs::write(&tools, TOOLS_LINE).unwrap();
    let (code, _, stderr) = p.just(&["vendor_kit", "sync"]);
    p.assert_ran(code, &stderr);
    assert_eq!(p.engine_args(), ["sync"]);
}

#[test]
#[ignore = "needs just, launcher/ and VK_MESSAGES; run by image/Dockerfile's test stage"]
fn mod_optional_path_is_relative_to_gen() {
    let p = project(1, "1");
    fs::write(p.root.join(".vendor_kit/gen/tools.just"), TOOLS_LINE).unwrap();
    let just_dir = p.root.join(".vendor_kit/cache/tool/just");
    fs::create_dir_all(&just_dir).unwrap();
    fs::write(
        just_dir.join("ns.just"),
        "hello:\n    @echo hello from ns\n",
    )
    .unwrap();
    let (code, stdout, stderr) = p.just(&["ns", "hello"]);
    assert_eq!(code, 0, "stderr: {stderr}");
    assert_eq!(stdout, "hello from ns\n");
    assert_eq!(p.calls(), "");
}

#[test]
#[ignore = "needs just, launcher/ and VK_MESSAGES; run by image/Dockerfile's test stage"]
fn old_shell_on_the_normal_path_prints_vk0009() {
    let p = project(1, "2");
    let (code, stdout, stderr) = p.just(&["vendor_kit", "add", "tool"]);
    assert_eq!(code, 3, "stderr: {stderr}");
    assert_eq!(stdout, "");
    assert!(
        stderr.lines().any(|l| l
            == "vendor_kit: fatal[VK0009]: Shell interface version 1 is older than required for general recipes in engine v1.0.0. Run first: just vendor_kit upgrade --engine"),
        "stderr: {stderr}"
    );
    assert!(!p.calls().contains("create"), "calls: {}", p.calls());
    assert!(!p.fake.join("engine.argv").exists());
}
