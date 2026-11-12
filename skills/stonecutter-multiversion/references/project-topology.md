# Project topology and task discovery

## Distinguish tree, branch, node, and ordinary module

- A tree coordinates branches and version nodes and owns one controller and one active node. Choose one tree for source families that must switch together; separate trees switch independently.
- A branch is a source family inside a tree (the root branch has the empty ID `""`). Every branch has its own `src/`, build template, and `versions/` directory.
- A node is one buildable Gradle project: a branch at one version.
- Gradle project paths come from settings, not filesystem spelling. A directory beneath `projects/` does not add a `:projects:` path prefix.
- Ordinary modules may live outside Stonecutter trees. A repository root that is not a tree controller may legitimately apply Java or aggregate tasks.
- Infer runtime loader identity from effective plugins, imports, and descriptors, not from a branch named `forge`.

## Layout A: flat multi-loader nodes

One tree, one `src/`, loader encoded in the node name. Suits small or mixin-heavy mods; loader-specific APIs are toggled with constants.

```kotlin
// settings.gradle.kts
stonecutter {
    create(rootProject) {
        fun match(project: String, vararg loaders: String, version: String = project) {
            for (loader in loaders) version("$project-$loader", version).buildscript("build.$loader.gradle.kts")
        }
        match("1.20.1", "fabric", "forge")
        match("1.21.1", "fabric", "neoforge")
        vcsVersion = "1.21.1-fabric"
    }
}
```

```text
src/                         shared, in active-node state
versions/1.20.1-fabric/      node: gradle.properties, optional src/ overrides
versions/1.21.1-neoforge/
build.fabric.gradle.kts      one template per loader
build.neoforge.gradle.kts
stonecutter.gradle.kts       controller: active node, tags, loader constants
```

- Always pass the logical version separately. A bare `1.21.1-fabric` is parsed as a SemVer prerelease and compares below `1.21.1`.
- Node paths are `:1.21.1-fabric`; the VCS and active values are full node names.
- Register every loader name in `constants.match(loader, ...)`, including loaders absent from some versions, so a condition naming any loader resolves on every node.
- Add the version and loader as property tags; default tags are only the node name and branch ID.
- Split native loader build scripts are the upstream-preferred flat setup. Do not force one build plugin to emulate every loader.

## Layout B: multi-project trees with branches

Several independently switchable trees (for example one per library), each with a common root branch and loader branches. Suits mods that lean on each loader's toolkit or publish a separate common artifact.

```kotlin
// settings.gradle.kts
include(":alpha", ":beta")
for (project in rootProject.children) project.projectDir = file("projects/${project.name}")

stonecutter {
    create("alpha", "beta") {
        versions("1.20.1", "1.21.1")
        branch("fabric")
        branch("forge")
        vcsVersion = "1.20.1"
    }
}
```

```text
projects/alpha/stonecutter.gradle.kts     controller for the alpha tree
projects/alpha/src/                       root (common) branch sources
projects/alpha/versions/1.20.1/           node :alpha:1.20.1
projects/alpha/fabric/src/                fabric branch sources
projects/alpha/fabric/build.gradle.kts    fabric branch template
projects/alpha/fabric/versions/1.20.1/    node :alpha:fabric:1.20.1
```

- Node paths are `:alpha:1.20.1` for the root branch and `:alpha:fabric:1.20.1` for a branch (0.9.8 and 0.10 `[probe]`).
- A branch without its own version list takes the tree's versions `[probe]`. On 0.9.x the copy happens when `branch(...)` is called, so declare `versions(...)` first or the branch stays empty; 0.10 copies lazily `[source]`. Give a branch an explicit list when a loader does not exist for every version.
- Each tree has its own active literal and its own switch tasks. The unqualified task switches every tree; `:alpha:Set active project to ...` switches one and leaves the others where they were `[probe]`.
- Controller parameters see the branch through `node.branch.id`, node scripts through `sc.branch.id` (empty for the root branch) `[probe]`; derive loader constants from it instead of parsing project names.
- Loader branches depend on the same-version node of the common branch, for example `project(":alpha:${sc.current.project}")` `[probe]`. If a branch packages the common node's sources or resources directly, also wire those tasks to the common node's `stonecutterGenerate`, or inactive nodes package stale files.
- A node needing a different build script than its branch can be redirected after the tree is created by setting that project's `buildFileName` in settings. Every such redirect is tied to a node name and must be removed with the node.
- A branch named after one loader family can host different runtime loaders per version. Define explicit constants for each real loader rather than reusing the branch name in conditions.

## Discover, scope, then execute

```bash
./gradlew projects
./gradlew tasks --all
```

Use the exact discovered paths. Do not transplant a library name, node inventory, or task path from another repository.

- Quote fully qualified controller switch tasks when only one tree should switch, for example `./gradlew ":alpha:Set active project to 1.21.1"`. An unqualified task name runs in every project that has it.
- Run switching/reset first and compilation in a separate Gradle invocation.
- Inspect test source sets and run configuration: compiling production code does not prove that test classes, metadata, and mixins are loaded.
- Verify the task graph reaches intended leaves. `build` selects every project's task; `:build` targets only the root task and its declared dependencies.
- Read CI commands before claiming coverage. A successful build is not evidence of a client launch or runtime GameTests.
- For read-only audits, inspect tracked settings/build/CI files instead. Gradle configuration itself writes caches and can generate sources.

## Overrides and canonical state

The active node and the VCS node can differ intentionally. Resetting is a source-changing operation, not a harmless read-only audit step.

Inspect per-node source overrides in every relevant branch before editing shared code. A complete override leaves one target unchanged even when the shared implementation changes, and the same relative path must be excluded from the shared source set while that node is active (see the core skill's pitfalls).

Topology is a design decision, not a fixed repository inventory: describe what the settings file registers, then verify it with `projects`.
