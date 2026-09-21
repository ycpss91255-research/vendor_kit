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
