---
name: minecraft-legacy-forge-modding
description: Use when working on MinecraftForge 1.20.1 / Forge 47.x projects, ForgeGradle or net.neoforged.moddev.legacyforge builds, Java 17, mods.toml, DeferredRegister and RegistryObject, SimpleChannel networking, capabilities, mixins, access transformers, reobfuscation, or Forge datagen.
version: 1.0.0
author: SirEdvin
license: MIT
compatibility: Independently authored for Forge 1.20.1 and Forge 47.x projects; verify exact Minecraft, Forge, ForgeGradle or legacy ModDevGradle, Java, mappings, and optional integration versions before applying API details.
metadata:
  hermes:
    tags: [minecraft, forge, minecraftforge, forgegradle, legacyforge, java17, datagen]
---

# Minecraft Legacy Forge Modding

Use this specialist after `minecraft-modding` for MinecraftForge `1.20.1` / Forge `47.x` projects, including builds using classic ForgeGradle or `net.neoforged.moddev.legacyforge`. This is not modern NeoForge: keep `mods.toml`, Forge event buses, Forge capabilities, `SimpleChannel`, access transformers, and reobfuscation behavior aligned with the existing repo.

References:

- `references/forge-1201-checklist.md`
- `../minecraft-modding/references/repository-inspection-checklist.md`
- `../minecraft-modding/references/integration-surfaces.md`

## Workflow

1. Read `gradle.properties`, `settings.gradle(.kts)`, build files, `META-INF/mods.toml`, `META-INF/accesstransformer.cfg`, mixin configs, run configs, and datagen providers.
2. Confirm exact Minecraft `1.20.1`, Forge `47.x`, Java 17 toolchain, mappings, ForgeGradle or legacy ModDevGradle plugin, and reobf task names.
3. Follow existing `DeferredRegister` / `RegistryObject` patterns for registries unless the project already uses another verified Forge pattern.
4. Keep networking in the existing `SimpleChannel` style. Verify protocol versioning, direction, encoder/decoder, and handler threading against neighboring packets.
5. Preserve capabilities, access transformers, mixins, datagen, and generated resource wiring as configured by the repo.

## Safety Rules

- Do not apply NeoForge-only docs to Forge 47.x code.
- Client-only classes must stay behind client setup/events or sided enqueue paths; run server validation when touched.
- Reobfuscation can be part of publish/build output. Do not remove `reobfJar` or equivalent tasks unless migration explicitly replaces them.

## Validation

- `./gradlew build --no-daemon`
- `./gradlew runData --no-daemon` or the repo's datagen task when providers changed.
- `./gradlew runServer --no-daemon` when side safety changed.
- If publishing output changed, inspect whether the build expects a reobfuscated jar.
