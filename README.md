# Minecraft Modding Skills

Reusable [Agent Skills](https://agentskills.io/specification) for Minecraft Java mod development.

This repository is designed to be installable by Hermes Agent, skills.sh-compatible tooling, and other agents that understand `SKILL.md` directories.

## Skills

| Skill | Purpose |
| --- | --- |
| `minecraft-modding` | Umbrella/router for Minecraft Java modding work across loaders, versions, Gradle, mappings, mixins, datagen, networking, and integrations. |
| `minecraft-fabric-modding` | Fabric Loader/API/Loom specialist for Fabric Java/Kotlin mods, `fabric.mod.json`, multiloader Fabric modules, events, networking, datagen, mixins, and access wideners. |
| `minecraft-neoforge-modding` | Modern NeoForge specialist for `1.21.1+`, ModDevGradle, Java 21+, registries/events, payload networking, data components, attachments, datagen, and server safety. |
| `minecraft-legacy-forge-modding` | MinecraftForge `1.20.1` / Forge `47.x` specialist for ForgeGradle or legacy ModDevGradle, Java 17, `mods.toml`, registries, `SimpleChannel`, capabilities, ATs, reobf, and datagen. |
| `kubejs-modding` | KubeJS/Rhino/ProbeJS specialist for pack scripts, recipes, tags, custom schemas, logs/reload behavior, and compiled Java addon boundaries. |
| `modrinth-api` | Read-only Modrinth API v2 specialist for project/search/version/file lookup, required `User-Agent`, loader/version filtering, hashes, and download verification. |
| `siredvin-minecraft-modding` | SirEdvin-specific overlay for local repositories, `site.siredvin.*` build conventions, core/fabric/forge modules, CC:Tweaked/peripheral projects, GTCEu work, and private Maven/build validation. |

## Install with Hermes

Install one skill directly:

```bash
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-fabric-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-neoforge-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/minecraft-legacy-forge-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/kubejs-modding
hermes skills install SirEdvin/minecraft-modding-skills/skills/modrinth-api
hermes skills install SirEdvin/minecraft-modding-skills/skills/siredvin-minecraft-modding
```

Or add the repository as a tap:

```bash
hermes skills tap add SirEdvin/minecraft-modding-skills
hermes skills search minecraft
hermes skills install SirEdvin/minecraft-modding-skills/minecraft-modding
hermes skills install SirEdvin/minecraft-modding-skills/minecraft-fabric-modding
hermes skills install SirEdvin/minecraft-modding-skills/minecraft-neoforge-modding
hermes skills install SirEdvin/minecraft-modding-skills/minecraft-legacy-forge-modding
hermes skills install SirEdvin/minecraft-modding-skills/kubejs-modding
hermes skills install SirEdvin/minecraft-modding-skills/modrinth-api
hermes skills install SirEdvin/minecraft-modding-skills/siredvin-minecraft-modding
```

## Install with skills.sh-compatible tooling

```bash
npx skills add SirEdvin/minecraft-modding-skills
```

## Recommended usage

For general Minecraft modding triage, load `minecraft-modding` first. Then add the smallest matching specialist:

| Work | Load |
| --- | --- |
| Fabric mod or Fabric module | `minecraft-modding` + `minecraft-fabric-modding` |
| Modern NeoForge `1.21.1+` | `minecraft-modding` + `minecraft-neoforge-modding` |
| Forge `1.20.1` / Forge `47.x` | `minecraft-modding` + `minecraft-legacy-forge-modding` |
| KubeJS/Rhino/ProbeJS scripts or Java addon boundary | `minecraft-modding` + `kubejs-modding` |
| Modrinth lookup/download/hash work | `modrinth-api` |

For SirEdvin repositories, load the umbrella, the relevant public specialist, and the overlay:

```text
/minecraft-modding
/minecraft-fabric-modding
/siredvin-minecraft-modding
```

The global skill intentionally avoids local filesystem paths and private repository assumptions. The SirEdvin overlay carries those local conventions so the public skill stays reusable.

## Provenance

See `PROVENANCE.md` for the license-safe attribution note and official documentation sources used for the newly authored specialist skills.
