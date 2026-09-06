# Reproducibility and representative-source audit

## Packwiz source boundary

Reviewed source commit
[`dfd8b68a4796c763e25bad50265ea1f1233e24f1`](https://github.com/packwiz/packwiz/tree/dfd8b68a4796c763e25bad50265ea1f1233e24f1):

- `core/index.go` default ignore list excludes root `/*.zip`, but not arbitrary
  nested ZIP exports. A previous `build/my-pack.zip` can enter the index on the
  next refresh/export unless `/build/` is explicitly ignored. Export outside the
  pack root (the workflow examples use a sibling `pack-exports` directory).
- `modrinth/export.go` refreshes before export; several error paths print an error
  and return rather than exit nonzero. Do not accept exit code alone: require a
  newly produced nonempty archive, parse its manifest, and inspect entries. Use a
  clean destination so a stale artifact cannot masquerade as successful output.
- `migrate/loader.go` changes the version of the already-selected single loader;
  it is not a generic Forge-to-Fabric conversion command. Exact versions still
  resolve loader metadata; `latest`/`recommended` are not reproducible release inputs.

The Packwiz binary is not available in every environment. Source inspection and
TOML/hash fixtures establish only the inspected contracts, not CLI execution.
Check the installed binary's help before using commands on another revision.

## Official example pack

[packwiz-example-pack at 313b70b](https://github.com/packwiz/packwiz-example-pack/tree/313b70b6be4ef05194c1f6898b42da1dbabcfb80)
provides a pinned, small **Minecraft 1.19 / Quilt 0.17.0** example:

- `pack.toml`: format `packwiz:1.1.0`, exact game/loader and index hash;
- `index.toml`: SHA-256 inventory, metafile markers;
- `mods/borderless-mining.pw.toml`: client side, explicit CDN URL/SHA-1,
  Modrinth project `kYq5qkSL`, version `gqoXgtxO`;
- `.packwizignore`: intentionally excludes `/README.md` from installation.

This is provenance for pack structure, not a recommendation to use its old mod
versions or its SHA-1-only metadata for newly authored downloads. A disposable
TOML/hash check verified this example's manifest-to-index hash and every indexed
file (`LICENSE` and both mod metafiles) without downloading JARs. This was Python
`tomllib`/`hashlib` verification over pinned public source bytes, not Packwiz CLI
execution.

## Installer and hosting pins

Pin/checksum bootstrap **and** the installer implementation it resolves; a pinned
bootstrap alone need not pin the downloaded installer. Read the matching bootstrap
options/source before changing resolution behavior. Serve an immutable release
snapshot of `pack.toml`, its index, metadata and authored files atomically. Never
publish a new manifest before its referenced content is available. A checksum
chain does not keep an upstream CDN alive; retain permitted artifacts or document
availability limitations. No public publication is part of a source audit.
