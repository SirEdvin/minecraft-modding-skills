# Fabric Version Checklist

Official sources used for this reference:

- Fabric developer guides: https://docs.fabricmc.net/develop/
- Fabric Loader docs: https://docs.fabricmc.net/develop/loader/
- Fabric Loom docs: https://docs.fabricmc.net/develop/loom/
- Fabric networking docs: https://docs.fabricmc.net/develop/networking
- Fabric data generation docs: https://docs.fabricmc.net/develop/data-generation/setup
- Fabric reference mod: https://github.com/FabricMC/fabric-docs/tree/main/reference/latest

## Files To Read First

- `gradle.properties`: Minecraft, loader, API, Loom, mappings, Java, Kotlin, mod id.
- `settings.gradle(.kts)`: module layout and plugin repositories.
- `build.gradle(.kts)`: Loom configuration, source sets, datagen, dependencies, run tasks.
- `fabric.mod.json`: entrypoints, mixins, access widener, dependencies, environment.
- `*.mixins.json` and `*.accesswidener`: transformer scope and target names.

## 1.20.1 Awareness

- Java is commonly 17 for Minecraft 1.20.1, but trust the Gradle toolchain.
- Fabric projects may use older networking helpers and `PacketByteBuf` patterns; do not replace them with newer payload APIs unless the active Fabric API version supports it and the task requires migration.
- Generated resources may be under `src/main/generated` or a project-specific directory; verify Gradle source-set wiring before editing JSON by hand.

## 1.21.1 Awareness

- Java is commonly 21 for Minecraft 1.21.1, but trust the Gradle toolchain.
- Verify current custom payload registration, codecs, and side-specific receive APIs against Fabric docs/source for the exact Fabric API version.
- Watch for Minecraft 1.21 changes around data components, resource locations, recipe inputs, tags, and rendering/client APIs.

## Kotlin

- Check whether the project uses `fabric-language-kotlin`, Kotlin JVM plugin, or a convention plugin wrapping them.
- Keep Kotlin code in the source set/module already used by the repo; do not introduce Kotlin into Java-only projects without a direct requirement.

## Multiloader Boundaries

- Shared/core: vanilla Minecraft abstractions and project interfaces only.
- Fabric: Loader/API imports, `fabric.mod.json`, access widener, Fabric entrypoints, Fabric networking/event/datagen bootstrap.
- Client Fabric: client initializer, renderers, screens, keybindings, client packet handlers.

## Checks

- `./gradlew build --no-daemon`
- `./gradlew runDatagen --no-daemon` when datagen changed and the task exists.
- `./gradlew runServer --no-daemon` when side safety may be affected.
