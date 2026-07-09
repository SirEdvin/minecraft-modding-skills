---
name: minecraft-neoforge-modding
description: Use when working on modern NeoForge Minecraft mods, NeoForge 1.21.1 or later, ModDevGradle, Java 21+, Kotlin compatibility, neoforge.mods.toml, registries/events, payload networking, data components, attachments, datagen, or dedicated-server safety.
license: MIT
compatibility: Independently authored for modern NeoForge projects; verify exact Minecraft, NeoForge, ModDevGradle or NeoGradle, Java, Kotlin, and mappings versions from repository files before applying API details.
metadata:
  author: SirEdvin
  version: "1.0.0"
  hermes-tags: "minecraft, neoforge, moddevgradle, java21, kotlin, networking, datagen"
---

# Minecraft NeoForge Modding

Use this specialist directly, or after `minecraft-modding`, for NeoForge `1.21.1+` codebases or NeoForge modules inside multiloader projects. Prefer current NeoForge docs over older Forge habits; do not introduce `net.minecraftforge.*` imports into NeoForge-native modules unless the repository is intentionally transitional.

References:

- `references/neoforge-version-checklist.md`

## Workflow

1. Read `gradle.properties`, `settings.gradle(.kts)`, build files, `libs.versions.toml`, `META-INF/neoforge.mods.toml`, event registration, datagen setup, and run configs.
2. Confirm exact Minecraft, NeoForge, ModDevGradle or NeoGradle, Java toolchain, mappings, and Kotlin bridge versions.
3. Follow existing constructor injection and event-bus patterns in the mod main class. Do not invent a global bootstrap if the generated/current pattern passes services through the constructor.
4. Use the repo's existing registry style. Modern NeoForge commonly uses `DeferredRegister` with the mod event bus; raw registration events need extra care.
5. Keep payload networking, data components, attachments, capabilities, datagen, and client setup version-specific; check official docs/source before naming APIs.

## Safety Rules

- Client classes must stay behind client-only event registration or sided setup. Test `runServer` when a change touches rendering, screens, key mappings, client payload handlers, or class initialization.
- Data components and attachments solve different problems. Use the one the docs and neighboring code use for the target object and persistence lifecycle.
- Kotlin is compatible when the project already configures it. Preserve source sets and loader bridge coordinates; do not add Kotlin to Java-only projects without a direct request.

## Validation

- Use the wrapper: `./gradlew build --no-daemon`.
- For runtime changes, run the actual repo tasks, usually `runClient` and `runServer`.
- For data providers, run the repo's datagen task and review generated output rather than hand-editing generated files.
