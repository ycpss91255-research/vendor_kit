# Research brief: concurrent-install locking for vendor_kit (prior art survey)

You are a research assistant. Use web search to find REAL prior art and answer with SOURCE LINKS (URLs) for every factual claim. Do not invent facts; if you cannot find a source, say "not found". Answer in English or Chinese (either is fine). Be concrete: cite documentation pages, source code files, issue trackers, mailing list posts, man pages.

## Background

`vendor_kit` has an `install` subcommand. It runs INSIDE a docker container; the project directory is bind-mounted at `/repo`; the process runs as the host user's UID. Steps:

1. Copy the whole `dist/` from the image into a temp dir `/repo/.<name>.tmp/`
2. Write a stamp file (version marker) inside it
3. `rename()` the temp dir to `/repo/.<name>/` (atomic replace; the old `.<name>/` is `rmtree`d first, then rename)

Every `just <task>` invocation may trigger `install` (when a `.version` file changed). Problem: two shells in the same project running `just` at the same time (or CI and a human at the same time) => two containers run `install` concurrently against the same bind-mounted directory.

Open decision #13: **whether to lock, and how**.

## Questions (answer each, with links)

### Q1. Prior art: "concurrent install into the same directory" locks

For EACH of the following, find: (a) the lock's form (lock file? `flock()`/`fcntl()`? `mkdir` atomicity? `open(O_EXCL)`? symlink?), (b) does a second process WAIT or FAIL immediately (and is there a timeout/retry), (c) how STALE locks are detected/cleaned (PID inside the file? mtime/age? boot id? never, requires manual removal?). Cite docs/source/issue links.

- apt / dpkg: `/var/lib/dpkg/lock`, `/var/lib/dpkg/lock-frontend`, `/var/lib/apt/lists/lock`, `/var/cache/apt/archives/lock` (fcntl locks?; "Could not get lock ... It is held by process NNN"; apt's wait behaviour since 1.9.11 "Waiting for cache lock")
- npm: historically `.lock` files in node_modules / cache (npm 5?), `npm install` concurrency issues; also npm's cacache uses lockfiles? (search "npm concurrent install same directory", "proper-lockfile", "lockfile" npm package used by npm with stale detection)
- pnpm: store lock, `node_modules/.modules.yaml`, `pnpm install` concurrency ("pnpm lock file / pnpm install waits for lock", `--lockfile-only`, "Another pnpm process is running"?)
- yarn: `yarn install` "Another yarn process is running" / `.yarn-integrity` / berry's lock
- pip: NO lock — consequences of concurrent `pip install` into same site-packages or same venv (issues on GitHub pypa/pip about concurrent installs corrupting)
- Cargo: "Blocking waiting for file lock on package cache" / "build directory" — `flock()` based, `cargo::util::flock`, wait behaviour, stale handling
- Nix: `/nix/var/nix/db/big-lock`, `/nix/var/nix/gc.lock`, temp store path locks `.lock` files, `lockFile` in libutil (pathlocks.cc), how nix deals with stale locks (it uses fcntl locks so kernel-released)
- Terraform: state locking (`.terraform.tfstate.lock.info`, backends use DynamoDB/etc.), `-lock-timeout`, `force-unlock`, lock ID
- Bazel: output base lock (`$(bazel info output_base)/lock`), "Another command holds the client lock", `--block_for_lock`, wait behaviour
- Git: `index.lock` (`O_EXCL` create), "Unable to create '.git/index.lock': File exists", `lockfile.c` / `lockfile.h`, cleanup on signal via atexit, stale lock requires manual rm; also `packed-refs.lock`, `--no-optional-locks`

### Q2. Locking a bind-mounted directory from inside a container

- Is `flock()` reliable across a docker bind mount (same host kernel, so yes?) Find sources.
- OverlayFS: flock on overlay — known issues?
- NFS: flock vs fcntl, NFSv3 needs lockd/statd, NFSv4 has locking in-protocol; Docker bind-mounts of NFS.
- macOS Docker Desktop: virtiofs / gRPC FUSE / osxfs — do `flock`/`fcntl` locks work across the VM boundary? Known issues (e.g. SQLite locking on Docker Desktop for Mac, `flock` not working on osxfs, Docker for Mac issue tracker).
- WSL2 / 9p mounts of Windows drives: flock support?
- Is `mkdir()` atomic and reliable across all of these (POSIX guarantee, NFS, FUSE, virtiofs)? Is `open(O_EXCL)` reliable on NFS (NFSv3 vs v4)?
- Does `rename()` of a directory work atomically on overlay/virtiofs/9p? Any known non-atomic rename on these FS?

### Q3. Can "temp dir + atomic rename" itself serve as the lock?

I.e. treat "`.<name>.tmp/` exists" as "someone is installing". Find prior art and pitfalls:
- rsync `--delay-updates` / `--partial-dir` / `.~tmp~` directory
- apt `/var/lib/apt/lists/partial/` and `/var/cache/apt/archives/partial/`
- Nix's temp store path naming (`/nix/store/<hash>-<name>.drv.chroot`, `tmp-` prefixes, `.lock` files next to store paths)
- Maven `.part` files, pip's temp build dirs, Go module cache `.tmp-` / `.partial` files + `.lock` files (`cmd/go/internal/lockedfile`) 
- Pitfalls: crash leaves stale temp dir; how do tools decide it's garbage (age? PID? boot id? just always delete on next run?); race between "check exists" and "mkdir" (TOCTOU) vs using mkdir's EEXIST as the atomic primitive.

### Q4. Compare options and recommend

Options for vendor_kit:
- A. No lock. Rely on rename atomicity. Last writer wins; both writers produce identical content (same image version) so the result is fine either way. Risk: one process's rmtree of `.<name>.tmp` vs the other's writes; one process renames while the other is still writing into its tmp dir (if both use the SAME tmp name). Discuss whether using a per-process tmp name (`.<name>.tmp.<pid>.<random>`) makes A safe.
- B. `mkdir .<name>.lock/` as lock (EEXIST => wait up to N seconds polling, then fail with message). Stale detection by mtime age (e.g. > 10 min => remove). Discuss stale-detection pitfalls: mtime of a directory; clock skew between container and host; PID-in-file not meaningful across containers (PID namespaces); boot id.
- C. `flock()` on a lock file (`.<name>.lock`), blocking with timeout. Kernel auto-releases on process death (no stale problem) — but reliability on Docker Desktop for Mac / NFS / 9p questionable.

Give pros/cons for each, and a recommendation with reasoning, citing the prior art found above. Also mention any relevant tools that chose "no lock, just atomic rename + unique temp name" (e.g. uv? pipx? asdf? mise? rustup? nvm? Homebrew? Go's module cache uses locks though).

## Output format

Markdown with sections Q1 (a table: tool | lock form | wait or fail | stale handling | source link), Q2, Q3, Q4. Every row/claim must have at least one URL. Mark "not found" where you could not verify.
