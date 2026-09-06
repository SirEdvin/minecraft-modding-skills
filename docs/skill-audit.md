# Skill audit scope and verification

The audit covers all 11 installable packages. Reusable skills contain general decision rules and applicable upstream API/source references, not a catalog of the maintainer's projects or session-specific build reports.

## Changes by topic

- Fabric, NeoForge, and legacy Forge: distinguish mappings, plugin behavior, runtime loader identity, and exact-version API contracts.
- 26.1 migration: preserve maintained targets and separate build, mapping, API, and behavior changes.
- Stonecutter: distinguish trees, branches, nodes, ordinary modules, task qualification, and source overrides without prescribing another repository's layout.
- Native UI: separate opening data, menu synchronization, validated server actions, client state, and target-specific rendering APIs.
- Testiarium: retain package-specific implementation references, loader run instructions, source-set boundaries, sequence completion, and runtime verification limits.
- GTCEu: use version-pinned official addon lifecycle and registry APIs.
- KubeJS: distinguish script reload, resource reload, registry restart, and versioned bindings.
- Modrinth: correct endpoint schemas, version selection, identification, and download verification.
- Packwiz: prevent nested-export contamination, detect stale/failed exports, and pin the complete installation chain.

## Verification layers

- Official Agent Skills validation and repository validation check all installable packages.
- Regression tests cover malformed frontmatter, fenced examples, and package-local support reachability.
- Discovery must enumerate the complete catalog.
- Compilation, unit tests, runtime GameTests, client/server behavior, and artifact checks are separate evidence layers. Record actual run results in the PR or test report, not as permanent skill content.

## Project-reference policy

Do not embed maintainer project names, URLs, namespaces, pinned revisions, task paths, or applicability inventories in generic skills. Distill the reusable lesson and use authoritative upstream sources for contracts. The `testiarium-gametest` package is the exception because its subject is that project's actual API and implementation. Attribution and repository installation URLs are not project-usage examples.
