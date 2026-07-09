# Framework Documentation Map

Use this map to choose sources before changing Minecraft mod code. Prefer official docs for exact APIs and use community docs only as secondary context.

## Fabric

- Developer guides: https://docs.fabricmc.net/develop/
- Template generator: https://fabricmc.net/develop/template/
- Docs reference mod: https://github.com/FabricMC/fabric-docs/tree/main/reference/latest
- Data generation setup: https://docs.fabricmc.net/develop/data-generation/setup
- Networking guide: https://docs.fabricmc.net/develop/networking

Key reminders from the docs:

- Fabric's core pieces are Fabric Loader, Fabric API, and Fabric Loom.
- The docs' examples use unobfuscated/Mojang-style names and versioned docs; verify mapping assumptions in older projects.
- Datagen can be enabled from project creation or manually via `fabricApi { configureDataGeneration() { ... } }`, a `DataGeneratorEntrypoint`, and a `fabric-datagen` entrypoint in `fabric.mod.json`; generated files commonly go under `src/main/generated`.
- Newer payload-based APIs, including the checked `1.21.1` line, use `CustomPacketPayload`, registered payload types/codecs, and `ServerPlayNetworking` / `ClientPlayNetworking`. Fabric `1.20.1` projects may instead use `Identifier` / `PacketByteBuf` APIs; follow the exact installed Fabric API and existing project pattern. Server receivers must validate client-provided data.

## NeoForge

- Main docs: https://docs.neoforged.net/
- Getting started: https://docs.neoforged.net/docs/gettingstarted/
- Toolchain features: https://docs.neoforged.net/toolchain/docs/
- Registries: https://docs.neoforged.net/docs/concepts/registries/
- Networking: https://docs.neoforged.net/docs/networking/
- Primers: https://docs.neoforged.net/primer/docs/

Key reminders from the docs:

- NeoForge docs are for NeoForge, not Java basics.
- NeoForge recommends generated projects through its mod generator and explains ModDevGradle/NeoGradle as the build plugins.
- Build output comes from `gradlew build`; runtime checks are usually `gradlew runClient` and `gradlew runServer`.
- The docs recommend testing dedicated-server behavior, including for client-only mods, to catch side mistakes.
- Registration prefers `DeferredRegister` attached to the mod event bus; `RegisterEvent` exists but is easier to misuse.
- Networking centers on `RegisterPayloadHandlersEvent` and custom payload registration/handlers.
- Primers are high-level and non-exhaustive; use them as a migration checklist, then verify against code and mappings.

## Forge

- Current Forge docs: https://docs.minecraftforge.net/en/latest/

Use Forge docs for active Forge projects, especially Minecraft 1.20.1 / Forge 47.x codebases. Do not apply NeoForge-only API guidance to legacy Forge modules unless the repo is actively migrating.

## CC:Tweaked / ComputerCraft

- Main docs: https://tweaked.cc/
- CC:Tweaked GitHub: https://github.com/cc-tweaked/CC-Tweaked

Key reminders:

- CC:Tweaked adds programmable computers, turtles, and peripherals and runs on both Forge and Fabric.
- It exposes Lua APIs, events, generic peripherals, and references such as item/block/entity details.
- For Java-side peripheral integrations, verify the exact CC:Tweaked artifact coordinates and API module for the active Minecraft/loader version.

## Common Integration Docs to Locate Per Project

- JEI, REI, EMI recipe/viewer APIs.
- ModMenu and Cloth Config for Fabric client configuration.
- Forge Config API Port for shared config code in Fabric projects.
- KotlinForForge / KotlinForForge-NeoForge when Kotlin entrypoints or loader bridges are present.
- Architectury only when a project already depends on it; do not introduce it as a default multi-loader abstraction.
- KubeJS/Rhino, GTCEu, LDLib, Registrate, Create, AE2, or other mod APIs as required by the specific repository.
