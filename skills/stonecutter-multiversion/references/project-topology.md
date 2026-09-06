# Real-project topology and task discovery

## Pinned evidence

Source inspection was supplemented by successful `projects tasks --all` discovery in disposable clones of both pins; this is not a claim that Minecraft builds or GameTests ran. Both projects pin Stonecutter **0.9.7**; retain that pin when using them. The separately tested 0.9.8 Java fixture does not upgrade their loader compatibility.

- [TemplateProject settings](https://github.com/SirEdvin/TemplateProject/blob/042d296e255d6a9e75e1d2f40da9937810e92004/settings.gradle.kts) and [controller](https://github.com/SirEdvin/TemplateProject/blob/042d296e255d6a9e75e1d2f40da9937810e92004/stonecutter.gradle.kts).
- [Minecraft-Modding-Libs settings](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/settings.gradle.kts), [root build](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/build.gradle.kts), [Testiarium controller](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/testiarium/stonecutter.gradle.kts), and [Fabric node build template](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/testiarium/fabric/build.gradle.kts).

## Distinguish tree, branch, node, and ordinary module

| Concern | Flat TemplateProject | Minecraft-Modding-Libs monorepo |
| --- | --- | --- |
| Tree controller | Repository root | Each of `:broccolium`, `:testiarium`, `:tweakium`, `:peripheralium` |
| Branch | Root branch | Root/common branch plus `fabric` and `forge` per tree |
| Node identity | `1.20.1-fabric`, `1.20.1-forge`, `1.21.1-fabric`, `1.21.1-neoforge` | `1.20.1` or `1.21.1` within each branch |
| Logical version | Loader suffix removed by explicit `version(project, version)` | Same as node name |
| Node path example | `:1.21.1-fabric` | `:testiarium:fabric:1.21.1` |
| Common node | No separately published common node | `:testiarium:1.21.1` |
| Non-Stonecutter module | None in this comparison | `:typed-peripheral-api` |

The monorepo maps project directories to `projects/<name>`; Gradle paths do **not** gain a `:projects:` prefix. Its `create("broccolium", "testiarium", "tweakium", "peripheralium")` creates separate trees, not one tree with four library branches. Within each tree, the loader branches share switching state. Across trees, inspect and reset each controller independently.

The `forge` branch hosts **Forge on 1.20.1 and NeoForge on 1.21.1**. Directory name alone is not loader identification: check conditional plugin application and imports. The controller derives `neoforge` and `legacyforge` constants from branch plus logical version.

The root applies `java` but is not a Stonecutter controller. Removing it because a single-tree template forbids `java` on its controller root would be incorrect.

## Discover, scope, then execute

In a writable development checkout with permission to configure Gradle:

```bash
./gradlew projects
./gradlew :testiarium:tasks --all
./gradlew :testiarium:fabric:1.21.1:tasks --all
./gradlew :testiarium:fabric:1.21.1:build --dry-run
```

Captured discovery confirms these projects and task inventories: TemplateProject has four node subprojects; Minecraft-Modding-Libs has 37 subprojects, including 24 versioned leaves, its tree/branch controllers, and the ordinary typed API module. The example dry-run is a next-step verification, not an executed build. Reconfirm tasks in your checkout. For read-only audits, inspect tracked settings/build/CI instead: Gradle configuration itself writes caches and may generate sources.

- Quote a **fully qualified** discovered controller switch task when only one tree should switch. The captured listing includes `:testiarium:Set active project to 1.21.1` and `:testiarium:Reset active project`. Unqualified task selection can reach multiple matching projects. Task-list parsers must retain names containing spaces, or they will silently omit these user-facing tasks.
- Run switching/reset first; start compilation in a separate Gradle invocation. Preserve the core skill's 0.9.8/Gradle 9.6.1 implicit-dependency warning.
- Trace inter-library dependencies using the matching version node. The Fabric Testiarium build uses `project(":testiarium:${sc.current.project}")`, not an old `:testiarium-core` path.
- Inspect explicit `sourceSets["testMod"]` and `sourceSets["cctTestMod"]` outputs: compiling main code does not establish that loader runs load those test classes, metadata, and mixins.
- Check the root `build` task graph includes intended leaves; distinguish `build` task selection from `:build`, which explicitly targets only the root task and its declared dependencies.
- The pinned CI invokes `./gradlew build --no-daemon`; it does not invoke the configured Minecraft client or GameTest server tasks. Do not report those runtime checks as CI coverage.

## Overrides and canonical state

At the pin, Testiarium's controller is active on `1.20.1`, while settings select `1.21.1` as `vcsVersion`. Neither is evidence of corruption. Shared source can intentionally remain in another active state; reset is a source-changing operation, not an audit step.

Read `projects/<library>/versions/<node>/src/...` **and** `projects/<library>/<loader>/versions/<node>/src/...` overrides before porting. The monorepo uses complete 1.21.1 replacements for registration, assertions, and client runner APIs; changing only shared 1.20.1 files can leave 1.21.1 unchanged.
