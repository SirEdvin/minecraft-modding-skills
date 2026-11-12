---
name: stonecutter-multiversion
description: Use when editing Stonecutter builds. Version-match its APIs.
license: MIT
compatibility: Stonecutter 0.10 needs Gradle 9.7+ on a Java 25 launcher; 0.9.8 needs Gradle 9.0+ on a Java 21 launcher. The two lines differ in API and defaults, so match every example to the pinned plugin version.
metadata:
  version: "0.3.2"
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

## Version gate

Read the plugin pin in `settings.gradle(.kts)` before anything else, and keep it unless an upgrade is the task. The official wiki shows the newest line by default, so an example can be valid upstream and still not compile on the pinned version.

| Concern | 0.9.8 | 0.10 |
| --- | --- | --- |
| Gradle | 9.0+ | 9.7+ |
| JVM that launches Gradle | 21+ | 25+ |
| Kotlin DSL | Gradle's embedded Kotlin | Gradle's embedded Kotlin (2.4 from Gradle 9.7) |
| Controller `plugins {}` block | required | optional no-op |
| Predicate versions | `dependencies` | `targets` (`dependencies` deprecated) |
| Typed property | `sc.properties.get<T>()` | `sc.properties.getAs<T>()`; `get`/`[]` return `String` |
| File filters | `filters` | `files` (`filters` deprecated) |
| Aggregated node tasks | `tasks.named()` | `tasks.names()` (`named` deprecated) |
| Active node in controller | `stonecutter.current` | `stonecutter.active` |
| `java` plugin on nodes | applied for you | apply it yourself |

The launcher JVM is not the Minecraft toolchain: nodes still compile for the Java level their game version needs.

Version-sensitive statements in the references carry an evidence label: `[source]` published source JAR or module metadata of that version, `[probe]` executed in a disposable fixture build, `[changelog]`/`[wiki]` official text only, `[unverified]` not confirmed. Re-verify anything labelled below `[source]` before a decision depends on it.

## References

Load on demand with `skill_view(name="stonecutter-multiversion", file_path="references/<file>")`:

- [Project topology and task discovery](references/project-topology.md): flat multi-loader nodes versus multi-project trees with branches, task paths, overrides.
- [Source syntax and resources](references/source-and-layout.md): conditions, swaps, replacements, default file formats, filters, disabled files.
- [Properties and data-driven setup](references/properties-and-data-setup.md): structured properties, tags, accessors, JSON/TOML/YAML tree files.
- [Controller and replacement mechanics](references/controller-and-replacements.md): aggregation, ordering, mutex, flags, replacement scopes.
- [Removing a version node](references/node-removal.md): ordered removal across settings, overrides, CI, publication, and dead conditionals.
- [Upgrading 0.9.8 to 0.10](references/upgrade-to-0.10.md): requirements, breaking changes, unchanged contracts, adoption decision.
- [Release and migration contracts](references/release-and-migration-contracts.md): choosing a version, migration audits, artifact and publication checks.

## How to Run

From the repository root, inspect `settings.gradle(.kts)`, every `stonecutter.gradle(.kts)`, shared build scripts, `stonecutter.properties.*`, `gradle.properties`, `versions/`, and `src/`. Then invoke the project wrapper:

```bash
./gradlew projects
./gradlew tasks --all
./gradlew build
```

Never guess generated task names or project paths; read them from `projects` and `tasks --all`. A Gradle repository root is not necessarily a Stonecutter controller, and one build can hold several trees.

For anything beyond a quick listing, run `--no-daemon`, redirect output to a log, and read bounded diagnostics from the log instead of streaming Gradle output:

```bash
./gradlew build --no-daemon > "$TMPDIR/stonecutter-build.log" 2>&1
```

## Quick Reference

```text
./gradlew "Set active project to <project>"
./gradlew "Refresh active project"
./gradlew "Reset active project"
./gradlew :<project>:build
./gradlew build
```

Settings register trees/branches/nodes; `stonecutter.gradle.kts` is the controller, `build.gradle.kts` or `build.<loader>.gradle.kts` is the node template, `stonecutter.properties.*` supplies structured values, and `src/` reflects the active node. Node directories are `versions/<project>/`; inactive sources under their `build/generated/stonecutter/` are disposable. Switch task names are the same on 0.9.8 and 0.10 `[probe]`.

## Procedure

1. **Inventory the existing model.**
   - Search for `dev.kikugie.stonecutter`, `stonecutter active`, `vcsVersion`, `versions(`, `version(`, `branch(`, `.buildscript(`, `buildFileName`, `//?`, `/*?`, `//$`, and `//~`.
   - Record each tree, branch, node project name, logical version, build script, loader, active node, VCS node, property source, Java level, build/test/run tasks, and publication task.
   - Choose Stonecutter for compatible deltas. Prefer separate branches/projects when target implementations are mostly unrelated.

2. **Create or align the settings model.** Use the pin the project already has. For a new project take the newest stable release from the Plugin Portal whose Gradle and launcher-JVM requirements every contributor machine and CI job can meet.

   ```kotlin
   plugins {
       id("dev.kikugie.stonecutter") version "<pinned version>"
   }

   stonecutter {
       create(rootProject) {
           versions("1.20.1", "1.21.1")
           version("1.21.11-snapshot", "1.21.11-rc2")
           vcsVersion = "1.21.1"
       }
   }
   ```

   - `versions(...)` uses each project name as its logical version; `version(project, version)` separates node identity from the compared version.
   - `active` and `vcsVersion` always take project names, not logical versions.
   - Pick the layout deliberately: see [project topology](references/project-topology.md) for flat `{version}-{loader}` nodes versus `create("a", "b") { branch("fabric") }` trees.
   - For Groovy scripts set `kotlinController = false` and `centralScript = "build.gradle"`. `centralScript` names the node build template, so never point it at the controller file.
   - Set `vcsVersion` deliberately. It is the canonical pre-commit source state.

3. **Configure the controller.** Assign the active node exactly once in `stonecutter.gradle.kts`:

   ```kotlin
   plugins {
       id("dev.kikugie.stonecutter") // required on 0.9.x, optional on 0.10
   }

   stonecutter active "1.21.1"

   stonecutter parameters {
       constants["release"] = project.property("mod.id") != "template"
   }
   ```

   - A literal active value is rewritten during switching. `stonecutter active file("active.txt")` keeps the state in a file that must already name a registered project. `stonecutter active null` is detached mode for CI: `src/` is not linked and every node uses generated sources.
   - Set flags before the `active` statement; they are read when the active node is assigned `[wiki]`.
   - Keep only Stonecutter configuration in `parameters {}`; dependencies and tasks belong to node build scripts.

4. **Parameterize node builds instead of cloning build scripts.**
   - Use `sc.current.project`, `sc.current.version`, and `sc.current.parsed`; compare with `sc.current.parsed >= "1.21"` or `matches(">=1.21 <1.21.5")`.
   - Keep shared values in the root and per-node values in `stonecutter.properties.*` or `versions/<project>/gradle.properties`; read [properties](references/properties-and-data-setup.md) before mixing the two on 0.10, where the fallback lookup changed.
   - Flat `{version}-{loader}` nodes need explicit tags and loader constants:

   ```kotlin
   stonecutter parameters {
       val (version, loader) = current.project.split('-', limit = 2)
       properties.tags(version, loader)
       constants.match(loader, "fabric", "neoforge")
   }
   ```

5. **Express the smallest source delta.** Read [source syntax and resources](references/source-and-layout.md) and use only syntax the pinned version implements.

6. **Use the daily switching ritual.**
   - Inspect `git status` before the first switch; switching rewrites tracked files.
   - Switch with an exact task name from `tasks --all`, then edit shared `src/` for that node and run its real compile, test, datagen, client, and server tasks.
   - Run `"Refresh active project"` when comment, swap, or replacement states look inconsistent.
   - Never edit `versions/<project>/build/generated/stonecutter/`.

7. **Add or remove a supported node.** Adding: declare the node, add every dependency/loader/Java/metadata/publishing/test-matrix value, list projects and tasks, switch to it, adapt conditionals, test the runtime, then build all nodes. Removing has ordering hazards; follow [removing a version node](references/node-removal.md).

8. **Build, release, upgrade, and commit cleanly.**
   - Root `./gradlew build` builds all registered nodes; node-qualified tasks target one node.
   - `buildAndCollect` is an official-template convenience task, not a core task. Confirm it exists.
   - Aggregate only tasks the applied plugins actually register. Never call `.get()` on the aggregated collection: it is lazy so that node projects are not forced to configure early.
   - Before changing the pin read [upgrading to 0.10](references/upgrade-to-0.10.md) and [release contracts](references/release-and-migration-contracts.md). Upgrade the Gradle wrapper and launcher JVM first, as a separately verified step.
   - Before commit run `"Reset active project"`, inspect `git diff`, and confirm changes are intentional rather than active-version noise.

## Pitfalls

- Run switching/reset and compilation as separate Gradle invocations. Combining them fails Gradle's implicit-dependency validation because source links are configured before the switch runs (0.9.8 and 0.10 `[probe]`).
- A file under `versions/<project>/src/` replaces the generated copy for that node while it is inactive, but when that node is active the shared file is still on the source set too and the build fails with a duplicate class (0.9.8 and 0.10 `[probe]`). Exclude the overridden shared path from Java, Kotlin, resources, `allJava`, and `allSource`, and build with each node active before claiming the overlay works.
- A green active-node build does not prove all nodes compile; run the root build.
- Switching rewrites the active literal and shared sources. It does not discard legitimate edits or guarantee a clean tree if the previous state was stale; a first round trip can normalize comment formatting.
- Shared `src/` reflects the active node, but qualified inactive-node run/test tasks execute generated sources. Generated-file edits are disposable.
- Do not treat an official template's pin, or the wiki's default page, as the version your project runs.
- Parallel NeoForge node builds may need artifact generation serialized; do not serialize the entire build for it.
- Generated-source tasks live in `stonecutter-impl` and say “Do not call manually.” Wire loader lifecycle tasks to depend on `stonecutterGenerate` instead.
- `parameters {}` is lazily evaluated Stonecutter configuration, not a substitute for `subprojects {}`.
- `org.gradle.*` launch settings stay in native `gradle.properties`.
- Do not apply `base`/`java` to a tree controller; its nodes are the buildable projects. An ordinary monorepo root outside the trees may still apply plugins or aggregate tasks.
- The `sc` alias switch changed: 0.9.x disables it by the mere presence of `dev.kikugie.stonecutter.no_short_extension`, even set to `false` `[source]`; 0.10 uses `dev.kikugie.stonecutter.short_extension=false` `[changelog]`.
- Do not set Gradle `group` blindly: official templates keep `mod.group` as metadata without assigning `project.group`.
- Do not bundle every Minecraft version into one mod JAR. Build and publish version-specific artifacts.

## Verification

Build every node, then repeat with another node active before restoring the VCS node. A root build verifies compilation for the executed targets only, not gameplay, publication contracts, or GameTest discovery; require fresh, nonempty test reports with no failures or errors for those.

```bash
./gradlew build --no-daemon > "$TMPDIR/stonecutter-build.log" 2>&1
```
