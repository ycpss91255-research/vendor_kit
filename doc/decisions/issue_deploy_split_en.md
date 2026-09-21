## Background

`vendor_kit` (ycpss91255-research/vendor_kit) is replacing the git-subtree distribution: a tool repo packs its `dist/` into a `FROM scratch` GHCR image; a downstream project runs `just vendor_kit add/upgrade` to fetch it, pin the version by digest, and three-way-merge init files. vendor_kit's scope is **moving files only** — it does not understand an application's runtime model. Its single promise about deliverables is: *anything a tool recipe produces must not depend on `.vendor_kit/`, `version.toml`, or GHCR at run time*. base's current deploy bundle already satisfies that (image travels as a tar, compose is fully resolved).

## Question

base's `dist/deploy/` (ADR-00000023: `image.tar.xz` + resolved `compose.yaml` + `.env`/`.env.local` + `config/` overrides + `deploy.sh`) is coupled to base's `setup.conf` → `.env.generated` → resolved-compose pipeline and to the "committed = developer default / not-in-repo = operator overlay" axis.

If a second tool repo ever needs a field bundle, one option is to extract deploy into its own tool repo (e.g. `deploy_kit`, itself a `dist/`; downstream would `add deploy_kit` and get `just deploy …`). vendor_kit would need no change for that.

We would like the base maintainers' assessment:

1. Can the dependency on `setup.conf` / the compose-generation pipeline be separated into a pure interface ("give me image + resolved compose + manifest, I produce the bundle")? What would it cost?
2. If separated, how would base re-attach (would base's `just deploy` call `deploy_kit`)? Who owns `deploy.manifest` and `cd-guard.sh`?
3. Is it worth doing now, or should it wait for a second consumer? (vendor_kit's current decision: deploy stays in base.)

## vendor_kit's current position

- deploy will **not** be built into vendor_kit.
- deploy stays in base; whether to extract it is base's call. vendor_kit only guarantees the run-time-independence rule above.

Tracking issue on the vendor_kit side: ycpss91255-research/vendor_kit#__VK__
