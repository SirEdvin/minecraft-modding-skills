# Structured properties and data-driven setup

## Sources and version boundary
- Official structured properties: https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/structured-properties
- Official data setup: https://stonecutter.kikugie.dev/wiki/v2/reference/gradle-api/data-driven-setup
- Release baseline: https://plugins.gradle.org/plugin/dev.kikugie.stonecutter
- Historical API evidence: https://stonecutter.kikugie.dev/blog/changes/0.9
- Reviewed 2026-09-06: portal lists 0.9.8, while the live wiki already documents 0.10 APIs. Treat wiki version-difference boxes as essential, not incidental.
- The wiki's claim that TOML/YAML setup support starts in 0.10 conflicts with the 0.9.1 changelog, which explicitly introduces both formats for setup and properties. Prefer JSON for portable examples; verify tagged implementation before rejecting or adopting TOML/YAML setup on 0.9.x.

## Property sources and resolution
- Native Gradle properties merge the node's properties with root properties, not arbitrary intermediate parents.
- Structured files are automatically discovered beside settings (all projects), beside the controller (its tree), and in each version directory (its node).
- Default filenames use `stonecutter.properties.*`; supported extensions documented are `.toml`, `.yml`, `.yaml`, `.json5`, `.json`.
- When multiple formats occupy one directory, default precedence is TOML, YAML, JSON; do not assume every file is merged.
- Current wiki explicitly loads extra files with `sc.properties.load(file(...))`; verify this method against the installed version before replacing older `sc.properties(file(...))` usage documented in the 0.9.1 changelog.
- `org.gradle.*` launch settings still belong in native `gradle.properties`.
- Do not migrate launch flags merely because `sc.properties` can read them.

## Accessor migration table
| Concern | 0.9.x baseline | 0.10 documented behavior |
| --- | --- | --- |
| Primitive properties | Structured values merge into Gradle project properties | Read through `sc.properties`; no project-property merge |
| Typed Kotlin access | `sc.properties.get<Int>("mod.version")` | `sc.properties.getAs<Int>("mod.version")` |
| String API | Do not assume the new non-reified overloads | `sc.properties["mod.id"]`, `get`, `getOrNull`, `getLazy`, `contains` |
| Native fallback | Project property lookup | `providers.gradleProperty("...")`, with different lookup rules |
| Raw paths | Colon-separated fully qualified paths | Dot-separated paths also supported |
| Tag resolution | Earlier matching rules | Broader search; formerly missing paths may resolve |

- The 0.9.1 changelog already documents typed `get`/`getOrNull`; the wiki's statement about accessors being added in 0.10 refers to the new string API, not absence of every older accessor.
- Missing optional properties and conversion failures are different: nullable access must not conceal malformed values.
- Composite objects do not count as primitive keys for the new `contains` check.
- `raw()` / `rawOrNull()` return structured `SCElement` values.
- Kotlin conversion documented in 0.9.1: `sc.properties.raw("my_list").to<List<String>>()`.
- Kotlin `to()` is reified; in Groovy inspect/work with the structured element rather than copying reified Kotlin calls.

## Tags
- Default tags are `sc.current.project` and `sc.branch.id`.
- Add loader and logical-version tags explicitly for a flat loader-suffixed project.
- Tags shorten nested keys; they do not create extra build nodes.
- Use the project's actual naming convention when splitting a project identifier; prerelease names may contain additional hyphens.
- Before an accessor migration, record resolved dependency values per node and compare afterward. Successful configuration alone does not prove equivalent property resolution.

## Data setup: choose a representation
- Versions-only array: flat nodes, optionally each with logical version and build script.
- Branches-first object: branch keys map to version lists; empty key `""` means root branch.
- Versions-first object: version keys map to branches containing that version.
- Keep one data source for both Gradle registration and CI matrix discovery rather than manually duplicating target lists.
- The schema is optional editor assistance, not proof that the installed plugin implements every field.
- Schema URLs: https://stonecutter.kikugie.dev/settings-schema/latest.json and https://stonecutter.kikugie.dev/settings-schema/0.9.json . Prefer the matching versioned schema for pinned projects.

## Minimal JSON setup
Load in settings using `stonecutter.create(rootProject, file("versions.json"))`.
Since 0.9.1, the documented alternative is:

```kotlin
stonecutter.create(rootProject) {
    load(file("versions.json"))
}
```

Create the referenced file through `write_file` only within the approved project scope:

```json
{
  "$schema": "https://stonecutter.kikugie.dev/settings-schema/0.9.json",
  "vcs": "1.21.1",
  "versions": ["1.20.1", "1.21.1"]
}
```

## Node notation
- Compact grammar: `project(:(version)(:buildscript))`.
- Project only: `1.21.1`.
- Separate project/version: `1.21.1-fabric:1.21.1`.
- Default version with custom script: `1.21.1::custom-build.gradle.kts`.
- All fields: `1.21.1-fabric:1.21.1:custom-build.gradle.kts`.
- Expanded objects require `project`; `version` and `buildscript` are optional.
- The `vcs` field identifies the project used for reset, not an arbitrary version predicate.

## Explicitly version-gated setup features
- Before 0.7.7, setup JSON is strict: JSON5 comments/trailing commas fail.
- Before 0.9.1, pass the file directly to `create`; do not call `load`.
- Serialized-string `load` is documented for 0.10; older versions accept files only.
- Explicit data-file `inherit` is documented for 0.10, not 0.9.x.
- Documented inheritance selectors: empty string for root, `*` for all branches, or a list of names.
- Inheritance is lazy and non-transitive: only owned nodes are copied; locally declared nodes win.
- Older data files can implicitly inherit root nodes by omitting a branch's versions; do not treat this as arbitrary sibling inheritance.

## Verification
Invoke `./gradlew projects` through `terminal` after a setup change and compare its node/branch inventory to the requested matrix. Then use the core skill's all-node build; verify resolved dependency values separately after property API migrations.
