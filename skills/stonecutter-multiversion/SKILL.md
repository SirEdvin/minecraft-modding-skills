---
name: stonecutter-multiversion
description: Maintain multi-version mods with Stonecutter.
license: MIT
compatibility: Stonecutter 0.9.7 on Gradle 9.0+; plugin, loader, game, and Java versions are version-sensitive.
metadata:
  version: "0.1.0"
  author: Hermes
  hermes:
    tags:
      - Stonecutter
      - Gradle
      - Minecraft
      - Modding
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
- Before a new setup or plugin upgrade, use `web_extract` on `https://stonecutter.kikugie.dev/wiki/start/settings` and `https://stonecutter.kikugie.dev/blog/changes/0.9`, then confirm the current release at `https://plugins.gradle.org/plugin/dev.kikugie.stonecutter`.
- Prefer an official template when migrating an existing mod: Fabric `https://codeberg.org/stonecutter/template-fabric`, NeoForge `https://codeberg.org/stonecutter/template-neoforge`, or multi-loader `https://codeberg.org/stonecutter/template-multiloader`.
- The optional IntelliJ plugin is `https://plugins.jetbrains.com/plugin/25044-stonecutter-dev`.

## How to Run

From the repository root, inspect `settings.gradle(.kts)`, `stonecutter.gradle(.kts)`, shared build scripts, `stonecutter.properties.*`, `gradle.properties`, `versions/`, and `src/` with `read_file` and `search_files`. Then invoke the project wrapper through the `terminal` tool:

```bash
./gradlew projects
./gradlew tasks --all
./gradlew build
```

Never guess generated task names or project paths. Read them from `projects` and `tasks --all`, especially when a project separates logical versions from node names.

## Quick Reference

```text
./gradlew projects
./gradlew tasks --all
./gradlew "Set active project to <project>"
./gradlew "Refresh active project"
./gradlew "Reset active project"
./gradlew :<project>:build
./gradlew :<project>:runClient
./gradlew :<project>:runServer
./gradlew build
```

```text
settings.gradle.kts                 tree/branch/node registration
stonecutter.gradle.kts              controller, active node, parameters
build.gradle.kts                    shared per-node build template
build.<loader>.gradle.kts           split loader build template
stonecutter.properties.toml         structured shared/version properties
versions/<project>/                 node project
versions/<project>/build/generated/stonecutter/ generated inactive sources
src/                                shared source in active-node state
```

## Procedure

1. **Inventory the existing model.**
   - Use `search_files` to locate `dev.kikugie.stonecutter`, `stonecutter active`, `vcsVersion`, `versions(`, `version(`, `.buildscript(`, `//?`, `/*?`, `//$`, and `//~`.
   - Record each tree, branch, node project name, logical version, build script, loader, active node, VCS node, property source, Java level, build/test/run tasks, and publication task.
   - Choose Stonecutter for compatible deltas. Prefer separate branches/projects when target implementations are mostly unrelated.

2. **Create or align the settings model.** At the reviewed 0.9.7 release, Kotlin DSL setup is:

   ```kotlin
   plugins {
       id("dev.kikugie.stonecutter") version "0.9.7"
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

5. **Express the smallest source delta.**

   ```java
   //? if >=1.21 {
   newApi();
   //?} else
   /*oldApi();*/

   //? if fabric && minecraft: >=1.21
   fabricOnly();
   ```

   - Closed scope: `//? if condition {` through `//?}`.
   - Line scope: condition affects the next non-empty line/logical block.
   - Lookup scope: `//? if condition >> 'token'`; add `+` after `>>` to capture the token.
   - Branch with `else`, `elif`, or `else if`; every branch before the last must be closed.
   - Predicates: `=`, `!=`, `<`, `>`, `<=`, `>=`, `~` (same major/minor), `^` (same major), plus `!`, `&&`, `||`, and parentheses.
   - Define loader/build booleans with `constants`, library versions with `dependencies`, repeated code alternatives with registered `swaps`, and broad reversible renames with `replacements.string`.
   - Prefer string replacements. Regex replacements are slower and require explicit forward and reverse patterns. Avoid ambiguous or cyclic replacement graphs.
   - Local swaps (`//$ if ...`) are present in 0.9.7, although the official page still carries a stale “under development” warning from the 0.9 prerelease cycle. Prefer registered swaps for repeated logic; use local replacements (`//~ if ... 'old' -> 'new'`) sparingly and review every transformed node.

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

8. **Choose a maintainable multi-loader layout.**
   - Flat nodes combine version and loader in one tree and use split build scripts/constants. They suit small or Mixin-heavy mods.
   - Branched `common`/`fabric`/`neoforge` sources isolate loader APIs and cache well, but require more Gradle wiring.
   - Official guidance prefers split native loader build scripts for long-term flat multi-loader maintenance. Do not force one build plugin to emulate every loader when native plugins are clearer.
   - Keep logical Minecraft version separate from project names such as `1.21.1-fabric`; otherwise the loader suffix is parsed as a SemVer prerelease.

9. **Handle resources and uncommon formats intentionally.**
   - 0.9.7 source defaults cover Java/Scala/Groovy/Gradle/JSON5, Kotlin, shaders, YAML, CFG, access wideners/transformers, and class tweakers—but not `.properties`, despite the FAQ claim.
   - For `.properties`, explicitly register `stonecutter handlers { inherit("aw", "properties") }` or another handler whose comment syntax matches the file.
   - Reuse a handler with `stonecutter handlers { inherit("aw", "your_extension") }` before writing an ANTLR-backed custom handler.
   - `stonecutter.filters` is exclusion-only; paths are relative to each `src/<source-set>` directory. Do not call `include`.
   - Use `sc.process(input, output)` only for files a loader consumes before ordinary source/resource processing; it is expensive and not normally cached/parallelized.
   - With Fabric Loom interface injection, set `loom.fabricModJsonPath` to the shared valid JSON file. Unprocessed placeholders must still leave valid JSON.

10. **Build, release, upgrade, and commit cleanly.**
    - Root `./gradlew build` builds all registered nodes; node-qualified `build`, `runClient`, and `runServer` target one node.
    - `buildAndCollect` is an official-template convenience task, not a core Stonecutter task. Confirm it exists before invoking it.
    - Aggregate only a publishing task that the applied publishing plugin actually registers, using `stonecutter.tasks.named("actualTaskName")`; do not assume official templates provide publishing tasks or eagerly call `.get()`.
    - Before upgrading Stonecutter, read every changelog entry from the installed version to the target, update the Gradle wrapper if required, sync, list projects/tasks, perform a switch/reset round trip, then build all nodes.
    - Before commit, invoke `./gradlew "Reset active project"`, inspect `git diff`, and confirm changes are intentional source/config edits rather than active-version noise.

## Pitfalls

- Stonecutter 0.9.7 generates tasks named `Set active project to ...`, `Refresh active project`, and `Reset active project`; some prose/docs still say “version.” Trust `tasks --all`.
- Switching rewrites the active literal and shared source state. It does not discard legitimate edits or guarantee a clean tree if the previous state was stale.
- Shared `src/` reflects the active node, but explicitly qualified inactive-node run/test tasks can execute generated sources when the loader exposes them. Generated-file edits are still disposable.
- A file under `versions/<project>/src/` overrides the corresponding shared/generated file for that node; review overrides before assuming a shared edit reaches every node.
- A green active-node build does not prove all nodes compile; run the root build.
- At the reviewed commits, all three official templates still pin Stonecutter 0.9.6. Compare a template's pin with the current release before adopting or upgrading it.
- Parallel NeoForge node builds may need the official multi-loader template's `createMinecraftArtifactsMutex` build service with `maxParallelUsages.set(1)` to serialize Minecraft artifact generation.
- Generated source tasks are in `stonecutter-impl` and say “Do not call manually.” Use normal build/test tasks unless integrating a loader lifecycle dependency such as NeoForge `createMinecraftArtifacts` depending on `stonecutterGenerate`.
- String replacements reject ambiguous/cyclic mappings; regex replacements lack those safety guarantees.
- Named replacement tokens must appear before the first non-empty, non-comment line to enable file-wide replacement behavior.
- `parameters {}` is lazily evaluated Stonecutter configuration, not a substitute for `subprojects {}` build customization.
- Native `gradle.properties` still controls `org.gradle.*` launch settings; structured properties only supply build-script values.
- Do not apply `base`/`java` to the tree's controller root; each Stonecutter node is the buildable project.
- If `dev.kikugie.stonecutter.no_short_extension` is present in `gradle.properties`, use the full `stonecutter` extension; its mere presence disables the `sc` alias, even when set to `false`.
- `generate_sources_on_sync=true` makes preprocessing errors fail IDE sync. Enable it only when that strictness is intentional.
- Do not set Gradle `group` blindly: official Fabric and multi-loader templates intentionally keep `mod.group` as metadata without assigning `project.group`.
- Do not bundle every Minecraft version into one mod JAR. Build and publish version-specific artifacts.

## Verification

Invoke the repository-wide build through the `terminal` tool; success proves every registered node can generate and consume its versioned sources:

```bash
./gradlew build
```
