# Legacy Forge build contracts and project evidence

## Plugin contract, not folder spelling

Use https://github.com/neoforged/ModDevGradle/blob/main/LEGACY.md for legacy plugin configuration and https://docs.minecraftforge.net/en/1.20.1/ for game APIs. Forge 1.20.1 uses Java 17, `net.minecraftforge.*`, `RegistryObject`, and `META-INF/mods.toml`; NeoForged tooling does not change the runtime loader identity.

The legacy plugin's remapping configurations are non-transitive. Explicitly supply required mod dependencies; create custom local-runtime remapping configurations before using them. `modApi` requires `java-library`. Discover actual tasks and outgoing artifacts: do not assume a task named `reobfJar` exists in every ModDevGradle version merely because the production artifact requires SRG reobfuscation.

Classic SimpleImpl examples at https://docs.minecraftforge.net/en/1.20.1/networking/simpleimpl/ use `NetworkRegistry.newSimpleChannel` and network-thread handlers. Forge 47.x patches may expose different channel/builder APIs; inspect the pinned dependency before copying construction or send signatures. Main-thread consumers do not eliminate server-side validation.

## Inspected implementation

[TemplateProject at 042d296e255d6a9e75e1d2f40da9937810e92004](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004): `settings.gradle.kts` assigns the 1.20.1 Forge node to `build.forge.gradle.kts`. That build uses `net.neoforged.moddev.legacyforge` 2.0.143, Java 17, and `legacyForge.mods`; it expands checked-in `src/main/resources/META-INF/mods.toml` via `processResources` instead of generating metadata from an MDK template. It excludes both other loader descriptors and configures no runs.

[Minecraft-Modding-Libs at 86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c): `settings.gradle.kts` declares common modules and `forge`/`fabric` branches for both 1.20.1 and 1.21.1. Discover node-qualified tasks instead of replacing its module graph with a single-version MDK.

## Verification and limits

The coordinator built all four template nodes in a disposable clone. The Forge production JAR contained only `META-INF/mods.toml` as loader metadata, with no unexpanded placeholders. Task discovery did not expose `reobfJar` or run tasks for this minimal Forge node; JAR descriptor inspection is not proof of bytecode reobfuscation or runtime correctness.

The coordinator also built 24 versioned library nodes plus the typed API. Aggregate unit-test evidence was 50 reports / 1060 executions with zero failures, errors, or skips; it is not a loader-specific GameTest claim. Client/server launches and GameTests remain untested.
