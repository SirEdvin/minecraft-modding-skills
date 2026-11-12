# Legacy Forge build contracts

## Plugin contract, not folder spelling

Use https://github.com/neoforged/ModDevGradle/blob/main/LEGACY.md for legacy plugin configuration and https://docs.minecraftforge.net/en/1.20.1/ for game APIs. Forge 1.20.1 uses Java 17, `net.minecraftforge.*`, `RegistryObject`, and `META-INF/mods.toml`; NeoForged tooling does not change the runtime loader identity.

The legacy plugin's remapping configurations are non-transitive. Explicitly supply required mod dependencies; create custom local-runtime remapping configurations before using them. `modApi` requires `java-library`. Discover actual tasks and outgoing artifacts: do not assume a task named `reobfJar` exists in every ModDevGradle version merely because the production artifact requires SRG reobfuscation.

Classic SimpleImpl examples at https://docs.minecraftforge.net/en/1.20.1/networking/simpleimpl/ use `NetworkRegistry.newSimpleChannel` and network-thread handlers. Forge 47.x patches may expose different channel/builder APIs; inspect the pinned dependency before copying construction or send signatures. Main-thread consumers do not eliminate server-side validation.

## Verify the target build

- Read effective plugins, mappings, toolchains, source sets, and loader metadata rather than inferring them from directory names. Preserve existing multi-module and versioned configuration.
- Discover node-qualified tasks before execution; plugin application does not guarantee a client, server, datagen, or GameTest run exists.
- Build the affected targets and inspect production artifacts for the expected loader descriptor, expanded placeholders, and correct remapping/reobfuscation. Descriptor presence alone does not prove bytecode correctness.
- Report compilation, unit tests, GameTests, and client/server startup separately. Restore canonical source state after preprocessing and inspect the diff.
