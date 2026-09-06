# NeoForge version contracts and project evidence

## Do not backport current documentation verbatim

For 1.21.1, use the matching API: `registerSimpleItem`, `FMLEnvironment.dist`, registrar-supplied payload handlers, `PacketDistributor.sendToServer`, and unsplit `GatherDataEvent`. Later item/block property IDs, client payload-handler events, physical-side accessors, and split datagen events are separate version boundaries. Inspect exact target sources for signatures and subscriber syntax.

Official source map:

- https://docs.neoforged.net/docs/1.21.1/items/ — version-matched item registration.
- https://docs.neoforged.net/docs/1.21.1/networking/payload/ — payload registration and handler threading.
- https://docs.neoforged.net/docs/1.21.1/resources/ — older datagen contract (reviewed in this audit).
- https://neoforged.net/news/21.2release/ — item/block ID boundary.
- https://docs.neoforged.net/docs/networking/payload/ — current API, not a 1.21.1 recipe.
- https://neoforged.net/news/26.1release/ — Java 25 and 26.1 migration context.

## Inspected implementation

[TemplateProject at 042d296e255d6a9e75e1d2f40da9937810e92004](https://github.com/SirEdvin/TemplateProject/tree/042d296e255d6a9e75e1d2f40da9937810e92004): `settings.gradle.kts` selects `build.neoforge.gradle.kts` for the 1.21.1 NeoForge node. That build uses ModDevGradle 2.0.143 and Java 21, registers the main source set, expands `META-INF/neoforge.mods.toml`, excludes other loader metadata, and orders Minecraft artifact creation after Stonecutter generation. It does not configure a client/server/datagen run: a plugin name alone does not guarantee run tasks.

[Minecraft-Modding-Libs at 86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c](https://github.com/SirEdvin/Minecraft-Modding-Libs/tree/86bfe0b75d0dceb26e713a6c3bdcc91ec74eac2c): `settings.gradle.kts` uses a branch named `forge` for both maintained Minecraft versions. Read effective plugins and descriptors before inferring the loader from a folder name; retain common modules and loader adapters.

## Verification and limits

Coordinator execution in disposable clones built all four template nodes. The 1.21.1 NeoForge production JAR contained exactly `META-INF/neoforge.mods.toml` as loader metadata, without unexpanded placeholders. Library builds covered 24 versioned nodes plus the typed API, with 50 JUnit reports / 1060 executions and no failures, errors, or skips in aggregate. Neither those counts nor successful compilation prove runtime side safety. No GameTests, client/server startup, or 26.1 runtime were exercised for this audit slice.
