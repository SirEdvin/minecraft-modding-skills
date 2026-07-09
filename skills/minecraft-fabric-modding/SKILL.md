---
name: minecraft-fabric-modding
description: Use when working on Fabric Minecraft mods, Fabric Loader/API/Loom, fabric.mod.json, Java or Kotlin Fabric code, multiloader Fabric modules, Fabric registries/events/networking/datagen, mixins, access wideners, or dedicated-server safety.
version: 1.0.0
author: SirEdvin
license: MIT
compatibility: Independently authored for Fabric projects; verify exact Minecraft, Fabric Loader, Fabric API, Loom, Yarn/Mojang mappings, Java, and Kotlin versions from repository files before applying API details.
metadata:
  hermes:
    tags: [minecraft, fabric, loom, fabric-api, kotlin, mixins, datagen]
---

# Minecraft Fabric Modding

Use this specialist after `minecraft-modding` when the target is Fabric or a Fabric module in a multiloader repository. Keep common gameplay logic in the shared/core layer only when the imports are loader-neutral; put Fabric entrypoints, metadata, access wideners, networking bootstrap, datagen entrypoints, and client setup in the Fabric layer.

References:

- `references/fabric-version-checklist.md`
- `../minecraft-modding/references/repository-inspection-checklist.md`
- `../minecraft-modding/references/framework-docs-map.md`

## Workflow

1. Read `gradle.properties`, `settings.gradle(.kts)`, root/module `build.gradle(.kts)`, `gradle/libs.versions.toml`, `fabric.mod.json`, mixin JSON, and `*.accesswidener` before editing.
2. Confirm the exact Minecraft, Fabric Loader, Fabric API, Loom, mappings, Java toolchain, Kotlin plugin, and `fabric-language-kotlin` versions when Kotlin is present.
3. Check whether the repository targets Fabric `1.20.1`, Fabric `1.21.1`, or another version; use docs/source matching that exact target.
4. Trace existing registries, Fabric API events, networking payload/channel setup, datagen providers, generated resource wiring, and client entrypoints.
5. Preserve multiloader boundaries: common code must not import Fabric APIs unless the project already intentionally exposes a Fabric abstraction.

## Version-Sensitive Areas

- Networking changed across Minecraft/Fabric API generations. For `1.20.1`, verify whether the project uses the legacy Fabric networking style already in the repo. For `1.21.1`, verify the current custom payload/codec APIs from Fabric docs and source before adding packets.
- Datagen commonly uses Fabric API's Loom DSL wiring, a `fabric-datagen` entrypoint, and a generated resources directory; keep the repo's existing output path.
- Access wideners are Fabric metadata, not Forge access transformers. Only widen the smallest member needed, and keep the widener declared in `fabric.mod.json`.
- Dedicated-server safety matters: never load client-only classes from the main initializer or common server paths. Keep screens, renderers, keybinds, and client networking receivers behind client entrypoints or environment-safe dispatch.

## Validation

- Run the narrowest existing Gradle task first, then `./gradlew build --no-daemon` when practical.
- For generated data, run the repo's actual datagen task, commonly `runDatagen`, and inspect generated resources.
- For side safety, run a dedicated server task when client code, entrypoints, networking, or renderers changed.
