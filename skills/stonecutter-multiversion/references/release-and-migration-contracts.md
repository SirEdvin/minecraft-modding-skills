# Stonecutter release and migration contracts

## Version selection

Check both channels before changing a pin:

- Stable plugin listing: https://plugins.gradle.org/plugin/dev.kikugie.stonecutter
- Stable metadata: https://maven.kikugie.dev/releases/dev/kikugie/stonecutter/maven-metadata.xml
- Prerelease metadata: https://maven.kikugie.dev/snapshots/dev/kikugie/stonecutter/maven-metadata.xml
- Changelog source: https://codeberg.org/stonecutter/docs/src/branch/main/changelogs
- Implementation: https://codeberg.org/stonecutter/stonecutter

If the docs website returns scrambled text or a bot challenge, do not summarize it as documentation. Read the upstream Git checkout and the published version's source JAR instead. Record immutable source commits and distinguish unshipped branch changes from the published artifact.

Reviewed on 2026-10-16: stable is **0.9.8**, published 2026-08-31; the newer channel contains **0.10-beta.1**. Do not silently install a prerelease because its version sorts higher.

### Stable 0.9.8

The 0.9.7-to-0.9.8 release adds IDE parameter annotations (`ConstantID`, `TargetID`, `SwapID`, `ReplacementID`) and updates KDoc URLs for the new wiki. It is not a gameplay migration and does not fix consumer publication, source overlay, access-transformer, or runtime-test wiring. Retain those consumer safeguards. The 0.9.7 task-ordering build-service change is already in the previous stable version.

### Separate 0.10 upgrade

Treat this as a toolchain and preprocessing migration, not a patch bump:

- The reviewed beta requires **Java 25 for the Gradle launcher and Gradle 9.7+**. Plugin authors embedding Stonecutter must also account for its Kotlin 2.4 requirement. Keep Minecraft bytecode/toolchains at the target game's Java version.
- Condition dependencies are being renamed to targets. Property accessor APIs and fallback lookup change. Read later changelog entries: alpha.8 **restored** structured-property exposure through `project.property`/`project.extra` behind default-enabled `EXPOSE_PROPERTIES`; do not repeat the obsolete alpha.7 removal claim as current behavior.
- `no_short_extension` becomes `short_extension` with inverted meaning. `APPLY_PLUGIN_TO_NODES` becomes `AUTO_APPLY_PLUGIN`; controller plugin application becomes automatic.
- `tasks.names` replaces deprecated `tasks.named` for Isolated Projects-compatible task paths. `.filters` is deprecated in favor of `.files`; custom scanner/format and serialized model APIs change. The beta adds Java-17-compatible annotations/model artifacts and schema-versioned cache models; this does not lower the plugin launcher requirement.
- Replacement validation/cycle behavior and inactive-scope processing change. New features include named/multiple local and PCRE replacements, branch inheritance, per-file replacement filters, and conditional file disabling. Processed files must be UTF-8.
- Later alphas fix deleted generated files, incremental processing, unmatched swaps, disabled-file over-exclusion, apostrophes, and task ordering before the active-node declaration. Test these paths before removing a local workaround; a changelog entry is not proof that a consumer's complete contract is satisfied.

## Migration audit workflow

1. Pin the pre-migration revision for **each** supported Minecraft version. Map old module paths to each logical branch/node, apply full-file override precedence, and compare all production source/resources, not only the active node. Count matched, changed, added and removed files programmatically. Keep build/test-only differences separate from gameplay/API changes.
2. Check generated inactive sources and active source roots independently. A full-file override must exclude the same shared relative path from Java, Kotlin, resources, `allJava`, and `allSource`. Verify sources JARs as well as classes; a build in only one active state is insufficient.
3. Preserve the consumer ABI: unique internal module identities, old public Maven coordinates, dependency capabilities, JVM/loader identities, test fixtures and source artifacts. Inspect actual POM/module metadata and packaged JARs across every node.
4. Treat access wideners/transformers as build inputs. Order Forge-family `createMinecraftArtifacts` after `stonecutterGenerate` and resolve the effective active/versioned transformer. Serialize artifact generation only where the loader tool requires it.
5. Track the entire metadata expansion map and shared build script as resource-task inputs. Prove raw dependency changes regenerate metadata **without** `clean` or `--rerun-tasks`, and inspect outputs. A task being up-to-date is not proof its placeholder values stayed valid.
6. Preserve data-component patch removals (`Optional.empty`) when rewriting another component. Test pocket and turtle paths independently. In nullable Java capability contexts, pass `null`; Kotlin `null as Void` throws before the lookup can execute.
7. Check GameTest bootstrap dependencies, source-set outputs and structure fixtures. `testMod` output does not imply the corresponding `main` output is present. Register all mandatory loaded mods as well as classpath dependencies. Never weaken production capability behavior to make plain JUnit loader-aware.
8. Delete the exact previous XML report before launch; require a newly created report, at least one executed non-skipped test, zero failures/errors, and consistent declared/testcase counts. Some loader startup failures exit zero. Keep expected optional skips distinct from passed tests.
9. Use `--no-daemon`, bounded runtime timeouts, and stdout/stderr log redirection. Read only concise diagnostics and parsed report totals into agent context. Build every node with both active states, reset to the VCS node, and inspect source diffs for preprocessing churn.

## Convention-toolkit verification

Build modding-buildenv using **its own wrapper**, publish the candidate to a scratch file Maven repository, then inject that repository/version into a disposable consumer with an init script. A Gradle 9 consumer composite runs toolkit build logic under Gradle 9 too; legacy ForgeGradle accessor generation can fail there even when the separately built plugin works. Do not upgrade the toolkit wrapper or commit a local repository merely to bypass this check. Do not pin consumers to an unpublished toolkit candidate.

## Evidence scope

The 0.9.8 upgrade was exercised in Minecraft-Modding-Libs and TemplateProject, including TemplateProject's switch/build/reset round trip. The 0.10 beta was researched, **not adopted or runtime-verified**. Consult repository audit reports for concrete task coverage; source equivalence, compilation, unit tests, loader tests and interactive gameplay are different levels of evidence.
