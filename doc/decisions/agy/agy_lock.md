# Research Brief: Concurrent-Install Locking for `vendor_kit` (Prior Art Survey)

This survey investigates how major package managers, build systems, infrastructure tools, and VCS clients handle concurrent installs into shared directories, evaluates filesystem-level locking across Docker container and VM boundaries, and assesses design options for `vendor_kit`.

---

## Q1. Prior Art: "Concurrent Install into the Same Directory" Locks

### Summary Comparison Table

| Tool | Lock Form | Wait or Fail | Stale Lock Handling | Primary Source Links |
| :--- | :--- | :--- | :--- | :--- |
| **apt / dpkg** | POSIX advisory `fcntl` record lock (`F_SETLK`/`F_SETLKW`) on lock files (`/var/lib/dpkg/lock`, `/var/lib/dpkg/lock-frontend`, `/var/lib/apt/lists/lock`, `/var/cache/apt/archives/lock`) | Historically **failed immediately** with PID of lock holder (`F_GETLK`). Since APT 1.9.11, **waits and polls** with timeout configured via `DPkg::Lock::Timeout` (default 120s interactive) | **Kernel-managed**: Kernel automatically releases `fcntl` locks when the holding process exits or crashes. Lock file remains on disk but is unheld. Database recovery handled via `dpkg --configure -a`. | [Debian APT salsa source (`fileutl.cc`)](https://salsa.debian.org/apt-team/apt/-/blob/main/apt-pkg/contrib/fileutl.cc)<br>[Debian Bug #928347: Lock timeout](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=928347)<br>[dpkg source (`dbmodify.c`)](https://git.dpkg.org/cgit/dpkg/dpkg.git/tree/lib/dpkg/dbmodify.c) |
| **npm** | Historically `open(O_CREAT \| O_EXCL)` lockfiles (via `isaacs/lockfile`) / `mkdir`. Modern cache uses `cacache` (lockless, content-addressable). `node_modules` install has **no cross-process lock**. | `lockfile` library: **polls with backoff & timeout**. `npm install` on `node_modules`: **fails/corrupts** on concurrent runs with `ENOTEMPTY` / `EEXIST`. | `isaacs/lockfile` uses `mtime` age threshold (`opts.stale`). `proper-lockfile` uses `mkdir` heartbeat + `mtime`. Modern `npm` delegates race resolution to sequential runs or `npm ci`. | [npm/cacache repository](https://github.com/npm/cacache)<br>[isaacs/lockfile repository](https://github.com/isaacs/lockfile)<br>[moxystudio/node-proper-lockfile](https://github.com/moxystudio/node-proper-lockfile) |
| **pnpm** | Global store locking via atomic operations / `proper-lockfile` (directory locks). No project-level lock on `node_modules`. | Store lock **waits/polls**. Concurrent project install **fails immediately** with `ERR_PNPM_ENOTEMPTY` or `EPERM`. | Relies on `proper-lockfile` stale mtime checks for store; interrupted runs can leave stale store locks, requiring process cleanup. | [pnpm Issue #594: Store lockfile](https://github.com/pnpm/pnpm/issues/594)<br>[pnpm Issue #6499: Concurrent install race](https://github.com/pnpm/pnpm/issues/6499) |
| **yarn** | **Yarn Classic (v1)**: `--mutex file[:path]` (`.yarn-single-instance`) or `--mutex network[:port]`. **Yarn Berry (v2+)**: Internal file locks / immutable installs. | **Classic**: Polls/waits or fails with `"Another yarn process is running"`. **Berry**: Fails immediately (`YN0028`) if lockfile/cache would be modified in `--immutable`. | **Classic**: Network mutex auto-releases on OS socket close; file mutex requires manual deletion if process was killed (`kill -9`). **Berry**: Kernel-released file locks. | [Yarn Classic CLI `--mutex` documentation](https://classic.yarnpkg.com/en/docs/cli/install/#toc-yarn-install-mutex)<br>[Yarn Classic `mutex.js` source](https://github.com/yarnpkg/yarn/blob/master/src/util/mutex.js)<br>[Yarn Berry Immutable Installs](https://yarnpkg.com/configuration/yarnrc#enableImmutableInstalls) |
| **pip** | **NO lock**. Pip performs uncoordinated writes to `site-packages` and the wheel cache. | **Concurrent runs race**: Fails with partial writes, corrupted `.dist-info`, `BadZipFile`, or `EOFError`. | **None**. Pip considers concurrent execution unsupported; users must serialize runs or use isolated virtual environments. | [pypa/pip Issue #2365: Thread/process safety](https://github.com/pypa/pip/issues/2365)<br>[pypa/pip Issue #5304: Concurrent wheel cache corruption](https://github.com/pypa/pip/issues/5304)<br>[pypa/pip Issue #8799: Cache lock race condition](https://github.com/pypa/pip/issues/8799) |
| **Cargo** | `cargo::util::flock`: OS advisory lock (`flock(2)` / `fcntl(2)` on Unix, `LockFileEx` on Windows) on `~/.cargo/registry`, `~/.cargo/git`, and `target/.cargo-lock`. | Attempts non-blocking lock; if held, prints `"Blocking waiting for file lock on <path>..."` and **blocks indefinitely**. | **Kernel-managed**: Operating system closes file descriptors on process exit or crash, releasing advisory locks instantly. Zero stale state. | [Rust Cargo `flock.rs` source](https://github.com/rust-lang/cargo/blob/master/src/cargo/util/flock.rs)<br>[Rust Cargo Issue #3529: Build directory locking](https://github.com/rust-lang/cargo/issues/3529) |
| **Nix** | POSIX `fcntl` record locks (`F_SETLK`/`F_SETLKW`) on `/nix/var/nix/db/big-lock`, `/nix/var/nix/gc.lock`, and `/nix/store/<hash>-<name>.lock`. | **Blocks indefinitely** (`F_SETLKW`) until lock is released. | **Kernel-managed**: Kernel automatically releases `fcntl` locks upon process termination or crash. | [Nix libutil file-system source](https://github.com/NixOS/nix/blob/master/src/libutil/file-system.cc)<br>[Nix local-store source](https://github.com/NixOS/nix/blob/master/src/libstore/local-store.cc) |
| **Terraform** | State lock metadata record (`.terraform.tfstate.lock.info` locally, or remote backend items e.g. DynamoDB, GCS, Azure Blob, S3). | **Fails immediately** with `"Error acquiring the state lock"` and lock metadata; optional **wait with timeout** via `-lock-timeout=<duration>`. | **Manual intervention**: Does not auto-expire (safety against split-brain). Requires inspecting Lock ID and running `terraform force-unlock <LOCK-ID>`. | [HashiCorp Terraform State Locking Docs](https://developer.hashicorp.com/terraform/language/state/locking)<br>[HashiCorp Terraform `force-unlock` CLI Docs](https://developer.hashicorp.com/terraform/cli/commands/force-unlock) |
| **Bazel** | Advisory file lock using `fcntl` (`F_SETLK`) on `$(bazel info output_base)/lock`. | Governed by `--block_for_lock` (default `true`): **polls/waits** with warning `"Another command holds the client lock and --block_for_lock is enabled. Waiting..."`. If `--noblock_for_lock`, **fails immediately**. | **Kernel-managed + PID polling**: `fcntl` releases on process death; Bazel polls PID of lock holder to avoid hanging on dead servers. | [Bazel Command-Line Reference (`--block_for_lock`)](https://bazel.build/reference/command-line-reference#flag--block_for_lock)<br>[Bazel Output Base Lock Implementation](https://github.com/bazelbuild/bazel/issues/13600) |
| **Git** | Atomic file creation via `open(path, O_CREAT \| O_EXCL \| O_WRONLY, 0666)` (`.git/index.lock`, `packed-refs.lock`, `HEAD.lock`). | **Fails immediately** with `"fatal: Unable to create '.git/index.lock': File exists."` (Read-only status bypassable via `--no-optional-locks`). | **Process signal cleanup + manual removal**: Cleaned up via `atexit` and `sigchain` on normal exit/SIGINT/SIGTERM. If `SIGKILL` or system crash occurs, lock file is abandoned and requires **manual `rm -f`**. | [Git `lockfile.c` source](https://github.com/git/git/blob/master/lockfile.c)<br>[Git `lockfile.h` source](https://github.com/git/git/blob/master/lockfile.h)<br>[Git `git-config` core.filesRefLockTimeout documentation](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefilesRefLockTimeout) |

---

### In-Depth Analysis of Individual Tools

#### 1. apt / dpkg
- **Lock Form**: dpkg and APT use POSIX `fcntl(fd, F_SETLK, &fl)` record locking. Four distinct lock files guard the lifecycle:
  - `/var/lib/dpkg/lock`: guards the status database modification during `dpkg` execution ([dpkg `dbmodify.c`](https://git.dpkg.org/cgit/dpkg/dpkg.git/tree/lib/dpkg/dbmodify.c)).
  - `/var/lib/dpkg/lock-frontend`: introduced in APT 1.9 / Debian 10 Buster to hold an overarching lock across multiple sequential `dpkg` child invocations.
  - `/var/lib/apt/lists/lock`: protects package list updates during `apt update`.
  - `/var/cache/apt/archives/lock`: protects package downloads into the local archive cache.
- **Wait vs Fail**: Historically, `dpkg` and `apt` failed immediately, querying the holding PID via `fcntl(fd, F_GETLK, &fl)` and reporting `"Could not get lock ... It is held by process NNN"`. Since APT 1.9.11 ([Debian Bug #928347](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=928347)), APT introduced the configuration option `DPkg::Lock::Timeout` (e.g. `apt-get -o DPkg::Lock::Timeout=120 install ...`), causing it to poll every second with the message `"Waiting for cache lock: Could not get lock..."` until the lock is released or the timeout expires.
- **Stale Handling**: Because `fcntl` locks are maintained in-kernel associated with the process's open file table, terminating the process (including via `kill -9` or a crash) automatically causes the kernel to release the lock. The zero-byte lock file remains on disk, but subsequent `fcntl(F_SETLK)` calls succeed immediately.

#### 2. npm
- **Lock Form**: Early npm versions used the [`isaacs/lockfile`](https://github.com/isaacs/lockfile) library, which used `open(path, O_CREAT | O_EXCL)` polling loops. Modern npm versions manage the cache through [`npm/cacache`](https://github.com/npm/cacache), a content-addressable cache with an atomic write strategy (write to temp file, then rename by content hash) rather than global directory locks.
- **Wait vs Fail**: `node_modules` installations lack a global cross-process lock. Running concurrent `npm install` processes against the same project directory results in race conditions (`ENOTEMPTY`, `EEXIST`, or corrupted module trees) ([npm/cli issues](https://github.com/npm/cli)).
- **Stale Handling**: When `isaacs/lockfile` was used, stale locks were detected using an `mtime` age threshold (`opts.stale`, default 10 seconds). In the broader Node.js ecosystem, [`moxystudio/node-proper-lockfile`](https://github.com/moxystudio/node-proper-lockfile) uses `mkdir` as an atomic primitive, maintaining a background heartbeat that updates the directory's `mtime` to prevent active locks from expiring.

#### 3. pnpm
- **Lock Form**: pnpm isolates dependencies in a global content-addressable filesystem (`cafs`) store and links them into project directories. Access to the global store is protected by store-level locking ([pnpm Issue #594](https://github.com/pnpm/pnpm/issues/594)).
- **Wait vs Fail**: When writing to the global store, pnpm waits for existing operations to release store locks. However, inside individual projects, running concurrent `pnpm install` commands leads to conflicts over `node_modules/.modules.yaml` and symlink creation, producing `ERR_PNPM_ENOTEMPTY` ([pnpm Issue #6499](https://github.com/pnpm/pnpm/issues/6499)).
- **Stale Handling**: Store locks that were interrupted abruptly (e.g. `SIGKILL`) historically left behind lock files, causing subsequent invocations to hang until processes were inspected and cleared.

#### 4. Yarn
- **Lock Form**: Yarn Classic (v1) implemented mutual exclusion via the `--mutex` flag ([Yarn Classic docs](https://classic.yarnpkg.com/en/docs/cli/install/#toc-yarn-install-mutex)). Supported modes:
  - `--mutex file[:path]`: creates a lock file (default `.yarn-single-instance`).
  - `--mutex network[:port]`: binds a local TCP server socket (default port `31997`).
- **Wait vs Fail**: If the mutex cannot be acquired, Yarn prints `"Another yarn process is running"` and waits or aborts depending on timeout configuration. In Yarn Berry (v2+), the CLI relies on immutable directory states and internal file locking, failing with error code `YN0028` if an install modifies the lockfile under `--immutable`.
- **Stale Handling**: The network mutex is cleaned up automatically by the OS on process termination (socket closure). The file mutex can become stale if Yarn is killed via `SIGKILL`, requiring manual deletion of `.yarn-single-instance`.

#### 5. pip
- **Lock Form**: Pip provides **no cross-process locking** for `site-packages`, virtual environment directories, or its wheel cache.
- **Consequences**: Concurrent `pip install` commands in the same environment or sharing a cache directory routinely corrupt environments. Reported failures include:
  - Cache write collisions resulting in truncated wheels and `BadZipFile` / `EOFError` ([pypa/pip Issue #5304](https://github.com/pypa/pip/issues/5304)).
  - Partial uninstalls and overwrites of metadata folders (`.dist-info`), leaving inconsistent dependency state ([pypa/pip Issue #2365](https://github.com/pypa/pip/issues/2365)).
- **Maintainer Stance**: The pip team has consistently documented that parallel pip invocations against the same environment are unsupported. Users and CI systems are required to isolate environments or serialize commands.

#### 6. Cargo
- **Lock Form**: Cargo encapsulates OS-level advisory locking in [`cargo::util::flock`](https://github.com/rust-lang/cargo/blob/master/src/cargo/util/flock.rs). On Unix systems, it uses `libc::flock(fd, operation)` (falling back to `fcntl` where appropriate); on Windows, it uses `LockFileEx`.
- **Wait vs Fail**: When Cargo accesses the package cache (`~/.cargo/registry`), git checkouts (`~/.cargo/git`), or build target directory (`target/.cargo-lock`), it executes a non-blocking lock attempt. If the lock is held, it invokes a notification callback that logs:
  `Blocking waiting for file lock on package cache` or `build directory`
  and transitions to a blocking lock call.
- **Stale Handling**: Because advisory locks are tracked by the OS kernel on the open file description, process termination automatically releases the lock. There is no possibility of a stale lock surviving a process crash.

#### 7. Nix
- **Lock Form**: Nix manages multi-user concurrent access to the Nix Store using POSIX `fcntl` record locks ([Nix `file-system.cc`](https://github.com/NixOS/nix/blob/master/src/libutil/file-system.cc), [`local-store.cc`](https://github.com/NixOS/nix/blob/master/src/libstore/local-store.cc)). Key locks include:
  - `/nix/var/nix/db/big-lock`: serializes SQLite database schema mutations.
  - `/nix/var/nix/gc.lock`: held in shared mode by builds and exclusive mode by garbage collection.
  - `/nix/store/<hash>-<name>.lock`: per-store-path locks held during derivation builds.
- **Wait vs Fail**: Nix blocks waiting for locks (`F_SETLKW`). If another process is currently realizing a store path, concurrent builds block on that path's `.lock` file. Once the builder completes the build and renames the temp directory to the final store path, it releases the lock; the waiting process wakes up, detects that the store path now exists, and skips rebuilding.
- **Stale Handling**: POSIX `fcntl` locks are released by the kernel upon process exit, preventing deadlocks from crashes.

#### 8. Terraform
- **Lock Form**: Terraform acquires an exclusive state lock before executing operations that alter state (`apply`, `destroy`, `import`) ([Terraform State Locking](https://developer.hashicorp.com/terraform/language/state/locking)). Local backends create `.terraform.tfstate.lock.info`; remote backends utilize backend-native locks (e.g. AWS DynamoDB item lock, Azure Blob lease, Google Cloud Storage lock). The lock payload contains a JSON record with an MD5/UUID Lock ID, operation, creator PID, hostname, and timestamp.
- **Wait vs Fail**: By default, Terraform fails immediately if a lock cannot be acquired:
  `Error: Error acquiring the state lock`
  It supports `-lock-timeout=<duration>` (e.g. `-lock-timeout=10m`), causing Terraform to retry acquiring the lock periodically until the duration elapses.
- **Stale Handling**: To prevent split-brain execution across distributed pipelines, locks **never auto-expire**. If a process crashes or is killed by CI, the lock remains. Recovery requires manual execution of [`terraform force-unlock <LOCK-ID>`](https://developer.hashicorp.com/terraform/cli/commands/force-unlock).

#### 9. Bazel
- **Lock Form**: Bazel secures its workspace execution directory via an exclusive lock on `$(bazel info output_base)/lock` using `fcntl` ([Bazel Issue #13600](https://github.com/bazelbuild/bazel/issues/13600)).
- **Wait vs Fail**: Controlled by the startup flag `--block_for_lock` (default `true`) ([Bazel CLI Docs](https://bazel.build/reference/command-line-reference#flag--block_for_lock)). When another Bazel client or server holds the lock, Bazel prints:
  `Another command holds the client lock and --block_for_lock is enabled. Waiting ...`
  and blocks/polls. When run with `--noblock_for_lock`, it exits immediately with an error.
- **Stale Handling**: Bazel combines `fcntl` with PID inspection. Because `fcntl(F_SETLKW)` could hang indefinitely if a previous server died in an abnormal state on network filesystems, Bazel uses polling to verify whether the recorded holding PID is still alive.

#### 10. Git
- **Lock Form**: Git uses atomic file creation via `open(path, O_CREAT | O_EXCL | O_WRONLY, 0666)` through its internal lockfile API ([Git `lockfile.c`](https://github.com/git/git/blob/master/lockfile.c), [`lockfile.h`](https://github.com/git/git/blob/master/lockfile.h)). Files locked include `.git/index.lock`, `.git/refs/...lock`, and `packed-refs.lock`.
- **Wait vs Fail**: Fails immediately with:
  `fatal: Unable to create '.git/index.lock': File exists.`
  For ref locking, Git supports `core.filesRefLockTimeout` ([Git config docs](https://git-scm.com/docs/git-config#Documentation/git-config.txt-corefilesRefLockTimeout)) to retry for a specified number of milliseconds before failing. Git also provides `--no-optional-locks` to prevent background tasks (like `git status` in prompt generators) from attempting to acquire optional index locks.
- **Stale Handling**: Git registers handlers using `atexit()` and `sigchain_add()` to delete lockfiles on normal exit, `SIGINT`, `SIGTERM`, or `SIGHUP`. However, if the process receives `SIGKILL` (`kill -9`) or crashes, signal handlers cannot execute. Git deliberately avoids automatic stale lock deletion to prevent data races, requiring the developer to manually delete the file (`rm -f .git/index.lock`).

---

## Q2. Locking a Bind-Mounted Directory from Inside a Container

When running `vendor_kit install` inside a container against a host directory bind-mounted at `/repo`, the locking semantics depend on the underlying host kernel, virtualization boundary, and filesystem drivers.

```
+-------------------------------------------------------------------------+
| Host OS (Linux / macOS / Windows WSL2)                                  |
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   | Linux VM (on macOS Docker Desktop / WSL2)                       |   |
|   |   (Shared Kernel for all containers running inside the VM)      |   |
|   |                                                                 |   |
|   |   +-----------------------+           +-----------------------+ |   |
|   |   | Container 1           |           | Container 2           | |   |
|   |   | (vendor_kit install)  |           | (vendor_kit install)  | |   |
|   |   | flock("/repo/.lock")  |           | flock("/repo/.lock")  | |   |
|   |   +-----------+-----------+           +-----------+-----------+ |   |
|   |               |                                   |             |   |
|   |               +-----------------+-----------------+             |   |
|   |                                 |                               |   |
|   |                     VFS Inode Lock List (Kernel)                |   |
|   +---------------------------------+-------------------------------+   |
+-------------------------------------|-----------------------------------+
                                      v
         Underlying Filesystem: ext4 / NFS / VirtioFS / 9p
```

### 1. `flock()` across a Docker Bind Mount on Native Linux
- **Verdict**: **Reliable**.
- **Technical Basis**: On a native Linux host, Docker containers share the exact same host Linux kernel and Virtual Filesystem (VFS) layer. Namespaces isolate PIDs, mounts, and network interfaces, but **do not isolate filesystem inode lock tables**. 
- An advisory lock placed via `flock(fd, LOCK_EX)` or `fcntl(fd, F_SETLK)` on an ext4, xfs, or btrfs bind mount attaches directly to the kernel `struct inode` lock list. Any other process—whether running on the bare host or inside an entirely separate Docker container—accessing the same inode observes the lock identically ([Linux `flock(2)` man page](https://man7.org/linux/man-pages/man2/flock.2.html)).

### 2. OverlayFS: `flock` and Directory Renames
- **`flock` on OverlayFS**: Advisory file locking on files created in the `upperdir` functions normally. However, historical issues existed when locking files that originated from the read-only `lowerdir` before copy-up occurred, because the lower and upper inodes have distinct identities.
- **Directory `rename()` on OverlayFS**: **Crucial pitfall**. If the directory being renamed exists on the `lowerdir` or in a merged view, `rename(2)` returns **`EXDEV` ("Invalid cross-device link")** unless the kernel module option `redirect_dir` is enabled ([Linux Kernel OverlayFS Documentation](https://docs.kernel.org/filesystems/overlayfs.html)). Because `vendor_kit` operates inside `/repo` (a bind mount to the host filesystem), this only triggers if the host directory itself resides on an OverlayFS layer (e.g. nested container-in-container setups).

### 3. NFS: `flock` vs `fcntl`, Protocol Differences, and Bind Mounts
- **NFSv3**: Stateless protocol. Locking requires auxiliary Network Lock Manager (`rpc.lockd`) and Network Status Monitor (`rpc.statd`) daemons. If firewall rules block dynamic ports or `statd` is inactive, locks fail or hang.
- **NFSv4**: Stateful protocol. Advisory locking is native to the protocol via `OPEN` and `LOCK` operations, utilizing server-lease timeouts over standard TCP port 2049.
- **`flock` vs `fcntl` on NFS**: Modern Linux kernels (since 2.6.12) translate user-space `flock()` calls into NFS byte-range locks across the wire by default. However, if the host mounts NFS with the **`nolock`** or `local_lock=all` mount option, locks are strictly local to that client's kernel and are **not propagated across different client machines** ([Linux NFS mount documentation](https://man7.org/linux/man-pages/man5/nfs.5.html)).
- **Docker Bind Mount of NFS**: If two containers run on the *same* host against an NFS bind mount, they share the host's NFS client inode cache, so locks coordinate between those containers. But if containers run across *separate host nodes* sharing an NFS server, lock latency, network partitions, and `nolock` mount flags make file locking unreliable.

### 4. macOS Docker Desktop: virtiofs / gRPC-FUSE / osxfs
- **Architecture**: Docker on macOS runs inside a Linux VM (HyperKit or Apple Virtualization framework). Bind mounts cross the hypervisor boundary between macOS and the Linux guest VM.
- **Cross-VM Locking Issues**:
  - `osxfs` (legacy) and `gRPC-FUSE`: Prone to lost locks and hangs.
  - `virtiofs` (modern default): Offers high I/O throughput, but POSIX and BSD file locking across the host-VM boundary has documented bugs. Specifically, in [Docker Desktop for Mac Issue #7004](https://github.com/docker/for-mac/issues/7004), users documented that `virtiofs` fails to coordinate locks properly, allowing multiple threads to acquire exclusive locks simultaneously, which breaks applications like SQLite.
- **Container-to-Container Coordination**: If both containers run inside the **same Docker Desktop Linux VM**, locks coordinate within the Linux VM's kernel VFS. However, coordination between a container process and a native macOS host process (e.g. host shell `just` vs container `vendor_kit`) over `virtiofs` is susceptible to synchronization failures.

### 5. WSL2 / 9p Mounts of Windows Drives
- **Architecture**: In WSL2, access to Windows drives (e.g. `/mnt/c/...`) goes through Plan 9 (`9p`) or `DrvFs` filesystem virtualization.
- **Locking Limitations**: The `9p` protocol does not implement full POSIX file locking semantics ([Microsoft WSL Issue #3574](https://github.com/microsoft/WSL/issues/3574)). Running `flock()` or `fcntl()` on files within `/mnt/c/` frequently results in I/O errors (`EIO`), silent failure, or ignored locks. Microsoft officially recommends keeping performance-critical or lock-sensitive repositories inside the WSL2 native ext4 virtual disk (`/home/...`) rather than Windows-mounted drives ([WSL Filesystem Documentation](https://learn.microsoft.com/en-us/windows/wsl/filesystems)).

### 6. Atomic Primitives: `mkdir()` vs `open(O_EXCL)`
- **`mkdir()` Reliability**: **Universal POSIX atomicity**.
  - On local filesystems (ext4/xfs), FUSE, virtiofs, 9p, and network filesystems (NFSv2 RFC 1094, NFSv3 RFC 1813, NFSv4 RFC 7530), `mkdir()` is guaranteed to be atomic by the server. If two processes execute `mkdir` simultaneously on the same path, exactly one succeeds (returns 0); the other fails with `EEXIST`.
- **`open(O_CREAT | O_EXCL)`**:
  - The Linux man page for [`open(2)`](https://man7.org/linux/man-pages/man2/open.2.html) contains an explicit warning:
    > *"O_EXCL is broken on NFS file systems, programs which rely on it for performing locking tasks will contain a race condition."*
  - While NFSv3 with exclusive creation mode and NFSv4 corrected this in the protocol specification, real-world NFS deployments and non-standard network appliances frequently exhibit race conditions with `O_EXCL`. `mkdir` remains the industry standard for portable, lockless mutual exclusion across network and virtual filesystems.

### 7. Atomicity of Directory `rename()`
- **Local Linux Filesystem**: `rename(old, new)` is atomic for single files and empty directories. **However**, POSIX stipulates that if `new` is an existing **non-empty directory**, `rename()` **fails with `ENOTEMPTY` (or `EEXIST`)** ([Linux `rename(2)` man page](https://man7.org/linux/man-pages/man2/rename.2.html)).
- **OverlayFS**: Renaming a directory residing in lower/merged layers fails with `EXDEV` without `redirect_dir`.
- **NFS**: Directory renames over NFS are not strictly atomic across multiple clients; client-side attribute caching causes temporary `ENOENT` visibility windows, and open files undergo client-side "silly renaming".
- **virtiofs / 9p**: Directory renames across the host boundary are mediated by FUSE/9p RPC requests and do not provide cross-host transactional guarantees.

---

## Q3. Can "Temp Dir + Atomic Rename" Itself Serve as the Lock?

A common proposal is to dispense with explicit lock primitives and rely on the existence of a staging directory (e.g. `.<name>.tmp/`) as an implicit lock.

### Prior Art Analysis

1. **`rsync --delay-updates`** ([rsync(1) man page](https://download.samba.org/pub/rsync/rsync.1)):
   - `rsync` stores each incoming file in a staging directory (`.~tmp~` by default). At the end of the entire transfer, files are renamed into place in rapid succession.
   - *Design distinction*: `rsync` uses this to prevent readers from seeing partially-written files, but it does **not** rely on `.~tmp~` to lock out concurrent `rsync` writers. Running two concurrent `rsync` processes to the same destination without external coordination results in mutual clobbering.
2. **APT Partial Directories** (`/var/lib/apt/lists/partial/` and `/var/cache/apt/archives/partial/`):
   - Incomplete downloads are stored in `partial/`. Once cryptographic hashes (SHA256) match, files are renamed to their parent destination.
   - *Locking synergy*: APT does **not** rely on the existence of `partial/` as a lock. It holds an explicit `fcntl` file lock on the archive/list directory (`/var/lib/apt/lists/lock`).
3. **Nix Store Derivation Paths**:
   - Nix builds derivations inside isolated temporary directories (`/nix/store/<hash>-<name>.drv.chroot` or temporary roots).
   - Once built and registered in SQLite, Nix atomically moves/registers the store path.
   - *Locking synergy*: Nix coordinates this by acquiring an explicit `.lock` file (`/nix/store/<hash>-<name>.lock`) using `fcntl` locks to ensure two builders do not build the same derivation concurrently.
4. **Go Module Cache (`cmd/go`)**:
   - Downloads modules into `.partial` or `.tmp-` files inside `$GOPATH/pkg/mod/cache/download/`.
   - *Locking synergy*: Go pairs temporary staging paths with an explicit advisory lock mechanism via the internal package [`cmd/go/internal/lockedfile`](https://github.com/golang/go/tree/master/src/cmd/go/internal/lockedfile), which uses `syscall.Flock` on dedicated `.lock` files.
5. **Apache Maven Resolver**:
   - Uses `.part` files alongside `.part.lock` files ([Maven Resolver](https://github.com/apache/maven-resolver)). Modern Maven versions provide the `maven-resolver-named-locks` module with `FileLockNamedLockFactory` using Java NIO `FileLock` (mapping to OS `fcntl`/`flock`).

---

### Critical Pitfalls of Implicit Staging Directory Locking

#### 1. The Fatal POSIX Directory Rename Limitation (`ENOTEMPTY`)
Under POSIX standards ([POSIX `rename()`](https://pubs.opengroup.org/onlinepubs/9699919799/functions/rename.html)):
```c
rename("/repo/.<name>.tmp", "/repo/.<name>");
```
If `/repo/.<name>/` already exists and contains files (e.g. from a previous version of `vendor_kit`), `rename()` **will not replace it**. It immediately returns **`ENOTEMPTY`** (or `EEXIST`).

To work around this, `vendor_kit` currently does:
1. `rmtree("/repo/.<name>")`
2. `rename("/repo/.<name>.tmp", "/repo/.<name>")`

**This invalidates atomicity**:
- Between step 1 and step 2, there is an unavoidable window where `/repo/.<name>` **does not exist at all**.
- Any concurrent task (e.g. another `just <task>` execution) reading from `.<name>` during this window crashes with missing file errors.
- If two installers run concurrently:
  - Process A removes `.<name>`.
  - Process B finishes its temp directory, attempts `rmtree` (which fails or races), and renames its temp dir.
  - Process A renames its temp dir over Process B's new install, failing with `ENOTEMPTY`.

#### 2. Stale Directory Left Behind on Crash
If a container is abruptly terminated (`kill -9`, OOM killer, terminal closed, host reboot, CI cancellation) while writing to `.<name>.tmp/`:
- `.<name>.tmp/` remains permanently on the host filesystem.
- If subsequent runs interpret "`.<name>.tmp/` exists" as "an installation is active", all future runs fail or block forever.

#### 3. Breakdown of Stale-Detection Heuristics in Containers
- **PID Checking (`kill(pid, 0)`)**: Completely broken. In Docker, processes run inside separate PID namespaces. Inside Container A, `vendor_kit` is PID 1 (or a low integer). If Container B reads that PID and calls `kill(1, 0)`, it probes its *own* container's init process, not Container A.
- **Age / `mtime` Expiry**:
  - Slow networks or large dist copies could cause a legitimate install to exceed an arbitrary threshold (e.g. 10 minutes), leading a second process to purge an active install.
  - On Linux, directory `mtime` updates only when files/directories are directly created or unlinked inside the top directory; writing deeply nested files inside `dist/` does not update the root directory's `mtime`.
  - Clock skew between host and container or virtual machines can lead to premature expiration.
- **Boot ID (`/proc/sys/kernel/random/boot_id`)**: Only detects system-wide reboots; it cannot detect container crashes or individual process termination.

#### 4. TOCTOU Race
Executing `if [ -d .<name>.tmp ]; then wait; else mkdir .<name>.tmp; fi` creates a classic Time-of-Check to Time-of-Use race. Even if `mkdir` is used as an atomic check, sharing a single static staging directory name (`.<name>.tmp`) means two racing processes will either collide inside that directory or leave an unrecoverable stale folder on crash.

---

## Q4. Options Comparison and Recommendation for `vendor_kit`

### Architectural Alternatives

```
Option A: No Lock (Unique Temp Dirs)
[Process 1] ---> writes to .<name>.tmp.1/ ---+
                                            |--> rmtree(.<name>) --> rename() [RACE WINDOW!]
[Process 2] ---> writes to .<name>.tmp.2/ ---+

Option B: Directory Lock (mkdir)
[Process 1] ---> mkdir(.<name>.lock/) ===> SUCCESS (Installs) ===> rmdir(.<name>.lock/)
[Process 2] ---> mkdir(.<name>.lock/) ===> EEXIST (Polls / Fails) [Risk: Stale on SIGKILL]

Option C: Kernel Advisory Lock (flock)
[Process 1] ---> flock(.<name>.lock, LOCK_EX) ===> SUCCESS (Installs) ===> close(fd)
[Process 2] ---> flock(.<name>.lock, LOCK_EX) ===> WAITS (Blocks)    ===> Acquires Lock
                                                  [Auto-released by kernel on crash]
```

### Option A: No Lock (Unique Temp Dirs + Rename)
- **Mechanism**: Every process writes into a unique per-process staging directory:
  `/repo/.<name>.tmp.<pid>.<random>/`
  Upon completion, it replaces `/repo/.<name>/`.
- **Pros**:
  - Completely immune to deadlocks and stale lock files.
  - No lock cleanup logic required.
- **Cons**:
  - **The `ENOTEMPTY` Dilemma**: Because POSIX cannot atomically replace a non-empty directory via `rename()`, the process must perform `rmtree()` first. Concurrent processes will race during this non-atomic removal window.
  - **Redundant Work**: If 5 shells trigger `just` at the same time, all 5 spawn Docker containers that download/copy `dist/` concurrently, causing high CPU/disk I/O contention.
  - **Orphan Accumulation**: Crashed installations leave unique `.tmp.*` directories on the host that require separate garbage collection sweeps.

### Option B: `mkdir .<name>.lock/` as Mutual Exclusion
- **Mechanism**: Process executes `mkdir("/repo/.<name>.lock")`.
  - Returns `0` (Success): Lock acquired. Runs install, removes directory when finished.
  - Returns `EEXIST`: Another process is installing. Polls with exponential backoff up to a timeout (e.g. 60s), or fails with a descriptive error.
- **Pros**:
  - Works across every filesystem imaginable (POSIX local, NFSv3, NFSv4, FUSE, virtiofs, 9p).
  - Simple to implement without specialized C bindings or syscall wrappers.
- **Cons**:
  - **Stale Lock Vulnerability**: If a user cancels with `Ctrl+C` in Docker, or the container is terminated (`kill -9`, OOM), the directory remains. Subsequent runs hang or fail.
  - **Unreliable Stale Detection**: Cleaning up via `mtime` is error-prone, and PID checking across containers is invalid due to PID namespaces.

### Option C: Advisory File Lock (`flock`) on `.<name>.lock`
- **Mechanism**: Process opens `/repo/.<name>.lock` and calls `flock(fd, LOCK_EX)`.
  - Uses non-blocking `LOCK_NB` first; if busy, prints:
    `"Waiting for another vendor_kit installation to finish..."`
    and blocks with a timeout.
- **Pros**:
  - **Automatic Stale Cleanup**: The OS kernel automatically releases the advisory lock when the file descriptor is closed (which happens when the container process exits or crashes).
  - **Zero Duplicate Work**: Concurrent processes cleanly wait in line; the second process wakes up, checks that the stamp file is already up to date, and exits in milliseconds without re-installing.
- **Cons**:
  - On macOS Docker Desktop crossing `virtiofs` or WSL2 over `/mnt/c` (`9p`), advisory locks can fail or fail to synchronize with host processes (though container-to-container synchronization on the same VM host kernel remains functional).

---

### Tools Utilizing Unique Staging vs Locking

| Tool | Approach | Rationale |
| :--- | :--- | :--- |
| **`uv`** (Astral) | **`flock` on lockfile** | Uses `LockedFile` ([uv cache source](https://github.com/astral-sh/uv/blob/main/crates/uv-cache/src/lib.rs)) to serialize cache writes and venv modifications, avoiding duplicate compilation and corrupt environments. |
| **`Go` module cache** | **`flock` + unique partial files** | Uses `cmd/go/internal/lockedfile` ([Go lockedfile](https://github.com/golang/go/tree/master/src/cmd/go/internal/lockedfile)) to hold an OS file lock while staging downloads in temporary files. |
| **`Cargo`** | **`flock` on target & cache** | Blocks on `cargo::util::flock` ([Cargo flock.rs](https://github.com/rust-lang/cargo/blob/master/src/cargo/util/flock.rs)) with explicit user notification. |
| **`asdf` / `mise`** | **Unique staging + atomic symlink** | Installs into unique version-specific directories (`~/.local/share/mise/installs/<tool>/<version>.<pid>`), then creates/swaps a symlink. Symlinks avoid directory `ENOTEMPTY` limitations. |
| **`Capistrano` / Deployers** | **Symlink switching** | Writes releases into timestamped directories (`releases/<timestamp>`), then atomically replaces a symlink (`current`) using `ln -sfn ... && mv -T ...`. |

---

### Final Recommendation for `vendor_kit`

To guarantee safety, avoid stale lock deadlocks, and eliminate race windows, `vendor_kit` should adopt a **layered locking and installation strategy**:

```
                              vendor_kit install
                                      |
                       Acquire flock(/repo/.<name>.lock)
                                      |
                     +----------------+----------------+
                     | (Lock held by another process)  |
                     v                                 v
               Acquired Immediately        Wait with polling timeout (e.g. 60s)
                     |                     Print user-friendly message
                     |                                 |
                     +----------------<----------------+
                     |
         Check .<name>/.version stamp
                     |
       +-------------+-------------+
       | Up-to-date                | Outdated / Missing
       v                           v
   Skip install              Generate unique temp dir:
   (Done in 1ms)             /repo/.<name>.tmp.<pid>.<uuid>/
                                   |
                             Populate dist/ & write stamp
                                   |
                             Replace directory
                             (Symlink swap OR exclusive-locked rmtree+rename)
                                   |
                             Release flock
```

#### Detailed Architecture:

1. **Advisory Lock File (`flock`)**:
   - Create and open `/repo/.<name>.lock` (`O_RDWR | O_CREAT, 0666`).
   - Attempt non-blocking lock: `flock(fd, LOCK_EX | LOCK_NB)`.
   - If blocked, display:
     `"vendor_kit: Waiting for concurrent installation on /repo/.<name> to complete..."`
     Poll or block with a timeout (e.g. 60 seconds).
   - *Why*: On Linux (CI environments and native developers), this provides **100% crash safety without stale lock files**, as the kernel guarantees lock cleanup on container death.

2. **Per-Process Unique Staging Directory**:
   - Write to `/repo/.<name>.tmp.<pid>.<random>/` instead of a static `.<name>.tmp/`.
   - *Why*: In the event that locking fails or is bypassed on degraded filesystems (e.g. WSL2 9p or weird NFS mounts), two processes will never write into or corrupt the same staging folder.

3. **Solve the `ENOTEMPTY` Problem**:
   Choose one of two patterns depending on whether `vendor_kit` allows symlinks:
   - **Pattern A (Symlink Switch - Recommended for Full Atomicity)**:
     Install into `/repo/vendor_versions/<name>-<version>-<uuid>/`.
     Create a temporary symlink pointing to it:
     `ln -sfn vendor_versions/<name>-<version>-<uuid> /repo/.<name>.tmp_link`
     Atomically replace the target via file rename:
     `rename("/repo/.<name>.tmp_link", "/repo/.<name>")`
     *Under POSIX, renaming a symlink over an existing symlink is strictly atomic and never returns `ENOTEMPTY`.*
   - **Pattern B (Locked Directory Replacement)**:
     If `.<name>` must remain a physical directory, keep the `rmtree` + `rename` sequence, but **strictly ensure it executes while holding the exclusive `flock`**. Because the lock serializes all `vendor_kit` processes, no two processes will ever attempt to delete or rename simultaneously, eliminating the race condition.

4. **Post-Lock Check**:
   Once the lock is acquired, the process should immediately inspect `/repo/.<name>/.version`. If another process just finished installing that exact version, the process can exit immediately without doing any redundant copy work.
