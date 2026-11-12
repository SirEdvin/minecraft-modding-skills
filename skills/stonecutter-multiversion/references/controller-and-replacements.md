# Controller, task orchestration, and replacement mechanics

## Execution model

- The controller script runs once during configuration; the build template runs for every node.
- `parameters {}` lazily supplies preprocessing configuration. Dependencies and task wiring belong in node build scripts.
- Assign the active node exactly once: literal, file-backed, or detached `null`. Put programmatic flags before that statement.
- 0.9.x requires `plugins { id("dev.kikugie.stonecutter") }` in the controller `[probe]`; 0.10 applies the plugin itself and treats the block as a no-op `[probe]`.
- The predicate-version container is `dependencies` on 0.9.x and `targets` on 0.10; the old name still works on 0.10 with a deprecation warning `[probe]`.
- Read the active node in the controller with `stonecutter.current` on 0.9.x and `stonecutter.active` on 0.10 `[changelog]`.
- Inside `parameters {}` prefer `project.property(...)` or `properties[...]` over `node.project.property(...)`.

## Lazy task aggregation

Valid only for a task the applied plugins actually register on the nodes:

```kotlin
tasks.register("publishAll") {
    group = "publishing"
    dependsOn(stonecutter.tasks.named("publishMods"))    // 0.9.x
    // dependsOn(stonecutter.tasks.names("publishMods")) // 0.10
}
```

- `named` returns lazy task providers; never force it with `.get()`.
- `names` (0.10) returns qualified task paths and is the only form that works with Isolated Projects; `named` still works on 0.10 with a deprecation warning `[probe]`.
- Both accept a node filter: `{ metadata.project.endsWith("-snapshot") }`.
- This is an API pattern, not a publishing workflow or permission to publish. Read `tasks --all` before using a task name from an example.

## Ordering versus dependencies

- `order` controls only the named task, not its prerequisites or consumers.
- Register ordering at most once per task; duplicates can create cycles.
- Default ordering parses each node's logical version, not its project name. Add a comparator for loader order: `versionComparator.thenComparingInt { if (it.metadata.project.endsWith("fabric")) 1 else 0 }`.
- Order concrete publishing tasks, not an umbrella task that only delegates.
- Missing tasks are skipped from 0.9.3; older versions fail `[changelog]`.
- 0.10 exposes the underlying lock as `StonecutterTaskMutexService.create(gradle, "name")` for `usesService(...)` in any build script. It prevents parallel runs without promising an order `[wiki]`.
- Do not serialize an entire build because one artifact-generation task is concurrency-sensitive.

## Lifecycle wiring

- Tasks in the `stonecutter-impl` group are implementation tasks, not manual entry points.
- Loader artifact generation must see generated sources. In the node build template:

```kotlin
tasks.named("createMinecraftArtifacts") {
    dependsOn("stonecutterGenerate")
}
```

- 0.10 merged `stonecutterPrepare` into `stonecutterGenerate` `[changelog]`; depend on `stonecutterGenerate` only.
- Customize switching with `for ((project, switch) in stonecutter.tasks.switch) switch.configure { }`.
- `stonecutterSwitchTo...` tasks exist for the IDE integration. Use the discovered `Set active project to ...` tasks.

## Flags

Properties have the prefix `dev.kikugie.stonecutter.` and live in the `gradle.properties` beside the controller. Names and defaults below are the 0.10 documentation `[wiki]`.

| Suffix | Purpose | Default |
| --- | --- | --- |
| `hard_mode` | Opt into Groovy scripts and silence the limitation notice | false |
| `auto_apply_plugin` | Apply the plugin to nodes (0.9.x name: `APPLY_PLUGIN_TO_NODES`) | true |
| `generate_sources_on_sync` | Generate sources during IDE Gradle sync | true |
| `generate_switch_actions` | Create IDE switch run configurations | true |
| `serialize_tree_model` | Write model cache for IDE/addon tooling | true |
| `extra_source_check` | Second source-directory discovery pass | true |
| `implicit_receiver` | Default predicate target | `minecraft` |
| `generate_manifest` | Add Stonecutter attributes to JAR manifests | true |
| `line_separator` (0.10) | Force a line ending in processed files; empty preserves | empty |
| `short_extension` (0.10) | Register the `sc` alias; property-only | true |
| `expose_properties` (0.10) | Mirror structured properties into project properties | true |
| `warn_duplicate_properties` (0.10) | Warn on overwritten structured keys | false |
| `suppressed_warnings` (0.10) | Mute listed warning IDs; errors cannot be muted | empty |

- 0.10 scopes flags: settings flags are set in `settings.gradle(.kts)`, controller flags in the controller, node and local flags in build scripts; a script cannot overwrite a flag of another scope `[changelog]`.
- With generation on sync enabled, a preprocessing error breaks IDE sync. Fix the preprocessing error; the sync integration is working as designed.
- Do not disable `extra_source_check` casually; late-added source directories depend on it.
- JAR manifests carry `Stonecutter-Plugin-Version`, `Stonecutter-Gradle-Version`, `Stonecutter-Node-Project`, and `Stonecutter-Node-Version` (0.10 `[probe]`). They show which node and plugin built an artifact; they do not replace compile or runtime testing.

## Replacement selection

- Prefer a condition for an isolated alternate block, a swap for a repeated fragment, and a string replacement for a reversible rename.
- The boolean passed to `replacements.string` is direction: true maps old to new, false reverses.
- String matching considers both input and output patterns, so already-replaced text is not expanded again.
- Regex needs explicit forward and reverse patterns; the engine cannot infer an inverse. Do not use regex only to avoid naming a literal.
- On 0.9.x ambiguous or cyclic string mappings are rejected at configuration. On 0.10 validity is checked while processing, ambiguity is still an error, and a cycle is left unreplaced `[changelog]`.

## Named global replacement state

```kotlin
stonecutter {
    replacements.string(current.parsed >= "1.21", "me_imports") {
        replace("io.github.me", "dev.me")
    }
}
```

- Unnamed global replacements affect every processed file. On 0.10 that includes JSON and other comment-less resource formats; see the source-syntax reference before upgrading.
- An identifier disables a replacement by default; register `"!me_imports"` to enable it by default.
- `//~ me_imports` enables subsequent processing; `//~ !me_imports` disables it. This is set/reset, not a toggle.
- Several IDs fit in one directive: `//~ enable_me !disable_me`.
- Put the enabling directive before code when the whole file needs it; later directives affect only what follows.
- Pass direction first, then the identifier; the identifier-first overload is deprecated on 0.10 `[source]`.

## Local replacement scope

- A local replacement has its own scope and can nest; nested replacements accumulate.
- Opener `//~ if >=1.21 '.getName()' -> '.name' {`, closer `//~}`.
- Simple identifier values may omit quotes; other values use single quotes with `\'` for embedded quotes.
- `as name` and anonymous `as _` declarations for the rest of the file are 0.10 only.
- Named local declarations can share IDs with each other or with globals, which links their activation. Use distinct identifiers unless sharing is intended.

## Overlap and preservation

1. The earlier starting match wins.
2. At an equal start the longer match wins.
3. For an identical range do not rely on a winner; the documented tie-break changed between versions.

- Output preservation means `MyClass` to `MyClassRewrite` does not become `MyClassRewriteRewrite` on refresh.
- Replacements can span ordinary text and comments, but a Stonecutter directive comment interrupts matching. A lookup that fails near a directive may reflect that boundary rather than a missing literal.

## Verification

Switch away and back with exact discovered task names, then inspect `git diff` for repeatable output. Build all nodes; a successful one-way rename does not prove reversibility.
