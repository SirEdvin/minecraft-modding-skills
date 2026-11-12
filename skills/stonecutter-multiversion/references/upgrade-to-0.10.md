# Upgrading Stonecutter 0.9.8 to 0.10

0.10 is a toolchain and preprocessing migration, not a patch bump. Do it as its own change: never together with adding or removing a node, a loader upgrade, or a dependency API migration, because each of those also moves generated sources and you lose the ability to attribute a diff.

## Requirements

| Requirement | Evidence |
| --- | --- |
| Gradle launched on Java 25 or newer | Module metadata declares `org.gradle.jvm.version = 25` `[source]`. On Java 21 plugin resolution fails with `Dependency requires at least JVM runtime version 25` `[probe]` |
| Gradle 9.7.0 or newer | The plugin checks it and fails with `Stonecutter requires at least Gradle 9.7.0` `[probe]` |
| Kotlin 2.4 | Supplied by Gradle: the 9.7.0 distribution ships Kotlin 2.4.0, 9.5.0 ships 2.3.20 `[probe]`. Build scripts need no Kotlin change. Only code that uses Stonecutter as a library must compile with Kotlin 2.4 `[changelog]` |
| Kotlin DSL | Default. Groovy scripts need `kotlinController = false` plus `centralScript`, or the `hard_mode` flag `[wiki]` |
| Node toolchains | Unchanged: keep each node's own toolchain. Fabric, Forge, and NeoForge nodes targeting Java 17 and 21 compile to their own class-file level under a Java 25 launcher `[probe]` |

Pick any Gradle from 9.7.0; 9.7.0 and 9.9.1 are confirmed with 0.10 `[probe]`. Move the wrapper and launcher JDK before the plugin: 0.9.8 runs on Gradle 9.9.1 with a Java 25 launcher `[probe]`.

The launcher requirement applies to every environment that configures the build: contributors' machines, IDE Gradle JVM, and each CI job. In CI install toolchain JDKs first and the launcher JDK last, or set `JAVA_HOME` explicitly, and check the Gradle startup line rather than assuming.

## Order of work

1. Start green: all nodes built on the current pin, sources reset to the VCS node, clean `git status`. Save `./gradlew projects` output, each node's resolved property values, and the file list of each built JAR.
2. Raise the Gradle wrapper to 9.7+ and the launcher to Java 25 while still on 0.9.8. Build all nodes. This isolates loader-plugin and convention-plugin incompatibilities with the new Gradle or JVM from Stonecutter changes. Stop here if a loader toolchain fails; that is a blocker to resolve first, not something to patch around.
3. Bump Stonecutter and every plugin that integrates with it (loader compatibility shims, Stonecutter addons) to releases that support 0.10.
4. Apply the mandatory edits below until `./gradlew projects` configures, then compare the node list and resolved property values with step 1.
5. Run a switch round trip to another node and back. Commit any one-time formatting normalization separately, then repeat the round trip and require a zero diff.
6. Build all nodes with each node active, run real tests, and compare JAR file lists with step 1. Look specifically at resources.
7. Update CI and contributor documentation for the launcher JDK.

## Mandatory edits

| Symptom or risk | Fix |
| --- | --- |
| `No type arguments expected for 'fun get(name: String): String'` `[probe]` | `sc.properties.get<T>()` → `getAs<T>()`; use `sc.properties["..."]` or `get` for strings |
| `compileJava` not found, no source sets `[probe]` | Stonecutter no longer applies `java` to nodes. Apply `java` or the loader plugin in the node script |
| A value from `versions/<project>/gradle.properties` is `null` through `sc.properties` `[probe]` | The fallback is now `providers.gradleProperty` (root file only). Move the value into structured properties or read it with `project.property` |
| A plugin in the node `plugins {}` block reports a missing project property that lives in a structured file `[probe]` | Upgrade that plugin to a 0.10-aware release, or declare the value where it reads it |
| Global replacement now rewrites `.json`, `.toml`, `.txt` resources `[probe]`, and through the same new default handlers `.md`, `.csv`, `.mcmeta`, `.properties`, XML `[source]` | Search resources for every replacement key; add `exclude(...)` or an identifier where data must keep the old text |
| `#?` comments in `.properties` `[probe]` and `.toml` `[source]` are now evaluated | Make them valid conditions or exclude the file. Remove a hand-registered handler for a now-default extension |
| File filter no longer matches | Patterns are relative to each source directory: drop the leading `java/` or `resources/`; move from `filters` to `files` `[changelog]` |
| A task depends on `stonecutterPrepare` | That task no longer exists `[probe]`; depend on `stonecutterGenerate` |
| `sc` alias unexpectedly present or absent | `no_short_extension` (presence disables) became `short_extension=false` `[changelog]` |
| Script code referencing `StonecutterFlag.APPLY_PLUGIN_TO_NODES` | The constant is `AUTO_APPLY_PLUGIN`; the `auto_apply_plugin` property is unchanged `[source]` |
| Non-UTF-8 source or resource fails processing | Convert to UTF-8 `[changelog]` |
| Preprocessing error inside code that is commented out for every node | Disabled scopes are now checked. Fix or delete the dead branch `[changelog]` |
| Addon, custom file handler, or tool reading `build/stonecutter-cache` breaks | Handler API and model schema changed (schema 2, separate `stonecutter-model` artifact) `[changelog]`. Port or upgrade it |

## Deprecated but still working

These still work on 0.10; migrate them in a follow-up, not as part of the bump, so the bump stays reviewable.

- `dependencies` → `targets` (deprecation warning `[probe]`).
- `stonecutter.tasks.named(...)` → `tasks.names(...)` (deprecation warning `[probe]`).
- `filters` → `files` (deprecated `[source]`); mind the changed base directory.
- Controller `stonecutter.current` → `stonecutter.active` (deprecated `[changelog]`).
- `plugins { id("dev.kikugie.stonecutter") }` in the controller is a no-op without a warning `[probe]`; remove it.
- `project.property("structured.key")` keeps working without a warning through `expose_properties` `[probe]`; move to `sc.properties` before turning that flag off.

## Contracts that did not change

Keep existing safeguards for these; 0.10 does not make them unnecessary `[probe]`.

- Task names `Set active project to ...`, `Refresh active project`, `Reset active project`.
- Switching and compiling in one Gradle invocation still fails implicit-dependency validation.
- A full-file override in `versions/<project>/src/` still collides with the shared file while that node is active. Keep the consumer-side exclusion.
- Loader artifact tasks still need an explicit dependency on `stonecutterGenerate`.
- A switch round trip is byte-identical once the sources are in 0.10 formatting.

Fixes listed in the changelog for deleted generated files, incremental processing, unmatched swaps, and apostrophes are `[changelog]` only. Test the affected path before deleting a local workaround.

## Adopt or stay

Stay on 0.9.8 while any of these holds:

- a loader, convention, or publishing plugin in the build is not verified on Gradle 9.7+ with a Java 25 launcher;
- contributors or CI cannot provide Java 25 for launching Gradle;
- the project is mid-release or mid-migration, so preprocessing changes cannot be reviewed in isolation;
- an addon or custom handler has no 0.10 port.

Adopt 0.10 when the build is otherwise quiet and at least one holds: a new project or template with no legacy constraints; a concrete need for a 0.10-only feature (conditional file disabling, named or filtered replacements, cross-branch inheritance, Isolated Projects); or the build already runs on Gradle 9.7+ and Java 25 for another reason.

Before either decision re-read the changelog from the pinned version through the target, including reversions in later entries: prerelease notes describe removals that the final release restored.
