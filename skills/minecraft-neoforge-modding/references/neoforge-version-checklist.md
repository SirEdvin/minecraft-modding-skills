# NeoForge Version Checklist

Official sources used for this reference:

- NeoForge docs: https://docs.neoforged.net/docs/gettingstarted/
- NeoForge 1.21.1 docs: https://docs.neoforged.net/docs/1.21.1/gettingstarted/
- ModDevGradle: https://github.com/neoforged/ModDevGradle
- NeoForge registries: https://docs.neoforged.net/docs/concepts/registries/
- NeoForge networking: https://docs.neoforged.net/docs/networking/
- NeoForge 1.21.1 networking: https://docs.neoforged.net/docs/1.21.1/networking/
- NeoForge data storage: https://docs.neoforged.net/docs/datastorage/attachments/
- NeoForge data components: https://docs.neoforged.net/docs/items/datacomponents/
- NeoForge datagen: https://docs.neoforged.net/docs/resources/

## Files To Read First

- `gradle.properties`: Minecraft, NeoForge, mod id, Java, Kotlin, mappings.
- `settings.gradle(.kts)`: plugin management, included modules, repository filters.
- `build.gradle(.kts)`: `net.neoforged.moddev` or wrapper plugin, runs, datagen, dependencies.
- `META-INF/neoforge.mods.toml`: metadata and dependency ranges.
- Mod constructor/main class: injected services, mod event bus, config, registry setup.

## 1.21.1+

- Minecraft 1.21.1 normally implies Java 21; newer NeoForge lines may require newer JDKs. Verify the active docs and Gradle toolchain.
- NeoForge docs are versioned. Use the docs version matching the repo, not only latest.
- ModDevGradle and NeoGradle are different plugins. Preserve the one already configured unless migration is the task.

## API Areas To Verify Exactly

- Registries and `DeferredRegister` object types.
- Mod lifecycle and event bus registration.
- Payload registration through `RegisterPayloadHandlersEvent` and version-specific payload helpers.
- Attachments, capabilities, saved data, and item/entity/block data components.
- Datagen provider constructors and lookup/provider parameters.
- Access transformers, mixins, and side-only client registration.

## Dedicated Server Check

Run a server task after changes that could load client classes or touch sided events:

```bash
./gradlew runServer --no-daemon
```

If the task requires EULA setup or local auth configuration, report that blocker precisely.
