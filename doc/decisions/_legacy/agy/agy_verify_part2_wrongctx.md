...ensures deterministic dependencies by writing installed package metadata and an overarching `content-hash` into `composer.lock`, warning or aborting during install if `composer.json` is modified without updating the lockfile [14][15].

## Q2 Manifest self-protection
- **Hash-based drift detection**: Tools embed cryptographic digests (e.g., Composer's `content-hash` [14], Cargo package checksums [5], Go `go.sum` hashes [3]) into lockfiles; altering the manifest flags a desync error.
- **Enforced CI immutability**: Strict operational modes like `cargo --locked` [6], `npm ci` [8], and `bundle install --deployment` [12] prohibit resolving new versions and abort if lockfiles differ from manifests.
- **Filesystem permission hardening**: Go marks unpacked module cache trees as read-only (`0555`/`0444`) to block accidental or malicious in-place modifications [2].
- **Atomic directory replacement**: Tools like Carvel vendir [16][17] synchronize dependency trees by staging to a temporary directory before executing an atomic rename, preventing corrupted states on interruption.

## Q3 Performance techniques
- **Top-level stamp / digest checks**: Bypassing per-file traversal on routine execution by validating a single top-level stamp or digest against the manifest/image ($O(1)$ fast-path) [14][17].
- **Stat & mtime caching**: Build systems and Git inspect `mtime`, `ctime`, and file size before triggering full cryptographic content hashing [20].
- **Hierarchical Merkle tree hashing**: Git tree objects [21] and Go module ziphashes [3] hash directory structures incrementally, allowing instant sub-tree comparison and pruning.
- **Content-addressable storage (CAS) & hardlinking**: Package managers like pnpm maintain a central deduplicated CAS store, mounting dependency trees via hardlinks/reflinks without duplicating disk I/O [18].
- **SIMD/parallel hashing**: Modern verification routines utilize SIMD-accelerated algorithms such as BLAKE3 [24] or thread-pooled SHA-256 for high-throughput batch checks.

## Q4 Options and recommendation
- **Option A (Full Deep Verification)**: Compute cryptographic hashes for every file on every invocation against the lock specification [3][20]. *Trade-off*: Maximum security against local tampering, but incurs high I/O latency on large trees.
- **Option B (Lazy Stamp Validation)**: Check only the top-level stamp or digest against the pinned image/manifest [14][17]. *Trade-off*: Sub-millisecond execution, but cannot detect manual edits inside the vendored folder.
- **Option C (Two-Tier Hybrid)**: Execute $O(1)$ stamp verification on daily command invocations; run comprehensive per-file integrity checks on explicit verification, CI gates, or stamp mismatch.
- **Recommendation**: Implement **Option C** combined with atomic staging directories (`tmp` write + rename) [16][17], pairing a read-only root stamp with on-demand parallel hashing [20][24].

## Sources
[1] https://go.dev/ref/mod#vendoring  
[2] https://go.dev/ref/mod#module-cache  
[3] https://go.dev/ref/mod#authenticating  
[4] https://doc.rust-lang.org/cargo/commands/cargo-vendor.html  
[5] https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html  
[6] https://doc.rust-lang.org/cargo/commands/cargo-install.html  
[7] https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json  
[8] https://docs.npmjs.com/cli/v10/commands/npm-ci  
[9] https://yarnpkg.com/features/zero-installs  
[10] https://classic.yarnpkg.com/en/docs/offline-mirror/  
[11] https://bundler.io/man/bundle-cache.1.html  
[12] https://bundler.io/man/bundle-install.1.html  
[13] https://getcomposer.org/doc/03-cli.md  
[14] https://getcomposer.org/doc/01-basic-usage.md#composer-lock-the-lock-file  
[15] https://getcomposer.org/doc/06-config.md#vendor-dir  
[16] https://carvel.dev/vendir/docs/latest/  
[17] https://carvel.dev/vendir/docs/latest/vendir-spec/  
[18] https://pnpm.io/motivation#saving-disk-space  
[19] https://copier.readthedocs.io/en/latest/updating/  
[20] https://git-scm.com/docs/git-update-index  
[21] https://git-scm.com/book/en/v2/Git-Internals-Git-Objects  
[22] https://github.com/opencontainers/image-spec  
[23] https://containers.dev/implementors/features/  
[24] https://github.com/BLAKE3-team/BLAKE3
