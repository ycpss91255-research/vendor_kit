## Prior-art table

| Tool | Where local path lives | How accidental commit is prevented | How to switch back | Source URL |
| :--- | :--- | :--- | :--- | :--- |
| **npm / pnpm / yarn** | Global symlink (`pnpm link <dir>`) or manifest protocols (`link:`, `portal:`, `file:`) in `package.json` | `link` CLI does not touch `package.json`; manifest protocols require git-hook / CI linters to forbid `link:`/`portal:` | `pnpm unlink <dir>` or reinstall published version via `pnpm add <pkg>` | [pnpm link](https://pnpm.io/cli/link), [Yarn portal](https://yarnpkg.com/features/protocols#portal) |
| **Python pip** | Virtualenv metadata (`direct_url.json` via PEP 660 / PEP 610); optional `requirements-dev.txt` | Uncommitted dev requirements file or CLI flag; `pip freeze --exclude-editable` strips editable paths | `pip install <pkg>` (reinstall from index) | [PEP 660](https://peps.python.org/pep-0660/), [PEP 610](https://peps.python.org/pep-0610/) |
| **Go** | Separate `go.work` file (or `replace` in `go.mod`) | `go.work` is recommended for `.gitignore`; `replace` in `go.mod` was heavily prone to accidental commits | `rm go.work` (or `go work drop <mod>`), or remove `replace` directive | [Go Proposal 45713](https://go.googlesource.com/proposal/+/master/design/45713-workspace.md), [Go Workspaces](https://go.dev/doc/tutorial/workspaces) |
| **Cargo** | `[patch]` in `.cargo/config.toml` (or `[patch]` in `Cargo.toml`) | `.cargo/config.toml` is conventionally git-ignored; `Cargo.toml` patches require manual commit scrutiny | Delete `[patch]` from config or run `cargo update` | [Cargo Config Patch](https://doc.rust-lang.org/cargo/reference/config.html#patch), [Overriding Dependencies](https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html) |
| **Nix Flakes** | CLI flag `--override-input <name> <path>` or `path:` in `flake.nix` | CLI override is transient (in-memory); does not write to `flake.nix` or `flake.lock` | Drop `--override-input` flag on next invocation | [Nix Flake Reference](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html) |
| **Terraform** | CLI config file (`~/.terraformrc` / `provider_installation { dev_overrides }`) or `TF_CLI_CONFIG_FILE` | Lives entirely in user/host config outside the `.tf` repository tree | Remove `dev_overrides` block from `.terraformrc` or unset `TF_CLI_CONFIG_FILE` | [Terraform dev_overrides](https://developer.hashicorp.com/terraform/cli/config/config-file#development-overrides-for-provider-developers) |
| **Bazel** | `user.bazelrc` (`--override_module=<mod>=<path>`) or `local_path_override` in `MODULE.bazel` | `user.bazelrc` is git-ignored (`try-import %workspace%/user.bazelrc` in `.bazelrc`); MODULE overrides require CI linter | Remove line from `user.bazelrc` or remove `local_path_override` | [Bazelrc Docs](https://bazel.build/run/bazelrc), [Bzlmod Overrides](https://bazel.build/external/overview#local-path-override) |
| **Helm** | `repository: "file://../chart"` in `Chart.yaml` or CLI `helm install ./local-chart` | CLI installs from local path directly; `Chart.yaml` file dependencies require CI check | Point `repository` back to remote Helm repository URL | [Helm Chart Dependencies](https://helm.sh/docs/topics/charts/#chart-dependencies) |
| **Gradle** | `--include-build <path>` CLI flag or `includeBuild()` in `settings.gradle` | CLI flag requires no file changes; local init scripts (`~/.gradle/init.d/`) keep `settings.gradle` clean | Omit `--include-build` flag | [Gradle Composite Builds](https://docs.gradle.org/current/userguide/composite_builds.html) |
| **Dagger** | CLI flag `-m ./path` or local path in `dagger.json` | CLI `-m` flag requires no file edit; `dagger.json` local paths require CI check | Pass git URL `-m github.com/...` or restore remote ref in `dagger.json` | [Dagger Module Dependencies](https://docs.dagger.io/manuals/developer/module-dependencies) |
| **Copier** | `_src_path` in `.copier-answers.yml` or CLI `copier copy <dir>` | `_src_path` tracks generator path; local paths can be overridden during `copier update --src-path` | Pass remote VCS URL to `copier update --src-path <url>` | [Copier Updating](https://copier.readthedocs.io/en/stable/updating/) |
| **Docker Compose** | `compose.override.yaml` (auto-merged over `compose.yaml`) | `compose.override.yaml` is conventionally added to `.gitignore` | `rm compose.override.yaml` | [Docker Compose Merge](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/) |
| **mise** | `.mise.local.toml` (`[tools] <name> = "path:..."`) | `.mise.local.toml` is git-ignored by default; takes precedence over committed `mise.toml` | Delete entry from `.mise.local.toml` | [mise Local Config](https://mise.jdx.dev/configuration.html#mise-local-toml) |
| **pre-commit** | `pre-commit try-repo <path>` CLI command | Ephemeral CLI command; does not alter `.pre-commit-config.yaml` | Run standard `pre-commit run` | [pre-commit try-repo](https://pre-commit.com/#pre-commit-try-repo) |

---

## Same-file vs separate-file: what prior art prefers and why

Prior art **overwhelmingly favors separate, uncommitted overlay files (or CLI flags/env vars)** over modifying the committed manifest file:

1. **Go Workspaces ([Go Proposal 45713](https://go.googlesource.com/proposal/+/master/design/45713-workspace.md)):** Prior to Go 1.18, developers used `replace` in `go.mod`. The proposal explicitly identified this as an antipattern because developers routinely committed machine-specific local paths to Git, breaking builds for team members and CI. `go.work` was introduced as an uncommitted workspace file (recommended for `.gitignore`) to isolate local file paths from the version-controlled `go.mod`.
2. **Terraform CLI Config ([Terraform dev_overrides](https://developer.hashicorp.com/terraform/cli/config/config-file#development-overrides-for-provider-developers)):** HashiCorp strictly placed `dev_overrides` in the host CLI config (`~/.terraformrc`) or via `TF_CLI_CONFIG_FILE`, never in `.tf` project files. The design rationale was that `.tf` manifests define shared infrastructure intent; local binaries belong to developer machine environments.
3. **Cargo Config Layering ([Cargo RFC 2959 / Reference](https://doc.rust-lang.org/cargo/reference/config.html#patch)):** While `Cargo.toml` has `[patch]`, Cargo also added `[patch]` to `.cargo/config.toml` specifically so that developers and local tools could override crates without producing dirty working trees in Git.
4. **Bazel ([Bazelrc Guide](https://bazel.build/run/bazelrc)):** Bazel separates `.bazelrc` (team-shared) from `user.bazelrc` (git-ignored, personal). Flag overrides like `--override_module` live in `user.bazelrc`.
5. **Docker Compose ([Compose Merge Docs](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/)):** Standardizes on `compose.override.yaml` (git-ignored) for bind-mounting local developer checkouts over container image paths, keeping base `compose.yaml` pristine.

**Conclusion:** Candidate (b) (separate `.version.local` file) aligns directly with modern tooling standards. Mutating `.version` (Candidate a) causes Git status pollution, accidental commits, CI breakage, and requires defensive pre-commit/CI guardrails.

---

## Integrity / lock behaviour in dev mode

| Tool | Lock / Integrity File | Dev Mode Behaviour | Source |
| :--- | :--- | :--- | :--- |
| **Go** | `go.sum` | Modules loaded from local directories (via `go.work` or directory `replace`) **omit checksum entries** in `go.sum` because mutable directories have no zip hash. | [Go Proposal 45713](https://go.googlesource.com/proposal/+/master/design/45713-workspace.md) |
| **Cargo** | `Cargo.lock` | `Cargo.lock` **omits the `checksum = "..."` key** for path dependencies and path-patched crates. | [Cargo Specifying Dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-path-dependencies) |
| **Terraform** | `.terraform.lock.hcl` | `dev_overrides` **completely bypasses `.terraform.lock.hcl`** and skips `terraform init`. It displays a prominent diagnostic **warning banner** on every command. | [Terraform dev_overrides](https://developer.hashicorp.com/terraform/cli/config/config-file#development-overrides-for-provider-developers) |
| **pnpm / npm** | `pnpm-lock.yaml` / `package-lock.json` | `link:` and directory dependencies store resolution as `type: directory` **without integrity hashes**. Symlinked packages (`pnpm link`) do not alter the lockfile at all. | [pnpm link](https://pnpm.io/cli/link) |
| **Nix Flakes** | `flake.lock` | `nix build --override-input` overrides inputs **in-memory only**, without modifying or checking against the `narHash` in `flake.lock`. | [Nix Flake Reference](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html) |
| **Python pip** | `direct_url.json` (PEP 610) | Records `dir_info: {editable: true}` without hash. `pip freeze --exclude-editable` excludes local editable paths from pinned outputs. | [PEP 610](https://peps.python.org/pep-0610/) |
| **Bazel** | `MODULE.bazel.lock` | `local_path_override` disables integrity verification; overrides are stripped/excluded from the lockfile. | [Bazel Lockfile Docs](https://bazel.build/external/overview#local-path-override) |

**Key takeaway for vendor_kit:** Prior art never requires recalculating or locking checksums for live local directories. Instead, tools **bypass verification** and print an **unmissable warning banner** indicating that developer overrides are active.

---

## Design options for vendor_kit and recommendation

### Candidate Options Evaluated

1. **Option A: `path:` in `.version`**
   - *Mechanics:* `.version` allows `<name> = "path:../tool"`.
   - *Pros:* Single file.
   - *Cons:* Directly violates prior-art consensus; pollutes `git diff`; high risk of committing machine-specific paths; breaks CI unless special linter is added.
2. **Option B: `.version.local` override file (Recommended foundation)**
   - *Mechanics:* `.version.local` is added to `.gitignore`. Launcher checks for `.version.local` first; keys inside override entries in `.version`.
   - *Pros:* Clean git status; zero chance of accidental commit; identical to `docker-compose.override.yml`, `go.work`, and `.mise.local.toml`.
3. **Option C: Environment variables / CLI flags only (`VENDOR_KIT_DEV_<name>=...`)**
   - *Mechanics:* Passed via `VENDOR_KIT_DEV_<NAME>=../tool just ...` or `just dev <name> ../tool`.
   - *Pros:* Fully transient.
   - *Cons:* Developer must set env vars in every shell session or prefix every `just` command.
4. **Option D: Hybrid (Option B + Option C CLI helper + Warning Banner)**
   - Combines `.version.local` persistence with `just` convenience commands and env var overrides.

---

### Detailed Recommendation (Option D: Hybrid)

#### 1. Manifest & Resolution
- **File:** Add `.version.local` to the project's `.gitignore` template.
- **Precedence:** `ENV (VENDOR_KIT_OVERRIDE_<NAME>)` > `.version.local` > `.version`.
- **Syntax in `.version.local`:**
  ```ini
  <name> = "path:../tool"
  ```
- **Path Resolution:** Relative paths are resolved strictly relative to the project root (`$PWD`).

#### 2. Docker Execution Mechanics
When `<name>` resolves to a local path (`$LOCAL_PATH`):
1. **Resolve path on host:** `LOCAL_DIST="$(realpath "$PROJECT_DIR/$LOCAL_PATH/dist")"`
2. **Container invocation:** Run the base `vendor_kit` runtime image instead of `<name>-dist:vX`, bind-mounting the host dist read-only:
   ```bash
   docker run --rm \
     -v "$PROJECT_DIR:/repo" \
     -v "$LOCAL_DIST:/dist:ro" \
     vendor_kit:latest \
     --name <name> --dev-mode install
   ```

#### 3. Stamp & Verify Behaviour (Following Terraform/Go prior art)
- **Install:** Copies `/dist` to `.<name>/` and writes `.<name>/.stamp` with:
  ```ini
  ref="dev:$LOCAL_PATH"
  mtime="..."
  ```
- **Verify & Run:**
  - When `ref` starts with `dev:`, **bypass sha256 checksum mismatch aborts**.
  - Always print a high-visibility ANSI warning banner (modeled after Terraform):
    ```text
    ┌──────────────────────────────────────────────────────────────┐
    │ WARNING: Local dev override active for '<name>'               │
    │ Source: ../tool/dist                                         │
    │ Integrity / sha256 verification is BYPASSED.                 │
    └──────────────────────────────────────────────────────────────┘
    ```
  - For rapid iteration, `install` or the launcher can re-sync `dist` if file `mtime` or directory contents changed, without requiring `docker build`.

#### 4. Developer Ergonomics
- `just dev <name> <path>`: Writes/updates `<name> = "path:<path>"` in `.version.local` and runs `install`.
- `just undev <name>`: Removes `<name>` from `.version.local` and reinstalls the pinned release from `.version`.

---

## Sources

- [Go Proposal 45713 (Multi-Module Workspaces)](https://go.googlesource.com/proposal/+/master/design/45713-workspace.md)
- [Go Workspaces Tutorial](https://go.dev/doc/tutorial/workspaces)
- [Terraform CLI Configuration: Development Overrides](https://developer.hashicorp.com/terraform/cli/config/config-file#development-overrides-for-provider-developers)
- [Cargo Configuration Reference: `[patch]`](https://doc.rust-lang.org/cargo/reference/config.html#patch)
- [Cargo Guide: Overriding Dependencies](https://doc.rust-lang.org/cargo/reference/overriding-dependencies.html)
- [Cargo Reference: Specifying Path Dependencies](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-path-dependencies)
- [Docker Compose: Merging Multiple Compose Files](https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/)
- [mise-en-place Configuration: `mise.local.toml`](https://mise.jdx.dev/configuration.html#mise-local-toml)
- [pnpm CLI: `pnpm link`](https://pnpm.io/cli/link)
- [Yarn Berry Documentation: `portal:` protocol](https://yarnpkg.com/features/protocols#portal)
- [PEP 660: Editable Installs for `pyproject.toml`](https://peps.python.org/pep-0660/)
- [PEP 610: Recording the Installed Distribution Package Source URL](https://peps.python.org/pep-0610/)
- [Nix Command Reference: `nix flake`](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-flake.html)
- [Bazel Guide: Configuring Bazel with `.bazelrc`](https://bazel.build/run/bazelrc)
- [Bazel Bzlmod: `local_path_override`](https://bazel.build/external/overview#local-path-override)
- [Helm Docs: Chart Dependencies](https://helm.sh/docs/topics/charts/#chart-dependencies)
- [Gradle User Manual: Composite Builds](https://docs.gradle.org/current/userguide/composite_builds.html)
- [Dagger Documentation: Managing Module Dependencies](https://docs.dagger.io/manuals/developer/module-dependencies)
- [Copier Documentation: Updating a Project](https://copier.readthedocs.io/en/stable/updating/)
- [pre-commit Documentation: `pre-commit try-repo`](https://pre-commit.com/#pre-commit-try-repo)
