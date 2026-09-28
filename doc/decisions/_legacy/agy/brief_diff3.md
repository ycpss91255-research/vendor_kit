# Research brief: should `just diff` in vendor_kit do a 3-way comparison?

You are doing PRIOR-ART RESEARCH. Use web search extensively. Every claim MUST cite a real, specific URL (official docs, source code on GitHub, man pages, issue threads). If you cannot find a source for something, say explicitly "not found" instead of guessing. Do NOT invent URLs. Do not read or modify local files; this is a pure web-research task.

## Background

vendor_kit is a tool distributed as a container image. Its `init` subcommand copies templates from the tool's `dist/` directory (Dockerfile, setup.toml, git hooks, ...) into the user's project as "initial files". After that, the user owns and maintains those files; tool upgrades never touch them.

After upgrading the tool, the user runs `just diff`. Currently this is a TWO-WAY comparison: the new template inside the image vs. the user's current file. It prints a unified diff and does not modify anything.

Problem: the user's own edits and the tool's upstream template changes are mixed together in the same diff. The user cannot tell which hunks are "the tool changed this" vs. "I changed this".

Open decision #11: should `diff` be a THREE-WAY comparison? (old template -> new template = what the tool changed; old template -> user file = what the user changed.)

Constraint/principle of this project: the tool must NOT automatically modify user-owned files.

## Questions to answer (with links to real examples / docs / source)

### 1. How template-upgrade tools handle this

For each of the following, answer: (a) where is the OLD baseline stored (a version/commit ref that lets you regenerate the old template, vs. a stored copy of the old output), (b) does it only DISPLAY differences or does it MERGE for you, (c) how are conflicts presented (conflict markers inline, .rej files, prompts, etc.)?

- Copier: `.copier-answers.yml` records the old template commit; `copier update` does a 3-way merge; conflict markers vs .rej mode (`--conflict` option). Link to docs and, if possible, the relevant source in copier's repo (e.g. how it regenerates the old template from the recorded commit).
- Cruft: `.cruft.json` records template + commit; `cruft check`, `cruft diff`, `cruft update` (produces `.rej` files on conflict). Link docs/source.
- Rails `rails app:update` (and the older `rake rails:update`): how it handles conflicts (interactive y/n/a/q/d/h prompts via Thor), and the community tool RailsDiff (railsdiff.org) that shows "what changed between generated apps of version X and Y".
- Yeoman: conflicter (`yeoman-generator` conflicter / mem-fs-editor), prompts y/n/a/x/d/h, `--force`.
- Projen: generated files are marked as managed and overwritten on every `projen` run; how it handles user edits (it does not merge; files are "owned" by projen; `.projenrc`). Link to docs.
- Nx migrations (`nx migrate` / `migrations.json`): code-mod based, not template-diff based. Link.
- cookiecutter: why it has no `update` command (link to the GitHub issue(s) discussing this and the reasons; e.g. cookiecutter/cookiecutter issue about updating existing projects) and how cruft/copier arose to fill that gap.
- Debian dpkg conffiles: the "Configuration file '/etc/...' ==> Modified (by you or by a script) since installation" prompt with options Y/I/N/O/D/Z; where dpkg stores the old md5sum (`/var/lib/dpkg/info/*.conffiles` and the status file); `.dpkg-dist` / `.dpkg-old` files. And `ucf` (Update Configuration File) which does a 3-way merge using stored copies in `/var/lib/ucf/cache` and `/var/lib/ucf/hashfile`. Link to dpkg and ucf man pages / Debian policy.
- Any other relevant prior art you find (e.g. Ansible/Chef "managed by" headers, Nix home-manager, `git rerere`, Django/other scaffolders, `terraform`-style generated file ownership, Bazel/`buildifier`, npm `create-*` tools) - optional.

### 2. Implementing a 3-way comparison

- `git merge-file` (man page; exit code = number of conflicts; `-p`, `--diff3`, `--zdiff3` styles).
- GNU `diff3` (`-m` merge mode, `-A`/`-E`/`-X`, exit codes).
- `patch --merge` (GNU patch 2.7+: `--merge`, `--merge=diff3`).
- In a container that only has the Python standard library: what can `difflib` do? It has `SequenceMatcher`, `unified_diff`, `ndiff`, but NO built-in 3-way merge. Are there known small pure-python 3-way merge implementations (e.g. `merge3` package by Bazaar/Breezy authors, `diff3` implementations on PyPI, `diff-match-patch`)? Link to them. Note that the tool's constraint is stdlib-only inside the image unless it vendors a tiny module.
- Also: a cheap alternative to a true 3-way merge is to just compute TWO two-way diffs (old->new = tool changes, old->user = user changes) and show them side-by-side, plus the set of files/hunks that overlap. Any prior art doing exactly that (e.g. `cruft diff` semantics, RailsDiff)?

### 3. Cost of keeping a copy of the old template baseline

Options for our tool:
- (i) Keep the old template copy inside `.<name>/` (a per-project directory that is NOT committed to git and is overwritten on every upgrade -> the baseline copy would be lost after upgrade unless captured first).
- (ii) Keep the old copy committed in the project, e.g. `.vendor_kit/base/<name>/` (goes into git; grows with number of templates; noisy in PRs).
- (iii) Store only the old image digest / version in a metadata file and re-pull the old image to regenerate the baseline (needs network + registry access + old image still exists).

What did prior art choose? Copier/cruft store a git ref and regenerate via git clone (option iii-like, but cheap because git). dpkg stores only an md5sum of the original (cannot do 3-way, only "modified or not"). ucf stores full copies in `/var/lib/ucf/cache` (option ii-like). Rails stores nothing (relies on railsdiff.org externally). Confirm each with links.

### 4. Recommend among options

- A: keep 2-way diff (status quo).
- B: 3-way, DISPLAY ONLY, output split into three sections: "tool changed", "you changed", "both changed (conflict)". No files written.
- C: 3-way + auto-merge non-conflicting hunks and write back to user files; leave conflict markers for conflicting hunks.

Give pros/cons of each, and a recommendation given the project's principle "the tool never auto-modifies user-owned files". Consider also what happens to the baseline copy when `init` was run by an old version that did not save a baseline (migration/bootstrapping problem), and what to do when the baseline is missing (fall back to 2-way).

## Output format

Write in English or Chinese, Markdown. Be concrete. Each section MUST end with a "Sources" list of URLs actually consulted. Mark anything you could not verify as "NOT VERIFIED".
