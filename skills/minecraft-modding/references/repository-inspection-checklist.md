# Repository Inspection Checklist

Before changing Minecraft mod code, inspect these files and answer these questions.

## Build and Version Files

- `gradle.properties`
  - Minecraft version (`minecraftVersion`, `minecraft_version`).
  - Loader versions (`forge`, `forgeVersion`, `neoforge`, `fabric-loader`, etc.).
  - Java target / toolchain if present.
  - Mod id, package/group, version, archives/base names, publishing ids.
- `settings.gradle`, `settings.gradle.kts`
  - Included modules/source sets.
  - `pluginManagement` repositories and content filters.
  - Plugin resolution strategy or custom plugin marker mappings.
- `build.gradle`, `build.gradle.kts`
  - Loader plugins (Loom, ForgeGradle, ModDevGradle, custom conventions).
  - Run tasks/configs, generated resources, publishing, datagen, jar-in-jar/include rules.
- `gradle/libs.versions.toml`
  - Dependency coordinates and version refs.
  - Loader-specific artifact names (e.g. `fabric`, `forge`, `neoforge` classifiers).

## Metadata and Resource Files

- `fabric.mod.json`
  - Mod id, dependencies, mixins, entrypoints (`main`, `client`, `fabric-datagen`), access widener, environment.
- `META-INF/mods.toml`
  - Forge metadata, mod loader, dependency ranges, placeholders.
- `META-INF/neoforge.mods.toml`
  - NeoForge metadata and placeholders.
- `*.accesswidener`
  - Fabric access-widener targets; verify common vs loader-facing files.
- `META-INF/accesstransformer.cfg` or equivalent
  - Forge/NeoForge access transformers.
- `*mixins*.json`
  - Mixin package, compatibility level, client/server split, referenced classes.
- `src/main/resources/assets/<modid>/` and `data/<modid>/`
  - Namespace correctness and generated/static split.
- `src/generated/resources/` or similar
  - Treat as generated if datagen providers exist.

## Code Patterns to Trace

- Mod main initializer / constructor.
- Client initializer / client event setup.
- Registration helpers for blocks, items, entities, menus, data components, creative tabs, attachments/capabilities.
- Networking payload definitions, codecs/readers, sender helpers, and receiver registration.
- Datagen entrypoints/providers and how generated resources are wired into Gradle.
- Config setup and loader-specific config bridges.
- Integration entrypoints for JEI/REI/EMI, CC:Tweaked peripherals, KubeJS, GTCEu, Create, AE2, or project-specific APIs.
- Test fixtures and game test namespaces if present.

## Questions to Answer Before Editing

1. Which Minecraft version and loader are active on this branch?
2. Is this project single-loader, multi-loader, or in migration?
3. Where does shared behavior belong, and where are loader adapters required?
4. Are the target files generated or source-of-truth?
5. Which official docs match the exact loader/version?
6. Which Gradle task proves this change most cheaply?
7. Does the change need client, server, and dedicated-server validation?
