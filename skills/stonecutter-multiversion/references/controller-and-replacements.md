# Controller, task orchestration, and replacement mechanics

## Sources
- Controller: https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/project-controller
- Replacements: https://stonecutter.kikugie.dev/wiki/v2/reference/syntax/replacements
- Release history: https://stonecutter.kikugie.dev/blog/changes/0.9
- Reviewed 2026-09-06; the current wiki mixes released 0.9.x behavior and forward-looking 0.10 APIs.

## Execution model
- Controller script executes once in configuration; the build template executes for every node.
- `parameters {}` lazily supplies preprocessing configuration, not arbitrary node task/dependency configuration.
- Use ordinary node build scripts for dependencies and task wiring.
- Assign active exactly once: literal, file-backed, or detached `null`.
- Put programmatic flags before active initialization.
- The 0.10 wiki calls the version container `targets`; released 0.9.x uses `dependencies`. The old name is documented as a deprecated alias in 0.10.
- Controller examples still use `node.project.property`; the 0.9.7 changelog recommends `project.property` instead. For 0.10 structured values, also account for the property-access migration in the companion reference.

## Lazy task aggregation
Documented Kotlin shape, valid only when the selected publishing plugin registers `publishMods`:

```kotlin
tasks.register("publishModsAndAnnounce") {
    group = "publishing"
    val publishMods = stonecutter.tasks.named("publishMods")
    dependsOn(publishMods)
    doLast {
        // Add an approved announcement implementation here.
    }
}
```

- This is an API pattern, not a ready publishing workflow or permission to publish.
- Keep the lazy collection as a dependency; do not force it with `.get()`.
- Filter example: `stonecutter.tasks.named("publishMods") { metadata.project.endsWith("-snapshot") }`.
- Inspect `./gradlew tasks --all` through `terminal` before using any task name from examples.

## Ordering versus dependencies
- `order` controls only the named task, not its prerequisites or downstream consumers.
- Register ordering at most once per task; duplicates can create cycles.
- Default ordering parses each node's logical version, not its project identifier.
- Order concrete publishing tasks, not only an umbrella task that delegates to them.
- Documented concrete examples: `order("publishModrinth")` and `order("publishCurseforge")`.
- A version-then-loader comparator is documented as `versionComparator.thenComparingInt { if (it.metadata.project.endsWith("fabric")) 1 else 0 }`.
- Wiki says missing-task leniency starts in 0.9; the release changelog specifically records the change in 0.9.3. For 0.9.0–0.9.2, verify rather than assuming leniency.
- 0.9.7 changed ordering from lock files to a build service limiting parallelism, including fixes for tasks such as `compileJava`.
- Do not serialize an entire build merely because one artifact-generation task is concurrency-sensitive.

## Lifecycle wiring
- Tasks in `stonecutter-impl` are implementation tasks, not normal manual entry points.
- NeoForge integration example belongs in the node build template:

```kotlin
tasks.named("createMinecraftArtifacts") {
    dependsOn("stonecutterGenerate")
}
```

- This dependency wiring differs from invoking `stonecutterGenerate` manually.
- Documented switch customization: `for ((project, switch) in stonecutter.tasks.switch) switch.configure { }`.
- Internal `stonecutterSwitchTo...` tasks are used by the IntelliJ integration; discover user-facing switch tasks instead of inventing internal suffixes.

## Flag diagnosis
All properties below have prefix `dev.kikugie.stonecutter.` and live in controller-root `gradle.properties`.

| Suffix | Purpose / documented current default |
| --- | --- |
| `hard_mode` | Suppress Groovy limitation warning; false; property-only |
| `auto_apply_plugin` | Apply plugin to nodes; true |
| `generate_sources_on_sync` | Generate during IntelliJ Gradle sync; true |
| `generate_switch_actions` | Create IntelliJ switch run configurations; true |
| `serialize_tree_model` | Write model cache for IDE/addon tooling; true |
| `extra_source_check` | Second source-directory discovery pass; true |
| `implicit_receiver` | Default predicate target; `minecraft` |
| `generate_manifest` | Include Stonecutter JAR metadata; true |

- A preprocessing error can break IDE sync when source generation on sync is enabled; the current documented default is enabled, so diagnose rather than assuming the user opted in.
- Late-added source directories motivate `extra_source_check`; do not disable it casually during addon integration.
- `StonecutterFlag.LINE_SEPARATOR` is documented for 0.10 only; no property key is documented, so do not invent one.
- The wiki dates `GENERATE_MANIFEST` to 0.8, but the 0.9 changelog explicitly introduces the flag in 0.9.4. Treat availability before 0.9.4 as unresolved without tagged-source verification.
- Manifest fields documented: `Stonecutter-Plugin-Version`, `Stonecutter-Gradle-Version`, `Stonecutter-Node-Project`, `Stonecutter-Node-Version`.
- These can help inspect artifact provenance; they do not replace compile/runtime testing.

## Replacement selection
- Prefer a condition for isolated alternate code blocks, a swap for repeated whole fragments, and a string replacement for reversible textual renames.
- The boolean passed to `replacements.string` is direction: true maps old to new; false reverses the map.
- String matching considers both input and output patterns, preventing already-replaced text from expanding repeatedly.
- Regex needs explicit forward and reverse patterns; the engine cannot infer an inverse from replacement text.
- Do not use regex solely to avoid naming the exact literal to replace.
- String replacements have ambiguity/cycle checks; regex cannot provide the same guarantees.

## Named global replacement state
```kotlin
stonecutter {
    replacements.string(current.parsed >= "1.21", "me_imports") {
        replace("io.github.me", "dev.me")
    }
}
```

- Unnamed global replacements affect all processed files.
- An identifier disables a replacement by default; register `"!me_imports"` to enable it by default.
- `//~ me_imports` enables subsequent processing; `//~ !me_imports` disables it.
- This is set/reset behavior, not toggling: repeated disable directives remain disabled.
- Multiple IDs fit in one directive: `//~ enable_me !disable_me`.
- Place the enabling directive before code if the replacement must affect the whole file; later directives deliberately affect only subsequent regions.

## Local replacement scope
- A local replacement has its own scope and can nest; nested replacements accumulate.
- Example opener: `//~ if >=1.21 '.getName()' -> '.name' {`; closer: `//~}`.
- Simple identifier values may omit quotes; other values use single quotes, escaping embedded quotes with `\'`.
- The current wiki also documents `as name_getter` and anonymous `as _` declarations for the rest of the file. These are unavailable in 0.9.x; do not add them to that release line.
- Named local declarations can share IDs with each other or globals, linking activation behavior; use distinct identifiers unless sharing is intentional.

## Overlap and preservation
1. Earlier starting match wins.
2. Equal start: longer match wins.
3. Exact same range: current wiki describes last-registered regex replacement winning.
- The 0.9 prerelease changelog describes exact-range tie resolution as effectively random/newly found. Avoid relying on tie order across versions.
- Output preservation means `MyClass` to `MyClassRewrite` should not become `MyClassRewriteRewrite` on refresh.
- Replacements can span ordinary text/comments, but Stonecutter directive comments interrupt matching.
- A lookup failing near another directive may reflect that boundary rather than a missing literal in the whole file.

## Verification
Invoke a switch away and back through `terminal`, using exact discovered task names, then inspect `git diff` for repeatable output. Run the core skill's all-node build; a successful one-way rename does not prove reversibility.
