# 參考：base（ycpss91255-docker/base）給下游的 just 介面（不是 agy 研究，是實際檔案節錄）

## dist/script/justfile（下游根 justfile，由 init.sh symlink）
```just
mod? docker 'script/docker/justfile.docker'
mod? base 'script/base/justfile.base'
mod? template 'script/template/justfile.template'
import? 'script/local/justfile.local'
default:
    @just --list
```

## dist/script/base/justfile.base（just base 命名空間）
```just
# Manage the `.base` subtree dependency (just). The `base` module of the
# layered consumer entry (ADR-00000011): `mod?`'d by dist/script/justfile
# (symlinked as <repo>/script/base/justfile.base) so the recipes resolve as
# the `base` namespace -- `just base upgrade` / `just base update`.
#
# Apt-aligned (ADR-00000011): `update` reports whether a newer base tag is
# available (refresh/check, the former docker `upgrade-check`); `upgrade`
# applies the subtree pull (the former docker `upgrade`); `init` (re-)wires
# the repo's symlinks + .gitignore; `completions` installs/uninstalls shell
# tab-completion (opt-in, no host rc edits). The `init.sh` / `upgrade.sh`
# scripts live under `.base/dist/script/base/` (relocated in
# ADR-00000011 §8 / ADR-00000006); they self-locate the subtree root via a
# walk-up, so the deep invocation path is the only change here.
#
# A module recipe's default cwd is this file's own directory; the recipes
# call ./.base/dist/script/base/<script> at the repo root, so
# `set working-directory := '../..'` pins them to the repo root. Reached via
# the consumer symlink (<repo>/script/base/justfile.base), `../..` resolves
# to the repo root.
set working-directory := '../..'

# source_file (not justfile) is this module's own file: inside a mod?'d
# module justfile resolves to the ROOT entry, so listing it would show the
# entry's namespaces instead of the base verbs. source_file pins
# --list to THIS module.
# just base -> list the base-management verbs
default:
    @just --justfile '{{source_file()}}' --list

# `help` is a named twin of `default` reachable as `just base help` (and
# `just base h`), since the dashed `just base --help` cannot be a just
# recipe/alias -- with a `help` recipe present just then hints "Did you mean
# 'help'?" instead of a bare error. Bare `just base` still lists via `default`.
alias h := help

# just base help (or `just base h`) -> language-aware recipe listing:
# translated one-line summaries via the shared `_msg help` i18n renderer
# (honours $LANG / --lang). Bare `just base` and `just --list` stay English.
help *args:
    @"$(dirname "$(readlink -f '{{source_file()}}')")/../docker/lib/help.sh" base {{args}}

# just base upgrade [vX.Y.Z] -> pull the .base subtree (empty = latest)
upgrade *args:
    ./.base/dist/script/base/upgrade.sh {{args}}

# `*args` on `update` is a `--help` shim only: update always runs the check
# and never upgrades, so non-help args are ignored; `-h|--help` reaches
# upgrade.sh's usage WITHOUT the network check (a dashed name cannot be a just
# recipe, so the entry cannot intercept `just base update --help` -- the recipe
# does). The blank line below detaches this rationale from the --list doc.

# just base update -> report whether a newer base tag is available (apt-style)
update *args:
    #!/usr/bin/env bash
    set -euo pipefail
    for _a in {{args}}; do
      case "${_a}" in
        -h|--help) exec ./.base/dist/script/base/upgrade.sh --help ;;
      esac
    done
    ./.base/dist/script/base/upgrade.sh --check || [ "$?" -eq 1 ]

# just base init -> (re-)wire repo symlinks + .gitignore
init *args:
    ./.base/dist/script/base/init.sh {{args}}

# just base completions install|uninstall [--shell bash|zsh|fish|all]
#   opt-in shell tab-completion; never edits a shell rc.
completions *args:
    script/base/completions.sh {{args}}
```

## ADR-00000011 決策節錄（§1–§3 與最終指令清單）
## Decision

### 1. Zero special cases: every action is a namespace

The entry mods every group; **nothing is top-level**. docker joins the
other namespaces:

```just
mod? docker   'script/docker/justfile.docker'
mod? test     'script/test/justfile.test'
mod? release  'script/release/justfile.release'
mod? base     'script/base/justfile.base'
mod? template 'script/template/justfile.template'      # consumer only in practice
import? 'script/local/justfile.local'                  # repo-owned user groups
default:
    @just --list
```

`just build` becomes `just docker build`. The cost (longer invocations)
is accepted in exchange for one rule with no exceptions, and completion
(below) makes the extra token a single `<tab>`.

### 2. Action-named namespaces

| was (ADR-00000010) | now | rationale |
|---|---|---|
| `just build/run/...` (top-level) | `just docker build/run/exec/stop/prune/setup/setup-tui` | docker is the action group, no special case |
| `just ci` | `just test` | the action is "test"; **all** CI checks live here, incl. lint |
| `just cd` | `just release` | the action is "cut a release" |
| `init` / `upgrade` / `upgrade-check` (root scripts) | `just base init` / `just base upgrade [ver]` / `just base update` | manage the `.base` dependency; `update`/`upgrade` mirror apt (refresh-check vs apply) |

`lint` is **not** a top-level peer of `test`; it is `just test lint`
(a sub-action of the test namespace). A new top-level command would need
its own `justfile.<x>` + scripts; lint is part of testing, so it stays
inside `test`.

### 3. min->max coverage via `--option` narrowing

Every command runs the **maximum** scope bare and **narrows** through
`--long` / `-short` options -- never bare positional args whose meaning is
positional:

```
just test                       # everything (shellcheck + bats + ... + coverage as configured)
just test --file <path>         # one spec file
just test --filter <regex>      # specs matching a pattern
just test lint                  # all linters
just test lint --shellcheck [<level>]   # only shellcheck (optionally at a severity level)
just test lint --hadolint               # only hadolint
just docker build                       # default stage
just docker build --stage <name>        # a specific stage (base self-test: --stage test-tools)
just base upgrade                       # latest tag
just base upgrade --tag <vX.Y.Z>        # a specific tag
```

The single-file test mode (previously supported) is preserved as
`--file`. `test-tools` is built explicitly as
`just docker build --stage test-tools`; the test runner invokes it
internally rather than `build` growing a magic `test` argument.

### 4. Generic tooling, per-repo content, single source of truth

## Final command list

```
just                              # list
just docker  build [--stage <s>] | run [-d] | start | exec [-t <svc> -- <cmd>]
             | stop | prune | setup | setup-tui
just test    [--file <f>] [--filter <re>]
just test    lint [--shellcheck [<level>] | --hadolint]
just test    coverage | behavioural
just release [--tag <vX.Y.Z>] [...]
just base    init | update | upgrade [--tag <vX.Y.Z>]
             | completions install [--shell <sh>] | completions uninstall
just template new <name>          # consumer: scaffold a repo-local group
just <group> <recipe>             # consumer repo-local groups
# every level: --help, --lang <code>
```

