## Q1 Prior art table

| Tool / Subsystem | Baseline Storage | What is Compared | When it Runs | Extra Files Handling | Source URL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **dpkg `--verify`** (`dpkg -V`) | Local database: `/var/lib/dpkg/info/<pkg>.md5sums` (generated from `.deb` at install time) | MD5 checksum of file contents; flags missing files (`missing`) and configuration files (`c`) | Manual only (`dpkg -V [pkg]`). Never runs on binary execution | **Ignored** (only verifies paths recorded in the package's `.md5sums`) | [1] |
| **rpm `-V`** (`rpm --verify`) | Local database: RPM DB (`/var/lib/rpm` or `/usr/lib/sysimage/rpm`, SQLite/NDB) | Up to 9 attributes: Size (`S`), Mode/perms (`M`), Digest/MD5/SHA256 (`5`), Device (`D`), Symlink target (`L`), User (`U`), Group (`G`), mtime (`T`), Capabilities (`P`) | Manual only (`rpm -V <pkg>`). Never runs on binary execution | **Ignored** (unowned files are not in rpmdb; external tools like `cruft` or `find` + `rpm -qf` are needed) | [2], [3] |
| **Nix `nix store verify`** | Local SQLite DB (`/nix/var/nix/db/db.sqlite`) storing NAR hash, size, and signatures | NAR hash (SHA-256 of serialized directory tree), store path registration, and Ed25519 digital signatures (`trusted-public-keys`) | Manual only (`nix store verify`). Nix enforces immutability at runtime via read-only filesystem mounts (permissions `0444`/`0555`) | **Treated as corruption** within a store path (alters the deterministic NAR hash); untracked top-level store paths are flagged as dead / garbage collected | [4], [5] |
| **Go modules `go mod verify`** | `go.sum` in project root (committed to Git) + Go Checksum Database (`sum.golang.org`) | Cryptographic SHA-256 directory tree hash (`h1:` scheme via `dirhash.HashDir`) | Manual only (`go mod verify`). Downloaded cache (`$GOPATH/pkg/mod`) is verified at download time and marked read-only (`0555`/`0444`) | **Treated as modification** (any untracked file changes the directory tree summary computed by `HashDir`) | [6], [7] |
| **Python wheel `RECORD`** (PEP 376 / 427) | `<pkg>.dist-info/RECORD` in `site-packages` (shipped inside wheel archive) | Relative path, cryptographic hash (e.g. `sha256=<digest>`), and file size in bytes | **Install time only** (by `pip` or `installer`). Runtime verification does not exist; `pip check` only verifies dependency constraints | **Ignored** (untracked files in `site-packages` are not listed in `RECORD` and are skipped) | [8], [9] |
| **Composer `installed.json` / `composer.lock`** | `vendor/composer/installed.json` (local receipt) and `composer.lock` (`dist.shasum`) | At install time: archive sha1/sha256. Post-install: `composer status` checks git-installed source packages via `git diff/status` | Archive hash checked at install time. `composer status` is manual only | **Ignored** for dist archives; flagged as untracked (`?`) only if installed from git source | [10], [11] |
| **npm / pnpm / yarn SRI** | `package-lock.json` / `pnpm-lock.yaml` (Subresource Integrity `integrity` sha512) + pnpm CAFS `index.db` | Tarball SHA-512 at download/unpack. In pnpm: `verify-store-integrity` checks file size and SHA-512 in global CAFS | Install time (`npm ci`, `pnpm install`). Never runs during `npm run` or `node <script>` | `npm ci` deletes and recreates `node_modules`. At runtime, extra files are **ignored** | [12], [13] |
| **Homebrew bottles** | Formula definitions (Ruby/API `bottle do sha256 ... end`) + `<keg>/INSTALL_RECEIPT.json` | SHA-256 hash of the pre-compiled bottle archive (`.tar.gz`) | Download/install time only (`brew install`). Post-install checks (`brew doctor`) only check broken symlinks, not content hashes | **Ignored** (Homebrew does not scan keg directories for extra files post-install) | [14], [15] |
| **Terraform `.terraform.lock.hcl`** | `.terraform.lock.hcl` in project root (committed to Git) | `zh:` (ZIP archive hash) and `h1:` (hash of extracted provider directory/binary) | `terraform init` only. Commands like `terraform plan` and `terraform apply` **do not verify provider hashes** | **Ignored** (Terraform executes the binary located at `.terraform/providers/...` without re-verifying the directory) | [16] |
| **Git index (stat cache)** | Binary file `.git/index` | `stat(2)` cache: `mtime`, `ctime`, `size`, `ino`, `dev`, `mode`, `uid`, `gid`. Reads and computes SHA-1/SHA-256 object hash only if stat changes | Runs on every command inspecting the worktree (`git status`, `git diff`, `git commit`) | **Explicitly detected and reported** (`git status` reports `Untracked files` unless excluded by `.gitignore`) | [17], [18] |
| **Bazel output cache** | In-memory Skyframe graph / disk cache (`FileArtifactValue`) | SHA-256 digest, mtime, size, inode. Flag `--experimental_check_output_files` toggles checking if outputs were modified externally | Checked during build evaluation. By default, Bazel trusts its internal output tree between builds | Extra/undeclared outputs generated in action execution directories are **purged / disallowed** by the action execution sandbox | [19], [20] |
| **Cargo vendoring** (`cargo vendor`) | `.cargo-checksum.json` inside each vendored crate directory | SHA-256 of package tarball (`package`) and each file listed under `"files"` map | Build time (`cargo build`) when compiling from a `DirectorySource` | **Ignored** (Cargo iterates only over the keys of the `"files"` JSON map; it does not scan the directory for extra files) | [21], [22] |
| **pre-commit cache** | `~/.cache/pre-commit/` metadata & repo clone directories | Repository Git commit SHA; existence of virtualenv marker files | Setup time only. On hook execution (`pre-commit run`), it invokes the cached virtualenv binary **without checking file hashes** | **Ignored** (any file manually created inside `~/.cache/pre-commit/...` remains unnoticed) | [23] |

---

### In-Depth Breakdown of Q1 Systems

#### 1. dpkg `--verify` and rpm `-V`
* **Baseline storage**: Both systems store baselines locally in system databases populated at install time from package metadata: dpkg uses plain text files in `/var/lib/dpkg/info/<package>.md5sums`, while RPM uses the Berkeley DB / SQLite / NDB database in `/var/lib/rpm`. Neither fetches baselines from the network during verification.
* **What is compared**: dpkg historically only verifies MD5 checksums of files (plus checking for missing files). RPM performs an extensive 9-attribute verification (`SM5DLUGTP`): file Size, Mode/permissions, SHA-256/MD5 digest, major/minor Device numbers, Symlink target string via `readlink(2)`, User ownership, Group ownership, Modification time (`mtime`), and POSIX Capabilities.
* **When it runs**: Strictly manual administrative audits (`dpkg -V`, `rpm -Va`). Neither dpkg nor RPM runs verification when binaries are executed.
* **Extra files handling**: Both ignore extra files. Because system directories like `/usr/bin` and `/usr/lib` are shared namespaces populated by thousands of packages, package managers track what *they* installed, not what else exists in the directory. Finding untracked files requires external reconciliation tools (such as `cruft`, `cruft-ng`, or `find /usr/bin | while read f; do dpkg -S "$f"; done`).

#### 2. Nix `nix store verify`
* **Baseline storage**: The local SQLite database (`/nix/var/nix/db/db.sqlite`). When substituting packages from binary caches (e.g. `cache.nixos.org`), Nix downloads a `.narinfo` manifest containing the expected `NarHash` and digital signatures.
* **What is compared**: The **NAR (Nix Archive) hash**. NAR is a deterministic serialization format for directory trees that encodes file contents, relative paths, symlink targets, and the executable bit (mode 0555 vs 0444) in sorted lexical order. It also verifies cryptographic signatures against `trusted-public-keys`.
* **When it runs**: Strictly manual (`nix store verify --all` or `nix-store --verify --check-contents`). During regular command execution, Nix does *not* recompute hashes. Instead, Nix guarantees integrity via the operating system: the `/nix/store` filesystem is mounted read-only, and files inside store paths are created with permissions `0444` (or `0555` for executables).
* **Extra files handling**: Because the NAR hash is a recursive cryptographic digest over the entire directory tree, dropping an extra file into `/nix/store/<hash>-<name>/` changes the calculated NAR hash and triggers a verification failure (`corrupted`). Untracked directories at the top-level `/nix/store` are treated as unreferenced paths and cleaned up by `nix-collect-garbage`.

#### 3. Go Modules (`go mod verify` / `go.sum`)
* **Baseline storage**: `go.sum` located in the project root (committed to Git). During download, Go checks the global transparency log at `sum.golang.org`.
* **What is compared**: Content hash using the `h1:` algorithm (`dirhash.Hash1`). It computes SHA-256 digests of all file contents, formats each entry as `"<hash>  <filename>\n"`, sorts them alphabetically, and hashes that entire summary.
* **When it runs**: `go mod verify` is manual. However, verification against `go.sum` is performed automatically at dependency download time. Once extracted into `$GOPATH/pkg/mod/`, Go strips write permissions from all files and directories (`chmod a-w`), making the module cache read-only to avoid accidental modifications.
* **Extra files handling**: Because `dirhash.HashDir` traverses the directory and includes every file in the summary, any extra or untracked file alters the summary and causes `go mod verify` to fail with:
  ```text
  <module>: dir has been modified (<path>)
  ```

#### 4. Python Wheels (`RECORD` / PEP 376 & 427)
* **Baseline storage**: Shipped inside the wheel archive and written to `site-packages/<distribution>.dist-info/RECORD`.
* **What is compared**: A CSV file where each row records `path,hash,size` (e.g. `package/foo.py,sha256=47DEQpj8HBSa-_TImW-5JCeuQeRkm5NMpJWZG3hSuFU,0`).
* **When it runs**: Verified strictly at installation time by wheel installers (`pip`, `installer`, `flit`). Python runtimes never verify `RECORD` when importing modules or executing scripts. Furthermore, `pip check` does *not* check file integrity—it only validates dependency compatibility across installed packages.
* **Extra files handling**: Ignored. Extra files created inside package directories (such as `.pyc` bytecode caches or user-added scripts) are omitted from `RECORD` and ignored by tooling.

#### 5. Composer & npm/pnpm Lockfiles
* **Baseline storage**: npm uses `package-lock.json`, pnpm uses `pnpm-lock.yaml`, Composer uses `composer.lock`. Hashes are formatted as W3C Subresource Integrity (SRI) strings (e.g. `sha512-...`).
* **What is compared**: At install time (`npm ci`, `composer install`), the installer verifies the hash of the downloaded `.tgz` or `.zip` archive before unpacking. In pnpm, `verify-store-integrity` (default `true`) validates files in its global content-addressable store (CAFS) by comparing file sizes and SHA-512 digests against `index.db`.
* **When it runs**: Only during dependency installation / resolution. Never on command execution (`npm run`, `node index.js`).
* **Extra files handling**: In npm, `npm ci` removes existing `node_modules` entirely before extraction. At runtime, arbitrary untracked files placed in `node_modules` are ignored. Composer's `composer status` command only detects modifications and untracked files for packages[agy] print timeout after 5m0s with turn in progress; returning partial output
## Part A sources
1. https://man7.org/linux/man-pages/man1/dpkg.1.html
2. https://man7.org/linux/man-pages/man8/rpm.8.html
3. https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-store-verify.html
4. https://go.dev/ref/mod#go-mod-verify
5. https://peps.python.org/pep-0376/#record
6. https://getcomposer.org/doc/03-cli.md#status
7. https://pnpm.io/npmrc#verify-store-integrity
8. https://docs.brew.sh/Bottles
9. https://developer.hashicorp.com/terraform/language/files/dependency-lock
10. https://git-scm.com/docs/racy-git
11. https://github.com/bazelbuild/bazel/blob/master/src/main/java/com/google/devtools/build/lib/pkgcache/PackageOptions.java
12. https://doc.rust-lang.org/cargo/reference/source-replacement.html
13. https://github.com/pre-commit/pre-commit/blob/main/pre_commit/store.py

## Q2 Manifest self-protection
- **Manifest hash storage:**
  - Python Wheel `RECORD` self-references its own row with empty hash/size (`RECORD,,`) to avoid cyclic dependency [5].
  - Debian repository root signs `InRelease` (or `Release.gpg`), which lists SHA256 hashes of `Packages.xz`, which index individual `.deb` hashes [16].
  - Nix `.narinfo` manifests record `NARHash` and append detached cryptographic signatures in a `Sig:` field [3, 17].
  - Terraform `.terraform.lock.hcl` records provider package hashes and relies on Git tree commits for lockfile integrity [9].
- **Signatures with Docker-only host:**
  - **Cosign / Sigstore:** Can run inside container (`docker run --rm gcr.io/projectsigstore/cosign verify ...`) to verify OCI image digest signatures keylessly via OIDC or with a static public key [14].
  - **Minisign:** Minimal Ed25519 signature tool; static binaries easily run in containers to verify `.stamp.minisig` [15].
  - **Nix-style signing:** `nix store sign` uses Ed25519 secret keys to sign store paths into binary caches [17].
- **Re-fetch and diff precedent:**
  - `nix-store --verify --check-contents --repair`: checks files against DB NAR hashes; upon corruption or missing files, it re-fetches the original path from remote binary substituters [18].
  - `go mod verify`: flags mutated files against `go.sum`; recovery requires re-downloading via `go clean -modcache` [4].
  - `git fsck`: detects corrupt objects; remediation requires re-fetching from a remote [19].

## Q3 Performance techniques
- **Git stat cache / racy-git:** Compares `mtime`, `size`, `ino`, `dev`, `mode` against index. If stat matches and file mtime is older than index timestamp, content is assumed clean without opening or hashing the file [10].
- **Bazel & Buck2:** Bazel's Skyframe caches file digests; `--experimental_check_output_files` toggles whether output files are re-checked across builds [11]. Buck2 uses file watchers (Watchman) and content-addressable storage (CAS) to skip reading unchanged outputs [21].
- **pnpm `verify-store-integrity`:** In `@pnpm/cafs` (`checkPkgFilesIntegrity`), pnpm checks file size first; if size differs or full check is triggered, it recomputes file SHA-512 against the store index [7, 20].
- **Install-only trust:** Wheel/pip (hashes validated on unpack only; `pip check` only checks dependency constraints [5, 23]); Homebrew (verifies bottle SHA-256 during download/pour; never re-verifies [8]); pre-commit (caches clones by git SHA and assumes immutability [13]).
- **Throughput & syscall costs:**
  - SHA-256 throughput on modern CPUs: ~1.5–3.0 GB/s per core with hardware acceleration (Intel SHA-NI / ARMv8 Crypto), ~350–500 MB/s pure software.
  - `stat`/`lstat` syscall: ~0.5–2 µs per file (~500k–2M ops/s in Linux dentry/inode cache), 100x–1000x faster than disk reads + hashing.

## Q4 Options and recommendation
- **Option A (Stamp file sha256 only):** Fast for small installs; fails to detect injected malicious files or changed file modes (`chmod +x`).
- **Option B (Stamp + file set + executable mode):** Comprehensive offline integrity; detects deletions, added files, and permission tampering.
- **Option C (Re-pull locked image digest & diff):** Network-dependent, slow registry calls, adds container unpack overhead on every invocation.
- **Extra files policy across tools:**
  - `dpkg -V` and `rpm -V`: **Ignore extra/unowned files**; only verify paths listed in package database [1, 2].
  - `pip`: **Ignores extra files**; `pip check` verifies dependencies only; uninstaller removes only files in `RECORD` [5, 23].
  - `terraform`: **Ignores extra files**; verifies only target provider binary [9].
  - `nix store verify`: **Detects extra files as corruption** because store paths are read-only and directory NAR hash includes all directory entries [3].
  - `go mod verify`: **Detects extra files as corruption** (`dir has been modified`) because `h1:` directory hash covers the full directory walk [4, 22].
- **Recommendation for vendor_kit:**
  - **Adopt Option B with Git-style stat caching:**
    1. **Treat EXTRA files as modified:** Follow Go and Nix. Extra files in `.<name>/` could be hijacked binary wrappers or malicious configs.
    2. **Stat cache:** Store `path,mode,size,mtime,sha256` in `.<name>/.stamp`. On run, compare directory file set, modes, and `mtime/size`. Re-hash only if stat differs.
    3. **Locking:** Pin image to full immutability digest (`ghcr.io/org/repo@sha256:...`) in the project `justfile`.

## Sources
1. https://man7.org/linux/man-pages/man1/dpkg.1.html
2. https://man7.org/linux/man-pages/man8/rpm.8.html
3. https://nix.dev/manual/nix/latest/command-ref/new-cli/nix3-store-verify.html
4. https://go.dev/ref/mod#go-mod-verify
5. https://peps.python.org/pep-0376/#record
6. https://getcomposer.org/doc/03-cli.md#status
7. https://pnpm.io/npmrc#verify-store-integrity
8. https://docs.brew.sh/Bottles
9. https://developer.hashicorp.com/terraform/language/files/dependency-lock
10. https://git-scm.com/docs/racy-git
11. https://github.com/bazelbuild/bazel/blob/master/src/main/java/com/google/devtools/build/lib/pkgcache/PackageOptions.java
12. https://doc.rust-lang.org/cargo/reference/source-replacement.html
13. https://github.com/pre-commit/pre-commit/blob/main/pre_commit/store.py
14. https://docs.sigstore.dev/cosign/overview/
15. https://jedisct1.github.io/minisign/
16. https://wiki.debian.org/SecureApt
17. https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-store-sign.html
18. https://nix.dev/manual/nix/latest/command-ref/nix-store/verify.html
19. https://git-scm.com/docs/git-fsck
20. https://github.com/pnpm/pnpm/blob/main/store/cafs/src/checkPkgFilesIntegrity.ts
21. https://buck2.build/docs/concepts/key_concepts/
22. https://pkg.go.dev/golang.org/x/mod/sumdb/dirhash#HashDir
23. https://pip.pypa.io/en/stable/cli/pip_check/
