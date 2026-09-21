# Research brief: prior art for "post-install integrity verification" (vendor_kit decision #12)

You are doing prior-art research. Use web search extensively. Every claim must cite a real, working source URL (official docs, man pages, source code on GitHub, RFCs, design docs, issue threads). If you cannot find a source for something, say explicitly "not found" instead of guessing. Do NOT invent URLs. Answer in English or Chinese, structured with the headings requested at the end.

## Background

vendor_kit is a small tool that installs a tool's `dist/` directory from a GHCR (GitHub Container Registry) OCI image into a project directory `.<name>/` (git-ignored). After installing it writes a stamp file `.<name>/.stamp`:
- line 1 = the image reference that was installed
- each following line = one file's sha256 (like `sha256sum` output)

Every time the user runs `just <command>`, the launcher first runs `verify`: it recomputes the sha256 of every file in `.<name>/`, compares with the stamp, and aborts on any mismatch ("files were hand-edited; delete and reinstall").

Constraints: the host machine only has Docker + git + just. `verify` runs inside a container (`docker run`), so any tool available in a Linux container image is acceptable, but nothing may be required on the host.

## Open decision #12: baseline and scope of `verify`

Please research and answer the following, with real case links:

### Q1. How existing "post-install integrity check" mechanisms work
For each of the following, describe: (a) where the baseline is stored (a manifest file shipped/generated locally vs. re-fetched from the origin), (b) what is compared (content hash / file set / permissions / owner / symlink target / mtime / size), (c) when it runs (every execution vs. install-time vs. manual only), (d) how extra files not in the manifest are treated.
- dpkg `--verify` (md5sums files) and rpm `-V` (rpmdb; size, mode, md5/digest, dev, link, user, group, mtime, capabilities)
- Nix `nix store verify` (NAR hash, read-only store, `--check-contents`, `--repair`, trusted signatures)
- Go modules `go.sum` and the module cache (`go mod verify`)
- Python wheel `RECORD` file (PEP 427 / PEP 376: path, hash, size) and `pip check` or similar
- Composer `installed.json` / `composer.lock` and npm/pnpm/yarn lockfile `integrity` (SRI) fields; `npm ci`; pnpm `verify-store-integrity`
- Homebrew bottle sha256 and `brew` install receipts
- Terraform `.terraform.lock.hcl` (h1 / zh hashes) and `terraform init` provider verification
- Git's own index (stat cache: mtime/ctime/size/inode, `git update-index --refresh`, racy-git) as a precedent for cheap change detection
- (bonus, if quick) Bazel content-addressed cache / `--experimental_check_output_files`, pre-commit's cache, rustup/cargo `.crates.toml`

### Q2. Protecting the stamp/manifest file itself from tampering
- Where do tools store the hash of the manifest itself (e.g. wheel RECORD excludes its own hash; Debian `Release` file signs `Packages` which hashes `.deb`)?
- Signatures: cosign (sigstore) for OCI images, minisign, GPG for apt Release, Nix store signatures (`nix store sign`, `trusted-public-keys`). Which are realistic when the host has only Docker?
- Alternative: instead of a local manifest, lock the source image digest (`ghcr.io/x/y@sha256:...`) and re-fetch/compare. Any precedent of "re-pull and diff" as integrity check?

### Q3. Performance: how tools avoid hashing everything on every run
- Git stat cache / racy-git (mtime+size, only hash when stat differs)
- Bazel / Buck2 content-addressed digests with mtime cache (`--experimental_check_output_files`, digest cache)
- pnpm `verify-store-integrity` (default true) and how it's implemented (checks mtime?, size?); npm `--ignore-scripts` etc.
- pre-commit cache dir behavior
- Any precedent of "only re-hash when file list/size/mtime changed", sampling, or "hash on install only, trust afterwards".
Give rough numbers if available (e.g. sha256 throughput, cost of stat vs read).

### Q4. Options and recommendation
Compare 2–3 options for vendor_kit's `verify`:
- A. Compare only content sha256 of files listed in the stamp (current behaviour).
- B. Stamp + file set + permissions/executable bit (like rpm -V minus mtime), i.e. detect extra files, missing files, chmod changes.
- C. Re-fetch the locked image digest and diff against installed files (no local trust needed).
For each give pros/cons, and a recommendation. Also explicitly answer: should extra files present in `.<name>/` but not listed in the stamp be treated as "modified"? What do dpkg, rpm, pip, nix, Terraform do with untracked files?

## Output format (required)

Use exactly these headings:
## Q1 Prior art table
(a markdown table: tool | baseline storage | what is compared | when it runs | extra files handling | source URL)
## Q2 Manifest self-protection
## Q3 Performance techniques
## Q4 Options and recommendation
## Sources
(numbered list of all URLs used)
