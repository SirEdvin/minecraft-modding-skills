# Integration Surfaces

Minecraft mods often fail at integration boundaries. Treat each dependency as a separate API surface with its own loader/version coordinates.

## CC:Tweaked / ComputerCraft

- Runs on Forge and Fabric and provides computers, turtles, Lua APIs, events, and peripheral APIs.
- Verify exact Maven coordinates for active Minecraft and loader (`common`, `common-api`, `core`, `fabric`, `fabric-api`, `forge`, etc. vary by version/project).
- Keep Java-side API dependencies separate from runtime mod dependencies if the project does so.
- Test peripherals on the logical server where possible; client rendering or menus may need separate client-only code.

## JEI / REI / EMI

- These are recipe/viewer integrations, often optional and loader-specific.
- Keep API/compile-only and runtime-only dependencies separate.
- Register integrations through the loader/API's expected plugin entrypoint.
- Do not assume JEI artifact names carry to NeoForge or Fabric unchanged.

## ModMenu / Cloth Config / Forge Config API Port

- Common in Fabric-facing projects for config UI or shared config implementation.
- Keep client-only config screens behind client entrypoints.
- Forge Config API Port may provide common/shared config flows on Fabric; verify the repo's pattern before replacing it.

## Kotlin Loader Bridges

- KotlinForForge and KotlinForForge-NeoForge are not interchangeable coordinates.
- Fabric Kotlin uses `fabric-language-kotlin`.
- Preserve existing Kotlin plugin and source set conventions.

## KubeJS / Rhino / GTCEu / LDLib / Registrate / Create / AE2

- These integration APIs are version-sensitive and sometimes transitive-heavy.
- Prefer source/docs lookup for the exact version when adding or changing API calls.
- Keep optional integration code gated so the base mod can load without optional dependencies when that is the project's existing design.

## Dependency Scope Rules

- `api`: only when downstream modules/consumers need the API exposed.
- `compileOnly`: compile against optional APIs without requiring them at runtime.
- `implementation`: required implementation dependency.
- `runtimeOnly`: needed to run dev/test environment but not compile directly.
- `include` / jar-in-jar: embeds a dependency; use only when the project already embeds that dependency or distribution requires it.
- Loader-specific buckets: follow the project's names (`fabric-cc`, `forge-raw`, `forge-jjar`, `externalMods-*`, etc.) instead of flattening.
