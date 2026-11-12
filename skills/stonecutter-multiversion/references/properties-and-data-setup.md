# Structured properties and data-driven setup

Property lookup rules changed between 0.9.x and 0.10. A build that configures successfully after an upgrade can still resolve a different value, so compare resolved values per node, not exit codes.

## Property sources and resolution

- Structured files are discovered beside settings (all projects), beside the controller (its tree), and in each version directory (its node) `[wiki]`.
- Default filenames are `stonecutter.properties.*` with `.toml`, `.yml`, `.yaml`, `.json5`, or `.json`. When several formats share a directory only the first of TOML, YAML, JSON is loaded; they are not merged `[wiki]`.
- Load additional files explicitly with `sc.properties.load(file(...))` (present on 0.9.8 and 0.10 `[source]`).
- `org.gradle.*` launch settings belong in native `gradle.properties`. Do not move launch flags because `sc.properties` can read them.

## Accessors by version

| Concern | 0.9.8 | 0.10 |
| --- | --- | --- |
| Typed Kotlin access | `sc.properties.get<Int>("mod.version")` `[probe]` | `sc.properties.getAs<Int>("mod.version")` `[probe]`; `getAsOrNull` returns `null` on a missing or unconvertible value `[wiki]` |
| String access | reified `get<String>` / `getOrNull<String>` | `sc.properties["mod.id"]`, `get`, `getOrNull` return `String`; `getLazy` returns a provider; `contains` / `in` test presence `[wiki]` |
| Visible as project property | always `[probe]` | by default, through the `expose_properties` flag `[probe]` |
| Fallback when no structured key matches | project property lookup, including `versions/<project>/gradle.properties` `[probe]` | `providers.gradleProperty`, root `gradle.properties` only `[probe]` |
| Raw paths | colon-separated | dot-separated also accepted; lists and maps are merged `[changelog]` |
| Tag matching | stricter | searches more leniently, so a formerly missing path may resolve `[changelog]` |

- On 0.10 a value kept in `versions/<project>/gradle.properties` is `null` through `sc.properties` but still visible through `project.property(...)` `[probe]`. Move such values into structured files, or keep reading them as project properties.
- `sc.properties.get<String>(...)` does not compile on 0.10 because `get` is no longer generic. Replace it with `sc.properties["..."]` for strings and `getAs<T>` for other types.
- A plugin applied in a node's `plugins {}` block reads project properties before the script body runs. One that takes its configuration from a structured property can fail on 0.10 until it is upgraded to a release that reads Stonecutter's API `[probe]`. Upgrade companion plugins together with Stonecutter.
- Exposure as project properties slows configuration and can be turned off with `expose_properties=false`; do that only after every `property("...")` read of a structured key is migrated `[wiki]`.
- Use the nullable accessors only for keys that are genuinely optional. On 0.10 `getAsOrNull` also returns `null` for a value that fails conversion, so a required or typed key read through it turns a typo into a silent default; read those with `getAs` and let the build fail.
- Composite objects are not primitive keys for `contains`. `raw()` / `rawOrNull()` return structured elements; convert in Kotlin with `.to<List<String>>()`, and inspect the element in Groovy instead of copying reified calls.

## Tags

- Default tags are the node's branch ID and project name on both lines `[source]`.
- Flat loader-suffixed nodes need explicit version and loader tags. Split on the project's actual naming convention; prerelease names can contain extra hyphens.
- Tags shorten nested keys; they do not create build nodes.
- 0.10 validates tags (no whitespace, no empty `:` segment) and adds `sc.properties.reset()` to drop every applied tag `[changelog]`.
- `warn_duplicate_properties` (0.10) raises overwritten keys from debug to warning. Leave it off when tagged files override each other on purpose.

## Data-driven tree files

- Versions-only array: flat nodes, optionally each with a logical version and build script.
- Branches-first object: branch keys map to version lists; the empty key `""` is the root branch.
- Versions-first object: version keys map to the branches containing that version.
- Keep one data source for Gradle registration and for the CI matrix instead of duplicating target lists. Removing a node then happens in one place.
- Load with `stonecutter.create(rootProject) { load(file("versions.json")) }`.
- JSON and JSON5 work on both lines. The wiki restricts TOML and YAML tree files to 0.10, while the 0.9.8 source already selects a converter by file extension; treat TOML/YAML trees on 0.9.x as `[unverified]`.
- 0.10 only `[changelog]`: `load("...")` from a string or provider (JSON unless a converter is passed), and `inherit` in data files.
- Published schemas are `https://stonecutter.kikugie.dev/settings-schema/latest.json` and `.../0.9.json`. Pin `0.9.json` on a 0.9.x project. A schema is editor assistance, not proof the installed plugin implements a field.

```json
{
  "$schema": "https://stonecutter.kikugie.dev/settings-schema/0.9.json",
  "vcs": "1.21.1",
  "versions": ["1.20.1", "1.21.1"]
}
```

## Node notation

- Compact grammar: `project(:(version)(:buildscript))`.
- `1.21.1`; `1.21.1-fabric:1.21.1`; `1.21.1::custom-build.gradle.kts`; `1.21.1-fabric:1.21.1:custom-build.gradle.kts`.
- Expanded objects require `project`; `version` and `buildscript` are optional.
- `vcs` names the project used for reset, not a version predicate.

## Branch inheritance

- A branch registered without a configuration block copies the root branch's versions on both lines `[wiki]`; on 0.9.x only versions already declared at that point `[source]`.
- 0.10 `inherit("common")`, `inherit("*")`, or a list copies from other branches. It is lazy and non-transitive: only versions a branch owns are copied, and locally declared nodes win `[changelog]`.
- On 0.9.x inheritance reaches the root branch only. Declare explicit version lists for anything else.

## Verification

Run `./gradlew projects` after a setup change and compare the node/branch inventory with the requested matrix. After an accessor or version migration, print or record each node's resolved dependency values before and after, then build all nodes.
