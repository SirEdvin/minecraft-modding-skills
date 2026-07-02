# Version Migration Guide

Minecraft migrations should be handled as evidence-driven checklists, not by broad search-and-replace.

## General Migration Flow

1. Read source branch files: `gradle.properties`, `settings.gradle(.kts)`, root/module build files, metadata files, and current imports.
2. Identify the target Minecraft, loader, mappings, and Java/JDK requirement.
3. Read the official primer/docs for every version step crossed.
4. Build a checklist grouped by Gradle/toolchain, metadata/resources, source APIs, datagen, networking, rendering/client, and integrations.
5. Port in small commits or patches by layer; run the narrowest useful Gradle task after each risky layer.
6. Remove stale imports, metadata, and dependency coordinates only after their replacement is verified.

## 1.20.1 Forge to 1.21.x NeoForge Watchpoints

- ForgeGradle/Forge 47.x projects are not the same as NeoForge/ModDevGradle projects.
- Confirm whether the target uses `net.neoforged.moddev`, an organization-specific wrapper plugin, or a transitional legacy Forge setup.
- Do not reintroduce `net.minecraftforge.*` imports into a module that is already NeoForge-native.
- Convert metadata deliberately: `META-INF/mods.toml` may become `META-INF/neoforge.mods.toml` in NeoForge modules.
- Verify Kotlin loader bridge coordinates: KotlinForForge vs KotlinForForge-NeoForge differ.
- Check dependency coordinates for JEI/REI/EMI/CC:Tweaked and other integrations. Artifact suffixes may be `forge`, `neoforge`, `fabric`, or version-specific.
- Minecraft 1.21 changes include private `ResourceLocation` constructors (`fromNamespaceAndPath`, `parse`, `withDefaultNamespace`, etc.), depluralized data/tag folders, rendering changes, datapack registry/holder changes, and recipe/input changes.
- 1.21+ code often uses data components / `CustomData` flows instead of older direct NBT/tag mutation patterns.

## 26.x Watchpoints

- NeoForge 26.1/26.2 docs may require newer JDKs and updated rendering/client APIs.
- The 26.2 primer highlights broad rendering pipeline changes, Vulkan-related abstractions, GPU formats, vertex format rewrites, GUI/HUD reorganization, font/text rendering changes, resource key/tag changes, and data component additions.
- Treat these as a review queue: locate affected code, verify exact mappings/API signatures, then migrate.

## Safe Diff Strategy

- First make dependency/plugin/metadata changes compile far enough to resolve sources.
- Then migrate source imports and API calls by feature area.
- Then update resources/datagen outputs.
- Finally validate runtime/client/server behavior.

Avoid mixing generated-resource churn, dependency upgrades, API migrations, and formatting in one opaque patch.
