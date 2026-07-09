# Forge 1.20.1 Checklist

Official sources used for this reference:

- MinecraftForge docs 1.20.x: https://docs.minecraftforge.net/en/1.20.x/
- Forge registries: https://docs.minecraftforge.net/en/1.20.x/concepts/registries/
- Forge events: https://docs.minecraftforge.net/en/1.20.x/concepts/events/
- Forge SimpleImpl networking: https://docs.minecraftforge.net/en/1.20.x/networking/simpleimpl/
- Forge capabilities: https://docs.minecraftforge.net/en/1.20.x/datastorage/capabilities/
- Forge access transformers: https://docs.minecraftforge.net/en/1.20.x/advanced/accesstransformers/
- Forge data generation: https://docs.minecraftforge.net/en/1.20.x/datagen/
- ForgeGradle: https://github.com/MinecraftForge/ForgeGradle
- NeoForged legacy Forge plugin: https://github.com/neoforged/ModDevGradle

## Build Modes

- ForgeGradle projects often use ForgeGradle plugin IDs and reobfuscation tasks.
- `net.neoforged.moddev.legacyforge` projects are still targeting legacy Forge; do not treat them as NeoForge source just because the plugin is published by NeoForged.
- Java 17 is normal for Minecraft 1.20.1, but verify the Gradle toolchain.

## Files To Read First

- `META-INF/mods.toml`: loader metadata, dependency ranges, placeholders.
- `META-INF/accesstransformer.cfg`: access changes included in the jar.
- Main mod class: mod event bus, Forge event bus, config, registry setup.
- Network class: `SimpleChannel`, protocol version, message IDs, login/play direction.
- Capability providers/attachments and invalidation logic.
- Datagen providers and run-data Gradle task wiring.

## Common Correct Patterns

- `DeferredRegister` plus `RegistryObject` for most mod registries.
- `FMLJavaModLoadingContext` or equivalent existing context access for the mod event bus, depending on the project's Forge version and wrappers.
- `SimpleChannel` with explicit protocol compatibility and server-side validation for client-originated packets.
- Capabilities for optional object behavior/storage where Forge 1.20.1 docs and neighboring code use them.

## Checks

- `./gradlew build --no-daemon`
- `./gradlew runData --no-daemon`
- `./gradlew runServer --no-daemon`
- Reobf task used by the repo, if distribution jar output is affected.
