# Project topology and task discovery

## Distinguish tree, branch, node, and ordinary module

- A tree coordinates branches and version nodes. Choose one tree for source families that must switch together; separate trees can have independent active states.
- Flat layouts can encode loader identity in a node name. Register the logical Minecraft version separately so loader suffixes do not affect version comparisons.
- Branched layouts separate common and loader-specific source families, each with version nodes. Resolve dependencies to the matching node rather than an obsolete module path.
- Gradle project paths come from settings, not filesystem spelling. A directory beneath `projects/` does not automatically add a `:projects:` path prefix.
- Ordinary modules may live outside Stonecutter trees. A repository root that is not a tree controller may legitimately apply Java or aggregate tasks; do not remove plugins merely because another module uses Stonecutter.
- Infer runtime loader identity from effective plugins, imports, and descriptors, not a branch named `forge`.

## Discover, scope, then execute

Invoke through `terminal` in a writable checkout where Gradle configuration is authorized:

```bash
./gradlew projects
./gradlew tasks --all
```

Use the exact discovered paths for subsequent task selection. Do not transplant a library name, node inventory, or task path from another repository.

- Quote fully qualified controller switch tasks when only one tree should switch. Preserve spaces when parsing task names; unqualified task selection can reach multiple projects.
- Run switching/reset first and compilation in a separate Gradle invocation. See the core skill's version-specific implicit-dependency warning.
- Inspect test source sets and run configuration: compiling production code does not prove that test classes, metadata, and mixins are loaded.
- Verify the task graph reaches intended leaves. `build` task selection differs from `:build`, which targets only the root task and its declared dependencies.
- Read CI commands before claiming coverage. A successful build is not evidence of a client launch or runtime GameTests.
- For read-only audits, inspect tracked settings/build/CI files instead. Gradle configuration itself can write caches and generate sources.

## Overrides and canonical state

The active node and configured VCS node can differ intentionally. Resetting is a source-changing operation, not a harmless read-only audit step.

Inspect per-node source overrides in every relevant branch before editing shared code. A complete override can leave one target unchanged even when the shared implementation changes. Preserve installed plugin/toolchain versions unless an upgrade is explicitly part of the task.

Use the core skill's official Stonecutter documentation and release-specific references for API syntax; topology is a design decision, not a fixed repository inventory.
