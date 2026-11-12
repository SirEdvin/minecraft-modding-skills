# Release and migration contracts

Stonecutter decides which sources a node compiles. It does not decide which artifact a loader toolchain publishes, which coordinates consumers resolve, or whether tests ran. Verify those contracts separately every time the tree, the plugin version, or the release wiring changes.

## Choosing a Stonecutter version

Check the published metadata, not the wiki's default page or a template's pin:

- Plugin Portal: https://plugins.gradle.org/plugin/dev.kikugie.stonecutter and `https://plugins.gradle.org/m2/dev/kikugie/stonecutter/maven-metadata.xml`
- Stable channel: https://maven.kikugie.dev/releases/dev/kikugie/stonecutter/maven-metadata.xml
- Prerelease channel: https://maven.kikugie.dev/snapshots/dev/kikugie/stonecutter/maven-metadata.xml
- Changelog and wiki sources: https://codeberg.org/stonecutter/docs (`changelogs/`, `docs/wiki/v2/`)
- Implementation: https://codeberg.org/stonecutter/stonecutter
- Official templates: https://codeberg.org/stonecutter (`template-fabric`, `template-neoforge`, `template-multiloader`)

Rules:

- The prerelease channel sorts higher than stable. Never pin an alpha or beta because it is the newest entry.
- Requirements are in the artifact, not the prose: read `org.gradle.jvm.version` in the version's `.module` file for the launcher JVM, and the Gradle floor in the version's source JAR. A changelog can lag or describe a prerelease state that the final release reverted.
- The wiki stores per-version snippets (`_versions/<topic>.<from>-<to>.md` in the docs repository). When the rendered site is unavailable or returns a bot challenge, read that repository instead of summarizing the error page.
- Record the commit you read. A branch head can already describe unreleased behaviour.
- A template shows one working combination of Stonecutter, Gradle, and loader plugins at its commit. Use it to find compatible companion-plugin versions, not as proof for your loader matrix.

## Migration audit workflow

Use when sources move into a Stonecutter tree, between layouts, or across a plugin line.

1. Pin the pre-migration revision for each supported game version. Map old module paths to each branch/node, apply full-file override precedence, and compare all production sources and resources, not only the active node. Count matched, changed, added, and removed files programmatically, and keep build/test-only differences apart from gameplay or API changes.
2. Check generated inactive sources and the active source roots independently. A full-file override must exclude the same shared relative path from Java, Kotlin, resources, `allJava`, and `allSource`. Verify sources JARs as well as classes; one active state is not enough.
3. Preserve the consumer ABI: unique internal module identities, existing public Maven coordinates, dependency capabilities, JVM and loader attributes, test fixtures, and source artifacts. Inspect the real POM, module metadata, and packaged JARs of every node.
4. Treat access wideners and transformers as build inputs. Order loader artifact generation after `stonecutterGenerate`, resolve the node's effective file, and serialize artifact generation only where the loader tool needs it.
5. Track the whole metadata expansion map and the shared build script as resource-task inputs. Prove that changing a raw dependency value regenerates metadata without `clean` or `--rerun-tasks`, and read the output. An up-to-date task says nothing about whether its placeholder values are still right.
6. A port that compiles can still drop semantics. For every production file that changed, name the behaviour difference and cover it with a test on the affected node; do not weaken production behaviour to make a plain unit test loader-aware.
7. Check test bootstrap dependencies, source-set outputs, and fixtures. A test source set's output does not imply the matching `main` output is on its classpath, and a loader run needs every mandatory mod loaded, not just on the compile classpath.
8. Delete the exact previous test report before a run. Require a newly created report, at least one executed non-skipped test, zero failures and errors, and consistent declared/actual counts. Some loader startup failures exit zero. Count expected optional skips separately from passes.
9. Run Gradle with `--no-daemon`, bounded timeouts for game processes, and redirected logs. Build every node with each active state, reset to the VCS node, and inspect the source diff for preprocessing churn.

## Build and publication contracts

- **Inventory first.** Before promising an all-version release, enumerate the expected artifacts (library × game version × loader, binaries and sources) from settings and publishing configuration. A root release plugin does not prove every leaf is attached.
- **Select the production artifact per loader toolchain.** The task named `jar` is not always the file players or consumers need: remapping toolchains produce the distributable from a separate remap or reobfuscation task and may write the development JAR to a different directory, while non-remapping toolchains publish `jar` directly. Resolve each node's artifact from the loader plugin's designated task and its declared outputs, and confirm the file with the node's manifest attributes.
- **Trace the release task.** Follow the actual release task's dependencies and attachment selection, run it with `--dry-run`, and compare the graph with the inventory. A configuration failure leaves the graph unverified; it does not show the task is absent. A dry run is neither a build nor an upload test.
- **Require unique filenames and complete coverage**, then compare digests of the published assets with the locally selected files. A ZIP that opens is not evidence it is the right node's artifact.
- **Derive metadata ranges from the central version values.** A dependency range hard-coded to a stable floor rejects a prerelease of the same version and can stop a loader before any test runs. Fix the metadata; do not bypass validation.
- **Versions and tags.** Read centralized versions and existing remote tags/releases before choosing a version. Never reuse a version or overwrite published assets. After publication read back the exact release and verify every expected version/loader asset instead of trusting the Gradle exit code.
- **Order concrete publishing tasks** with the controller's ordering API when the destination cares about upload order, not the umbrella task that delegates to them.
- **Report four states separately:** migration/runtime acceptance, current-checkout buildability, release-task coverage, and actual public publication. Earlier acceptance does not certify a fresh release preflight.

## Verifying a shared convention plugin

When nodes apply an in-house convention or toolkit plugin, build that plugin with its own wrapper, publish the candidate to a scratch file-based Maven repository, and inject repository and version into a disposable consumer with an init script. A composite build runs the toolkit's build logic under the consumer's Gradle, which can fail in legacy loader tooling even when the separately built plugin works. Do not raise the toolkit's wrapper or commit a local repository to get past that, and do not pin consumers to an unpublished candidate.

## Evidence levels

Source equivalence, compilation, unit tests, loader-run tests, and interactive gameplay are different levels of evidence. State which one a claim rests on, and name what was not run.
