//! VK recipe 的參數解析（04 指令、共同選項、各指令專用選項、說明與用法錯誤）。
//!
//! 輸入是 `just vendor_kit` 之後的參數（第一個是指令名），輸出是結構化的 [`Invocation`]，
//! 或一個 [`UsageError`]。這裡不印任何東西：錯誤帶著訊息表條目與占位符的值，
//! 要怎麼印由呼叫端經 `diagnostics`（診斷）與 `output`（用法）決定。不用 clap 之類會自己印訊息的套件。
//!
//! 規則：
//!
//! - 位置參數只放 `<repo>`；`test <path>` 是例外，`test dist` 是完整指令名（04 說明與用法錯誤）。
//! - 選項可放位置參數前或後；單獨的 `--` 是選項結束標記，之後一律當位置參數，即使以 `-` 開頭（GLOSSARY）。
//! - `-y`／`--yes` 只收可能詢問的指令：`add`、`upgrade <repo>`、`upgrade --engine`（含 `--engine=<tag>`）、
//!   `remove`、`install`、`uninstall`（04 共同選項；`add`、`remove`、`uninstall` 是 #372 N14 照「可能詢問才接受」
//!   加的，04 的組合清單待維護者確認）。判準看指令可不可能詢問，不看這次有沒有問到：這次沒問到也收。
//!   不會詢問的指令（`dev`、`undev`、`update`、`sync`、`prune`、`test`）不收。`-y` 只省略詢問，不擴大授權範圍
//!   （判定在各指令，這裡不管）。
//! - `--dry-run`（預演，#372 N11；只有長選項）可寫 recipe 都收：`add`、`upgrade`（含 `--engine`）、`remove`、
//!   `install`、`uninstall`、`dev`、`undev`（含 `--engine`）、`prune`。唯讀的 `update`、`test`、`test dist` 與
//!   `sync` 不收（VK0026；`sync` 是救援路徑，收了就進凍結文法，這一版不收）。語意由各指令實作：算出完整計畫、
//!   stdout 印出會改的內容、不詢問、除執行紀錄外不寫檔；跟 `-y` 可以並用，`-y` 沒有作用（不收 `-y` 的指令照樣
//!   不收）。`install --dry-run`、`upgrade --engine --dry-run` 屬救援路徑（見下）。
//! - 引擎一律用 `--engine`，只有 `upgrade`、`dev`、`undev` 收；帶版本只收 `upgrade --engine=<tag>`，
//!   `--engine <tag>` 的 `<tag>` 算多出的位置參數。工具用 `<repo>@<tag>`，只有 `add`、`upgrade` 收。
//! - `--registry-token-file <path>` 只有 `update`、`add`、`upgrade <repo>` 收；值是單獨的 `-` 算用法錯誤。
//! - `--image-path <registry>/<path>`（名稱暫定，待維護者確認，#372 N2b）只有長選項、只有 `add` 收：線上 `add`
//!   還沒有版本鎖定行時，工具 image 在 registry 的位置。值只收 `ghcr.io/<路徑>`（路徑照
//!   [`imageref::is_valid_path`]），不帶 tag 或 digest；不合算不允許的參數（VK0026，`<value>` 印那個值）。
//! - `dev <repo>` 必須帶 `-p <dir>`、`dev --engine` 必須帶 `-i <image>`，各自不收對方的選項（04 本機覆寫）。
//! - `-h`／`--help`（出現在 `--` 之前）只准與決定印哪份用法的 `--engine` 並用；`<repo>`、`--engine=<tag>`
//!   都不算。`test dist -h` 的 `dist` 是指令名的一部分，可以並用。
//!
//! 契約沒寫、這裡取嚴的細節（之後放寬不破壞相容）：
//!
//! - 同一個選項給兩次（含 `-y` 與 `--yes`、`--engine` 與 `--engine=<tag>`）時，第二個算不允許的參數；`-h` 例外。
//! - 帶值的選項只收以空白分開的 `-i <image>`、`--image <image>`，不收 `--image=<image>`，短選項不合併（`-yi` 不認得）。
//! - `add` 的 `--image-path` 與 `-i` 並用時，`--image-path` 算不允許的參數（`-i` 的引用已含路徑）。
//! - 帶值的選項一律把下一個參數原樣當值，即使它以 `-` 開頭或是 `--`。
//! - 不收 tag 的指令遇到 `<repo>@<tag>`，整個參數算不允許的參數，不檢查 tag 格式；`<repo>` 是空字串也一樣。
//! - `dev`、`undev`、`upgrade` 的 `<repo>` 不是合法的 just 名稱（`[A-Za-z_][A-Za-z0-9_-]*`）時，整個參數（含
//!   `@<tag>`）算不允許的參數（VK0026，#372 N84）。`add`、`remove`、`update` 這一版還不檢查。
//! - `dist` 不論在不在 `--` 之後，都當 `test dist` 的指令名，不當 path。
//!
//! 錯誤的優先次序：先 VK0026（不認得、多出或不允許的參數，取最前面的那一個），再 VK0027（tag 格式不合），
//! 最後 VK0025（缺必要參數）。不認得的指令名報 VK0026；經 just 時到不了引擎，只有直接呼叫引擎時會遇到（#372 N108）。
//!
//! 救援路徑（04 說明與用法錯誤的表）：`install`（含 `-y`、`--dry-run`）、`upgrade --engine`（含 `=<tag>`、`-y`、
//! `--dry-run`）、`sync`，以及用法的 `just vendor_kit`、`install -h`、`upgrade --engine -h`、`sync -h`（長選項同）。
//! `install --dry-run`、`upgrade --engine --dry-run` 是 #372 N11 加進來的（待維護者確認）。這些呼叫的文法跨介面版永久不變
//! （#372 維護者 10/05 定救援路徑協定選 A、ADR-0007），改這裡的規則時不能動到它們，測試釘住。
//! `bootstrap.sh` 只檢查與 `--repair` 的保留入口（`plan::entry`）不經這裡：入口 `vendor_kit` 先認出來，
//! 這裡一律當不認得的指令名（VK0026），測試釘住。

use std::ffi::{OsStr, OsString};
use std::fmt;

use imageref::Tag;
use messages::Message;

/// VK recipe 的指令名；`test dist` 是完整指令名，獨立一個值。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Name {
    Add,
    Upgrade,
    Dev,
    Undev,
    Remove,
    Update,
    Sync,
    Install,
    Uninstall,
    Prune,
    Test,
    TestDist,
}

impl Name {
    /// 打在 `just vendor_kit` 後的指令名；`test dist` 由 `test` 的位置參數決定，不從這裡來。
    fn from_command(s: &str) -> Option<Name> {
        Some(match s {
            "add" => Name::Add,
            "upgrade" => Name::Upgrade,
            "dev" => Name::Dev,
            "undev" => Name::Undev,
            "remove" => Name::Remove,
            "update" => Name::Update,
            "sync" => Name::Sync,
            "install" => Name::Install,
            "uninstall" => Name::Uninstall,
            "prune" => Name::Prune,
            "test" => Name::Test,
            _ => return None,
        })
    }

    /// 印在用法裡的指令名。
    pub fn as_str(self) -> &'static str {
        match self {
            Name::Add => "add",
            Name::Upgrade => "upgrade",
            Name::Dev => "dev",
            Name::Undev => "undev",
            Name::Remove => "remove",
            Name::Update => "update",
            Name::Sync => "sync",
            Name::Install => "install",
            Name::Uninstall => "uninstall",
            Name::Prune => "prune",
            Name::Test => "test",
            Name::TestDist => "test dist",
        }
    }

    /// 收 `--engine` 的指令（04 指令表）。
    fn takes_engine(self) -> bool {
        matches!(self, Name::Upgrade | Name::Dev | Name::Undev)
    }
}

impl fmt::Display for Name {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

/// 解析好的一次 VK recipe 呼叫。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Invocation {
    /// 執行指令。
    Run(Command),
    /// 印該指令的用法；`engine` 為真時印 `--engine` 那份。
    Help { name: Name, engine: bool },
}

impl Invocation {
    /// 是不是救援路徑的呼叫（crate 文件「救援路徑」）：`install`、`upgrade --engine`、`sync`，
    /// 以及 `install -h`、`upgrade --engine -h`、`sync -h`。不帶指令的用法呼叫是 [`UsageError::NoCommand`]，
    /// 不在這裡判。
    pub fn is_rescue(&self) -> bool {
        match self {
            Invocation::Run(c) => matches!(
                c,
                Command::Install { .. } | Command::UpgradeEngine { .. } | Command::Sync
            ),
            Invocation::Help { name, engine } => match name {
                Name::Install | Name::Sync => !engine,
                Name::Upgrade => *engine,
                _ => false,
            },
        }
    }
}

/// 各指令的參數值（04 指令表）。路徑與 image 保留原本的 [`OsString`]。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Command {
    /// `add <repo>[@<tag>] [-i <image>] [--image-path <registry>/<path>] [-y] [--dry-run] [--registry-token-file <path>]`
    Add {
        repo: String,
        tag: Option<Tag>,
        image: Option<OsString>,
        yes: bool,
        /// 帶了 `--dry-run`（crate 文件的規則）。
        dry_run: bool,
        /// `--image-path` 的值，已驗過是 `ghcr.io/<路徑>`（crate 文件的規則）。
        image_path: Option<String>,
        registry_token_file: Option<OsString>,
    },
    /// `upgrade <repo>[@<tag>] [-y] [--dry-run] [--registry-token-file <path>]`
    UpgradeTool {
        repo: String,
        tag: Option<Tag>,
        yes: bool,
        dry_run: bool,
        registry_token_file: Option<OsString>,
    },
    /// `upgrade --engine[=<tag>] [-y] [--dry-run]`
    UpgradeEngine {
        tag: Option<Tag>,
        yes: bool,
        dry_run: bool,
    },
    /// `dev <repo> -p <dir> [--dry-run]`
    DevTool {
        repo: String,
        path: OsString,
        dry_run: bool,
    },
    /// `dev --engine -i <image> [--dry-run]`
    DevEngine { image: OsString, dry_run: bool },
    /// `undev <repo> [--dry-run]`
    UndevTool { repo: String, dry_run: bool },
    /// `undev --engine [--dry-run]`
    UndevEngine { dry_run: bool },
    /// `remove <repo> [-y] [--dry-run]`
    Remove {
        repo: String,
        yes: bool,
        dry_run: bool,
    },
    /// `update [<repo>] [--registry-token-file <path>]`
    Update {
        repo: Option<String>,
        registry_token_file: Option<OsString>,
    },
    /// `sync`
    Sync,
    /// `install [-y] [--dry-run]`
    Install { yes: bool, dry_run: bool },
    /// `uninstall [-y] [--dry-run]`
    Uninstall { yes: bool, dry_run: bool },
    /// `prune [--dry-run]`
    Prune { dry_run: bool },
    /// `test [<path>]`
    Test { path: Option<OsString> },
    /// `test dist`
    TestDist,
}

/// 用法錯誤（訊息表 VK0024–VK0027，都是 error、以 2 結束）。
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum UsageError {
    /// VK0024：只打 `just vendor_kit`，沒有指令。
    NoCommand,
    /// VK0025：缺必要參數；值是 `<argument>`，例如 `<repo>`、`-p <dir>`。
    Missing(String),
    /// VK0026：不認得、多出或此處不允許的參數；值是 `<value>`，即使用者打的那個參數。
    Disallowed(String),
    /// VK0027：tag 格式不合；值是 `<tag>`，即使用者打的 tag。
    InvalidTag(String),
}

impl UsageError {
    /// 對應的訊息表條目。
    pub fn message(&self) -> &'static Message {
        match self {
            UsageError::NoCommand => &messages::VK0024,
            UsageError::Missing(_) => &messages::VK0025,
            UsageError::Disallowed(_) => &messages::VK0026,
            UsageError::InvalidTag(_) => &messages::VK0027,
        }
    }

    /// 訊息文字裡要填的占位名稱與值；VK0024 沒有占位符。
    pub fn placeholder(&self) -> Option<(&'static str, &str)> {
        match self {
            UsageError::NoCommand => None,
            UsageError::Missing(v) => Some(("argument", v)),
            UsageError::Disallowed(v) => Some(("value", v)),
            UsageError::InvalidTag(v) => Some(("tag", v)),
        }
    }
}

impl fmt::Display for UsageError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            UsageError::NoCommand => f.write_str("no command specified"),
            UsageError::Missing(v) => write!(f, "missing required argument: {v}"),
            UsageError::Disallowed(v) => write!(f, "unknown, extra, or disallowed argument: {v}"),
            UsageError::InvalidTag(v) => write!(f, "invalid tag format: {v}"),
        }
    }
}

impl std::error::Error for UsageError {}

/// 解析 `just vendor_kit` 之後的參數。
pub fn parse<S: AsRef<OsStr>>(args: &[S]) -> Result<Invocation, UsageError> {
    let Some((first, rest)) = args.split_first() else {
        return Err(UsageError::NoCommand);
    };
    let first = first.as_ref();
    let name = first
        .to_str()
        .and_then(Name::from_command)
        .ok_or_else(|| disallowed(first))?;
    let rest: Vec<&OsStr> = rest.iter().map(AsRef::as_ref).collect();
    if let Some(help) = help(name, &rest)? {
        return Ok(help);
    }
    build(name, tokenize(&rest))
}

fn lossy(s: &OsStr) -> String {
    s.to_string_lossy().into_owned()
}

fn disallowed(s: &OsStr) -> UsageError {
    UsageError::Disallowed(lossy(s))
}

fn is_help(s: &OsStr) -> bool {
    s == "-h" || s == "--help"
}

/// `--` 之前出現 `-h`／`--help` 時，判斷能不能並用並回 [`Invocation::Help`]；沒有就回 `None`。
fn help(name: Name, rest: &[&OsStr]) -> Result<Option<Invocation>, UsageError> {
    let asked = rest.iter().take_while(|a| **a != "--").any(|a| is_help(a));
    if !asked {
        return Ok(None);
    }
    let (mut engine, mut dist) = (false, false);
    for arg in rest {
        if is_help(arg) {
            continue;
        }
        if *arg == "--engine" && name.takes_engine() && !engine {
            engine = true;
        } else if *arg == "dist" && name == Name::Test && !dist {
            dist = true;
        } else {
            return Err(disallowed(arg));
        }
    }
    let name = if dist { Name::TestDist } else { name };
    Ok(Some(Invocation::Help { name, engine }))
}

/// 一個參數（或帶值選項連同它的值）分出的種類；`at` 是它在參數裡的位置，用來取最前面的錯誤。
#[derive(Debug)]
struct Token<'a> {
    at: usize,
    raw: &'a OsStr,
    kind: Kind<'a>,
}

#[derive(Debug)]
enum Kind<'a> {
    Yes,
    /// `--dry-run`。
    DryRun,
    /// `--engine`，或 `--engine=<tag>`（帶原字串）。
    Engine(Option<&'a str>),
    Value(Opt, Option<&'a OsStr>),
    Positional,
    Unknown,
}

/// 帶值的選項。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Opt {
    Image,
    ImagePath,
    Path,
    TokenFile,
}

impl Opt {
    /// VK0025 的 `<argument>`：使用者打的選項加上值的名稱。
    fn missing(self, typed: &OsStr) -> String {
        let value = match self {
            Opt::Image => "<image>",
            Opt::ImagePath => "<registry>/<path>",
            Opt::Path => "<dir>",
            Opt::TokenFile => "<path>",
        };
        format!("{} {value}", lossy(typed))
    }
}

fn tokenize<'a>(rest: &[&'a OsStr]) -> Vec<Token<'a>> {
    let mut tokens = Vec::new();
    let mut ended = false;
    let mut i = 0;
    while i < rest.len() {
        let raw = rest[i];
        let at = i;
        i += 1;
        if ended {
            tokens.push(Token {
                at,
                raw,
                kind: Kind::Positional,
            });
            continue;
        }
        let text = raw.to_str();
        let opt = match text {
            Some("--") => {
                ended = true;
                continue;
            }
            Some("-y" | "--yes") => Some(Kind::Yes),
            Some(DRY_RUN) => Some(Kind::DryRun),
            Some("--engine") => Some(Kind::Engine(None)),
            Some(t) if t.starts_with("--engine=") => Some(Kind::Engine(t.get("--engine=".len()..))),
            Some("-i" | "--image") => Some(Kind::Value(Opt::Image, None)),
            Some("-p" | "--path") => Some(Kind::Value(Opt::Path, None)),
            Some("--registry-token-file") => Some(Kind::Value(Opt::TokenFile, None)),
            Some("--image-path") => Some(Kind::Value(Opt::ImagePath, None)),
            Some(t) if t.starts_with('-') && t != "-" => Some(Kind::Unknown),
            None if raw.as_encoded_bytes().starts_with(b"-") => Some(Kind::Unknown),
            _ => None,
        };
        let kind = match opt {
            Some(Kind::Value(o, _)) => {
                let value = rest.get(i).copied();
                if value.is_some() {
                    i += 1;
                }
                Kind::Value(o, value)
            }
            Some(k) => k,
            None => Kind::Positional,
        };
        tokens.push(Token { at, raw, kind });
    }
    tokens
}

/// 指令收哪些選項（不看組合）；不收的在第一輪就算不允許。
fn accepts(name: Name, kind: &Kind<'_>) -> bool {
    match kind {
        Kind::Yes => matches!(
            name,
            Name::Add | Name::Upgrade | Name::Remove | Name::Install | Name::Uninstall
        ),
        // 可寫 recipe 都收；唯讀的 `update`、`test` 與救援的 `sync` 不收（crate 文件的規則）。
        Kind::DryRun => !matches!(
            name,
            Name::Update | Name::Sync | Name::Test | Name::TestDist
        ),
        Kind::Engine(None) => name.takes_engine(),
        Kind::Engine(Some(_)) => name == Name::Upgrade,
        Kind::Value(Opt::Image, _) => matches!(name, Name::Add | Name::Dev),
        Kind::Value(Opt::ImagePath, _) => name == Name::Add,
        Kind::Value(Opt::Path, _) => name == Name::Dev,
        Kind::Value(Opt::TokenFile, _) => {
            matches!(name, Name::Add | Name::Upgrade | Name::Update)
        }
        Kind::Positional => !matches!(
            name,
            Name::Sync | Name::Install | Name::Uninstall | Name::Prune
        ),
        Kind::Unknown => false,
    }
}

/// 一次呼叫裡收下的參數，以及找到的問題。
#[derive(Default)]
struct Seen<'a> {
    yes: Option<usize>,
    dry_run: Option<usize>,
    engine: Option<(usize, Option<&'a str>)>,
    image: Option<(usize, &'a OsStr)>,
    image_path: Option<(usize, &'a OsStr)>,
    path: Option<(usize, &'a OsStr)>,
    token_file: Option<(usize, &'a OsStr)>,
    positionals: Vec<(usize, &'a OsStr)>,
    /// VK0026 的候選：(位置, 參數)。
    bad: Vec<(usize, String)>,
    /// VK0027 的候選。
    bad_tag: Vec<(usize, String)>,
    /// 帶值選項沒有值（VK0025）。
    missing_value: Option<String>,
}

impl<'a> Seen<'a> {
    fn reject(&mut self, at: usize, raw: &OsStr) {
        self.bad.push((at, lossy(raw)));
    }

    /// 選項只准給一次；第二次算不允許。
    fn once<T>(&mut self, slot: Option<T>, at: usize, raw: &OsStr, value: T) -> Option<T> {
        if slot.is_some() {
            self.reject(at, raw);
            slot
        } else {
            Some(value)
        }
    }

    fn collect(name: Name, tokens: &[Token<'a>]) -> Seen<'a> {
        let mut s = Seen::default();
        for t in tokens {
            if !accepts(name, &t.kind) {
                s.reject(t.at, t.raw);
                continue;
            }
            match t.kind {
                Kind::Yes => s.yes = s.once(s.yes, t.at, t.raw, t.at),
                Kind::DryRun => s.dry_run = s.once(s.dry_run, t.at, t.raw, t.at),
                Kind::Engine(tag) => s.engine = s.once(s.engine, t.at, t.raw, (t.at, tag)),
                Kind::Value(opt, None) => {
                    if s.missing_value.is_none() {
                        s.missing_value = Some(opt.missing(t.raw));
                    }
                }
                Kind::Value(opt, Some(v)) => {
                    let slot = match opt {
                        Opt::Image => s.image,
                        Opt::ImagePath => s.image_path,
                        Opt::Path => s.path,
                        Opt::TokenFile => s.token_file,
                    };
                    let slot = s.once(slot, t.at, t.raw, (t.at, v));
                    match opt {
                        Opt::Image => s.image = slot,
                        Opt::ImagePath => s.image_path = slot,
                        Opt::Path => s.path = slot,
                        Opt::TokenFile => s.token_file = slot,
                    }
                    // VK 不從 stdin 讀，token 檔是單獨的 `-` 時印 `-`（訊息表 VK0026）。
                    if opt == Opt::TokenFile && v == "-" {
                        s.reject(t.at + 1, v);
                    }
                }
                Kind::Positional => s.positionals.push((t.at, t.raw)),
                Kind::Unknown => s.reject(t.at, t.raw),
            }
        }
        s
    }

    /// 對象（`<repo>` 或 `--engine`）只能一個；最前面那個是對象，其餘都是多出的參數。
    /// 回傳：是不是引擎，以及工具名的參數。
    fn target(&mut self, takes_engine: bool) -> (bool, Option<(usize, &'a OsStr)>) {
        let mut targets: Vec<(usize, Option<&'a OsStr>)> = self
            .positionals
            .iter()
            .map(|&(at, raw)| (at, Some(raw)))
            .collect();
        if takes_engine && let Some((at, _)) = self.engine {
            targets.push((at, None));
        }
        targets.sort_by_key(|&(at, _)| at);
        let mut it = targets.into_iter();
        let first = it.next();
        for (at, raw) in it {
            match raw {
                Some(raw) => self.reject(at, raw),
                None => self.bad.push((at, engine_raw(self.engine))),
            }
        }
        match first {
            None => (false, None),
            Some((_, None)) => (true, None),
            Some((at, Some(raw))) => (false, Some((at, raw))),
        }
    }

    /// 該模式不收的選項算不允許。
    fn forbid(&mut self, slot: Option<(usize, &OsStr)>, typed: &str) {
        if let Some((at, _)) = slot {
            self.bad.push((at, typed.to_owned()));
        }
    }

    /// 工具名，可帶 `@<tag>`（`with_tag` 為假時整個參數算不允許）。`just_name` 為真時工具名必須是合法的
    /// just 名稱（[`is_just_name`]），不合時整個參數算不允許。
    fn repo(
        &mut self,
        repo: (usize, &OsStr),
        with_tag: bool,
        just_name: bool,
    ) -> Option<(String, Option<Tag>)> {
        let (at, raw) = repo;
        let Some(text) = raw.to_str() else {
            self.reject(at, raw);
            return None;
        };
        let (name, tag) = match text.split_once('@') {
            Some((name, tag)) if with_tag => (name, Some(tag)),
            Some(_) => {
                self.reject(at, raw);
                return None;
            }
            None => (text, None),
        };
        if name.is_empty() || (just_name && !is_just_name(name)) {
            self.reject(at, raw);
            return None;
        }
        let tag = match tag.map(Tag::parse) {
            None => None,
            Some(Ok(t)) => Some(t),
            Some(Err(e)) => {
                self.bad_tag.push((at, e.input().to_owned()));
                None
            }
        };
        Some((name.to_owned(), tag))
    }

    /// `--image-path` 的值：只收 `ghcr.io/<路徑>`，不帶 tag 或 digest；不合時那個值算不允許的參數。
    fn image_path_value(&mut self) -> Option<String> {
        let (at, raw) = self.image_path?;
        match raw.to_str().filter(|v| is_image_path(v)) {
            Some(v) => Some(v.to_owned()),
            None => {
                self.reject(at + 1, raw);
                None
            }
        }
    }

    fn engine_tag(&mut self) -> Option<Tag> {
        let (at, tag) = self.engine?;
        match Tag::parse(tag?) {
            Ok(t) => Some(t),
            Err(e) => {
                self.bad_tag.push((at, e.input().to_owned()));
                None
            }
        }
    }

    /// 依優先次序取第一個錯誤：VK0026 → VK0027 → 帶值選項缺值 → `missing`。
    fn finish(self, missing: Option<&str>) -> Result<(), UsageError> {
        if let Some((_, v)) = self.bad.into_iter().min_by_key(|(at, _)| *at) {
            return Err(UsageError::Disallowed(v));
        }
        if let Some((_, v)) = self.bad_tag.into_iter().min_by_key(|(at, _)| *at) {
            return Err(UsageError::InvalidTag(v));
        }
        if let Some(v) = self.missing_value {
            return Err(UsageError::Missing(v));
        }
        match missing {
            Some(v) => Err(UsageError::Missing(v.to_owned())),
            None => Ok(()),
        }
    }
}

/// just 的名稱：`[A-Za-z_][A-Za-z0-9_-]*`（與 `fetch::is_namespace` 同一條規則；指令之間互不依賴，照抄）。
fn is_just_name(s: &str) -> bool {
    let mut b = s.bytes();
    b.next()
        .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
        && b.all(|c| c.is_ascii_alphanumeric() || c == b'_' || c == b'-')
}

/// `--engine` 參數的原字串，給 VK0026 的 `<value>`。
fn engine_raw(engine: Option<(usize, Option<&str>)>) -> String {
    match engine {
        Some((_, Some(tag))) => format!("--engine={tag}"),
        _ => "--engine".to_owned(),
    }
}

const REPO: &str = "<repo>";

/// 預演選項（crate 文件的規則）：只有長選項。
pub const DRY_RUN: &str = "--dry-run";

/// `--image-path` 的值合不合（crate 文件）：`ghcr.io/` 加合法的路徑；路徑的規則不收 `:`、`@`，所以帶 tag 或
/// digest 都不合。
pub fn is_image_path(value: &str) -> bool {
    value
        .strip_prefix(imageref::GHCR)
        .and_then(|rest| rest.strip_prefix('/'))
        .is_some_and(imageref::is_valid_path)
}

fn build(name: Name, tokens: Vec<Token<'_>>) -> Result<Invocation, UsageError> {
    let mut s = Seen::collect(name, &tokens);
    let dry_run = s.dry_run.is_some();
    let cmd = match name {
        Name::Add | Name::Remove | Name::Update => {
            let (_, target) = s.target(false);
            let repo = target.and_then(|r| s.repo(r, name == Name::Add, false));
            let token_file = s.token_file.map(|(_, v)| v.to_owned());
            let image = s.image.map(|(_, v)| v.to_owned());
            let image_path = s.image_path_value();
            if image.is_some() {
                s.forbid(s.image_path, "--image-path");
            }
            let yes = s.yes.is_some();
            let need = (name != Name::Update && target.is_none()).then_some(REPO);
            s.finish(need)?;
            match (name, repo) {
                (Name::Update, repo) => Command::Update {
                    repo: repo.map(|(r, _)| r),
                    registry_token_file: token_file,
                },
                (Name::Add, Some((repo, tag))) => Command::Add {
                    repo,
                    tag,
                    image,
                    yes,
                    dry_run,
                    image_path,
                    registry_token_file: token_file,
                },
                (_, Some((repo, _))) => Command::Remove { repo, yes, dry_run },
                (_, None) => return Err(UsageError::Missing(REPO.to_owned())),
            }
        }
        Name::Upgrade => {
            let (engine, target) = s.target(true);
            let yes = s.yes.is_some();
            if engine {
                s.forbid(s.token_file, "--registry-token-file");
                let tag = s.engine_tag();
                s.finish(None)?;
                Command::UpgradeEngine { tag, yes, dry_run }
            } else {
                let repo = target.and_then(|r| s.repo(r, true, true));
                let registry_token_file = s.token_file.map(|(_, v)| v.to_owned());
                s.finish(target.is_none().then_some(REPO))?;
                let Some((repo, tag)) = repo else {
                    return Err(UsageError::Missing(REPO.to_owned()));
                };
                Command::UpgradeTool {
                    repo,
                    tag,
                    yes,
                    dry_run,
                    registry_token_file,
                }
            }
        }
        Name::Dev => {
            let (engine, target) = s.target(true);
            if engine {
                s.forbid(s.path, &typed(&tokens, s.path, "-p"));
                let image = s.image.map(|(_, v)| v.to_owned());
                s.finish(image.is_none().then_some("-i <image>"))?;
                let Some(image) = image else {
                    return Err(UsageError::Missing("-i <image>".to_owned()));
                };
                Command::DevEngine { image, dry_run }
            } else {
                s.forbid(s.image, &typed(&tokens, s.image, "-i"));
                let repo = target.and_then(|r| s.repo(r, false, true));
                let path = s.path.map(|(_, v)| v.to_owned());
                let need = if target.is_none() {
                    Some(REPO)
                } else if path.is_none() {
                    Some("-p <dir>")
                } else {
                    None
                };
                s.finish(need)?;
                match (repo, path) {
                    (Some((repo, _)), Some(path)) => Command::DevTool {
                        repo,
                        path,
                        dry_run,
                    },
                    _ => return Err(UsageError::Missing(REPO.to_owned())),
                }
            }
        }
        Name::Undev => {
            let (engine, target) = s.target(true);
            let repo = target.and_then(|r| s.repo(r, false, true));
            s.finish((!engine && target.is_none()).then_some(REPO))?;
            match repo {
                _ if engine => Command::UndevEngine { dry_run },
                Some((repo, _)) => Command::UndevTool { repo, dry_run },
                None => return Err(UsageError::Missing(REPO.to_owned())),
            }
        }
        Name::Sync | Name::Prune => {
            s.finish(None)?;
            match name {
                Name::Sync => Command::Sync,
                _ => Command::Prune { dry_run },
            }
        }
        Name::Install | Name::Uninstall => {
            let yes = s.yes.is_some();
            s.finish(None)?;
            match name {
                Name::Install => Command::Install { yes, dry_run },
                _ => Command::Uninstall { yes, dry_run },
            }
        }
        Name::Test | Name::TestDist => {
            // 第一個 `dist` 讓指令成為 `test dist`，之後不收任何 path；沒有 `dist` 時只收一個 path。
            let dist = s
                .positionals
                .iter()
                .find(|(_, raw)| *raw == "dist")
                .copied();
            let mut path = None;
            for &(at, raw) in &s.positionals.clone() {
                if Some((at, raw)) == dist {
                    continue;
                }
                if dist.is_some() || path.is_some() {
                    s.reject(at, raw);
                } else {
                    path = Some(raw.to_owned());
                }
            }
            s.finish(None)?;
            if dist.is_some() {
                Command::TestDist
            } else {
                Command::Test { path }
            }
        }
    };
    Ok(Invocation::Run(cmd))
}

/// 帶值選項使用者實際打的寫法（`-i` 或 `--image`），給 VK0026 的 `<value>`。
fn typed(tokens: &[Token<'_>], slot: Option<(usize, &OsStr)>, short: &str) -> String {
    slot.and_then(|(at, _)| tokens.iter().find(|t| t.at == at))
        .map_or_else(|| short.to_owned(), |t| lossy(t.raw))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used)]
mod tests {
    use super::*;

    fn tag(s: &str) -> Tag {
        Tag::parse(s).unwrap()
    }

    fn os(s: &str) -> OsString {
        OsString::from(s)
    }

    fn run(args: &[&str]) -> Command {
        match parse(args) {
            Ok(Invocation::Run(c)) => c,
            other => panic!("{args:?} → {other:?}"),
        }
    }

    fn help_of(args: &[&str]) -> (Name, bool) {
        match parse(args) {
            Ok(Invocation::Help { name, engine }) => (name, engine),
            other => panic!("{args:?} → {other:?}"),
        }
    }

    fn err(args: &[&str]) -> UsageError {
        match parse(args) {
            Err(e) => e,
            Ok(ok) => panic!("{args:?} → {ok:?}"),
        }
    }

    fn bad(args: &[&str], value: &str) {
        assert_eq!(
            err(args),
            UsageError::Disallowed(value.to_owned()),
            "{args:?}"
        );
    }

    fn missing(args: &[&str], argument: &str) {
        assert_eq!(
            err(args),
            UsageError::Missing(argument.to_owned()),
            "{args:?}"
        );
    }

    fn bad_tag(args: &[&str], t: &str) {
        assert_eq!(err(args), UsageError::InvalidTag(t.to_owned()), "{args:?}");
    }

    // ---- 錯誤與訊息表的對應 ----

    #[test]
    fn errors_map_to_usage_codes() {
        let cases = [
            (UsageError::NoCommand, "VK0024", None),
            (
                UsageError::Missing("<repo>".into()),
                "VK0025",
                Some(("argument", "<repo>")),
            ),
            (
                UsageError::Disallowed("--bogus".into()),
                "VK0026",
                Some(("value", "--bogus")),
            ),
            (
                UsageError::InvalidTag("v01.0.0".into()),
                "VK0027",
                Some(("tag", "v01.0.0")),
            ),
        ];
        for (e, code, ph) in cases {
            assert_eq!(e.message().code, code);
            assert_eq!(e.message().exit_code(), 2);
            assert_eq!(e.placeholder(), ph);
            if let Some((name, _)) = ph {
                assert!(e.message().text.contains(&format!("<{name}>")));
            }
        }
    }

    #[test]
    fn no_command() {
        assert_eq!(err(&[]), UsageError::NoCommand);
    }

    #[test]
    fn unknown_command_names_are_rejected() {
        bad(&["foo"], "foo");
        bad(&["help"], "help");
        bad(&["-h"], "-h");
        bad(&["--version"], "--version");
        bad(&["dist"], "dist");
        bad(&["Add"], "Add");
    }

    // ---- add ----

    #[test]
    fn add_takes_yes() {
        for args in [
            &["add", "lint", "-y"][..],
            &["add", "--yes", "lint@v1.2.0"],
            &["add", "lint", "-i", "lint.tar", "-y"],
        ] {
            match run(args) {
                Command::Add { yes, .. } => assert!(yes, "{args:?}"),
                other => panic!("{args:?} → {other:?}"),
            }
        }
    }

    #[test]
    fn add_valid() {
        assert_eq!(
            run(&["add", "lint"]),
            Command::Add {
                repo: "lint".into(),
                tag: None,
                image: None,
                yes: false,
                dry_run: false,
                image_path: None,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["add", "lint@v1.2.0"]),
            Command::Add {
                repo: "lint".into(),
                tag: Some(tag("v1.2.0")),
                image: None,
                yes: false,
                dry_run: false,
                image_path: None,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["add", "-i", "lint.tar", "lint"]),
            Command::Add {
                repo: "lint".into(),
                tag: None,
                image: Some(os("lint.tar")),
                yes: false,
                dry_run: false,
                image_path: None,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["add", "lint", "--image", "ghcr.io/o/lint:v1.0.0"]),
            Command::Add {
                repo: "lint".into(),
                tag: None,
                image: Some(os("ghcr.io/o/lint:v1.0.0")),
                yes: false,
                dry_run: false,
                image_path: None,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["add", "lint", "--registry-token-file", "tok"]),
            Command::Add {
                repo: "lint".into(),
                tag: None,
                image: None,
                yes: false,
                dry_run: false,
                image_path: None,
                registry_token_file: Some(os("tok"))
            }
        );
        assert_eq!(
            run(&["add", "--image-path", "ghcr.io/acme/lint", "lint@v1.2.0"]),
            Command::Add {
                repo: "lint".into(),
                tag: Some(tag("v1.2.0")),
                image: None,
                yes: false,
                dry_run: false,
                image_path: Some("ghcr.io/acme/lint".into()),
                registry_token_file: None
            }
        );
    }

    #[test]
    fn add_errors() {
        missing(&["add"], "<repo>");
        missing(&["add", "-i", "x.tar"], "<repo>");
        missing(&["add", "lint", "-i"], "-i <image>");
        missing(&["add", "lint", "--image"], "--image <image>");
        missing(
            &["add", "lint", "--registry-token-file"],
            "--registry-token-file <path>",
        );
        bad(&["add", "lint", "base"], "base");
        bad(&["add", "lint", "-y", "--yes"], "--yes");
        bad(&["add", "lint", "-y", "-y"], "-y");
        bad(&["add", "--engine"], "--engine");
        bad(&["add", "lint", "-p", "d"], "-p");
        bad(&["add", "lint", "--bogus"], "--bogus");
        bad(&["add", "lint", "--repair"], "--repair");
        bad(&["add", "lint", "--image=x.tar"], "--image=x.tar");
        bad(&["add", "lint", "-i", "a", "-i", "b"], "-i");
        bad(&["add", "lint", "--registry-token-file", "-"], "-");
        bad(&["add", "@v1.0.0"], "@v1.0.0");
        bad_tag(&["add", "lint@v1.02.0"], "v1.02.0");
        bad_tag(&["add", "lint@1.0.0"], "1.0.0");
        bad_tag(&["add", "lint@"], "");
        bad_tag(&["add", "lint@v1.0.0-rc1"], "v1.0.0-rc1");
    }

    #[test]
    fn add_image_path_errors() {
        missing(
            &["add", "lint", "--image-path"],
            "--image-path <registry>/<path>",
        );
        for value in [
            "acme/lint",
            "docker.io/acme/lint",
            "ghcr.io/acme/lint:v1.0.0",
            "ghcr.io/acme/lint@sha256:00",
            "ghcr.io/",
            "ghcr.io/Acme/lint",
            "ghcr.io//lint",
        ] {
            bad(&["add", "lint", "--image-path", value], value);
        }
        bad(
            &[
                "add",
                "lint",
                "--image-path",
                "ghcr.io/a/l",
                "--image-path",
                "ghcr.io/a/l",
            ],
            "--image-path",
        );
        bad(
            &["add", "lint", "-i", "x.tar", "--image-path", "ghcr.io/a/l"],
            "--image-path",
        );
        bad(
            &["add", "lint", "--image-path=ghcr.io/a/l"],
            "--image-path=ghcr.io/a/l",
        );
        for name in ["upgrade", "update", "remove", "dev"] {
            bad(
                &[name, "lint", "--image-path", "ghcr.io/a/l"],
                "--image-path",
            );
        }
        assert!(is_image_path("ghcr.io/acme/sub/lint"));
    }

    // ---- upgrade ----

    #[test]
    fn upgrade_tool_valid() {
        assert_eq!(
            run(&["upgrade", "lint"]),
            Command::UpgradeTool {
                repo: "lint".into(),
                tag: None,
                yes: false,
                registry_token_file: None,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "-y", "lint@v0.9.0", "--registry-token-file", "t"]),
            Command::UpgradeTool {
                repo: "lint".into(),
                tag: Some(tag("v0.9.0")),
                yes: true,
                registry_token_file: Some(os("t")),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "lint", "--yes"]),
            Command::UpgradeTool {
                repo: "lint".into(),
                tag: None,
                yes: true,
                registry_token_file: None,
                dry_run: false
            }
        );
    }

    #[test]
    fn upgrade_engine_valid() {
        assert_eq!(
            run(&["upgrade", "--engine"]),
            Command::UpgradeEngine {
                tag: None,
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine=v1.4.0", "-y"]),
            Command::UpgradeEngine {
                tag: Some(tag("v1.4.0")),
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "-y", "--engine"]),
            Command::UpgradeEngine {
                tag: None,
                yes: true,
                dry_run: false
            }
        );
    }

    #[test]
    fn upgrade_errors() {
        missing(&["upgrade"], "<repo>");
        missing(&["upgrade", "-y"], "<repo>");
        bad(&["upgrade", "--engine", "v1.4.0"], "v1.4.0");
        bad(&["upgrade", "--engine", "lint"], "lint");
        bad(&["upgrade", "lint", "--engine"], "--engine");
        bad(&["upgrade", "lint", "--engine=v1.0.0"], "--engine=v1.0.0");
        bad(&["upgrade", "lint", "base"], "base");
        bad(
            &["upgrade", "--engine", "--registry-token-file", "t"],
            "--registry-token-file",
        );
        bad(
            &["upgrade", "--engine", "--engine=v1.0.0"],
            "--engine=v1.0.0",
        );
        bad(&["upgrade", "lint", "-y", "--yes"], "--yes");
        bad(&["upgrade", "lint", "-i", "x"], "-i");
        bad(&["upgrade", "lint", "-p", "d"], "-p");
        // 解析結果與介面版無關；介面版不合時引擎先報版本（回 3），見 engine/vendor_kit 的 cli 測試。
        bad(&["upgrade", "--engine", "--bogus"], "--bogus");
        bad(&["upgrade", "lint", "-yi"], "-yi");
        bad(&["upgrade", "lint", "--registry-token-file", "-"], "-");
        bad_tag(&["upgrade", "lint@v1.0"], "v1.0");
        bad_tag(&["upgrade", "--engine=1.4.0"], "1.4.0");
        bad_tag(&["upgrade", "--engine="], "");
        bad_tag(&["upgrade", "--engine=v1.4.0+build"], "v1.4.0+build");
    }

    /// `dev`、`undev`、`upgrade` 的 `<repo>` 不是合法的 just 名稱：整個參數算不允許（#372 N84），
    /// 排在 tag 格式之前；`add`、`remove`、`update` 這一版不檢查。
    #[test]
    fn tool_name_must_be_a_just_name() {
        for name in ["1lint", "li.nt", "li nt", "-lint", "lint/x", "lïnt"] {
            bad(&["upgrade", name], name);
            bad(&["dev", name, "-p", "d"], name);
            bad(&["undev", name], name);
        }
        bad(&["upgrade", "li.nt@v1.0.0"], "li.nt@v1.0.0");
        bad(&["upgrade", "li.nt@v1.0"], "li.nt@v1.0");
        bad(&["upgrade", "--", "-lint"], "-lint");
        for name in ["_lint", "Lint-2", "a_b-c"] {
            assert!(matches!(
                run(&["upgrade", name]),
                Command::UpgradeTool { repo, .. } if repo == name
            ));
        }
        assert_eq!(
            run(&["remove", "li.nt"]),
            Command::Remove {
                repo: "li.nt".into(),
                yes: false,
                dry_run: false
            }
        );
    }

    // ---- dev ----

    #[test]
    fn dev_valid() {
        assert_eq!(
            run(&["dev", "lint", "-p", "../lint"]),
            Command::DevTool {
                repo: "lint".into(),
                path: os("../lint"),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["dev", "--path", "../lint", "lint"]),
            Command::DevTool {
                repo: "lint".into(),
                path: os("../lint"),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["dev", "--engine", "-i", "vendor_kit:dev"]),
            Command::DevEngine {
                image: os("vendor_kit:dev"),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["dev", "--image", "e.tar", "--engine"]),
            Command::DevEngine {
                image: os("e.tar"),
                dry_run: false
            }
        );
    }

    #[test]
    fn dev_errors() {
        missing(&["dev"], "<repo>");
        missing(&["dev", "lint"], "-p <dir>");
        missing(&["dev", "lint", "-p"], "-p <dir>");
        missing(&["dev", "lint", "--path"], "--path <dir>");
        missing(&["dev", "--engine"], "-i <image>");
        missing(&["dev", "--engine", "-i"], "-i <image>");
        bad(&["dev", "lint", "-p", "d", "-i", "x"], "-i");
        bad(&["dev", "lint", "-p", "d", "--image", "x"], "--image");
        bad(&["dev", "--engine", "-i", "x", "-p", "d"], "-p");
        bad(&["dev", "--engine", "-i", "x", "--path", "d"], "--path");
        bad(&["dev", "--engine=v1.0.0", "-i", "x"], "--engine=v1.0.0");
        bad(&["dev", "lint@v1.0.0", "-p", "d"], "lint@v1.0.0");
        bad(&["dev", "lint", "base", "-p", "d"], "base");
        bad(&["dev", "lint", "-p", "d", "-y"], "-y");
        bad(
            &["dev", "lint", "-p", "d", "--registry-token-file", "t"],
            "--registry-token-file",
        );
        bad(&["dev", "lint", "-p", "d", "-p", "e"], "-p");
    }

    // ---- undev ----

    #[test]
    fn undev_valid() {
        assert_eq!(
            run(&["undev", "lint"]),
            Command::UndevTool {
                repo: "lint".into(),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["undev", "--engine"]),
            Command::UndevEngine { dry_run: false }
        );
    }

    #[test]
    fn undev_errors() {
        missing(&["undev"], "<repo>");
        bad(&["undev", "lint", "--engine"], "--engine");
        bad(&["undev", "--engine", "lint"], "lint");
        bad(&["undev", "--engine=v1.0.0"], "--engine=v1.0.0");
        bad(&["undev", "lint@v1.0.0"], "lint@v1.0.0");
        bad(&["undev", "lint", "base"], "base");
        bad(&["undev", "lint", "-y"], "-y");
        bad(&["undev", "lint", "-p", "d"], "-p");
        bad(&["undev", "--engine", "-i", "x"], "-i");
    }

    // ---- remove ----

    #[test]
    fn remove_valid() {
        assert_eq!(
            run(&["remove", "lint"]),
            Command::Remove {
                repo: "lint".into(),
                yes: false,
                dry_run: false
            }
        );
        for yes in ["-y", "--yes"] {
            assert_eq!(
                run(&["remove", yes, "lint"]),
                Command::Remove {
                    repo: "lint".into(),
                    yes: true,
                    dry_run: false
                }
            );
        }
    }

    #[test]
    fn remove_errors() {
        missing(&["remove"], "<repo>");
        bad(&["remove", "lint", "base"], "base");
        bad(&["remove", "lint@v1.0.0"], "lint@v1.0.0");
        bad(&["remove", "--engine"], "--engine");
        bad(&["remove", "lint", "-y", "--yes"], "--yes");
        bad(&["remove", "lint", "--", "-y"], "-y");
        bad(
            &["remove", "lint", "--registry-token-file", "t"],
            "--registry-token-file",
        );
    }

    // ---- update ----

    #[test]
    fn update_valid() {
        assert_eq!(
            run(&["update"]),
            Command::Update {
                repo: None,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["update", "lint", "--registry-token-file", "t"]),
            Command::Update {
                repo: Some("lint".into()),
                registry_token_file: Some(os("t"))
            }
        );
    }

    #[test]
    fn update_errors() {
        bad(&["update", "lint", "base"], "base");
        bad(&["update", "lint@v1.0.0"], "lint@v1.0.0");
        bad(&["update", "--engine"], "--engine");
        bad(&["update", "-y"], "-y");
        bad(&["update", "--exit-code"], "--exit-code");
        bad(&["update", "--registry-token-file", "-"], "-");
        missing(
            &["update", "--registry-token-file"],
            "--registry-token-file <path>",
        );
    }

    #[test]
    fn dry_run_is_every_writing_command() {
        for args in [
            &["add", "lint", "--dry-run"][..],
            &["add", "--dry-run", "lint@v1.2.0", "-y"],
            &["add", "lint", "-i", "lint.tar", "--dry-run"],
        ] {
            match run(args) {
                Command::Add { dry_run, .. } => assert!(dry_run, "{args:?}"),
                other => panic!("{args:?} → {other:?}"),
            }
        }
        assert_eq!(
            run(&["install", "--dry-run"]),
            Command::Install {
                yes: false,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["install", "-y", "--dry-run"]),
            Command::Install {
                yes: true,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["upgrade", "--dry-run", "lint@v1.2.0", "-y"]),
            Command::UpgradeTool {
                repo: "lint".into(),
                tag: Some(tag("v1.2.0")),
                yes: true,
                dry_run: true,
                registry_token_file: None
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine=v2.0.0", "--dry-run"]),
            Command::UpgradeEngine {
                tag: Some(tag("v2.0.0")),
                yes: false,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["remove", "lint", "--dry-run"]),
            Command::Remove {
                repo: "lint".into(),
                yes: false,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["uninstall", "--dry-run", "-y"]),
            Command::Uninstall {
                yes: true,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["dev", "lint", "-p", "d", "--dry-run"]),
            Command::DevTool {
                repo: "lint".into(),
                path: os("d"),
                dry_run: true
            }
        );
        assert_eq!(
            run(&["dev", "--dry-run", "--engine", "-i", "e.tar"]),
            Command::DevEngine {
                image: os("e.tar"),
                dry_run: true
            }
        );
        assert_eq!(
            run(&["undev", "lint", "--dry-run"]),
            Command::UndevTool {
                repo: "lint".into(),
                dry_run: true
            }
        );
        assert_eq!(
            run(&["undev", "--engine", "--dry-run"]),
            Command::UndevEngine { dry_run: true }
        );
        assert_eq!(
            run(&["prune", "--dry-run"]),
            Command::Prune { dry_run: true }
        );
        // 唯讀的 `update`、`test` 與救援的 `sync` 不收；不收 `-y` 的指令照樣不收 `-y`。
        for args in [
            &["update", "--dry-run"][..],
            &["sync", "--dry-run"],
            &["test", "--dry-run"],
            &["test", "dist", "--dry-run"],
        ] {
            bad(args, "--dry-run");
        }
        bad(&["prune", "--dry-run", "-y"], "-y");
        bad(&["undev", "lint", "-y", "--dry-run"], "-y");
        // 只有長選項、只能給一次、不跟 -h 並用；`--` 之後是位置參數。
        bad(&["add", "lint", "--dry-run", "--dry-run"], "--dry-run");
        bad(&["install", "--dry-run=yes"], "--dry-run=yes");
        bad(&["add", "lint", "--dry-run", "-h"], "lint");
        bad(&["install", "--dry-run", "-h"], "--dry-run");
        bad(&["install", "--", "--dry-run"], "--dry-run");
    }

    // ---- 不帶參數的指令 ----

    #[test]
    fn argumentless_commands() {
        assert_eq!(run(&["sync"]), Command::Sync);
        assert_eq!(
            run(&["install"]),
            Command::Install {
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["install", "-y"]),
            Command::Install {
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["install", "--yes"]),
            Command::Install {
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["uninstall"]),
            Command::Uninstall {
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["uninstall", "-y"]),
            Command::Uninstall {
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["uninstall", "--yes"]),
            Command::Uninstall {
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(run(&["prune"]), Command::Prune { dry_run: false });
        // 單獨的 `--` 後面沒東西，沒有影響。
        assert_eq!(run(&["sync", "--"]), Command::Sync);
    }

    #[test]
    fn argumentless_command_errors() {
        for name in ["sync", "install", "uninstall", "prune"] {
            bad(&[name, "lint"], "lint");
            bad(&[name, "--engine"], "--engine");
            bad(&[name, "--bogus"], "--bogus");
            bad(&[name, "-i", "x"], "-i");
            bad(
                &[name, "--registry-token-file", "t"],
                "--registry-token-file",
            );
            bad(&[name, "--", "-y"], "-y");
        }
        // 不會詢問的指令不收 `-y`（crate 文件）。
        for name in ["sync", "prune"] {
            bad(&[name, "-y"], "-y");
        }
        bad(&["install", "-y", "-y"], "-y");
        bad(&["uninstall", "-y", "--yes"], "--yes");
        bad(&["install", "--repair"], "--repair");
    }

    // ---- test ----

    #[test]
    fn test_valid() {
        assert_eq!(run(&["test"]), Command::Test { path: None });
        assert_eq!(
            run(&["test", "test/unit"]),
            Command::Test {
                path: Some(os("test/unit"))
            }
        );
        assert_eq!(run(&["test", "dist"]), Command::TestDist);
        assert_eq!(
            run(&["test", "--", "-weird"]),
            Command::Test {
                path: Some(os("-weird"))
            }
        );
    }

    #[test]
    fn test_errors() {
        bad(&["test", "test/a", "test/b"], "test/b");
        bad(&["test", "test/a", "test/b", "test/c"], "test/b");
        bad(&["test", "dist", "test/a"], "test/a");
        bad(&["test", "test/a", "dist"], "test/a");
        bad(&["test", "dist", "dist"], "dist");
        bad(&["test", "-y"], "-y");
        bad(&["test", "--engine"], "--engine");
        bad(&["test", "dist", "--bogus"], "--bogus");
    }

    // ---- 選項結束標記 ----

    #[test]
    fn end_of_options_makes_the_rest_positional() {
        assert_eq!(
            run(&["remove", "--", "-lint"]),
            Command::Remove {
                repo: "-lint".into(),
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "-y", "--", "lint"]),
            Command::UpgradeTool {
                repo: "lint".into(),
                tag: None,
                yes: true,
                registry_token_file: None,
                dry_run: false
            }
        );
        // `--` 之後的 `-y`、`--engine` 是位置參數，所以是多出的參數。
        bad(&["upgrade", "lint", "--", "-y"], "-y");
        bad(&["upgrade", "--engine", "--", "--engine"], "--engine");
        // 只有第一個 `--` 是標記，第二個是位置參數。
        bad(&["remove", "lint", "--", "--"], "--");
        // 帶值選項把下一個參數原樣當值，即使它是 `--`。
        assert_eq!(
            run(&["dev", "lint", "-p", "--"]),
            Command::DevTool {
                repo: "lint".into(),
                path: os("--"),
                dry_run: false
            }
        );
        assert_eq!(
            run(&["dev", "lint", "-p", "-x"]),
            Command::DevTool {
                repo: "lint".into(),
                path: os("-x"),
                dry_run: false
            }
        );
    }

    // ---- -h / --help ----

    #[test]
    fn help_for_every_command() {
        for (name, n) in [
            ("add", Name::Add),
            ("upgrade", Name::Upgrade),
            ("dev", Name::Dev),
            ("undev", Name::Undev),
            ("remove", Name::Remove),
            ("update", Name::Update),
            ("sync", Name::Sync),
            ("install", Name::Install),
            ("uninstall", Name::Uninstall),
            ("prune", Name::Prune),
            ("test", Name::Test),
        ] {
            assert_eq!(help_of(&[name, "-h"]), (n, false));
            assert_eq!(help_of(&[name, "--help"]), (n, false));
            assert_eq!(help_of(&[name, "-h", "--help"]), (n, false));
        }
        assert_eq!(help_of(&["test", "dist", "-h"]), (Name::TestDist, false));
        assert_eq!(
            help_of(&["test", "--help", "dist"]),
            (Name::TestDist, false)
        );
    }

    #[test]
    fn help_with_engine() {
        for (name, n) in [
            ("upgrade", Name::Upgrade),
            ("dev", Name::Dev),
            ("undev", Name::Undev),
        ] {
            assert_eq!(help_of(&[name, "--engine", "-h"]), (n, true));
            assert_eq!(help_of(&[name, "--help", "--engine"]), (n, true));
        }
    }

    #[test]
    fn help_combined_with_other_arguments() {
        // `<repo>` 不算決定用法的參數。
        bad(&["add", "lint", "-h"], "lint");
        bad(&["upgrade", "-h", "lint"], "lint");
        bad(&["remove", "lint", "--help"], "lint");
        // 印第一個不是 -h／--help 或 --engine 的參數。
        bad(&["upgrade", "--engine", "-y", "-h", "--bogus"], "-y");
        bad(&["upgrade", "-h", "--engine=v1.0.0"], "--engine=v1.0.0");
        bad(&["install", "-h", "-y"], "-y");
        bad(&["dev", "-h", "-p", "d"], "-p");
        // 不收 --engine 的指令，--engine 也不准並用。
        bad(&["sync", "--engine", "-h"], "--engine");
        bad(&["add", "-h", "--engine"], "--engine");
        bad(&["upgrade", "--engine", "--engine", "-h"], "--engine");
        bad(&["test", "dist", "dist", "-h"], "dist");
        bad(&["test", "test/a", "-h"], "test/a");
        // `--` 之後的 -h 是位置參數，不是說明。
        assert_eq!(
            run(&["remove", "--", "-h"]),
            Command::Remove {
                repo: "-h".into(),
                yes: false,
                dry_run: false
            }
        );
        // `--` 之前有 -h 時，`--` 本身也不准並用。
        bad(&["remove", "-h", "--", "lint"], "--");
    }

    // ---- 優先次序 ----

    #[test]
    fn first_disallowed_argument_wins() {
        bad(
            &[
                "upgrade",
                "--registry-token-file",
                "t",
                "--engine",
                "--bogus",
            ],
            "--registry-token-file",
        );
        bad(&["add", "--bogus", "lint", "base"], "--bogus");
        bad(&["add", "lint", "base", "--bogus"], "base");
    }

    #[test]
    fn disallowed_before_tag_before_missing() {
        bad(&["upgrade", "lint@v01.0.0", "--bogus"], "--bogus");
        bad_tag(&["add", "lint@v01.0.0", "-i"], "v01.0.0");
        bad(&["dev", "-i", "x"], "-i");
        bad_tag(&["upgrade", "a@v1", "--registry-token-file", "t"], "v1");
    }

    #[test]
    fn non_utf8_arguments() {
        use std::os::unix::ffi::OsStrExt;
        let raw = OsStr::from_bytes(b"lint\xff");
        let args = [OsStr::new("remove"), raw];
        assert!(matches!(parse(&args), Err(UsageError::Disallowed(_))));
        let opt = OsStr::from_bytes(b"--x\xff");
        let args = [OsStr::new("sync"), opt];
        assert!(matches!(parse(&args), Err(UsageError::Disallowed(_))));
        let args = [OsStr::from_bytes(b"\xff")];
        assert!(matches!(parse(&args), Err(UsageError::Disallowed(_))));
        // path 的值保留原本的位元組。
        let dir = OsStr::from_bytes(b"d\xff");
        let args = [OsStr::new("dev"), OsStr::new("lint"), OsStr::new("-p"), dir];
        assert_eq!(
            parse(&args),
            Ok(Invocation::Run(Command::DevTool {
                repo: "lint".into(),
                path: dir.to_owned(),
                dry_run: false
            }))
        );
    }

    // ---- 救援路徑：文法跨介面版永久不變（#372 定救援路徑協定選 A） ----

    #[test]
    fn rescue_path_grammar_is_pinned() {
        assert_eq!(err(&[]), UsageError::NoCommand);
        assert_eq!(
            run(&["install"]),
            Command::Install {
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["install", "-y"]),
            Command::Install {
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["install", "--dry-run"]),
            Command::Install {
                yes: false,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["install", "--dry-run", "-y"]),
            Command::Install {
                yes: true,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine"]),
            Command::UpgradeEngine {
                tag: None,
                yes: false,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine=v2.0.0", "-y"]),
            Command::UpgradeEngine {
                tag: Some(tag("v2.0.0")),
                yes: true,
                dry_run: false
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine", "--dry-run"]),
            Command::UpgradeEngine {
                tag: None,
                yes: false,
                dry_run: true
            }
        );
        assert_eq!(
            run(&["upgrade", "--engine=v2.0.0", "--dry-run", "-y"]),
            Command::UpgradeEngine {
                tag: Some(tag("v2.0.0")),
                yes: true,
                dry_run: true
            }
        );
        assert_eq!(run(&["sync"]), Command::Sync);
        for h in ["-h", "--help"] {
            assert_eq!(help_of(&["install", h]), (Name::Install, false));
            assert_eq!(help_of(&["upgrade", "--engine", h]), (Name::Upgrade, true));
            assert_eq!(help_of(&["sync", h]), (Name::Sync, false));
        }
    }

    #[test]
    fn reserved_bootstrap_entries_are_not_commands() {
        // plan::entry 的保留入口只由入口 vendor_kit 認，一般路徑不收。
        for name in ["@shell-check", "@shell-repair"] {
            assert_eq!(err(&[name]), UsageError::Disallowed(name.into()));
            assert_eq!(err(&[name, "-h"]), UsageError::Disallowed(name.into()));
        }
    }

    #[test]
    fn rescue_calls_are_recognized() {
        for a in [
            &["install"][..],
            &["install", "-y"],
            &["install", "--dry-run"],
            &["install", "--dry-run", "-y"],
            &["upgrade", "--engine"],
            &["upgrade", "--engine=v2.0.0", "-y"],
            &["upgrade", "--engine", "--dry-run"],
            &["upgrade", "--engine=v2.0.0", "--dry-run", "-y"],
            &["sync"],
            &["install", "-h"],
            &["upgrade", "--engine", "--help"],
            &["sync", "-h"],
        ] {
            assert!(parse(a).unwrap().is_rescue(), "{a:?}");
        }
        for a in [
            &["add", "lint"][..],
            &["upgrade", "lint"],
            &["upgrade", "-h"],
            &["update"],
            &["add", "-h"],
            &["dev", "--engine", "-h"],
            &["undev", "--engine"],
            &["prune"],
            &["upgrade", "lint", "--dry-run"],
            &["dev", "--engine", "-i", "e.tar", "--dry-run"],
        ] {
            assert!(!parse(a).unwrap().is_rescue(), "{a:?}");
        }
    }

    #[test]
    fn names_print_as_typed() {
        assert_eq!(Name::TestDist.to_string(), "test dist");
        assert_eq!(Name::Upgrade.as_str(), "upgrade");
    }
}
