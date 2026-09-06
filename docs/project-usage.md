# Using the skills in a Minecraft project

This guide connects the independently installable packages to real development tasks. It is repository-level onboarding, not another skill that must be installed, and it does not replace the target project's build configuration.

## Select the smallest useful combination

| Task | Primary package | Add only when applicable | Do not infer |
| --- | --- | --- | --- |
| Fabric source change | `fabric-modding` | Stonecutter, native UI, Testiarium | Yarn names merely because the loader is Fabric |
| Modern NeoForge source change | `neoforge-modding` | Stonecutter, native UI, Testiarium | NeoForge version from a directory called `forge` |
| MinecraftForge-era source change | `neoforge-legacy-modding` | Stonecutter, native UI, Testiarium | That NeoForged tooling makes the runtime NeoForge |
| 1.21.x to 26.1.x port | `minecraft-26-1-migration` | Matching loader skills and Stonecutter | That 26.1 APIs apply to retained 1.20/1.21 targets |
| Shared-source/multi-version change | `stonecutter-multiversion` | Every loader actually affected | That Gradle project ID equals game version |
| Native screen/menu work | `minecraft-native-ui` | Loader networking/registration guidance | That a client widget may mutate server inventory |
| Testiarium GameTest | `testiarium-gametest` | Loader and Stonecutter | That a green build executed any GameTests |
| Java GTCEu addon | `gtceu-addon` | Matching loader skill | That a KubeJS recipe example is a Java registry API |
| Pack-side scripts | `kubejs-modding` | GTCEu when its scripting API is involved; pack authoring | That the event API is stable across KubeJS majors |
| Pack assembly/distribution | `minecraft-modpack-authoring` | KubeJS; Modrinth for source metadata | That source-project Gradle dependencies constitute a pack |
| Mod/version/file discovery | `modrinth-api` | Pack authoring when modifying a pack | That a display name or first result identifies the right artifact |

Read the selected package's `SKILL.md`, then only the reference files needed for the task. Named companion packages are suggestions, not required sibling filesystem paths. Install companions explicitly if the agent does not already have them.

## Project intake before changes

Record a compact project brief:

```text
Task and acceptance criteria:
Repository revision and current dirty-state summary:
Minecraft targets, loader per target, mappings namespace:
Gradle wrapper, plugin pins, Java runtime and target toolchains:
Source roots: shared / loader / generated / test / per-node overrides:
Module -> tree -> branch -> node relationships:
Exact affected task paths discovered from the build:
Canonical source state / VCS reset point:
Selected skills and why:
Validation: compile / unit tests / datagen / server / client / artifacts:
Explicitly out of scope: dependency upgrades / port / publication / installation:
```

Use file-reading and search tools on settings, build scripts, version catalogs, metadata, and CI. Treat `AGENTS.md` as workflow guidance, but reconcile stale paths/version descriptions against those executable files. Ask about architectural ambiguity; do not silently change the project's loader, module layout, mappings, or dependency versions to match a skill example.

Before commands that configure a build or rewrite sources, inspect `git status --short --branch`. Discovery itself can run Gradle configuration code and write generated files. For an audit, use a disposable checkout of the reviewed revision, not the user's active tree. Keep full build logs outside the contribution and summarize errors rather than dumping them into agent context.

## Example A: flat multi-loader template

Reviewed source: [SirEdvin/TemplateProject at 042d296](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004).

- [Settings](https://github.com/SirEdvin/TemplateProject/blob/042d296e255d6a9e75e1d2f40da9937810e92004/settings.gradle.kts) defines one Stonecutter tree at the root with loader-suffixed nodes: 1.20.1 Fabric/Forge and 1.21.1 Fabric/NeoForge.
- The build script is selected per loader, while the logical Minecraft version is registered separately from the node name.
- [Controller](https://github.com/SirEdvin/TemplateProject/blob/042d296e255d6a9e75e1d2f40da9937810e92004/stonecutter.gradle.kts) selects `1.21.1-fabric` as active, tags properties by version/loader, and defines loader constants.
- That revision pins Stonecutter 0.9.7; do not upgrade it merely because a skill's smoke fixture uses 0.9.8.
- For a cross-loader source fix: load Stonecutter plus Fabric, legacy Forge, and modern NeoForge guidance as the changed code demands. For a Fabric-only metadata change, do not load unrelated addon or pack skills.

## Example B: modular library repository

Reviewed source: [SirEdvin/Minecraft-Modding-Libs at 86bfe0b](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c).

- [Settings](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/settings.gradle.kts) creates separate non-root Stonecutter trees for Broccolium, Testiarium, Tweakium, and Peripheralium. `typed-peripheral-api` is separately included rather than being another versioned tree.
- Each tree has common/root, Fabric, and `forge` branches with 1.20.1 and 1.21.1 nodes. A branch name is not proof of its runtime loader.
- [Testiarium's Forge-branch build](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/projects/testiarium/forge/build.gradle.kts) selects legacy Forge for 1.20.1 and NeoForge for 1.21.1. It selects Java 17/21 separately and wires different source sets for unit tests, GameTests, and ComputerCraft tests.
- The repository root applies Java, but it is not a Stonecutter controller root. The prohibition against applying Java to a controller must not be generalized to every repository root.
- [CI](https://github.com/SirEdvin/Minecraft-Modding-Libs/blob/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c/.github/workflows/ci.yml) runs the repository build. It does not demonstrate that an interactive client or every registered GameTest ran.
- For Testiarium work, combine its skill with the corresponding loader and Stonecutter. Discover paths containing library, branch, and version; do not reuse an old `projects/testiarium-core` path from a different revision.

These are architectural examples, not universal templates or evidence that every skill is used by both projects. No GTCEu, KubeJS, Packwiz, or 26.1 migration is implied by these examples; those packages require their own applicability checks and source evidence.

## Execution and evidence contract

Invoke through the agent's terminal tool from the target repository root (use the checked-in Windows wrapper on Windows):

```bash
./gradlew projects
./gradlew tasks --all
```

Then select exact discovered tasks. Never guess `runGameTest`, a publishing task, or a flattened node path. For Stonecutter, complete a switch/reset in one invocation and run compilation in a subsequent invocation so the source links are reconfigured.

Use a layered report:

1. Configuration/task discovery: nodes and tasks exist at the reviewed revision.
2. Compilation: state precisely which target tasks executed, were up-to-date, or failed.
3. Unit tests: examine test counts; `NO-SOURCE` is not passing tests.
4. GameTests: record discovered/executed tests and the fresh machine-readable report, including failures/timeouts.
5. Runtime: server classloading and client behavior require separate evidence; a headless client additionally needs a display strategy and explicit timeout.
6. Artifact checks: metadata, loader identity, mapping/remapping, dependency inclusion, and unique version/loader filenames.

Return to the project's canonical source state and inspect the diff. Do not automatically publish, merge, accept a server EULA, or commit generated output. A dependency/network blocker is a blocker to that verification layer, not a reason to fabricate successful output or silently skip targets.
