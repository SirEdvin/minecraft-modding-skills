# SirEdvin Repository Map

Local root: `/home/siredvin/projects/`

| Repository | Local branch observed | Minecraft / loader | Layout | Notes |
| --- | --- | --- | --- | --- |
| Turtlematic | `1.20` | MC 1.20.1, Forge 47.2.0, Fabric API 0.92.0 | `core`, `forge`, `fabric` | custom build conventions 0.8.18, CC:Tweaked 1.116.1, access wideners and mixins in core/fabric/forge. |
| DigitalItems | `1.20` | MC 1.20.1, Forge 47.2.0, Fabric API 0.92.0 | `core`, `forge`, `fabric` | custom build conventions 0.8.18, CC:Tweaked 1.113.0. |
| UnlimitedPeripheralWorks | `1.20` | MC 1.20.1, Forge 47.3.39, Fabric API 0.92.6 | `core`, `forge`, `fabric` | custom build conventions 0.8.26, large optional integration surface: AE2, Create, KubeJS/Rhino, Powah, etc. |
| CloudSolutions | `1.20` | MC 1.20.1, Forge 47.4.10, Fabric API 0.92.0 | `core`, `forge`, `fabric` | custom build conventions 0.8.18. |
| Minecraft-Modding-Libs | active local merge-port branch | MC 1.21.1, Fabric + NeoForge-style modules | `broccolium-*`, `tweakium-*`, `peripheralium-*` | custom build conventions 0.9.0, includes `net.neoforged`/`net.neoforged.moddev` repository filters and plugin resolution strategy. |
| SmartHome-Appliances | `1.21` | MC 1.21.1, Fabric active; Forge module commented in settings | `core`, `fabric`, `forge` dir exists | custom build conventions 0.8.14, Fabric active with 1.21.1 dependencies. |
| GregTech-True-Age-of-Steam | local build-environment migration branch | MC 1.20.1, Forge 47.4.10, GTCEu | single `src/main` Forge project | AGENTS.md says Java 17, mod id `gttruesteam`, package `site.siredvin.gttruesteam`; custom build conventions 0.9.0; uses GTCEu/KubeJS/Rhino/Architectury/JEI/EMI/LDLib/Registrate. |
| Custom Gradle convention build | `main` | Gradle convention plugin project | build logic repo | projectVersion 0.9.0; wraps Fabric Loom, ForgeGradle, NeoForge ModDevGradle, CurseForgeGradle. |

Always treat this table as cached context. Re-run `git status --short --branch` and read repo files before changing code.

## Common Multi-loader Shape

Most app-style repos use:

```text
projects/
  core/
  fabric/
  forge/
```

`settings.gradle.kts` maps included Gradle modules to `projects/<module>`. Common code belongs in core; loader-specific entrypoints, metadata, mixins, run configs, and adapters belong in Fabric or Forge/NeoForge modules.

## MML Shape

`Minecraft-Modding-Libs` uses library modules:

```text
projects/
  broccolium-core/
  broccolium-fabric/
  broccolium-forge/
  tweakium-core/
  tweakium-fabric/
  tweakium-forge/
  peripheralium-core/
  peripheralium-fabric/
  peripheralium-forge/
```

For 1.21 work, the `*-forge` modules may actually be NeoForge-facing. Verify metadata (`neoforge.mods.toml`), plugins, and imports before assuming legacy Forge.
