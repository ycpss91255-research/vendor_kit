# Research brief part 2 (vendor_kit decision #12: baseline and scope of `verify`)

Do NOT run shell commands and do NOT use the read_url/fetch tool (they are auto-denied in headless mode); use ONLY the web search tool and its result snippets. Be CONCISE: total output under 150 lines. Every claim must cite a real, working URL (official docs, man pages, GitHub source, issue threads). If you cannot find a source, write "not found" instead of guessing. Do NOT invent URLs.

## Background
vendor_kit installs a tool's `dist/` from a GHCR OCI image into a project dir `.<name>/` (git-ignored) and writes `.<name>/.stamp`: line 1 = installed image ref, following lines = sha256 of each file. On every `just <cmd>` a launcher runs `verify` inside a container (`docker run`): recompute sha256 of every file under `.<name>/`, compare with the stamp, abort on mismatch ("hand-edited; delete and reinstall"). Host has only Docker + git + just.

## Part A — Sources for a prior-art table (already drafted; I only need URLs)
Provide one authoritative URL for each of these claims (man page / official doc / source file):
1. dpkg `--verify` uses `/var/lib/dpkg/info/<pkg>.md5sums`, md5 only, manual, ignores extra files.
2. rpm `-V` attributes S M 5 D L U G T P, from rpmdb, manual, ignores unowned files.
3. `nix store verify` NAR hash + signatures, `--check-contents`, store read-only 0444/0555, manual.
4. `go mod verify` + `go.sum` h1: dirhash; module cache made read-only; "dir has been modified".
5. Wheel RECORD (PEP 376/427) path,hash,size; checked at install only; `pip check` only checks deps.
6. Composer `composer.lock` dist shasum / `composer status`.
7. npm `package-lock.json` integrity (SRI) and `npm ci`; pnpm `verify-store-integrity` option.
8. Homebrew bottle sha256, INSTALL_RECEIPT.json.
9. Terraform `.terraform.lock.hcl` zh:/h1: hashes verified only at `terraform init`.
10. Git index stat cache / racy-git.
11. Bazel `--experimental_check_output_files`.
12. Cargo vendor `.cargo-checksum.json`.
13. pre-commit cache.

## Part B — Q2: protecting the stamp/manifest file itself
- Where do tools store the hash of the manifest itself (wheel RECORD omits its own hash; Debian Release signs Packages which hashes .deb; Nix narinfo Sig; Terraform lock hashes)?
- Signatures usable when the host only has Docker: cosign/sigstore for OCI images (`cosign verify`, keyless), minisign, GPG for apt Release, Nix `nix store sign`. Cite docs.
- Alternative: lock the source image digest (`ghcr.io/x/y@sha256:...`) and re-pull + diff. Any precedent of "re-fetch and diff as integrity check" (e.g. Nix `--repair`, `go mod verify` re-download, `terraform init` re-verify, `git fsck`)?

## Part C — Q3: performance, avoiding full re-hash each run
- Git racy-git / stat cache (mtime+size, hash only if stat differs) — cite Documentation/technical/racy-git.txt.
- Bazel digest cache / `--experimental_check_output_files`; Buck2.
- pnpm `verify-store-integrity` implementation (checks size/mtime? sha512?) — cite pnpm source or docs.
- Any precedent of "hash on install only, trust afterwards" or "only re-hash when stat changed", or sampling.
- Rough numbers: sha256 throughput (MB/s) on typical CPU; stat cost vs read.

## Part D — Q4: options and recommendation for vendor_kit verify
Compare:
- A. content sha256 of files listed in stamp only (current).
- B. stamp + file set (missing/extra) + mode/executable bit (rpm -V minus mtime).
- C. re-pull locked image digest and diff against installed files.
Pros/cons each, a recommendation, and explicitly: should EXTRA files not in the stamp be treated as "modified"? What do dpkg, rpm, pip, nix, go, terraform do with untracked files (cite)?

## Output format (required headings)
## Part A sources
(numbered 1..13 matching above, one URL each)
## Q2 Manifest self-protection
## Q3 Performance techniques
## Q4 Options and recommendation
## Sources
(all URLs used, numbered)
