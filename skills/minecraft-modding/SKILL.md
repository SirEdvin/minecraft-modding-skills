---
name: minecraft-modding
description: Use when developing, debugging, migrating, or reviewing Minecraft Java mods across Fabric, Forge, NeoForge, Gradle/Loom/ModDevGradle, mixins, access wideners/transformers, data generation, networking, resources, and integrations such as CC:Tweaked, JEI/REI/EMI, Architectury, and Kotlin loader bridges.
license: MIT
compatibility: Requires a Java/Gradle Minecraft mod repository and network access for version-specific Fabric, Forge, NeoForge, and integration documentation.
metadata:
  author: SirEdvin
  version: "1.0.0"
  hermes-tags: "minecraft, modding, fabric, forge, neoforge, gradle, mixins, datagen"
---

# Minecraft Modding

## Overview

Use this umbrella skill to route Minecraft Java mod work without guessing the loader, mappings, or active Minecraft version. Minecraft modding is version-sensitive: a pattern that is correct for Forge 1.20.1 can be wrong for NeoForge 1.21.1 or later 26.x docs, and Fabric APIs differ again. Treat the repository's Gradle files and upstream docs as the root system; let memory only suggest where to look.

This skill is intentionally global and portable. If a project has local conventions, private Maven coordinates, or organization-specific build plugins, load a project-specific overlay skill after this one.

## Specialist Routing

Load this umbrella first, then load only the smallest matching specialist:

- `minecraft-fabric-modding` for Fabric Loader/API/Loom, `fabric.mod.json`, Fabric access wideners, Fabric networking/events/datagen, Fabric Kotlin, or Fabric modules in multiloader repos.
- `minecraft-neoforge-modding` for modern NeoForge `1.21.1+`, ModDevGradle, `neoforge.mods.toml`, NeoForge registries/events/payloads/components/attachments/datagen, or Java 21+ NeoForge work.
- `minecraft-legacy-forge-modding` for MinecraftForge `1.20.1` / Forge `47.x`, ForgeGradle or `net.neoforged.moddev.legacyforge`, `mods.toml`, `DeferredRegister` / `RegistryObject`, `SimpleChannel`, capabilities, ATs, reobf, or Forge datagen.
- `kubejs-modding` for KubeJS/Rhino/ProbeJS scripts, pack recipes/tags/schemas, reload/log debugging, or Java addon integration boundaries.
- `modrinth-api` for read-only Modrinth v2 project/search/version/file lookup, loader/version filtering, downloads, hashes, and required `User-Agent` handling.

For SirEdvin repositories, load `siredvin-minecraft-modding` after the relevant public specialist.

Supporting references:

- `references/framework-docs-map.md` — official docs and when to consult each.
- `references/repository-inspection-checklist.md` — files and symbols to inspect before editing.
- `references/version-migration-guide.md` — version-sensitive migration checkpoints.
- `references/integration-surfaces.md` — common integration mods and dependency-scope cautions.
- `templates/modding-agent-prompt.md` — prompt template for delegating work to another coding agent.

## When to Use

- The user mentions Minecraft modding, Fabric, Forge, NeoForge, ForgeGradle, ModDevGradle, Loom, mixins, access wideners, access transformers, generated resources, or Gradle mod metadata.
- A task touches `gradle.properties`, `settings.gradle(.kts)`, `build.gradle(.kts)`, `libs.versions.toml`, `fabric.mod.json`, `mods.toml`, `neoforge.mods.toml`, mixin JSON, access widener files, access transformers, or generated resource directories.
- You need to add or change registration, networking, data generation, item/block/entity behavior, client/server side separation, recipes/tags/models/lang, publishing metadata, or loader-specific entrypoints.
- You are migrating a mod between Minecraft versions or between Forge and NeoForge.
- You are integrating with CC:Tweaked, JEI/REI/EMI, ModMenu, Architectury, Kotlin loader bridges, Forge Config API Port, KubeJS/Rhino, or another mod API.

Do not use this as a substitute for official version docs. The correct API surface must be checked against the active Minecraft/loader version.

## Discovery Procedure

1. **Identify the active repository and branch.**
   - Check `git status --short --branch` and remotes before editing.
   - Do not assume the default branch maps to the user's target Minecraft version.

2. **Read build metadata first.**
   - Inspect `gradle.properties` for `minecraftVersion`, `minecraft_version`, loader versions, Java target, mod id/name/group/version, and publishing ids.
   - Inspect `settings.gradle(.kts)` for included modules, `pluginManagement`, repository filters, and plugin resolution strategy.
   - Inspect root and module `build.gradle(.kts)` plus `gradle/libs.versions.toml` for loader plugins, dependency scopes, generated resource wiring, run configs, and publishing conventions.

3. **Map the loader/module layout before coding.**
   - Common logic may live in `common`, `core`, or a shared source set.
   - Fabric-specific logic usually lives in a Fabric module/source set with `fabric.mod.json`, Fabric entrypoints, and access wideners.
   - Forge/NeoForge-specific logic usually lives in a Forge/NeoForge module/source set with `META-INF/mods.toml` or `META-INF/neoforge.mods.toml`, event bus wiring, and access transformers or loader-specific mixins.
   - Single-loader mods may have all code in `src/main/java` and resources in `src/main/resources`; do not force a multi-loader abstraction into them.

4. **Inspect neighboring code and metadata.**
   - Trace existing registration helpers, mod initializers, event listeners, networking payloads, data providers, mixin configs, resource namespace paths, and generated data conventions.
   - Search for the target symbol and sibling patterns before adding new APIs.
   - For resources, verify the namespace matches the mod id and that generated files are produced by datagen when the repository already uses datagen.

5. **Consult official docs for the active version.**
   - Fabric docs identify Fabric Loader, Fabric API, and Fabric Loom as the core toolchain and include a reference mod under `FabricMC/fabric-docs/reference/latest`.
   - Fabric datagen uses `fabricApi { configureDataGeneration() { ... } }`, a `fabric-datagen` entrypoint, and commonly outputs to `src/main/generated` via `runDatagen`.
   - Newer payload-based Fabric APIs, including the checked `1.21.1` line, use `CustomPacketPayload`, `PayloadTypeRegistry`, and side-specific `ServerPlayNetworking` / `ClientPlayNetworking`. Fabric `1.20.1` projects may instead use `Identifier` / `PacketByteBuf` APIs; follow the exact installed Fabric API and existing project pattern. Always validate client-originated packets on the server.
   - NeoForge docs are NeoForge-specific, not Java tutorials. Use the getting-started, toolchain, registry, networking, and version primer pages for the active target.
   - NeoForge registration usually prefers `DeferredRegister` attached to the mod event bus; raw `RegisterEvent` is available but easier to misuse.
   - NeoForge networking uses `RegisterPayloadHandlersEvent` and custom payload registration/handlers.
   - Forge docs remain relevant for Forge 1.20.x and legacy ForgeGradle projects.

6. **Make the smallest loader-correct change.**
   - Put cross-loader behavior in common code only when the API is genuinely common.
   - Put loader adapter code, entrypoints, run configs, dependency wiring, or metadata in the loader-specific module.
   - Avoid copying Forge-only imports into NeoForge modules or Fabric-only entrypoints into common code.

7. **Validate through the repository's wrapper.**
   - Prefer the narrowest useful Gradle task first, then a full build/check.
   - Use `--no-daemon` when the user or project prefers it.
   - For runtime behavior, use the repo's run tasks (`runClient`, `runServer`, `runData`, `runDatagen`, etc.) after inspecting actual task names.

## Loader-Specific Notes

### Fabric

- Confirm Fabric Loader, Fabric API, and Loom versions in Gradle metadata.
- `fabric.mod.json` controls mod id, entrypoints (`main`, `client`, often `fabric-datagen`), mixins, access widener, dependencies, and environment.
- Access wideners are Fabric-facing; do not confuse them with Forge access transformers.
- Datagen normally uses a `DataGeneratorEntrypoint`, a generated resources directory, and `runDatagen`.
- Networking uses registered custom payload codecs and side-specific handlers. Keep server authority and validation explicit.

### Forge 1.20.x / legacy Forge

- Confirm Forge version and ForgeGradle or organization-specific convention plugins.
- `META-INF/mods.toml` is the mod metadata source; preserve placeholder style used by the build.
- Forge event bus, capabilities, `DeferredRegister`, access transformers, and run configurations differ from Fabric and modern NeoForge.
- KotlinForForge and Java/Kotlin source conventions vary by project. Do not flatten them into generic Java-only patterns.

### NeoForge 1.21+ / 26.x

- Confirm NeoForge version and whether the repo uses ModDevGradle or an organization-specific convention wrapping it.
- `META-INF/neoforge.mods.toml` may replace or coexist with old `mods.toml` layouts depending on migration state.
- Prefer NeoForge docs for registries, events, networking, capabilities/attachments, data components, and datagen.
- Migration primers are high-level and non-exhaustive. Use them to make a checklist, then verify actual code and mappings.
- Do not reintroduce `net.minecraftforge.*` imports into a module that has already migrated to NeoForge unless the project is intentionally using legacy Forge compatibility.

## Version Migration Checkpoints

When migrating versions, read `references/version-migration-guide.md` and build a red/green checklist around the active source and target. Common checkpoints include:

- Java/JDK requirement and Gradle wrapper compatibility.
- Resource/data folder names and pack format changes.
- Registry object and holder/data component changes.
- Networking payload/codec changes.
- Rendering API changes.
- ItemStack/NBT/data component changes.
- Access widener/transformer or mixin target drift.
- Loader metadata and dependency coordinate changes.
- Run task names and generated resource wiring.

## Common Pitfalls

1. **Assuming the loader from a directory name.** A directory called `forge` may contain legacy Forge, NeoForge, or a transitional convention. Verify plugins, imports, and metadata.
2. **Skipping `gradle.properties`.** This file often carries the active Minecraft/loader version and Java target. Read it before applying any docs or migration notes.
3. **Mixing access mechanisms.** Fabric access wideners, Forge access transformers, NeoForge conventions, and mixins solve similar pain in different ways. Use the one already configured.
4. **Editing generated resources without the generator.** If the repo has datagen, update the provider and regenerate instead of hand-editing generated JSON.
5. **Trusting local Gradle caches.** Dependency or plugin resolution that works locally can fail in CI if repositories or plugin markers are missing.
6. **Wrong dependency scope.** Keep `api`, `compileOnly`, `implementation`, `runtimeOnly`, `include`, jar-in-jar, and loader-specific runtime buckets aligned with neighboring code.
7. **Client code on dedicated servers.** Client-only classes must stay behind the loader's client entrypoints/events or sided guards.
8. **Version-primer overreach.** Primers are non-exhaustive; they are a migration map, not proof that a code change is complete.

## Verification Checklist

- [ ] Active branch, repo, Minecraft version, loader version, Java target, and module layout were read from files.
- [ ] Official docs were checked for the active loader/version when API details mattered.
- [ ] Existing registration/networking/datagen/mixin/resource patterns were traced before editing.
- [ ] Changes are in the smallest correct common or loader-specific layer.
- [ ] Metadata placeholders and resource namespaces were preserved.
- [ ] Relevant Gradle validation ran through `./gradlew ... --no-daemon` or a blocker was reported clearly.
- [ ] For migrations, the target no longer contains stale imports/metadata from the old loader unless intentionally transitional.
