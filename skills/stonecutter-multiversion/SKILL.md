---
name: stonecutter-multiversion
description: Maintain multi-version mods with Stonecutter.
license: MIT
compatibility: Stonecutter 0.9.8 on Gradle 9.0+; plugin, loader, game, and Java versions are version-sensitive.
metadata:
  version: "0.1.0"
  author: Hermes
  hermes-tags: "Stonecutter, Gradle, Minecraft, Modding"
---

# Stonecutter Multi-Version Modding

Use Stonecutter to set up, develop, test, and maintain Minecraft mods across compatible game versions and loaders from one shared source tree. This skill does not replace Fabric or NeoForge API guidance and is a poor fit when each target needs a near-total rewrite. It uses the project's Gradle wrapper and official Stonecutter documentation/templates; no separate script is required.

## When to Use

- “Set up Stonecutter for this mod.”
- “Add or remove a supported Minecraft version.”
- “Switch, build, test, or release every Stonecutter node.”
- “Maintain Fabric and NeoForge variants from shared sources.”
- “Fix Stonecutter comments, swaps, replacements, or properties.”
- “Upgrade Stonecutter or clean preprocessing noise before commit.”

## Prerequisites

- A Gradle project with `gradlew`; Stonecutter 0.9.7 requires Gradle 9.0 or newer.
- A JDK/toolchain for every target Minecraft version; loader plugins may provision toolchains, but verify them before building.
- No environment variables or credentials are required for local switching/building. Publishing credentials belong to the selected publishing plugin, not Stonecutter.
- Before setup or upgrade, use `web_extract` on `https://stonecutter.kikugie.dev/wiki/v2/`, `https://stonecutter.kikugie.dev/blog/changes/0.9`, and `https://plugins.gradle.org/plugin/dev.kikugie.stonecutter`.
- Reviewed 2026-09-06: the portal lists 0.9.8 (published 2026-08-31); the wiki already documents 0.10 APIs. Match examples to the installed plugin, not merely the newest documentation. The 0.9.8 changelog adds IDE parameter-ID annotations and updated documentation links; do not infer a 0.10 runtime API from that release.
- Prefer an official template when migrating an existing mod: Fabric `https://codeberg.org/stonecutter/template-fabric`, NeoForge `https://codeberg.org/stonecutter/template-neoforge`, or multi-loader `https://codeberg.org/stonecutter/template-multiloader`.
- The optional IntelliJ plugin is `https://plugins.jetbrains.com/plugin/25044-stonecutter-dev`.

## How to Run

From the repository root, inspect `settings.gradle(.kts)`, `stonecutter.gradle(.kts)`, shared build scripts, `stonecutter.properties.*`, `gradle.properties`, `versions/`, and `src/` with `read_file` and `search_files`. Then invoke the project wrapper through the `terminal` tool:

```bash
./gradlew projects
./gradlew tasks --all
./gradlew build
```

Never guess generated task names or project paths. Read them from `projects` and `tasks --all`, especially when a project separates logical versions from node names. For multiple library trees, first read [real-project topology and task discovery](references/project-topology.md); a Gradle repository root is not necessarily a Stonecutter controller.

Load detailed topics on demand with `skill_view(name="stonecutter-multiversion", file_path="references/<file>")`:
- `references/properties-and-data-setup.md`: load for property resolution, typed/raw access, JSON schemas, CI matrices, inheritance, or 0.10 accessor migration.
- `references/controller-and-replacements.md`: load for lazy aggregation, ordering, lifecycle hooks, IDE flags, reversible replacements, or version-sensitive syntax.

These references distinguish release evidence from forward-looking wiki APIs and record unresolved documentation conflicts; verify tagged implementation when a disputed feature matters.

## Quick Reference

```text
./gradlew "Set active project to <project>"
./gradlew "Refresh active project"
./gradlew "Reset active project"
./gradlew :<project>:build
./gradlew :<project>:runClient
./gradlew :<project>:runServer
./gradlew build
```

Settings register trees/branches/nodes; `stonecutter.gradle.kts` is the controller, `build.gradle.kts` or `build.<loader>.gradle.kts` is the node template, `stonecutter.properties.*` supplies structured values, and `src/` reflects the active node. Node directories are `versions/<project>/`; inactive sources under their `build/generated/stonecutter/` are disposable.

## Procedure

1. **Inventory the existing model.**
   - Use `search_files` to locate `dev.kikugie.stonecutter`, `stonecutter active`, `vcsVersion`, `versions(`, `version(`, `.buildscript(`, `//?`, `/*?`, `//$`, and `//~`.
   - Record each tree, branch, node project name, logical version, build script, loader, active node, VCS node, property source, Java level, build/test/run tasks, and publication task.
   - Choose Stonecutter for compatible deltas. Prefer separate branches/projects when target implementations are mostly unrelated.

2. **Create or align the settings model.** The published 0.9.8 plugin uses this Kotlin DSL setup (retain an existing pin unless an upgrade is in scope):

   ```kotlin
   plugins {
       id("dev.kikugie.stonecutter") version "0.9.8"
   }

   stonecutter {
       create(rootProject) {
           versions("1.20.1", "1.21.1")
           version("1.21.11-snapshot", "1.21.11-rc2")
           vcsVersion = "1.21.1"
       }
   }
   ```

   - `versions(...)` uses each project name as its logical version.
   - `version(project, version)` separates directory/node identity from conditional comparison.
   - `active` and `vcsVersion` always use project names, not logical versions.
   - For loader-specific scripts, append `.buildscript("build.fabric.gradle.kts")` or the matching real filename.
   - For Groovy controller/build scripts, set `kotlinController = false` and `centralScript = "build.gradle"`; never set `centralScript` to the Stonecutter controller filename.
   - Keep one tree when branches must switch together; separate trees switch independently.
   - Set `vcsVersion` deliberately. It is the canonical pre-commit source state.

3. **Configure the controller.** Apply the plugin and assign the active node exactly once in `stonecutter.gradle.kts`:

   ```kotlin
   plugins {
       id("dev.kikugie.stonecutter")
   }

   stonecutter active "1.21.1"

   stonecutter parameters {
       dependencies["example_api"] = project.property("deps.example_api") as String
       constants["release"] = project.property("mod.id") != "template"
   }
   ```

   - A literal active value is rewritten during switching.
   - `stonecutter active file("active.txt")` uses file-backed state. Before the first configuration, seed that UTF-8 file with one exact registered project name; switch tasks maintain it afterward.
   - `stonecutter active null` is detached mode for CI: shared `src/` is not linked as an active source and each node uses generated sources.
   - Configure Stonecutter flags before the `active` statement.
   - Keep only Stonecutter configuration in `parameters {}`; configure ordinary dependencies/tasks in node build scripts.
   - In 0.9.7, prefer `project.property()` over `node.project.property()` inside `parameters {}`.

4. **Parameterize node builds instead of cloning build scripts.**
   - Use `sc.current.project`, `sc.current.version`, and `sc.current.parsed` in build scripts.
   - Use `sc.current.parsed >= "1.21"`, `sc.current.parsed eq "1.21"`, or `sc.current.parsed matches ">=1.21 <1.21.5"` in Kotlin DSL; use `.matches(...)` in Groovy.
   - Keep shared values in the root and per-node values under `versions/<project>/gradle.properties`, or use `stonecutter.properties.toml|yaml|json5`.
   - Structured properties automatically use branch ID and project name as tags. For flat `{version}-{loader}` nodes, add both explicitly:

   ```kotlin
   stonecutter {
       val (version, loader) = current.project.split('-', limit = 2)
       properties.tags(version, loader)
       constants.match(loader, "fabric", "neoforge")
   }
   ```

5. **Express the smallest source delta.** Read [source syntax and layouts](references/source-and-layout.md) for conditions, swaps, replacements, resource handlers, and multi-loader layout choices. Keep released 0.9.x APIs; do not import 0.10 syntax implicitly.

6. **Use the daily switching ritual.** Invoke through `terminal`:

   ```bash
   ./gradlew projects
   ./gradlew tasks --all
   ./gradlew "Set active project to 1.21.1"
   ```

   - Before the first switch in an existing repository, inspect `git status`; checkpoint or stash unrelated source changes because switching rewrites tracked files.
   - Replace `1.21.1` only with an exact generated task suffix from `tasks --all`.
   - Edit shared `src/` only after switching to the node being developed.
   - Run that node's real compile, test, datagen, client, and dedicated-server tasks.
   - Run `./gradlew "Refresh active project"` when comment/swap/replacement states look inconsistent.
   - Never edit `versions/<project>/build/generated/stonecutter/`; inactive-node sources are derived and disposable.

7. **Add or remove a supported node.**
   - Before removing the active or VCS node, switch to a retained node; if necessary, select a retained `vcsVersion` and reset to it before deleting the old declaration.
   - Update the node declaration in `settings.gradle(.kts)` or its JSON/TOML/YAML settings file.
   - Add/remove every corresponding dependency, loader, Java, metadata compatibility, publishing, and test-matrix property.
   - Invoke `./gradlew projects` and `./gradlew tasks --all` through `terminal`; verify the exact node and loader task paths.
   - Switch to the new/nearest node, adapt conditional code, and test the active runtime.
   - Run root `./gradlew build` to build all nodes from shared/generated sources.
   - For removals, use `search_files` to clear stale project names, logical versions, constants, properties, publication selectors, and CI matrix entries; then remove the obsolete `versions/<project>/` directory and inspect the complete diff.

8. **Build, release, upgrade, and commit cleanly.**
    - Root `./gradlew build` builds all registered nodes; node-qualified `build`, `runClient`, and `runServer` target one node.
    - `buildAndCollect` is an official-template convenience task, not a core Stonecutter task. Confirm it exists before invoking it.
    - Aggregate only a publishing task that the applied publishing plugin actually registers, using `stonecutter.tasks.named("actualTaskName")`; do not assume official templates provide publishing tasks or eagerly call `.get()`.
    - Before upgrading Stonecutter, read every changelog entry from the installed version to the target, update the Gradle wrapper if required, sync, list projects/tasks, perform a switch/reset round trip, then build all nodes.
    - Before commit, invoke `./gradlew "Reset active project"`, inspect `git diff`, and confirm changes are intentional source/config edits rather than active-version noise.

## Pitfalls

- Stonecutter 0.9.7 generates tasks named `Set active project to ...`, `Refresh active project`, and `Reset active project`; some prose/docs still say “version.” Trust `tasks --all`.
- Switching rewrites the active literal and shared source state. It does not discard legitimate edits or guarantee a clean tree if the previous state was stale. A first round trip can normalize comment formatting; compare repeatability after reviewing that normalization.
- Run switching/reset and compilation as separate Gradle invocations. In a 0.9.8 / Gradle 9.6.1 fixture, combining reset and build in one invocation caused an implicit task-dependency failure because source links were configured before switching.
- Shared `src/` reflects the active node, but explicitly qualified inactive-node run/test tasks can execute generated sources when the loader exposes them. Generated-file edits are still disposable.
- A file under `versions/<project>/src/` overrides the corresponding shared/generated file for that node; review overrides before assuming a shared edit reaches every node.
- A green active-node build does not prove all nodes compile; run the root build.
- Earlier inspection found official templates pinned to 0.9.6; that is historical, not a live guarantee. Read each template's current pin before adopting it.
- Parallel NeoForge node builds may need the official multi-loader template's `createMinecraftArtifactsMutex` build service with `maxParallelUsages.set(1)` to serialize Minecraft artifact generation.
- Generated source tasks are in `stonecutter-impl` and say “Do not call manually.” Use normal build/test tasks unless integrating a loader lifecycle dependency such as NeoForge `createMinecraftArtifacts` depending on `stonecutterGenerate`.
- String replacements reject ambiguous/cyclic mappings; regex replacements lack those safety guarantees.
- Enable named replacements before code for file-wide effect; later `//~ id` / `//~ !id` directives intentionally set/reset processing for subsequent regions, not a boolean toggle.
- `parameters {}` is lazily evaluated Stonecutter configuration, not a substitute for `subprojects {}` build customization.
- Native `gradle.properties` still controls `org.gradle.*` launch settings; structured properties only supply build-script values.
- Do not apply `base`/`java` to a Stonecutter tree controller; its nodes are buildable projects. An ordinary monorepo root outside those trees may apply `java` or aggregate tasks. Do not remove it merely because Stonecutter is used elsewhere.
- If `dev.kikugie.stonecutter.no_short_extension` is present in `gradle.properties`, use the full `stonecutter` extension; its mere presence disables the `sc` alias, even when set to `false`.
- `generate_sources_on_sync=true` makes preprocessing errors fail IDE sync; the current wiki documents true as the default. Diagnose preprocessing before treating sync failure as broken IDE integration.
- Do not set Gradle `group` blindly: official Fabric and multi-loader templates intentionally keep `mod.group` as metadata without assigning `project.group`.
- Do not bundle every Minecraft version into one mod JAR. Build and publish version-specific artifacts.

## Verification

Invoke the repository-wide build through the `terminal` tool and confirm the task report includes every intended node; success verifies compilation for the executed targets, not client/server behavior, publication, or skipped tasks:

```bash
./gradlew build
```
