# Research brief: prior art for "local development mode" of a vendored-tool installer (vendor_kit decision #6)

You are doing prior-art research. Use web search extensively. Every claim must cite a real, working source URL (official docs, man pages, source code on GitHub, RFCs, design docs, issue threads, blog posts by maintainers). If you cannot find a source for something, say explicitly "not found" instead of guessing. Do NOT invent URLs. Answer in English or Chinese, structured with the headings requested at the end.

## Background

vendor_kit is a small framework:
- A *tool repo* has a `dist/` directory. CI packages `dist/` into a GHCR OCI image named `<name>-dist:vX` (its Dockerfile is `FROM vendor_kit`, so the image contains both the vendor_kit runtime and `/dist`).
- A *project repo* has a version file `.version` with lines like `<name> = "ghcr.io/org/<name>-dist:v3@sha256:..."`.
- A launcher (a `justfile`) runs, on every invocation: `docker run --rm -v $PWD:/repo <image> --name <name> install|verify|...`. `install` copies the image's `/dist` into the project's `.<name>/` (git-ignored) and writes a stamp file `.<name>/.stamp` (image ref + per-file sha256). `verify` recomputes the sha256s and aborts on mismatch.
- Constraint: the host machine only has Docker + git + just. Nothing else may be required on the host.

## The problem (open decision #6: local development mode)

The person *developing the tool itself* edits `dist/` in the tool repo and wants to try it immediately inside some project repo, WITHOUT doing `docker build` + `docker push` + updating `.version` for every single line change. We need to design a "local dev mode".

## Questions

### Q1. Prior art: how do existing tools express "use my local checkout instead of the published version"?
For EACH of the following, describe with source links: (i) where the local path is expressed - is it written into the *same* versioned manifest file, or into a *separate* file that is not committed to git? (ii) how do they prevent the local path from being committed accidentally (gitignore convention, warning, CI failure, lockfile behaviour, etc.)? (iii) how do you switch back to the published version?
1. npm `link` / pnpm `link` / yarn `link` (and `file:` / `link:` protocol dependencies, pnpm `overrides`, yarn `portal:`)
2. pip `-e` / editable installs (PEP 660), also `pip install -e` and `requirements-dev.txt` conventions
3. Go `replace` directive in go.mod vs `go.work` workspaces (why go.work is a separate file, `go.work` in .gitignore recommendation, `-modfile`, `GOFLAGS=-mod=mod`)
4. Cargo `[patch]` section, path dependencies, and `.cargo/config.toml` `[patch]` / `paths` override (why a config-level override exists in addition to Cargo.toml)
5. Nix flakes: `--override-input`, `path:` inputs, `flake.lock`
6. Terraform `dev_overrides` in the CLI config file (`.terraformrc` / `provider_installation { dev_overrides {...} }`) - why in CLI config and not in `.tf` files, and what happens to the lock file / `terraform init` in that mode
7. Bazel `--override_repository` / `--override_module` (bzlmod), typically in `.bazelrc` or `user.bazelrc` (gitignored), and `local_path_override` in MODULE.bazel
8. Helm: `helm install ./local-chart` (local path) vs repository chart; `dependencies` with `file://` repository in Chart.yaml
9. Gradle `includeBuild` composite builds and `--include-build` CLI flag; `settings.gradle` vs init scripts
10. Dagger modules: local module path vs git ref (`dagger call -m ./path` vs `-m github.com/...`), dagger.json dependencies with local paths
11. Copier: `--vcs-ref` and using a local directory as template; `_src_path` in `.copier-answers.yml`
12. Any other relevant examples you find (e.g. Docker Compose `override` files, `docker-compose.override.yml` convention; Deno import maps; Bun `link`; Poetry path dependencies with `develop = true`; Homebrew `--HEAD`; asdf/mise `path:` version source; pre-commit `repo: local` and `try-repo`; Renovate/dependabot handling of path deps).

### Q2. Under our constraints, two candidate designs. Which pattern does prior art favor and why?
(a) Allow `.version` to contain `<name> = "path:../tool"`. The launcher then runs `docker run -v ../tool/dist:/dist:ro vendor_kit:vN ...` - i.e. use the bare vendor_kit image and bind-mount the developer's local `dist/` over `/dist`, instead of using the published tool image.
(b) Do NOT touch `.version`. Add a separate, git-ignored `.version.local` file whose entries override `.version`.
Please discuss: why Go chose go.work as a separate file rather than encouraging `replace` in go.mod (link to the Go workspace design doc / proposal 45713); why Terraform put dev_overrides in the CLI config rather than in .tf; why Cargo has both `[patch]` in Cargo.toml and config-level overrides; why Bazel encourages `user.bazelrc`; why docker-compose has an override file convention. Then say which of (a)/(b) (or a hybrid) prior art favors.

### Q3. Integrity checks in dev mode
In dev mode the local `dist/` changes constantly, so a sha256 stamp will always mismatch. How do prior-art tools handle integrity / lock / reproducibility checks when a dependency is a local path or editable install? E.g.: does npm/pnpm lockfile record `link:`/`file:` deps without integrity hash? does Go skip go.sum for replaced-path modules? does Cargo.lock record checksum for path deps? does Nix flake.lock record path inputs? does Terraform skip the dependency lock file for dev_overrides (and print a warning on every run)? does pip freeze show `-e` entries? Do they: skip verification, reinstall on every run, use symlinks so nothing is copied, or print a persistent warning banner?

### Q4. Give 2-3 concrete design options for vendor_kit and a recommendation
Consider: (a) `path:` in `.version`, (b) `.version.local` override, (c) an environment variable such as `VENDOR_KIT_DEV_<NAME>=../tool` or a `just dev <name> ../tool` command, (d) hybrid. For each: how it handles the stamp/verify, how it avoids committing local paths, how you switch back, visibility (does the user notice they are in dev mode - e.g. Terraform's warning banner), and the Docker specifics (bind mount of `../tool/dist` over `/dist`, read-only, path resolution relative to the project). Give a recommendation with reasons, grounded in the prior art found.

## Output format
Use these headings, in this order:
1. `## Prior-art table` - a Markdown table: tool | where local path lives (same manifest / separate uncommitted file / CLI flag / env) | how accidental commit is prevented | how to switch back | source URL(s)
2. `## Same-file vs separate-file: what prior art prefers and why` - with links to the design rationale docs
3. `## Integrity / lock behaviour in dev mode` - per tool, with links
4. `## Design options for vendor_kit and recommendation`
5. `## Sources` - full list of URLs actually used
Mark anything you could not find as "not found". Keep the whole answer under ~250 lines.
