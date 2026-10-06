//! 各指令 `-h`／`--help` 的用法文字。
//!
//! 實際的 help 輸出就是唯一來源（04 共同選項），04 不另寫一份。文字只列這一版 `args` 收的選項；
//! 之後加的選項（`add --image-path`、`add`／`remove`／`uninstall` 的 `-y`、`--dry-run`）由加它的 PR
//! 在這裡補上自己的那一行。

/// 印哪一份用法：一個指令一份；`upgrade`、`dev`、`undev` 帶 `--engine` 時各另一份。
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Help {
    Add,
    UpgradeTool,
    UpgradeEngine,
    DevTool,
    DevEngine,
    UndevTool,
    UndevEngine,
    Remove,
    Update,
    Sync,
    Install,
    Uninstall,
    Prune,
    Test,
    TestDist,
}

impl Help {
    /// 全部的用法，順序同 04 指令表。
    pub const ALL: [Help; 15] = [
        Help::Add,
        Help::UpgradeTool,
        Help::UpgradeEngine,
        Help::DevTool,
        Help::DevEngine,
        Help::UndevTool,
        Help::UndevEngine,
        Help::Remove,
        Help::Update,
        Help::Sync,
        Help::Install,
        Help::Uninstall,
        Help::Prune,
        Help::Test,
        Help::TestDist,
    ];

    /// 用法全文，每行以 LF 結尾。
    pub fn text(self) -> &'static str {
        match self {
            Help::Add => ADD,
            Help::UpgradeTool => UPGRADE_TOOL,
            Help::UpgradeEngine => UPGRADE_ENGINE,
            Help::DevTool => DEV_TOOL,
            Help::DevEngine => DEV_ENGINE,
            Help::UndevTool => UNDEV_TOOL,
            Help::UndevEngine => UNDEV_ENGINE,
            Help::Remove => REMOVE,
            Help::Update => UPDATE,
            Help::Sync => SYNC,
            Help::Install => INSTALL,
            Help::Uninstall => UNINSTALL,
            Help::Prune => PRUNE,
            Help::Test => TEST,
            Help::TestDist => TEST_DIST,
        }
    }
}

const ADD: &str = r"Usage: just vendor_kit add <repo>[@<tag>] [options]

Add a tool at its latest version, at <tag>, or from a local image.

Options:
  -i, --image <image>               Use a local image or image tar instead of the registry
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help
";

const UPGRADE_TOOL: &str = r"Usage: just vendor_kit upgrade <repo>[@<tag>] [options]

Move a tool to its latest version, or to <tag>, which may be older.

Options:
  -y, --yes                         Answer yes to the questions upgrade asks
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help

For the engine: just vendor_kit upgrade --engine -h
";

const UPGRADE_ENGINE: &str = r"Usage: just vendor_kit upgrade --engine[=<tag>] [options]

Move the engine to its latest version, or to <tag>, which may be older.
The first run switches the engine and stops; rerun the command it prints to finish.

Options:
  -y, --yes                         Answer yes to the questions upgrade asks
  -h, --help                        Print this help
";

const DEV_TOOL: &str = r"Usage: just vendor_kit dev <repo> -p <dir>

Use a local directory as the source of a tool in this working directory.

Options:
  -p, --path <dir>                  Local tool directory, relative to the install directory
  -h, --help                        Print this help

For the engine: just vendor_kit dev --engine -h
";

const DEV_ENGINE: &str = r"Usage: just vendor_kit dev --engine -i <image>

Use a local engine image in this working directory.

Options:
  -i, --image <image>               Local engine image
  -h, --help                        Print this help
";

const UNDEV_TOOL: &str = r"Usage: just vendor_kit undev <repo>

Stop using the local source of a tool and sync it to its pinned version.

Options:
  -h, --help                        Print this help

For the engine: just vendor_kit undev --engine -h
";

const UNDEV_ENGINE: &str = r"Usage: just vendor_kit undev --engine

Stop using the local engine image and return to the pinned engine.

Options:
  -h, --help                        Print this help
";

const REMOVE: &str = r"Usage: just vendor_kit remove <repo>

Remove a tool. Init files are kept.

Options:
  -h, --help                        Print this help
";

const UPDATE: &str = r"Usage: just vendor_kit update [<repo>] [options]

Check for new versions of all tools and the engine, or of <repo> only.
Prints one line per item: <repo> current: <tag> latest: <tag>

Options:
      --registry-token-file <path>  Read a registry token from <path> to list versions
  -h, --help                        Print this help
";

const SYNC: &str = r"Usage: just vendor_kit sync

Bring the content of every pinned tool in line with its pinned version.
Tool recipes run this first.

Options:
  -h, --help                        Print this help
";

const INSTALL: &str = r"Usage: just vendor_kit install [options]

Finish or redo the VK install in this directory.

Options:
  -y, --yes                         Answer yes to the questions install asks
  -h, --help                        Print this help
";

const UNINSTALL: &str = r"Usage: just vendor_kit uninstall

Remove VK from this directory. Init files are kept.

Options:
  -h, --help                        Print this help
";

const PRUNE: &str = r"Usage: just vendor_kit prune

Remove local resources no longer in use: caches of unpinned tools,
VK temporary files, and stopped containers VK created.

Options:
  -h, --help                        Print this help
";

const TEST: &str = r"Usage: just vendor_kit test [<path>]

Check the install. With <path>, then run your tests under <path>.

Options:
  -h, --help                        Print this help

To check a tool delivery: just vendor_kit test dist -h
";

const TEST_DIST: &str = r"Usage: just vendor_kit test dist

Check the tool delivery in this repo.

Options:
  -h, --help                        Print this help
";
